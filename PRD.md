## Punjabi Conversational Learning — MVP PRD (Proof of Concept)

### Summary
Build a proof-of-concept web-based Punjabi speaking practice tool that lets users converse in real-world scenarios with an AI partner. Users speak Punjabi; the system transcribes their speech to Gurmukhi, Romanised, and English meaning, and the AI replies naturally in Punjabi (speech + text) with the same three outputs. A side-panel “Help Mode” provides on-demand grammar, vocabulary, cultural notes, and alternative phrasings. Initial dialect focus: Doabi Punjabi. Target user is a basic conversationalist seeking more fluency, vocabulary breadth, confidence, and improved accent.

### Goals (MVP)
- Enable real-time, scenario-based Punjabi conversation practice with AI.
- Provide three synchronized representations for all turns: Gurmukhi, Romanised Punjabi, and English meaning.
- Reduce thinking time and filler words ("um/uh") to encourage faster speech.
- Support a pausable “Help Mode” assistant for grammar, vocab, and cultural clarifications.
- Validate feasibility and user value with minimal engineering complexity.

### Non-Goals (MVP)
- Multi-dialect switching (beyond Doabi) and advanced accent coaching.
- Formal curriculum, spaced repetition, or progress dashboards.
- Classroom/teacher admin tooling.
- Mobile apps; focus is a web-based PoC.
- Robust privacy controls beyond basic disclosures.

## Users & Jobs-To-Be-Done

### Primary Users
- Basic conversational Punjabi speakers (heritage speakers or learners) who can produce short, simple sentences but lack a speaking partner and need confidence, faster recall, and clearer pronunciation.

### Secondary Stakeholders
- None for MVP (no teachers/parents/admin). Future: teachers or parents could observe progress.

### Key Jobs-To-Be-Done
- Practice realistic conversations to build fluency and reduce hesitation.
- Hear natural Punjabi responses and model pronunciation.
- Understand what was said via Gurmukhi, Romanised Punjabi, and English meaning.
- Ask for help mid-session without derailing practice.

### Success Moments (Observable)
- Complete a curated scenario with fewer interruptions/help requests.
- Sustain multiple back-and-forth turns fluidly.
- Noticeably faster speech with fewer fillers.

Assumptions:
- Users tolerate web mic permissions and desktop/laptop usage for PoC.
- English meaning is always displayed in MVP to support comprehension.

Open Questions:
- Age focus (adults vs teens) — assumed adults for MVP.
- Weekly practice habits — assumed short, frequent sessions (e.g., ~10 minutes, 3x/week).

## Value & Outcomes

### Outcomes
- Faster Punjabi with less “ums”/thinking time.
- Larger active vocabulary in context.
- Greater speaking confidence.
- Improved accent/pronunciation relative to user baseline.

### KPIs (MVP)
- Words per minute (WPM) during user speech (goal: increase over baseline within a session and across sessions).
- Amount of mistakes (proxy metrics: ASR corrections needed, AI correction prompts, grammatical error flags) — goal: decreasing trend.
- Vocabulary breadth (unique content words spoken per session; prompted vs spontaneous) — goal: increasing trend.
- User satisfaction (self-reported confidence after session) — goal: majority report confidence improved.

### Guardrails
- None beyond basic content acceptability for PoC. Note: future releases should add content safety and cost guardrails.

### PoC Success Criteria
- Technical feasibility: Stable live turn-taking loop with acceptable latency for ASR and TTS.
- Usability: ≥70% of test users complete one curated scenario end-to-end.
- Perceived value: Median post-session confidence rating ≥4/5.

## Scope & Constraints (MVP)

### In Scope
- Scenario-based conversation with 1–2 curated scenarios (e.g., market, school pickup) and one custom-prompt scenario.
- Doabi dialect for AI speech/lexicon.
- Live speech interaction: user → ASR → display (Gurmukhi/Romanised/English) → AI reply (Punjabi TTS + same three displays).
- Side-panel “Help Mode” (pauses the scenario) for grammar, vocabulary, cultural notes, and alternative expressions.
- Basic session analytics (local or lightweight) sufficient to compute KPIs above.

### Out of Scope
- Accounts, profiles, and persistent progress tracking beyond basic session stats.
- Saving/replaying conversations (future roadmap).
- Achievement system, badges, streaks (future roadmap).
- Accent-aware feedback beyond simple confidence cues (future roadmap suggests Whisper confidences).

### Constraints
- ASR: “As good as Whisper can do” — accept Whisper baseline performance for Punjabi Doabi.
- TTS: Natural Punjabi output via OpenAI TTS (or equivalent) with acceptable latency.
- Platform: Web app (desktop-first) for PoC.

## Non-Functional Requirements

### Performance
- End-to-end per-turn latency (user finishes speaking → AI audio starts) target: ≤3–5 seconds median for PoC.
- Transcription display updates near-real-time or within 1–2 seconds after end of utterance.

### Reliability
- Session should tolerate transient network hiccups; simple retry on ASR/TTS calls.
- Graceful error states with retry affordances; preserve current scenario state where possible.

### Security & Privacy (PoC)
- Minimal: disclose that audio is processed by third-party models (ASR/TTS/LLM). No long-term storage by default in MVP.

### Accessibility & i18n
- Basic readability (legible Gurmukhi font, Romanised display). Full a11y not in focus for PoC.

### Observability
- Lightweight client logs and event tracking for turn latency, errors, WPM, help invocations.

## Interfaces & UX

### Surfaces
- Web app (desktop-first) with mic input, transcript panes, scenario selector, and Help Mode side panel.

### Main Views
- Home/Scenario Select: choose curated scenario or enter custom prompt.
- Conversation View:
  - Mic control (record/stop), visual level/meter, turn status.
  - User transcript: Gurmukhi, Romanised, English.
  - AI reply: Punjabi audio playback; text: Gurmukhi, Romanised, English.
  - Help Mode side panel (invoked via pause button).

### States & Errors
- No mic permission: inline guidance to enable.
- Noisy/low confidence ASR: show hint and allow quick re-try.
- TTS/LLM errors: display non-blocking alert with retry; keep transcripts.

### Help Mode (Paused State)
- Input: free-form questions (grammar, vocabulary, cultural notes, alternative phrasing; show examples).
- Output: concise explanations with examples in the three displays when relevant.
- Resume returns to conversation context.

### Analytics Events (MVP)
- session_started, session_ended
- scenario_selected (type: curated/custom, id or prompt hash)
- turn_completed (latency_ms, asr_confidence_avg, tokens_spoken, fillers_count)
- help_opened, help_topic (grammar/vocab/culture/alternatives), help_closed
- error (type, surface)

## Risks & Dependencies

### External Dependencies
- ASR (Whisper) for Punjabi.
- LLM (GPT or equivalent) for context-aware character responses.
- TTS (OpenAI TTS or equivalent) for natural Punjabi audio.

### Key Risks
- ASR accuracy for Doabi and in noisy environments; Romanisation correctness.
- Latency stacking (ASR → LLM → TTS) harming conversation flow.
- Inconsistent or overly formal/informal AI tone without tight prompt/guardrails.
- Lack of training data for dialect nuances.

### Mitigations (MVP-level)
- Keep utterances short; encourage turn-taking; show “speaking tips.”
- Cache TTS voices and keep prompts focused/contextual.
- Provide quick “re-try last line” control for user.

## Delivery Envelope

### Timeline
- PoC target: 3–4 weeks to implement and user-test internally.

### Team
- 1–2 engineers; 1 product/design partner.

### Budget (PoC)
- Minimal infra; usage-based spend on ASR/LLM/TTS. Monitor cost per session.

### MVP Cut-Lines
- Must-have: one curated scenario, custom prompt scenario, live speech loop, tri-script displays, Help Mode, basic analytics.
- Nice-to-have: second curated scenario, basic filler-word counter, simple per-session summary.
- Stretch: accent cues using ASR confidences.

## Acceptance Criteria (MVP)
- User can select a scenario and complete ≥1 full exchange cycle: user speaks → tri-script transcript → AI tri-script + audio reply.
- Help Mode can be opened, asked a question, and closed; scenario resumes where paused.
- Median end-to-end per-turn latency ≤5s in test conditions.
- Session summary shows WPM, fillers count, unique vocab estimate, and a brief confidence check.

## Open Questions
- Do we pin a single voice for AI across scenarios, or vary by character?
- Should English meaning be hideable by power users in later iterations?
- What is the minimum viable Romanisation scheme for consistency (e.g., agreed mapping)?

## Future Roadmap (Post-MVP)
- More scenario types and user personas; save/review conversations.
- Basic progress tracking and achievement system.
- Accent-aware feedback using Whisper confidence metrics and targeted drills.
- Multi-dialect support and dialect switching.


