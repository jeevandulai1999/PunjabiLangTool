"""Data models describing vowel pronunciation feedback."""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class DetectedPhonemeCluster(BaseModel):
    """Represents a contiguous cluster of phoneme predictions for a vowel."""

    phonemes: List[str] = Field(description="Ordered list of detected phoneme labels")
    start: Optional[float] = Field(
        default=None,
        ge=0.0,
        description="Start time in seconds of the cluster (min of constituent phonemes)",
    )
    end: Optional[float] = Field(
        default=None,
        ge=0.0,
        description="End time in seconds of the cluster (max of constituent phonemes)",
    )
    duration_ms: Optional[float] = Field(
        default=None,
        ge=0.0,
        description="Computed duration of the cluster in milliseconds",
    )
    average_confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Mean confidence of the constituent phoneme predictions",
    )


class VowelScoreDetails(BaseModel):
    """Breakdown of the scoring heuristics applied to a vowel."""

    levenshtein_distance: Optional[int] = Field(
        default=None,
        ge=0,
        description="Edit distance between expected and detected phoneme sequences",
    )
    phoneme_similarity: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Normalised score derived from the Levenshtein distance",
    )
    duration_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Score reflecting how close the duration was to the canonical average",
    )
    duration_difference_ms: Optional[float] = Field(
        default=None,
        ge=0.0,
        description="Absolute difference between detected and canonical duration (ms)",
    )
    formant_similarity: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Score provided by a downstream formant analysis hook",
    )
    overall_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Weighted aggregate score combining all heuristics",
    )


class VowelAssessment(BaseModel):
    """Assessment of a single expected vowel against detected phonemes."""

    expected_vowel: str = Field(description="Canonical Gurmukhi vowel under evaluation")
    detected_cluster: Optional[DetectedPhonemeCluster] = Field(
        default=None, description="Detected phoneme cluster aligned to the vowel"
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Overall confidence that the detected vowel matches the canonical sound",
    )
    match: bool = Field(
        description="Flag indicating whether the vowel satisfied the configured threshold"
    )
    scores: VowelScoreDetails = Field(
        description="Breakdown of the heuristic scores contributing to the assessment"
    )


class VowelFeedback(BaseModel):
    """Aggregate feedback for multiple vowels in a pronunciation attempt."""

    assessments: Dict[str, VowelAssessment] = Field(
        description="Mapping of expected vowels to their assessment details"
    )

