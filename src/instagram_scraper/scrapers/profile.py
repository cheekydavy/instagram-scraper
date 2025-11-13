"""Profile scraper."""

from typing import Dict, Any
from ..models.profile import ProfileModel
from .base import BaseScraper

class ProfileScraper(BaseScraper):
    async def scrape(self, username: str) -> ProfileModel:
        url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
        resp = await self._make_request("GET", url)
        data = resp.json()["data"]["user"]
        
        posts_summary = data.get("edge_owner_to_timeline_media", {}).get("count", 0)
        
        return ProfileModel(
            username=data["username"],
            full_name=data.get("full_name", ""),
            biography=data.get("biography", ""),
            followers=data["edge_followed_by"]["count"],
            following=data["edge_follow"]["count"],
            posts_count=posts_summary,
            is_private=data.get("is_private", False),
            profile_pic_url=data.get("profile_pic_url", ""),
            external_url=data.get("external_url", ""),
            sample_posts=[
                {
                    "shortcode": edge["node"]["shortcode"],
                    "caption": edge["node"].get("edge_media_to_caption", {}).get("edges", [{}])[0].get("node", {}).get("text", ""),
                    "likes": edge["node"]["edge_media_preview_like"]["count"],
                    "timestamp": edge["node"]["taken_at_timestamp"]
                }
                for edge in data.get("edge_owner_to_timeline_media", {}).get("edges", [])
            ]
        )