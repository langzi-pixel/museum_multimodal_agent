from __future__ import annotations
import json
import uuid
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from app.settings import get_settings
from app.schemas import ArtifactInput, ArtifactResult, JobResult
from app.agents.recognition_agent import RecognitionAgent
from app.agents.generation_agent import GenerationAgent
from app.agents.review_agent import ReviewAgent
from app.agents.tts_agent import TTSAgent
from app.agents.sync_agent import SyncAgent

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


class MuseumAgentPipeline:
    def __init__(self):
        self.settings = get_settings()
        self.runtime_dir = Path(self.settings.RUNTIME_DIR)
        self.runtime_dir.mkdir(parents=True, exist_ok=True)
        self.recognition = RecognitionAgent()
        self.generation = GenerationAgent()
        self.review = ReviewAgent()
        self.tts = TTSAgent(str(self.runtime_dir))
        self.sync = SyncAgent()

    def process_one(self, item: ArtifactInput) -> ArtifactResult:
        knowledge = self.recognition.run(item)
        styles = self.generation.run(knowledge)
        styles = self.review.run(knowledge, styles)
        aid = item.aid or self._safe_id(knowledge.artifact_name)
        styles = self.tts.run(aid, styles)
        result = ArtifactResult(
            aid=item.aid,
            input_file=item.image_path,
            knowledge=knowledge,
            styles=styles,
        )
        return self.sync.run(result)

    def process_zip(self, zip_path: str) -> JobResult:
        job_id = datetime.now().strftime("%Y%m%d_%H%M%S_") + uuid.uuid4().hex[:6]
        job_dir = self.runtime_dir / "jobs" / job_id
        extract_dir = job_dir / "input"
        extract_dir.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_dir)

        items = self._load_items_from_dir(extract_dir)
        results: List[ArtifactResult] = []
        errors = []
        for item in items:
            try:
                results.append(self.process_one(item))
            except Exception as e:
                errors.append({"input": item.model_dump(), "error": str(e)})

        out = JobResult(
            job_id=job_id,
            total_count=len(items),
            success_count=len(results),
            fail_count=len(errors),
            results=results,
            errors=errors,
        )
        (job_dir / "result.json").write_text(out.model_dump_json(indent=2), encoding="utf-8")
        return out

    def _load_items_from_dir(self, root: Path) -> List[ArtifactInput]:
        json_files = list(root.rglob("*.json"))
        image_files = [p for p in root.rglob("*") if p.suffix.lower() in IMAGE_EXTS]
        items: List[ArtifactInput] = []

        used_images = set()
        for jf in json_files:
            data = json.loads(jf.read_text(encoding="utf-8"))
            image_path = data.get("image_path")
            if not image_path:
                # 选同名图片或第一张未使用图片
                same_stem = [p for p in image_files if p.stem == jf.stem]
                candidate = same_stem[0] if same_stem else next((p for p in image_files if p not in used_images), None)
                if candidate:
                    image_path = str(candidate)
                    used_images.add(candidate)
            items.append(ArtifactInput(
                aid=data.get("aid") or data.get("id"),
                collection_name=data.get("collection_name") or data.get("name"),
                original_description=data.get("original_description") or data.get("description"),
                image_path=image_path,
                image_url=(data.get("image_materials") or [None])[0] if isinstance(data.get("image_materials"), list) else data.get("image_url"),
                video_materials=data.get("video_materials") or [],
                position=data.get("position"),
                category_name=data.get("freeclassificationmanagement_classification_name") or data.get("category_name"),
                extra=data,
            ))

        # 没有 JSON 时，按图片直接生成任务
        if not items:
            for img in image_files:
                items.append(ArtifactInput(
                    aid=img.stem,
                    collection_name=img.stem,
                    image_path=str(img),
                    original_description="",
                ))
        return items

    @staticmethod
    def _safe_id(text: Optional[str]) -> str:
        text = text or "artifact"
        return "".join(ch if ch.isalnum() else "_" for ch in text)[:64]
