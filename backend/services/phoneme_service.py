"""Phoneme extraction service using a universal recognizer.

This module wraps the Allosaurus universal phoneme recognizer so that we can
extract time-aligned phoneme probabilities for Punjabi audio. Allosaurus was
chosen because its multilingual training corpus includes Indo-Aryan languages
and it exposes timestamped outputs, which makes it a good fit for Punjabi while
keeping the dependency lightweight compared to training a custom model.
"""

from __future__ import annotations

from io import BytesIO
from math import exp
from typing import BinaryIO, List, Optional
import os
import tempfile

from allosaurus.app import read_recognizer
from pydub import AudioSegment

from backend.models.transcript import PhonemePrediction


class PhonemeService:
    """Service responsible for extracting phoneme timelines from audio."""

    def __init__(self, model_name: str = "latest", default_language: str = "eng"):
        """Initialise the service.

        Args:
            model_name: Allosaurus model identifier. ``"latest"`` gives the
                community-maintained universal model which has broad phoneme
                coverage, including Punjabi sounds.
            default_language: Allosaurus language tag used during inference.
                Punjabi aligns best with the Indo-Aryan mapping which is exposed
                through the ``"eng"`` configuration in the current release.
        """

        self._model_name = model_name
        self._default_language = default_language
        self._recognizer = None

    def _get_recognizer(self):
        if self._recognizer is None:
            self._recognizer = read_recognizer(self._model_name)
        return self._recognizer

    def extract_phonemes(
        self,
        audio_file: BinaryIO,
        language: Optional[str] = None,
    ) -> List[PhonemePrediction]:
        """Extract a timeline of phoneme probabilities from an audio stream.

        Args:
            audio_file: Binary audio file object (any format supported by
                :mod:`pydub`). The pointer is reset to the start if the stream is
                seekable so that callers can reuse it afterwards.
            language: Optional language tag recognised by Allosaurus. When not
                provided the default configured for the service is used.

        Returns:
            List of dictionaries with ``phoneme``, ``start``, ``end`` (seconds)
            and ``confidence`` (0-1 probability when available).
        """

        # Read the audio data into memory so that we can fan it out to
        # conversion and recognition steps without assuming ``audio_file`` is a
        # real filesystem resource.
        raw_bytes = audio_file.read()
        if hasattr(audio_file, "seek"):
            audio_file.seek(0)

        audio_segment = AudioSegment.from_file(BytesIO(raw_bytes))
        audio_segment = audio_segment.set_channels(1).set_frame_rate(16000)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
            audio_segment.export(tmp, format="wav")

        recognizer = self._get_recognizer()
        target_language = language or self._default_language

        try:
            timeline = recognizer.recognize(
                tmp_path,
                lang=target_language,
                timestamp=True,
            )
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

        return list(self._iter_segments(timeline))

    @staticmethod
    def _iter_segments(timeline) -> List[PhonemePrediction]:
        """Normalise the different structures returned by Allosaurus."""

        if timeline is None:
            return []

        # ``timeline`` may be a list of objects or raw strings. Yield wrapped
        # structures so downstream code can work with a single representation.
        normalised: List[PhonemePrediction] = []
        for segment in timeline:
            phoneme = getattr(segment, "phoneme", None) or getattr(segment, "token", None)
            if phoneme is None:
                phoneme = str(segment)

            start = getattr(segment, "start", None)
            end = getattr(segment, "end", None)

            confidence = None
            if hasattr(segment, "confidence") and segment.confidence is not None:
                confidence = float(segment.confidence)
            elif hasattr(segment, "prob") and segment.prob is not None:
                confidence = float(segment.prob)
            elif hasattr(segment, "score") and segment.score is not None:
                confidence = float(segment.score)
            elif hasattr(segment, "log_prob") and segment.log_prob is not None:
                # Allosaurus exposes log probabilities – convert them to linear
                # space for easier interpretation.
                confidence = float(exp(segment.log_prob))

            normalised.append(
                PhonemePrediction(
                    phoneme=phoneme,
                    start=float(start) if start is not None else None,
                    end=float(end) if end is not None else None,
                    confidence=confidence,
                )
            )

        return normalised


_phoneme_service: Optional[PhonemeService] = None


def get_phoneme_service() -> PhonemeService:
    """Return a singleton instance of :class:`PhonemeService`."""

    global _phoneme_service
    if _phoneme_service is None:
        _phoneme_service = PhonemeService()
    return _phoneme_service

