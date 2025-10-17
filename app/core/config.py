from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional, Dict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra="ignore"
    )

    APP_NAME: str = "wald-2api"
    APP_VERSION: str = "1.1.0"
    DESCRIPTION: str = "一个将 app.wald.ai 转换为兼容 OpenAI 格式 API 的高性能代理。"

    API_MASTER_KEY: Optional[str] = None
    WOS_SESSION_COOKIE: Optional[str] = None

    API_REQUEST_TIMEOUT: int = 180
    NGINX_PORT: int = 8088

    # 模型别名到 Wald.ai 内部 llmEngine 名称的精确映射
    MODEL_MAPPING: Dict[str, str] = {
        # 根据抓包数据精确映射
        "gpt-3.5-turbo": "GPTo3",
        "gpt-5": "GPT5",
        "gpt-5-mini": "GPT5_MINI",
        "grok-3-mini": "GROK_3_MINI",
        "grok-3": "GROK_3",
        "grok-4": "GROK_4",
        "gemini-2.5-flash": "GEMINI2",
        "claude-3-opus": "CLAUDE", # 抓包显示为 CLAUDE
        "claude-3-sonnet": "CLAUDE2", # 抓包显示为 CLAUDE2
        "claude-3.5-haiku": "CLAUDE3", # 抓包显示为 CLAUDE3
        "wald-gpt": "WALD_GPT"
    }

settings = Settings()
