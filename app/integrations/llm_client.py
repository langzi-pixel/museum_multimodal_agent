from __future__ import annotations
import json
import requests
from typing import Dict, Any, List
from app.settings import get_settings


class LLMClient:
    """OpenAI-compatible Chat Completions client.

    MOCK_MODE=true 时不会访问网络，便于提交材料和本地演示。
    """

    def __init__(self):
        self.settings = get_settings()

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.4) -> str:
        if self.settings.MOCK_MODE or not self.settings.ARK_API_KEY:
            return self._mock_chat(messages)

        headers = {
            "Authorization": f"Bearer {self.settings.ARK_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.settings.ARK_MODEL,
            "messages": messages,
            "temperature": temperature,
        }
        resp = requests.post(
            self.settings.ARK_BASE_URL,
            headers=headers,
            json=payload,
            timeout=self.settings.ARK_TIMEOUT_SECONDS,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    def json_chat(self, messages: List[Dict[str, str]], temperature: float = 0.2) -> Dict[str, Any]:
        text = self.chat(messages, temperature=temperature)
        try:
            return json.loads(text)
        except Exception:
            start = text.find("{")
            end = text.rfind("}")
            if start >= 0 and end > start:
                return json.loads(text[start:end + 1])
            raise ValueError(f"LLM 返回不是有效 JSON: {text[:300]}")

    def _mock_chat(self, messages: List[Dict[str, str]]) -> str:
        joined = "\n".join(m.get("content", "") for m in messages)
        if "JSON" in joined or "json" in joined:
            return json.dumps({
                "artifact_name": "妇好鸮尊",
                "dynasty": "商代晚期",
                "category": "青铜器",
                "material": "青铜",
                "unearthed_info": "1976 年出土于河南安阳殷墟妇好墓。",
                "museum": "河南博物院",
                "location": "主展馆",
                "visual_features": ["鸮鸟造型", "双足与宽尾形成三点支撑", "器身饰有精细纹饰"],
                "historical_context": "体现了商代青铜铸造、礼制文化与鸟神崇拜。",
                "source_summary": "该器物为商代晚期鸟形铜酒器，因内壁铭文“妇好”得名。",
                "confidence": 0.91,
            }, ensure_ascii=False)
        return "这是 MOCK_MODE 下生成的讲解内容。"
