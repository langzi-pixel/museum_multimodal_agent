from __future__ import annotations
from pathlib import Path
from app.settings import get_settings


class StorageClient:
    """对象存储适配层。

    MOCK_MODE 下返回本地可访问 URL；真实环境可替换为华为 OBS / 阿里 OSS / MinIO 上传。
    """

    def __init__(self):
        self.settings = get_settings()

    def upload_audio(self, local_path: str, object_key: str) -> str:
        if self.settings.MOCK_MODE or not self.settings.OBS_ACCESS_KEY:
            return f"{self.settings.PUBLIC_BASE_URL}/static/audio/{Path(local_path).name}"

        # 真实接入时在这里调用 obs.ObsClient.putFile。
        # 为避免提交密钥和依赖复杂化，Demo 保持适配层占位。
        prefix = self.settings.OBS_PUBLIC_PREFIX.rstrip("/")
        return f"{prefix}/{object_key}" if prefix else object_key
