from __future__ import annotations
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ArtifactInput(BaseModel):
    aid: Optional[str] = None
    collection_name: Optional[str] = None
    original_description: Optional[str] = None
    image_path: Optional[str] = None
    image_url: Optional[str] = None
    video_materials: List[str] = Field(default_factory=list)
    position: Optional[str] = None
    category_name: Optional[str] = None
    extra: Dict[str, Any] = Field(default_factory=dict)


class ArtifactKnowledge(BaseModel):
    aid: Optional[str] = None
    artifact_name: str
    dynasty: str = "未知"
    category: str = "文物"
    material: str = "未知"
    unearthed_info: str = ""
    museum: str = "河南博物院"
    location: str = ""
    visual_features: List[str] = Field(default_factory=list)
    historical_context: str = ""
    source_summary: str = ""
    confidence: float = 0.8


class StyleText(BaseModel):
    style_id: str
    style_name: str
    voice_name: str
    text: str
    word_count: int
    estimated_duration_sec: float
    review_score: float = 0.0
    review_notes: List[str] = Field(default_factory=list)
    audio_url: Optional[str] = None
    local_audio_path: Optional[str] = None


class ArtifactResult(BaseModel):
    aid: Optional[str] = None
    input_file: Optional[str] = None
    knowledge: ArtifactKnowledge
    styles: List[StyleText]
    sync_status: str = "pending"
    sync_response: Dict[str, Any] = Field(default_factory=dict)


class JobResult(BaseModel):
    job_id: str
    total_count: int
    success_count: int
    fail_count: int
    results: List[ArtifactResult]
    errors: List[Dict[str, Any]] = Field(default_factory=list)
