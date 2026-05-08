from __future__ import annotations
import json
from pathlib import Path
import requests
from app.settings import get_settings


class BusinessAPI:
    """业务后台同步适配层。"""

    def __init__(self):
        self.settings = get_settings()
        self.runtime_dir = Path(self.settings.RUNTIME_DIR)
        self.runtime_dir.mkdir(parents=True, exist_ok=True)

    def sync_artifact_result(self, payload: dict) -> dict:
        if self.settings.MOCK_MODE or not self.settings.BUSINESS_SYNC_API_URL:
            path = self.runtime_dir / "sync_records.jsonl"
            with path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(payload, ensure_ascii=False) + "\n")
            return {"mode": "mock", "saved_to": str(path), "code": 1, "msg": "本地回写成功"}

        resp = requests.post(
            self.settings.BUSINESS_SYNC_API_URL,
            json=payload,
            timeout=self.settings.BUSINESS_SYNC_TIMEOUT_SECONDS,
        )
        resp.raise_for_status()
        return resp.json()
