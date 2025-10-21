"""Utilities for analysing Punjabi vowel pronunciation from phoneme streams."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple

from backend.models.transcript import PhonemePrediction
from backend.models.vowel_feedback import (
    DetectedPhonemeCluster,
    VowelAssessment,
    VowelFeedback,
    VowelScoreDetails,
)


@dataclass(frozen=True)
class VowelMappingEntry:
    """Configuration describing how a phoneme cluster maps to a Punjabi vowel."""

    phoneme_sequences: Sequence[Sequence[str]]
    average_duration_ms: Optional[float] = None
    formant_targets: Optional[Dict[str, float]] = None


def _sequence(value: Iterable[str]) -> Tuple[str, ...]:
    return tuple(value)


DEFAULT_VOWEL_MAPPING: Dict[str, VowelMappingEntry] = {
    "ਅ": VowelMappingEntry(phoneme_sequences=[_sequence(["a"]), _sequence(["ə"])], average_duration_ms=110.0),
    "ਆ": VowelMappingEntry(phoneme_sequences=[_sequence(["aː"]), _sequence(["aa"])], average_duration_ms=180.0),
    "ਇ": VowelMappingEntry(phoneme_sequences=[_sequence(["ɪ"]), _sequence(["i"])], average_duration_ms=120.0),
    "ਈ": VowelMappingEntry(phoneme_sequences=[_sequence(["iː"]), _sequence(["ii"])], average_duration_ms=190.0),
    "ਉ": VowelMappingEntry(phoneme_sequences=[_sequence(["ʊ"]), _sequence(["u"])], average_duration_ms=120.0),
    "ਊ": VowelMappingEntry(phoneme_sequences=[_sequence(["uː"]), _sequence(["uu"])], average_duration_ms=190.0),
    "ਏ": VowelMappingEntry(phoneme_sequences=[_sequence(["e"]), _sequence(["eː"])], average_duration_ms=150.0),
    "ਐ": VowelMappingEntry(phoneme_sequences=[_sequence(["ai"]), _sequence(["æ"])], average_duration_ms=170.0),
    "ਓ": VowelMappingEntry(phoneme_sequences=[_sequence(["o"]), _sequence(["oː"])], average_duration_ms=150.0),
    "ਔ": VowelMappingEntry(phoneme_sequences=[_sequence(["au"]), _sequence(["ɔ"])], average_duration_ms=170.0),
}


FormantScorer = Callable[[DetectedPhonemeCluster, str, VowelMappingEntry], Optional[float]]


class VowelAnalyzer:
    """Analyse phoneme predictions and score them against expected vowels."""

    def __init__(
        self,
        mapping_table: Optional[Dict[str, VowelMappingEntry]] = None,
        match_threshold: float = 0.6,
        formant_scorer: Optional[FormantScorer] = None,
    ) -> None:
        self.mapping_table: Dict[str, VowelMappingEntry] = mapping_table or DEFAULT_VOWEL_MAPPING
        self.match_threshold = match_threshold
        self.formant_scorer = formant_scorer
        self._phoneme_lookup: Dict[str, str] = self._build_phoneme_lookup()

    def _build_phoneme_lookup(self) -> Dict[str, str]:
        lookup: Dict[str, str] = {}
        for vowel, entry in self.mapping_table.items():
            for sequence in entry.phoneme_sequences:
                for phoneme in sequence:
                    lookup.setdefault(phoneme, vowel)
        return lookup

    def collapse_phonemes(
        self, predictions: Sequence[PhonemePrediction]
    ) -> List[Tuple[str, List[PhonemePrediction]]]:
        """Collapse phonemes into contiguous clusters labelled by vowel."""

        clusters: List[Tuple[str, List[PhonemePrediction]]] = []
        current_vowel: Optional[str] = None
        current_cluster: List[PhonemePrediction] = []

        for prediction in predictions:
            vowel = self._phoneme_lookup.get(prediction.phoneme)
            if vowel is None:
                if current_cluster:
                    clusters.append((current_vowel or "", current_cluster))
                    current_cluster = []
                    current_vowel = None
                continue

            if current_vowel != vowel and current_cluster:
                clusters.append((current_vowel or vowel, current_cluster))
                current_cluster = []

            current_vowel = vowel
            current_cluster.append(prediction)

        if current_cluster:
            clusters.append((current_vowel or "", current_cluster))

        return clusters

    def analyze(
        self,
        expected_vowels: Sequence[str],
        predictions: Sequence[PhonemePrediction],
    ) -> VowelFeedback:
        """Analyse predictions for the expected vowels and return structured feedback."""

        clusters = self.collapse_phonemes(predictions)
        cluster_index = 0
        assessments: Dict[str, VowelAssessment] = {}

        for expected in expected_vowels:
            entry = self.mapping_table.get(expected)
            cluster_predictions: Optional[List[PhonemePrediction]] = None

            while cluster_index < len(clusters):
                vowel_label, predictions_for_vowel = clusters[cluster_index]
                cluster_index += 1
                if vowel_label == expected:
                    cluster_predictions = predictions_for_vowel
                    break

            assessments[expected] = self._evaluate_vowel(expected, entry, cluster_predictions)

        return VowelFeedback(assessments=assessments)

    def _evaluate_vowel(
        self,
        expected_vowel: str,
        mapping_entry: Optional[VowelMappingEntry],
        cluster_predictions: Optional[Sequence[PhonemePrediction]],
    ) -> VowelAssessment:
        if not cluster_predictions:
            return VowelAssessment(
                expected_vowel=expected_vowel,
                detected_cluster=None,
                confidence=0.0,
                match=False,
                scores=VowelScoreDetails(levenshtein_distance=None),
            )

        detected_cluster = self._build_cluster(cluster_predictions)

        expected_sequence = self._get_reference_sequence(mapping_entry)
        detected_sequence = detected_cluster.phonemes

        levenshtein_distance = self._levenshtein(expected_sequence, detected_sequence)
        phoneme_similarity = self._normalise_similarity(levenshtein_distance, expected_sequence, detected_sequence)

        duration_score, duration_delta = self._duration_score(detected_cluster, mapping_entry)
        formant_similarity = self._formant_score(detected_cluster, expected_vowel, mapping_entry)

        overall_score = self._aggregate_scores(
            phoneme_similarity=phoneme_similarity,
            duration_score=duration_score,
            formant_similarity=formant_similarity,
        )

        return VowelAssessment(
            expected_vowel=expected_vowel,
            detected_cluster=detected_cluster,
            confidence=overall_score,
            match=overall_score >= self.match_threshold,
            scores=VowelScoreDetails(
                levenshtein_distance=levenshtein_distance,
                phoneme_similarity=phoneme_similarity,
                duration_score=duration_score,
                duration_difference_ms=duration_delta,
                formant_similarity=formant_similarity,
                overall_score=overall_score,
            ),
        )

    def _build_cluster(
        self, predictions: Sequence[PhonemePrediction]
    ) -> DetectedPhonemeCluster:
        phonemes = [prediction.phoneme for prediction in predictions]

        start_times = [p.start for p in predictions if p.start is not None]
        end_times = [p.end for p in predictions if p.end is not None]

        start = min(start_times) if start_times else None
        end = max(end_times) if end_times else None
        duration_ms = (end - start) * 1000 if start is not None and end is not None else None

        confidences = [p.confidence for p in predictions if p.confidence is not None]
        average_confidence = sum(confidences) / len(confidences) if confidences else None

        return DetectedPhonemeCluster(
            phonemes=phonemes,
            start=start,
            end=end,
            duration_ms=duration_ms,
            average_confidence=average_confidence,
        )

    def _get_reference_sequence(self, entry: Optional[VowelMappingEntry]) -> Sequence[str]:
        if entry and entry.phoneme_sequences:
            return entry.phoneme_sequences[0]
        return []

    @staticmethod
    def _levenshtein(expected: Sequence[str], detected: Sequence[str]) -> int:
        if not expected:
            return len(detected)
        if not detected:
            return len(expected)

        dp = [[0] * (len(detected) + 1) for _ in range(len(expected) + 1)]
        for i in range(len(expected) + 1):
            dp[i][0] = i
        for j in range(len(detected) + 1):
            dp[0][j] = j

        for i, expected_symbol in enumerate(expected, start=1):
            for j, detected_symbol in enumerate(detected, start=1):
                cost = 0 if expected_symbol == detected_symbol else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,  # deletion
                    dp[i][j - 1] + 1,  # insertion
                    dp[i - 1][j - 1] + cost,  # substitution
                )

        return dp[-1][-1]

    @staticmethod
    def _normalise_similarity(
        distance: int,
        expected: Sequence[str],
        detected: Sequence[str],
    ) -> float:
        baseline = max(len(expected), len(detected), 1)
        similarity = max(0.0, 1.0 - (distance / baseline))
        return similarity

    def _duration_score(
        self,
        cluster: DetectedPhonemeCluster,
        entry: Optional[VowelMappingEntry],
    ) -> Tuple[Optional[float], Optional[float]]:
        if cluster.duration_ms is None or entry is None or entry.average_duration_ms is None:
            return None, None

        delta = abs(cluster.duration_ms - entry.average_duration_ms)
        normalised = max(0.0, 1.0 - (delta / max(entry.average_duration_ms, 1.0)))
        return normalised, delta

    def _formant_score(
        self,
        cluster: DetectedPhonemeCluster,
        expected_vowel: str,
        entry: Optional[VowelMappingEntry],
    ) -> Optional[float]:
        if self.formant_scorer is None or entry is None:
            return None

        score = self.formant_scorer(cluster, expected_vowel, entry)
        if score is None:
            return None
        return max(0.0, min(1.0, score))

    @staticmethod
    def _aggregate_scores(
        *,
        phoneme_similarity: float,
        duration_score: Optional[float],
        formant_similarity: Optional[float],
    ) -> float:
        weights: List[Tuple[float, float]] = [(phoneme_similarity, 0.6)]
        if duration_score is not None:
            weights.append((duration_score, 0.2))
        if formant_similarity is not None:
            weights.append((formant_similarity, 0.2))

        total_weight = sum(weight for _, weight in weights)
        if total_weight == 0:
            return 0.0

        score = sum(value * weight for value, weight in weights) / total_weight
        return max(0.0, min(1.0, score))


__all__ = [
    "DEFAULT_VOWEL_MAPPING",
    "VowelAnalyzer",
    "VowelMappingEntry",
]

