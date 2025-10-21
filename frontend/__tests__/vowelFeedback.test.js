const fs = require('fs');
const path = require('path');
describe('PunjabiApp vowel feedback UI', () => {
  let app;

  const createResponse = (jsonPayload) => ({
    ok: true,
    json: () => Promise.resolve(jsonPayload)
  });

  beforeEach(() => {
    const htmlPath = path.resolve(__dirname, '..', 'index.html');
    const html = fs.readFileSync(htmlPath, 'utf8');
    document.documentElement.innerHTML = html;

    global.navigator = window.navigator;

    global.URL.createObjectURL = jest.fn(() => 'blob:mock');
    global.URL.revokeObjectURL = jest.fn();

    global.fetch = jest.fn((requestUrl) => {
      if (requestUrl.endsWith('/api/scenarios')) {
        return Promise.resolve(createResponse({ scenarios: [] }));
      }
      if (requestUrl.endsWith('/api/account/balance')) {
        return Promise.resolve(createResponse({ available: false }));
      }
      if (requestUrl.includes('/api/usage/global/summary')) {
        return Promise.resolve(createResponse({ usage: { total_cost: '$0.00' } }));
      }
      return Promise.resolve(createResponse({}));
    });

    jest.isolateModules(() => {
      require('../static/js/app.js');
    });
  });

  afterEach(() => {
    jest.useRealTimers();
    jest.clearAllMocks();
    document.documentElement.innerHTML = '';
  });

  test('renders vowel timeline, table and playback controls', () => {
    jest.useFakeTimers();

    expect(document.getElementById('start-custom-btn')).not.toBeNull();

    app = new window.PunjabiApp();

    const transcript = {
      duration_seconds: 1.6,
      vowel_feedback: {
        assessments: {
          'ਅ': {
            expected_vowel: 'ਅ',
            detected_cluster: {
              start: 0.12,
              end: 0.45,
              duration_ms: 330,
              phonemes: ['AA', 'AH']
            },
            confidence: 0.85,
            match: true,
            scores: { overall_score: 0.92 }
          },
          'ਈ': {
            expected_vowel: 'ਈ',
            detected_cluster: {
              start: 0.52,
              end: 0.94,
              duration_ms: 420,
              phonemes: ['IY']
            },
            confidence: 0.6,
            match: false,
            scores: { overall_score: 0.58 }
          }
        }
      }
    };

    app.handleVowelFeedback('turn-test', transcript, 'blob:mock');

    const emptyState = document.getElementById('vowel-feedback-empty');
    expect(emptyState.style.display).toBe('none');

    const cards = document.querySelectorAll('.vowel-turn-card');
    expect(cards.length).toBe(1);

    const timelineSegments = cards[0].querySelectorAll('.timeline-segment');
    expect(timelineSegments.length).toBe(2);
    expect(timelineSegments[0].textContent).toContain('ਅ');

    const rows = cards[0].querySelectorAll('tbody tr');
    expect(rows.length).toBe(2);
    expect(rows[0].querySelector('.expected-vowel').textContent).toBe('ਅ');
    expect(rows[0].querySelector('.confidence-value').textContent).toBe('85%');

    const playButtons = cards[0].querySelectorAll('.vowel-play-btn');
    expect(playButtons.length).toBeGreaterThan(0);

    const audioEntry = app.vowelAudioMap.get('turn-test');
    expect(audioEntry).toBeTruthy();
    audioEntry.element.play = jest.fn(() => Promise.resolve());
    audioEntry.element.pause = jest.fn();
    const playSpy = audioEntry.element.play;

    playButtons[0].click();
    expect(playSpy).toHaveBeenCalled();
    expect(playButtons[0].classList.contains('playing')).toBe(true);

    jest.runOnlyPendingTimers();
    expect(playButtons[0].classList.contains('playing')).toBe(false);
  });

  test('keeps empty state visible when no feedback is returned', () => {
    app = new window.PunjabiApp();

    const emptyContainerBefore = document.getElementById('vowel-feedback-turns');
    emptyContainerBefore.innerHTML = '';

    app.handleVowelFeedback('turn-empty', { vowel_feedback: { assessments: {} } }, 'blob:none');

    const emptyState = document.getElementById('vowel-feedback-empty');
    expect(emptyState.style.display).toBe('block');
    expect(emptyState.textContent).toContain('Vowel analysis unavailable');
    expect(global.URL.revokeObjectURL).toHaveBeenCalledWith('blob:none');
  });
});
