
try:
    # pydantic v2
    from pydantic_settings import BaseSettings
except Exception:
    try:
        # pydantic v1
        from pydantic import BaseSettings
    except Exception:
        # fallback simple BaseSettings replacement
        class BaseSettings:
            def __init__(self, **kwargs):
                for k,v in kwargs.items():
                    setattr(self, k, v)

class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CACHE_TTL: int = 20  # seconds
    LOG_LEVEL: str = "INFO"
    MCP_SERVER_STATUS: str = "OK"
    RATE_LIMIT_INTERVAL: float = 1.0  # seconds between requests

settings = Settings()
