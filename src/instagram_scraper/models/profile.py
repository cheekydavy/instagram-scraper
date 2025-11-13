"""Profile data model."""

from typing import List, Any, Optional
from pydantic import BaseModel

class ProfileModel(BaseModel):
    username: str
    full_name: str
    biography: str
    followers: int
    following: int
    posts_count: int
    is_private: bool
    profile_pic_url: str
    external_url: Optional[str] = None
    sample_posts: List[dict[str, Any]] = []