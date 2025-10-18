// Punjabi Language Learning Tool - Frontend Application

class PunjabiApp {
    constructor() {
        this.currentSessionId = null;
        this.currentScenario = null;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.selectedHelpTopic = null;
        this.selectedConfidenceRating = null;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadScenarios();
        this.checkAccountBalance();
    }
    
    setupEventListeners() {
        // Scenario selection
        document.getElementById('start-custom-btn').addEventListener('click', () => this.startCustomScenario());
        
        // Recording
        const recordBtn = document.getElementById('record-btn');
        recordBtn.addEventListener('mousedown', () => this.startRecording());
        recordBtn.addEventListener('mouseup', () => this.stopRecording());
        recordBtn.addEventListener('touchstart', (e) => { e.preventDefault(); this.startRecording(); });
        recordBtn.addEventListener('touchend', (e) => { e.preventDefault(); this.stopRecording(); });
        
        // Help mode
        document.getElementById('help-btn').addEventListener('click', () => this.openHelpPanel());
        document.getElementById('close-help-btn').addEventListener('click', () => this.closeHelpPanel());
        document.getElementById('ask-help-btn').addEventListener('click', () => this.askHelp());
        
        // Help topics
        document.querySelectorAll('.topic-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.selectHelpTopic(e.target.dataset.topic));
        });
        
        // Session control
        document.getElementById('end-session-btn').addEventListener('click', () => this.endSession());
        document.getElementById('new-session-btn').addEventListener('click', () => this.returnToScenarios());
        
        // Confidence rating
        document.querySelectorAll('.rating-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.selectConfidenceRating(parseInt(e.target.dataset.rating)));
        });
    }
    
    async loadScenarios() {
        try {
            const response = await fetch('/api/scenarios');
            const data = await response.json();
            
            const scenarioList = document.getElementById('scenario-list');
            scenarioList.innerHTML = '';
            
            data.scenarios.forEach(scenario => {
                const card = document.createElement('div');
                card.className = 'scenario-card';
                card.innerHTML = `
                    <h3>${scenario.title}</h3>
                    <p>${scenario.description}</p>
                    <p class="goals"><strong>Goals:</strong> ${scenario.goals.join(', ')}</p>
                `;
                card.addEventListener('click', () => this.startScenario(scenario.id));
                scenarioList.appendChild(card);
            });
        } catch (error) {
            console.error('Failed to load scenarios:', error);
            alert('Failed to load scenarios. Please refresh the page.');
        }
    }
    
    async startScenario(scenarioId) {
        this.showLoading(true);
        
        try {
            const formData = new FormData();
            formData.append('scenario_id', scenarioId);
            
            const response = await fetch('/api/sessions/start', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) throw new Error('Failed to start session');
            
            const data = await response.json();
            this.currentSessionId = data.session_id;
            this.currentScenario = data.scenario;
            
            this.showScreen('conversation-screen');
            this.updateScenarioInfo(data.scenario);
            this.addAITurn(data.greeting.transcript, data.greeting.audio_url);
            
            // Enable record button after greeting loads
            document.getElementById('record-btn').disabled = false;
            
        } catch (error) {
            console.error('Failed to start scenario:', error);
            alert('Failed to start scenario. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }
    
    async startCustomScenario() {
        const prompt = document.getElementById('custom-prompt').value.trim();
        
        if (!prompt) {
            alert('Please enter a scenario description.');
            return;
        }
        
        this.showLoading(true);
        
        try {
            // First, create custom scenario
            const scenarioResponse = await fetch('/api/scenarios/custom', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: prompt, dialect: 'doabi' })
            });
            
            if (!scenarioResponse.ok) throw new Error('Failed to create custom scenario');
            
            const scenario = await scenarioResponse.json();
            
            // Then start session with it
            this.currentScenario = scenario;
            
            // Create temporary scenario ID for custom scenarios
            const formData = new FormData();
            formData.append('scenario_id', scenario.id || 'market_shopping'); // Fallback to a default
            
            const sessionResponse = await fetch('/api/sessions/start', {
                method: 'POST',
                body: formData
            });
            
            if (!sessionResponse.ok) throw new Error('Failed to start session');
            
            const data = await sessionResponse.json();
            this.currentSessionId = data.session_id;
            
            this.showScreen('conversation-screen');
            this.updateScenarioInfo(this.currentScenario);
            this.addAITurn(data.greeting.transcript, data.greeting.audio_url);
            
            document.getElementById('record-btn').disabled = false;
            
        } catch (error) {
            console.error('Failed to start custom scenario:', error);
            alert('Failed to start custom scenario. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }
    
    updateScenarioInfo(scenario) {
        document.getElementById('scenario-title').textContent = scenario.title;
        document.getElementById('scenario-description').textContent = scenario.description;
        document.getElementById('persona-name').textContent = scenario.persona_name;
        document.getElementById('persona-role').textContent = scenario.persona_role;
    }
    
    async startRecording() {
        if (!this.currentSessionId) return;
        
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };
            
            this.mediaRecorder.onstop = () => {
                this.processTurn();
            };
            
            this.mediaRecorder.start();
            
            const recordBtn = document.getElementById('record-btn');
            recordBtn.classList.add('recording');
            recordBtn.querySelector('.record-text').textContent = 'Recording...';
            
        } catch (error) {
            console.error('Failed to access microphone:', error);
            alert('Please allow microphone access to record your speech.');
        }
    }
    
    stopRecording() {
        if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
            this.mediaRecorder.stop();
            this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
            
            const recordBtn = document.getElementById('record-btn');
            recordBtn.classList.remove('recording');
            recordBtn.querySelector('.record-text').textContent = 'Hold to Speak';
        }
    }
    
    async processTurn() {
        if (this.audioChunks.length === 0) return;
        
        this.showLoading(true);
        
        try {
            // Use the actual MIME type from MediaRecorder
            // Most browsers use webm or ogg, not wav
            const mimeType = this.mediaRecorder.mimeType || 'audio/webm';
            const audioBlob = new Blob(this.audioChunks, { type: mimeType });
            
            // Determine file extension based on MIME type
            let extension = 'webm';
            if (mimeType.includes('wav')) extension = 'wav';
            else if (mimeType.includes('ogg')) extension = 'ogg';
            else if (mimeType.includes('mp4')) extension = 'mp4';
            else if (mimeType.includes('mpeg')) extension = 'mp3';
            
            const formData = new FormData();
            formData.append('audio', audioBlob, `recording.${extension}`);
            
            console.log(`Sending audio: ${(audioBlob.size / 1024).toFixed(2)} KB, type: ${mimeType}, extension: ${extension}`);
            
            const response = await fetch(`/api/sessions/${this.currentSessionId}/turn`, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
                console.error('Server error:', errorData);
                throw new Error(errorData.detail || 'Failed to process turn');
            }
            
            const data = await response.json();
            
            // Add user turn
            this.addUserTurn(data.user.transcript);
            
            // Add AI response
            this.addAITurn(data.ai.transcript, data.ai.audio_url);
            
            // Update metrics
            this.updateMetrics(data.metrics);
            
        } catch (error) {
            console.error('Failed to process turn:', error);
            alert('Failed to process your speech. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }
    
    addUserTurn(transcript) {
        const turnDiv = document.createElement('div');
        turnDiv.className = 'turn user';
        turnDiv.innerHTML = `
            <div class="turn-bubble">
                <div class="turn-text gurmukhi">${transcript.gurmukhi}</div>
                <div class="turn-text romanised">${transcript.romanised}</div>
                <div class="turn-text english">${transcript.english}</div>
            </div>
        `;
        
        const conversationTurns = document.getElementById('conversation-turns');
        conversationTurns.appendChild(turnDiv);
        conversationTurns.scrollTop = conversationTurns.scrollHeight;
    }
    
    addAITurn(transcript, audioUrl) {
        const turnDiv = document.createElement('div');
        turnDiv.className = 'turn ai';
        turnDiv.innerHTML = `
            <div class="turn-bubble">
                <div class="turn-text gurmukhi">${transcript.gurmukhi}</div>
                <div class="turn-text romanised">${transcript.romanised}</div>
                <div class="turn-text english">${transcript.english}</div>
            </div>
            <div class="audio-player">
                <audio controls autoplay>
                    <source src="${audioUrl}" type="audio/mpeg">
                </audio>
            </div>
        `;
        
        const conversationTurns = document.getElementById('conversation-turns');
        conversationTurns.appendChild(turnDiv);
        conversationTurns.scrollTop = conversationTurns.scrollHeight;
    }
    
    async updateMetrics(metrics) {
        document.getElementById('turn-count').textContent = metrics.turn_count;
        document.getElementById('word-count').textContent = metrics.total_words;
        document.getElementById('avg-confidence').textContent = 
            metrics.average_confidence ? (metrics.average_confidence * 100).toFixed(0) + '%' : '--';
        
        // Update cost estimate
        try {
            const response = await fetch(`/api/usage/${this.currentSessionId}`);
            if (response.ok) {
                const data = await response.json();
                document.getElementById('api-cost').textContent = data.usage.total_cost;
            }
        } catch (error) {
            console.error('Failed to update cost:', error);
        }
    }
    
    openHelpPanel() {
        document.getElementById('help-panel').classList.add('open');
    }
    
    closeHelpPanel() {
        document.getElementById('help-panel').classList.remove('open');
        document.getElementById('help-response').textContent = '';
    }
    
    selectHelpTopic(topic) {
        this.selectedHelpTopic = topic;
        
        document.querySelectorAll('.topic-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        event.target.classList.add('active');
    }
    
    async askHelp() {
        const query = document.getElementById('help-query').value.trim();
        
        if (!query) {
            alert('Please enter a question.');
            return;
        }
        
        this.showLoading(true);
        
        try {
            const response = await fetch(`/api/sessions/${this.currentSessionId}/help`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    query: query,
                    topic: this.selectedHelpTopic
                })
            });
            
            if (!response.ok) throw new Error('Failed to get help');
            
            const data = await response.json();
            document.getElementById('help-response').textContent = data.response;
            
        } catch (error) {
            console.error('Failed to get help:', error);
            alert('Failed to get help. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }
    
    async endSession() {
        if (!confirm('Are you sure you want to end this session?')) return;
        
        this.showLoading(true);
        
        try {
            const response = await fetch(`/api/sessions/${this.currentSessionId}/complete`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: this.selectedConfidenceRating ? `confidence_rating=${this.selectedConfidenceRating}` : ''
            });
            
            if (!response.ok) throw new Error('Failed to complete session');
            
            const summary = await response.json();
            this.showSummary(summary);
            
        } catch (error) {
            console.error('Failed to end session:', error);
            alert('Failed to end session properly.');
            this.returnToScenarios();
        } finally {
            this.showLoading(false);
        }
    }
    
    async showSummary(summary) {
        document.getElementById('summary-wpm').textContent = 
            summary.metrics.words_per_minute ? summary.metrics.words_per_minute.toFixed(1) : '--';
        document.getElementById('summary-words').textContent = summary.metrics.total_words;
        document.getElementById('summary-vocab').textContent = summary.metrics.unique_vocab_count;
        document.getElementById('summary-turns').textContent = summary.metrics.turn_count;
        document.getElementById('summary-confidence').textContent = 
            summary.metrics.average_confidence ? (summary.metrics.average_confidence * 100).toFixed(0) + '%' : '--';
        
        // Fetch and display usage data
        await this.loadUsageData();
        
        this.showScreen('summary-screen');
    }
    
    async loadUsageData() {
        try {
            const response = await fetch(`/api/usage/${this.currentSessionId}`);
            if (!response.ok) throw new Error('Failed to fetch usage');
            
            const data = await response.json();
            const usage = data.usage;
            
            // Update cost in summary
            document.getElementById('summary-api-cost').textContent = usage.total_cost;
            
            // Show detailed breakdown
            const breakdownHtml = `
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.9em;">
                    <div><strong>Whisper (ASR):</strong> ${usage.whisper.minutes.toFixed(2)} min</div>
                    <div style="text-align: right;">${usage.whisper.cost}</div>
                    
                    <div><strong>GPT (${usage.gpt.model}):</strong> ${usage.gpt.total_tokens} tokens</div>
                    <div style="text-align: right;">${usage.gpt.cost}</div>
                    
                    <div><strong>TTS (Speech):</strong> ${usage.tts.characters} chars</div>
                    <div style="text-align: right;">${usage.tts.cost}</div>
                    
                    <div style="border-top: 1px solid #ccc; padding-top: 5px;"><strong>Total:</strong></div>
                    <div style="border-top: 1px solid #ccc; padding-top: 5px; text-align: right;"><strong>${usage.total_cost}</strong></div>
                </div>
            `;
            document.getElementById('usage-breakdown').innerHTML = breakdownHtml;
            
        } catch (error) {
            console.error('Failed to load usage data:', error);
            document.getElementById('summary-api-cost').textContent = 'N/A';
            document.getElementById('usage-breakdown').innerHTML = '<p style="color: #999;">Usage data unavailable</p>';
        }
    }
    
    selectConfidenceRating(rating) {
        this.selectedConfidenceRating = rating;
        
        document.querySelectorAll('.rating-btn').forEach(btn => {
            btn.classList.remove('selected');
        });
        
        event.target.classList.add('selected');
        
        // Auto-submit after rating selected
        setTimeout(() => this.endSession(), 500);
    }
    
    returnToScenarios() {
        // Reset state
        this.currentSessionId = null;
        this.currentScenario = null;
        this.selectedConfidenceRating = null;
        document.getElementById('conversation-turns').innerHTML = '';
        document.getElementById('custom-prompt').value = '';
        document.getElementById('record-btn').disabled = true;
        
        this.showScreen('scenario-selection');
    }
    
    showScreen(screenId) {
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });
        document.getElementById(screenId).classList.add('active');
    }
    
    showLoading(show) {
        document.getElementById('loading').classList.toggle('active', show);
    }
    
    async checkAccountBalance() {
        try {
            const response = await fetch('/api/account/balance');
            const data = await response.json();
            
            const balanceEl = document.getElementById('account-balance');
            const noteEl = document.getElementById('balance-note');
            
            if (data.available && data.data) {
                // If we can get balance info
                const balance = data.data;
                
                // OpenAI API may return different formats, try to extract useful info
                if (balance.hard_limit_usd) {
                    balanceEl.textContent = `$${balance.hard_limit_usd.toFixed(2)} limit`;
                    balanceEl.style.color = '#4CAF50';
                    noteEl.textContent = 'Account active';
                } else if (balance.credits) {
                    balanceEl.textContent = `${balance.credits} credits`;
                    balanceEl.style.color = '#4CAF50';
                } else {
                    balanceEl.textContent = 'Account Active';
                    balanceEl.style.color = '#4CAF50';
                    noteEl.textContent = 'Balance details unavailable';
                }
            } else {
                // Balance check not available (most common case)
                balanceEl.textContent = 'View on OpenAI';
                balanceEl.style.color = '#666';
                noteEl.innerHTML = '<a href="https://platform.openai.com/account/billing" target="_blank" style="color: #2196F3; text-decoration: none;">Check Balance →</a>';
            }
            
            // Also fetch and display global usage
            await this.displayGlobalUsage();
            
        } catch (error) {
            console.error('Failed to check balance:', error);
            document.getElementById('account-balance').textContent = 'View on OpenAI';
            document.getElementById('balance-note').innerHTML = '<a href="https://platform.openai.com/account/billing" target="_blank" style="color: #2196F3; text-decoration: none;">Check Balance →</a>';
        }
    }
    
    async displayGlobalUsage() {
        try {
            const response = await fetch('/api/usage/global/summary');
            if (response.ok) {
                const data = await response.json();
                const noteEl = document.getElementById('balance-note');
                
                // Add global spending info
                const currentNote = noteEl.textContent;
                if (currentNote && !currentNote.includes('Spent')) {
                    noteEl.innerHTML = `Session spent: ${data.usage.total_cost}<br>${noteEl.innerHTML}`;
                }
            }
        } catch (error) {
            console.error('Failed to get global usage:', error);
        }
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new PunjabiApp();
});

