"""Speech service client: self-hosted, OpenAI-compatible, optional.

The browser captures and plays audio; recognition and synthesis happen
here, server-side, against {SPEECH_URL}. The language sent with STT/TTS is
the session language — there is no separate speech-language config.
"""
from __future__ import annotations

import sys

import httpx

from core.pizzasim import optional_env


class SpeechUnavailable(Exception):
    pass


class SpeechService:
    """All-or-nothing: enabled only if SPEECH_URL is set, all models are
    configured, and the service answered the startup probe with 2xx."""

    def __init__(self):
        self.url = (optional_env("SPEECH_URL") or "").rstrip("/")
        self.stt_model = optional_env("SPEECH_STT_MODEL")
        self.tts_model = optional_env("SPEECH_TTS_MODEL")
        self.voice = optional_env("SPEECH_TTS_VOICE")
        # Optional English voice: both-or-neither. A monolingual default
        # voice cannot speak English, so English sessions may get their
        # own pair; half-configured counts as unset (issue #11).
        self.tts_model_en = optional_env("SPEECH_TTS_MODEL_EN")
        self.voice_en = optional_env("SPEECH_TTS_VOICE_EN")
        if bool(self.tts_model_en) != bool(self.voice_en):
            print("SPEECH_TTS_MODEL_EN/SPEECH_TTS_VOICE_EN: only one is "
                  "set — English falls back to the default voice",
                  file=sys.stderr)
            self.tts_model_en = self.voice_en = None
        # Optional bearer token for a speech service that requires one.
        # Unset → no Authorization header, exactly as before.
        key = optional_env("SPEECH_API_KEY")
        self.headers = {"Authorization": f"Bearer {key}"} if key else {}
        self.enabled = False
        if self.url and self.stt_model and self.tts_model and self.voice:
            try:
                httpx.get(f"{self.url}/v1/models", headers=self.headers,
                          timeout=3.0).raise_for_status()
                self.enabled = True
            except httpx.HTTPError:
                print("speech service not answering — text-only mode",
                      file=sys.stderr)

    def stt(self, audio: bytes, filename: str, content_type: str,
            lang: str) -> str:
        try:
            response = httpx.post(
                f"{self.url}/v1/audio/transcriptions",
                files={"file": (filename, audio, content_type)},
                data={"model": self.stt_model, "language": lang},
                headers=self.headers, timeout=60.0)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise SpeechUnavailable(str(exc)) from exc
        return response.json().get("text", "")

    def tts(self, text: str, lang: str) -> tuple[bytes, str]:
        model, voice = self.tts_model, self.voice
        if lang == "en" and self.tts_model_en and self.voice_en:
            model, voice = self.tts_model_en, self.voice_en
        try:
            response = httpx.post(
                f"{self.url}/v1/audio/speech",
                json={"model": model, "voice": voice,
                      "input": text, "language": lang},
                headers=self.headers, timeout=60.0)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise SpeechUnavailable(str(exc)) from exc
        return (response.content,
                response.headers.get("content-type", "audio/mpeg"))
