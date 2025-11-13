"""Posts scraper with pagination."""

import json
from urllib.parse import quote
from typing import Dict, Any, List
from ..models.post import PostModel
from ..config.settings import settings 
from .base import BaseScraper

DOC_ID_FEED = "9310670392322965" 

class PostsScraper(BaseScraper):
    def __init__(self, user_id: str):
        super().__init__()
        self.user_id = user_id

    async def scrape(self, max_posts: int = 50) -> List[PostModel]:
        posts = []
        cursor = None
        url = "https://www.instagram.com/graphql/query"
        variables = {
            "id": self.user_id,
            "first": settings.max_posts_per_request,
            "after": cursor
        }

        while len(posts) < max_posts:
            variables["after"] = cursor
            body = f"variables={quote(json.dumps(variables))}&doc_id={DOC_ID_FEED}"
            
            resp = await self._make_request(
                "POST",
                url,
                data=body,
                headers={"content-type": "application/x-www-form-urlencoded"}
            )
            
            data = resp.json()["data"]["user"]["edge_owner_to_timeline_media"]
            edges = data["edges"]
            
            for edge in edges:
                if len(posts) >= max_posts:
                    break
                node = edge["node"]
                posts.append(PostModel(
                    shortcode=node["shortcode"],
                    caption=node.get("edge_media_to_caption", {}).get("edges", [{}])[0].get("node", {}).get("text", ""),
                    likes=node["edge_media_preview_like"]["count"],
                    comments=node["edge_media_to_comment"]["count"],
                    timestamp=node["taken_at_timestamp"],
                    is_video=node.get("is_video", False),
                    media_type=node.get("__typename", "GraphImage"),
                    accessibility_caption=node.get("accessibility_caption", "")
                ))
            
            page_info = data["page_info"]
            if not page_info["has_next_page"]:
                break
            cursor = page_info["end_cursor"]

            await asyncio.sleep(random.uniform(settings.request_delay_min, settings.request_delay_max))

        return posts