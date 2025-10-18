## Punjabi Conversational Learning — MVP Delivery Plan

### Objective
Deliver a desktop-first, web-based Proof of Concept that enables live Punjabi conversation practice with tri-script transcripts, AI Punjabi TTS replies, and a pausable Help Mode. Dialect: Doabi.

### Workstreams
1) Core Conversation Loop
2) Scenario Engine (curated + custom prompt)
3) Help Mode Assistant
4) Frontend UI/UX
5) Analytics & Session Summary
6) Infrastructure & Ops
7) QA & Usability

---

## Milestones & Tasks

### Milestone 1 — Core Conversation Loop
- Mic capture and VAD (basic)
- ASR via Whisper; return Gurmukhi transcript and token-level confidences
- Romanisation pipeline (consistent mapping) and English meaning via LLM translate
- AI turn generation (LLM) with concise, context-aware replies
- TTS for Punjabi (Doabi voice selection); streaming or chunked playback
- Turn-taking state machine; per-turn timing and error handling

Deliverable: User speaks; system displays tri-script; AI replies with audio + tri-script.

### Milestone 2 — Scenario Engine
- Curated scenarios x1 (market) with character persona and goals
- Custom prompt scenario: accept user prompt → seed persona + scene
- Scenario context window management (facts, location, persona constraints)
- Dialect prompt-tuning for Doabi tone/lexicon consistency

Deliverable: User can choose curated scenario or supply a custom prompt; AI stays in role.

### Milestone 3 — Help Mode
- Pause/resume conversation session state
- Side panel UI with free-form Q&A to assistant
- Assistant prompt patterns for: grammar, vocabulary, cultural notes, alternative phrasing
- Rich answers with examples; show tri-script where relevant

Deliverable: Users can pause, ask for explanations, resume.

### Milestone 4 — Frontend UX
- Desktop-first responsive layout
- Transcript panes for user and AI (Gurmukhi, Romanised, English)
- Mic control (record/stop), waveform meter, status indicator
- AI audio playback controls; retry last user utterance
- Scenario selector and minimal home screen

Deliverable: Usable, legible UI with clear state and controls.

### Milestone 5 — Analytics & Summary
- Event logging: session_started/ended, scenario_selected, turn_completed, help_opened/closed, error
- Metrics: words per minute, fillers count (heuristic), unique vocab estimate, help invocation count
- Session summary view with KPI snapshot and simple confidence check (Likert)

Deliverable: Minimal analytics to evaluate PoC success criteria.

### Milestone 6 — Infra & Ops
- Environment setup, keys management, rate limit handling
- Simple retry/backoff for ASR/LLM/TTS failures
- Light cost monitoring (per-session rough cost)
- Error reporting hooks

Deliverable: Stable PoC runtime with basic reliability.

### Milestone 7 — QA & Usability
- Functional test checklist per acceptance criteria (below)
- Latency profiling (ASR→LLM→TTS) and simple optimizations
- Doabi phrasing spot checks; romanisation consistency spot checks
- Fast user tests (5–10 sessions) and UI tweaks

Deliverable: PoC quality sufficient for internal demo.

---

## Roles & Ownership
- Engineering: Core loop, integration, UI, analytics
- Product/Design: Scenarios, Help Mode prompt patterns, UX flows, success criteria

---

## Acceptance Criteria
- User completes ≥1 full exchange cycle: speak → tri-script → AI tri-script + audio
- Help Mode opens, answers a question with useful examples, and resumes scenario
- Median end-to-end turn latency ≤5s in test conditions
- Session summary shows WPM, fillers, unique vocab estimate, and confidence check
- AI remains in character for curated scenario ≥90% of turns

---

## Cut-Lines (MVP Scope Control)
- Must-have: one curated scenario, custom prompt scenario, live loop, Help Mode, basic analytics
- Nice-to-have: second curated scenario, re-try last utterance, filler counter
- Stretch: accent cues using ASR confidences, streaming TTS

---

## Risks & Mitigations
- ASR accuracy for Doabi and noisy rooms → encourage short utterances; simple noise tips UI
- Latency stacking → parallelize requests where possible; keep prompts minimal; cache TTS voice
- Inconsistent tone → tighten system prompts; persona check rules; short context memory
- Romanisation variability → fix a mapping table and unit test samples

---

## Technical Notes (non-implementation)
- ASR: Whisper for Punjabi; capture confidences for basic error cues
- Translation/English meaning: LLM translate short utterances
- Romanisation: deterministic scheme for Gurmukhi→Latin mapping
- LLM: persona-constrained, short replies, Doabi lexicon hints
- TTS: Punjabi voice with natural prosody; prefer low-latency mode

---

## QA Checklist (Excerpt)
- Mic permission flow works; visible fallback instructions
- ASR returns text in Gurmukhi; romanisation matches scheme; English meaning reasonable
- AI reply delivered with audio; text tri-script aligns with audio content
- Help Mode: grammar, vocab, cultural, alternatives produce relevant outputs
- Error handling: graceful retry for ASR/LLM/TTS failures
- Analytics: events emitted; summary computes WPM, fillers, vocab estimate

---

## Go/No-Go for Post-MVP
- ≥70% curated-scenario completion rate in test group
- Median confidence rating ≥4/5 after session
- Stable median latency ≤5s


