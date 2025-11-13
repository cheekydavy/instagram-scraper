"""Post data model."""

from pydantic import BaseModel
from typing import Optional

class PostModel(BaseModel):
    shortcode: str
    caption: Optional[str] = None
    likes: int
    comments: int
    timestamp: int
    is_video: bool = False
    media_type: str = "GraphImage"
    accessibility_caption: Optional[str] = None