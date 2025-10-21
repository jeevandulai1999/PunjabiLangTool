"""Unit tests for the vowel analyzer utilities."""

from __future__ import annotations

from typing import Dict, Optional

import pytest

from backend.models.transcript import PhonemePrediction
from backend.models.vowel_feedback import VowelFeedback
from backend.services.vowel_analyzer import VowelAnalyzer, VowelMappingEntry


def make_prediction(
    phoneme: str,
    start: float,
    end: float,
    confidence: Optional[float] = None,
) -> PhonemePrediction:
    return PhonemePrediction(phoneme=phoneme, start=start, end=end, confidence=confidence)


def test_analyze_returns_feedback_for_expected_vowels() -> None:
    analyzer = VowelAnalyzer()
    expected_vowels = ["ਅ", "ਈ"]
    predictions = [
        make_prediction("a", 0.0, 0.1, 0.8),
        make_prediction("iː", 0.1, 0.35, 0.9),
    ]

    feedback = analyzer.analyze(expected_vowels, predictions)

    assert isinstance(feedback, VowelFeedback)
    assert set(feedback.assessments.keys()) == {"ਅ", "ਈ"}
    assert feedback.assessments["ਅ"].detected_cluster is not None
    assert feedback.assessments["ਅ"].detected_cluster.phonemes == ["a"]
    assert feedback.assessments["ਅ"].confidence > 0.5


def test_confidence_penalises_levenshtein_distance() -> None:
    mapping = {
        "ਆ": VowelMappingEntry(
            phoneme_sequences=[["aa"], ["a"]],
            average_duration_ms=180.0,
        )
    }
    analyzer = VowelAnalyzer(mapping_table=mapping)

    perfect_predictions = [make_prediction("aa", 0.0, 0.2, 0.9)]
    imperfect_predictions = [make_prediction("a", 0.0, 0.2, 0.9)]

    perfect_feedback = analyzer.analyze(["ਆ"], perfect_predictions)
    imperfect_feedback = analyzer.analyze(["ਆ"], imperfect_predictions)

    assert perfect_feedback.assessments["ਆ"].confidence > imperfect_feedback.assessments["ਆ"].confidence
    assert imperfect_feedback.assessments["ਆ"].scores.levenshtein_distance == 1


def test_duration_score_included_when_data_available() -> None:
    mapping: Dict[str, VowelMappingEntry] = {
        "ਇ": VowelMappingEntry(phoneme_sequences=[["i"]], average_duration_ms=100.0)
    }
    analyzer = VowelAnalyzer(mapping_table=mapping)

    short_prediction = [make_prediction("i", 0.0, 0.09)]
    long_prediction = [make_prediction("i", 0.0, 0.2)]

    short_feedback = analyzer.analyze(["ਇ"], short_prediction)
    long_feedback = analyzer.analyze(["ਇ"], long_prediction)

    short_score = short_feedback.assessments["ਇ"].scores.duration_score
    long_score = long_feedback.assessments["ਇ"].scores.duration_score

    assert short_score is not None and long_score is not None
    assert long_score < short_score
    assert short_feedback.assessments["ਇ"].scores.duration_difference_ms == pytest.approx(10.0, rel=1e-3)


def test_formant_hook_contributes_to_confidence() -> None:
    def formant_hook(cluster, vowel, entry):  # pragma: no cover - simple passthrough
        if vowel == "ਅ":
            return 0.8
        return 0.2

    analyzer = VowelAnalyzer(formant_scorer=formant_hook)
    predictions = [make_prediction("a", 0.0, 0.1, 0.9)]

    feedback = analyzer.analyze(["ਅ"], predictions)
    details = feedback.assessments["ਅ"].scores

    assert details.formant_similarity == pytest.approx(0.8, rel=1e-6)
    expected_confidence = (
        0.6 * details.phoneme_similarity
        + 0.2 * details.duration_score
        + 0.2 * details.formant_similarity
    )
    assert feedback.assessments["ਅ"].confidence == pytest.approx(expected_confidence, rel=1e-6)

