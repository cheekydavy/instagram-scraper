"""Media scraper/downloader."""

import asyncio
import random
from urllib.parse import quote
import json
from typing import Dict, Any, List
from ..models.media import MediaModel
from .base import BaseScraper, ua
from ..utils.headers import get_headers

DOC_ID_POST = "8845758582119845"

class MediaScraper(BaseScraper):
    async def scrape(self, shortcode: str) -> MediaModel:
        temp_username = "nasa"
        profile_resp = await self._make_request("GET", f"https://www.instagram.com/{temp_username}/")
        csrf_token = profile_resp.cookies.get("csrftoken", "dummy_csrf")  # Extract from set-cookie
        
        self.client.headers.update(get_headers(ua, csrf_token))
        
        url = "https://www.instagram.com/graphql/query"
        variables = {"shortcode": shortcode}
        body = f"variables={quote(json.dumps(variables))}&doc_id={DOC_ID_POST}"
        
        resp = await self._make_request(
            "POST",
            url,
            data=body,
            headers={"content-type": "application/x-www-form-urlencoded"}
        )
        
        print(f"DEBUG: IG Media JSON = {resp.json()}")
        
        try:
            response_data = resp.json()
            if "errors" in response_data:
                raise ValueError(f"IG GraphQL Error: {response_data['errors']}")
            data = response_data["data"]["xdt_shortcode_media"]
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Parse Error: {e}. Full Response: {resp.text[:200]}")
        
        media_urls = []
        
        if data.get("video_url"):
            media_urls.append(data["video_url"])
        elif data.get("video_versions"):
            for version in data["video_versions"]:
                media_urls.append(version["url"])
        elif data.get("edge_sidecar_to_children"):
            for child in data["edge_sidecar_to_children"]["edges"]:
                child_node = child["node"]
                if child_node.get("video_url"):
                    media_urls.append(child_node["video_url"])
                elif child_node.get("video_versions"):
                    media_urls.append(child_node["video_versions"][0]["url"])
                else:
                    media_urls.append(child_node["display_url"])
        elif data.get("display_url"): 
            media_urls.append(data["display_url"])
        else:
            raise ValueError("No media URLs found in response")
        
        return MediaModel(
            shortcode=shortcode,
            media_urls=media_urls,
            thumbnail_url=data.get("thumbnail_src", ""),
            is_video=bool(data.get("video_versions") or data.get("video_url"))
        )