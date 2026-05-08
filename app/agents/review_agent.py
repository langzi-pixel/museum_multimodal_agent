from __future__ import annotations
from typing import List
from app.schemas import ArtifactKnowledge, StyleText


class ReviewAgent:
    """内容质检 Agent：检查事实一致性、长度、AI 腔和口播流畅度。"""

    def run(self, knowledge: ArtifactKnowledge, styles: List[StyleText]) -> List[StyleText]:
        reviewed = []
        for item in styles:
            notes = []
            score = 1.0
            if knowledge.artifact_name not in item.text:
                notes.append("未包含文物名称")
                score -= 0.25
            if len(item.text) < 80:
                notes.append("文本略短")
                score -= 0.15
            if "作为一个AI" in item.text or "我是AI" in item.text:
                notes.append("存在 AI 自称")
                score -= 0.30
            if item.text.count("。") < 3:
                notes.append("句式层次不足")
                score -= 0.10

            item.review_score = round(max(score, 0.0), 2)
            item.review_notes = notes or ["通过基础质检"]
            reviewed.append(item)
        return reviewed
