from __future__ import annotations
from pathlib import Path
import wave
import math
import struct
from app.settings import get_settings


class TTSClient:
    """TTS 适配层。

    Demo 默认生成可播放的 mock wav 文件。真实接入讯飞/火山/阿里等 TTS 时，
    可以在 synthesize() 中替换为 WebSocket 或 HTTP 调用。
    """

    def __init__(self):
        self.settings = get_settings()

    def synthesize(self, text: str, voice_name: str, output_path: str) -> dict:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        duration = max(2.0, min(45.0, len(text) / 4.2))

        if self.settings.MOCK_MODE:
            self._write_mock_wav(path, duration_sec=duration)
            return {
                "local_audio_path": str(path),
                "duration_sec": round(duration, 2),
                "voice_name": voice_name,
                "provider": "mock-wav",
            }

        # 真实环境中可以替换为讯飞 TTS WebSocket 调用。
        self._write_mock_wav(path, duration_sec=duration)
        return {
            "local_audio_path": str(path),
            "duration_sec": round(duration, 2),
            "voice_name": voice_name,
            "provider": "placeholder",
        }

    @staticmethod
    def _write_mock_wav(path: Path, duration_sec: float, sample_rate: int = 16000):
        frames = int(duration_sec * sample_rate)
        # 生成静音 wav，速度快、体积小，用于证明 TTS 链路已经产生产物。
        with wave.open(str(path), "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(b"\x00\x00" * frames)
