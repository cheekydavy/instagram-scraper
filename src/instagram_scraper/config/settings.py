"""Configuration settings using Pydantic."""

from pydantic_settings import BaseSettings
from typing import List
from dotenv import load_dotenv
from pydantic import field_validator

load_dotenv()

class ScraperSettings(BaseSettings):
    proxies_list: List[str] = []

    @field_validator("proxies_list", mode="before")
    @classmethod
    def parse_proxies_list(cls, v):
        """Parse proxies_list: Accept empty, comma-separated, or JSON list."""
        if v is None or v == "":
            return []
        if isinstance(v, str):
            try:
                import json
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return [str(item) for item in parsed]
            except json.JSONDecodeError:
                pass
            return [proxy.strip() for proxy in v.split(",") if proxy.strip()]
        return v  

    request_delay_min: int = 2
    request_delay_max: int = 5
    max_retries: int = 3
    max_posts_per_request: int = 12
    ig_app_id: str = "936619743392459"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = ScraperSettings()