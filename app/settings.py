from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    MOCK_MODE: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8001
    PUBLIC_BASE_URL: str = "http://127.0.0.1:8001"
    RUNTIME_DIR: str = "runtime"

    ARK_API_KEY: str = ""
    ARK_BASE_URL: str = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    ARK_MODEL: str = "doubao-seed-1-8-251228"
    ARK_TIMEOUT_SECONDS: int = 120

    BUSINESS_SYNC_API_URL: str = ""
    BUSINESS_SYNC_TIMEOUT_SECONDS: int = 30

    OBS_ACCESS_KEY: str = ""
    OBS_SECRET_KEY: str = ""
    OBS_SERVER: str = "https://obs.cn-north-4.myhuaweicloud.com"
    OBS_BUCKET: str = "yinglongzhiyou"
    OBS_PUBLIC_PREFIX: str = ""

    XFYUN_APP_ID: str = ""
    XFYUN_API_KEY: str = ""
    XFYUN_API_SECRET: str = ""
    XFYUN_TTS_URL: str = "wss://tts-api.xfyun.cn/v2/tts"


@lru_cache
def get_settings() -> Settings:
    return Settings()
