from __future__ import annotations
from app.schemas import ArtifactInput, ArtifactKnowledge
from app.integrations.llm_client import LLMClient


class RecognitionAgent:
    """文物识别与信息抽取 Agent。"""

    def __init__(self):
        self.llm = LLMClient()

    def run(self, item: ArtifactInput) -> ArtifactKnowledge:
        prompt = f"""
你是文博资料识别 Agent。请根据文物图片路径、在线图片链接和已有文字资料，抽取结构化知识。
必须返回 JSON，不要返回 Markdown。
字段：artifact_name, dynasty, category, material, unearthed_info, museum, location,
visual_features(list), historical_context, source_summary, confidence。

输入：
- aid: {item.aid}
- collection_name: {item.collection_name}
- original_description: {item.original_description}
- image_path: {item.image_path}
- image_url: {item.image_url}
- category_name: {item.category_name}
- position: {item.position}
""".strip()
        data = self.llm.json_chat([
            {"role": "system", "content": "你是严谨的文博资料结构化抽取助手。"},
            {"role": "user", "content": prompt},
        ])

        if item.collection_name and not data.get("artifact_name"):
            data["artifact_name"] = item.collection_name
        if item.aid:
            data["aid"] = item.aid
        if item.position and not data.get("location"):
            data["location"] = item.position

        return ArtifactKnowledge(**data)
