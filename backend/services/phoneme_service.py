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
from pathlib import Path
from typing import BinaryIO, Callable, Iterable, List, Optional, Tuple
import os
import subprocess
import tempfile

from allosaurus.app import read_recognizer
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

from backend.models.transcript import PhonemePrediction


try:  # pragma: no cover - exercised in integration tests instead
    from imageio_ffmpeg import get_ffmpeg_exe
except Exception:  # pragma: no cover - missing optional dependency
    get_ffmpeg_exe = None  # type: ignore[assignment]

class PhonemeService:
    """Service responsible for extracting phoneme timelines from audio."""

    def __init__(self, model_name: str = "latest", default_language: str = "ipa"):
        """Initialise the service.

        Args:
            model_name: Allosaurus model identifier. ``"latest"`` gives the
                community-maintained universal model which has broad phoneme
                coverage, including Punjabi sounds.
            default_language: Allosaurus language tag used during inference.
                ``"ipa"`` yields the universal phoneme inventory which captures
                Punjabi vowels reliably across accents.
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

        source_name = getattr(audio_file, "name", "") or "audio"
        wav_path, cleanup = self._prepare_wav_bytes(raw_bytes, source_name)

        recognizer = self._get_recognizer()
        target_language = language or self._default_language

        try:
            timeline = recognizer.recognize(
                wav_path,
                lang_id=target_language,
                timestamp=True,
            )
        finally:
            cleanup()

        return list(self._iter_segments(timeline))

    def _prepare_wav_bytes(self, raw_bytes: bytes, source_name: str) -> Tuple[str, Callable[[], None]]:
        """Return a path to a normalised WAV file derived from ``raw_bytes``."""

        try:
            return self._export_with_pydub(raw_bytes)
        except (FileNotFoundError, CouldntDecodeError, OSError) as exc:
            if get_ffmpeg_exe is None:
                raise RuntimeError(
                    "ffmpeg/ffprobe binaries are unavailable. Install imageio-ffmpeg "
                    "or place ffmpeg on PATH to enable phoneme extraction."
                ) from exc
            return self._export_with_ffmpeg(raw_bytes, source_name)

    def _export_with_pydub(self, raw_bytes: bytes) -> Tuple[str, Callable[[], None]]:
        audio_segment = AudioSegment.from_file(BytesIO(raw_bytes))
        audio_segment = audio_segment.set_channels(1).set_frame_rate(16000)

        tmp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        try:
            audio_segment.export(tmp_file, format="wav")
        finally:
            tmp_file.close()

        return tmp_file.name, lambda: self._safe_unlink(tmp_file.name)

    def _export_with_ffmpeg(self, raw_bytes: bytes, source_name: str) -> Tuple[str, Callable[[], None]]:
        assert get_ffmpeg_exe is not None  # for type checkers

        suffix = Path(source_name).suffix or ".tmp"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as src_file:
            src_file.write(raw_bytes)
            src_path = src_file.name

        dest_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        dest_path = dest_file.name
        dest_file.close()

        ffmpeg_path = get_ffmpeg_exe()
        command = [
            ffmpeg_path,
            "-y",
            "-i",
            src_path,
            "-ac",
            "1",
            "-ar",
            "16000",
            dest_path,
        ]

        try:
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as exc:  # pragma: no cover - requires ffmpeg failure
            stderr = exc.stderr.decode(errors="ignore") if exc.stderr else ""
            raise RuntimeError(
                "Failed to convert audio using ffmpeg: " + stderr.strip()
            ) from exc
        finally:
            self._safe_unlink(src_path)

        return dest_path, lambda: self._safe_unlink(dest_path)

    @staticmethod
    def _safe_unlink(path: str) -> None:
        try:
            os.unlink(path)
        except OSError:
            pass

    @staticmethod
    def _iter_segments(timeline) -> List[PhonemePrediction]:
        """Normalise the different structures returned by Allosaurus."""

        if timeline is None:
            return []

        if isinstance(timeline, str):
            return list(PhonemeService._parse_timeline_string(timeline))

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

    @staticmethod
    def _parse_timeline_string(timeline: str) -> Iterable[PhonemePrediction]:
        for line in timeline.splitlines():
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) < 3:
                continue

            try:
                start = float(parts[0])
                window = float(parts[1])
            except ValueError:
                start = None
                window = None

            phoneme = parts[2]
            end = start + window if start is not None and window is not None else None

            yield PhonemePrediction(
                phoneme=phoneme,
                start=start,
                end=end,
                confidence=None,
            )


_phoneme_service: Optional[PhonemeService] = None


def get_phoneme_service() -> PhonemeService:
    """Return a singleton instance of :class:`PhonemeService`."""

    global _phoneme_service
    if _phoneme_service is None:
        _phoneme_service = PhonemeService()
    return _phoneme_service

