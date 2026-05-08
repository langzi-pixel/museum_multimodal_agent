from __future__ import annotations
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from app.pipeline import MuseumAgentPipeline
from app.schemas import ArtifactInput
from app.settings import get_settings

settings = get_settings()
app = FastAPI(
    title="文博多模态内容生产与语音讲解 Agent 系统",
    description="图片/资料包上传、文物识别、多风格讲解生成、TTS、业务回写的一体化 Agent Demo。",
    version="1.0.0",
)

runtime_dir = Path(settings.RUNTIME_DIR)
(runtime_dir / "uploads").mkdir(parents=True, exist_ok=True)
(runtime_dir / "audio").mkdir(parents=True, exist_ok=True)
app.mount("/static/audio", StaticFiles(directory=str(runtime_dir / "audio")), name="audio")

pipeline = MuseumAgentPipeline()


@app.get("/health")
def health():
    return {"code": 1, "msg": "ok", "mock_mode": settings.MOCK_MODE}


@app.post("/api/v1/process_one")
def process_one(item: ArtifactInput):
    result = pipeline.process_one(item)
    return {"code": 1, "msg": "处理完成", "data": result.model_dump()}


@app.post("/api/v1/process_zip")
def process_zip(file: UploadFile = File(...)):
    suffix = Path(file.filename or "upload.zip").suffix.lower()
    if suffix != ".zip":
        return {"code": 0, "msg": "仅支持 zip 压缩包", "data": None}

    save_path = runtime_dir / "uploads" / (file.filename or "upload.zip")
    with save_path.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    job = pipeline.process_zip(str(save_path))
    return {
        "code": 1,
        "msg": "压缩包处理完成",
        "data": job.model_dump(),
    }
