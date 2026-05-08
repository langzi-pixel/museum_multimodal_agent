from __future__ import annotations
from typing import List
from app.schemas import ArtifactKnowledge, StyleText


STYLE_PRESETS = [
    {"style_id": "expert", "style_name": "专家严谨风", "voice_name": "xiaoyan"},
    {"style_id": "kids", "style_name": "儿童科普风", "voice_name": "xiaoqi"},
    {"style_id": "talkshow", "style_name": "脱口秀风", "voice_name": "xiaofeng"},
    {"style_id": "classic", "style_name": "古风雅韵风", "voice_name": "xiaomei"},
    {"style_id": "internet", "style_name": "网感趣味风", "voice_name": "xiaoyou"},
    {"style_id": "guide", "style_name": "导游讲解风", "voice_name": "xiaoyu"},
    {"style_id": "shortvideo", "style_name": "短视频口播风", "voice_name": "xiaoxue"},
    {"style_id": "study", "style_name": "研学课程风", "voice_name": "xiaoshi"},
]


class GenerationAgent:
    """多风格文物讲解生成 Agent。"""

    def run(self, knowledge: ArtifactKnowledge) -> List[StyleText]:
        styles: List[StyleText] = []
        for preset in STYLE_PRESETS:
            text = self._build_text(knowledge, preset["style_name"])
            styles.append(StyleText(
                style_id=preset["style_id"],
                style_name=preset["style_name"],
                voice_name=preset["voice_name"],
                text=text,
                word_count=len(text),
                estimated_duration_sec=round(len(text) / 4.2, 2),
            ))
        return styles

    @staticmethod
    def _build_text(k: ArtifactKnowledge, style_name: str) -> str:
        feature_text = "、".join(k.visual_features[:4]) if k.visual_features else "造型独特、工艺精湛"
        base = (
            f"欢迎了解{k.museum}馆藏文物《{k.artifact_name}》。"
            f"它通常被归入{k.dynasty}的{k.category}，材质为{k.material}。"
            f"这件文物的主要特征包括{feature_text}。"
            f"{k.unearthed_info}{k.historical_context}"
        )
        if style_name == "专家严谨风":
            return base + "从考古与艺术史角度看，它不仅是器物，更是礼制、审美与技术体系共同作用的结果。"
        if style_name == "儿童科普风":
            return base + "你可以把它想象成古人留下的一张立体名片，告诉我们他们怎样生活、怎样表达敬畏。"
        if style_name == "脱口秀风":
            return base + "别看它静静站在展柜里，放在三千多年前，它可是妥妥的高端定制款。"
        if style_name == "古风雅韵风":
            return base + "凝眸其形，似可见殷商烟云、礼乐余响，在青铜光泽中缓缓铺展。"
        if style_name == "网感趣味风":
            return base + "这不是普通文物，这是古代审美、技术和仪式感同时在线的代表作。"
        if style_name == "导游讲解风":
            return base + "大家可以重点观察它的整体轮廓和细部纹饰，这些地方最能体现它的价值。"
        if style_name == "短视频口播风":
            return base + "一分钟看懂这件文物：它的价值不只在好看，更在于它背后浓缩的时代信息。"
        if style_name == "研学课程风":
            return base + "同学们可以思考三个问题：它为什么这样造型？它服务于什么场景？它反映了怎样的社会观念？"
        return base
