from __future__ import annotations
from pathlib import Path
from typing import List
from app.schemas import StyleText
from app.integrations.tts_client import TTSClient
from app.integrations.storage_client import StorageClient


class TTSAgent:
    """语音合成与上传 Agent。"""

    def __init__(self, runtime_dir: str):
        self.runtime_dir = Path(runtime_dir)
        self.tts = TTSClient()
        self.storage = StorageClient()

    def run(self, aid: str, styles: List[StyleText]) -> List[StyleText]:
        audio_dir = self.runtime_dir / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)
        for style in styles:
            filename = f"{aid or 'artifact'}_{style.style_id}.wav"
            local_path = audio_dir / filename
            tts_info = self.tts.synthesize(style.text, style.voice_name, str(local_path))
            style.local_audio_path = tts_info["local_audio_path"]
            style.estimated_duration_sec = tts_info["duration_sec"]
            object_key = f"museum_agent/{filename}"
            style.audio_url = self.storage.upload_audio(str(local_path), object_key)
        return styles
