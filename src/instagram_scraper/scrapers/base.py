"""Abstract base scraper with common logic."""

import asyncio
import random
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import httpx
from fake_useragent import UserAgent
from ..config.settings import settings
from ..utils.proxies import get_proxy
from ..utils.headers import get_headers

ua = UserAgent()

class BaseScraper(ABC):
    def __init__(self):
        self.client: Optional[httpx.AsyncClient] = None
        self.session_headers: Dict[str, str] = {}

    async def __aenter__(self):
        proxy = get_proxy(settings.proxies_list)
        
        if proxy:
            proxy_url = proxy.get("http://") or proxy.get("https://") or str(proxy)
            print(f"DEBUG: Using proxy: {proxy_url}")
        else:
            print(f"DEBUG: No proxy configured (proxies_list has {len(settings.proxies_list)} items)")
        
        self.client = httpx.AsyncClient(
            timeout=10.0,
            headers=get_headers(ua),
            proxies=proxy  
        )
        self.session_headers = self.client.headers.copy()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()

    async def _make_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[str] = None,
        **kwargs
    ) -> httpx.Response:
        for attempt in range(settings.max_retries):
            try:
                resp = await self.client.request(
                    method, url, params=params, json=json, data=data, **kwargs
                )
                if resp.status_code == 429 or resp.status_code == 403:
                    print(f"DEBUG: IG Block - Status {resp.status_code}, Preview: {resp.text[:100]}...")
                    await asyncio.sleep(2 ** attempt + random.uniform(0, 1))  
                    if attempt > 0:
                        self.client.headers.update(get_headers(ua))
                        # Rotate proxy on retry
                        proxy = get_proxy(settings.proxies_list)
                        if proxy:
                            
                            await self.client.aclose()
                            proxy_url = proxy.get("http://") or proxy.get("https://") or str(proxy)
                            print(f"DEBUG: Rotating to new proxy: {proxy_url}")
                            self.client = httpx.AsyncClient(
                                timeout=10.0,
                                headers=get_headers(ua),
                                proxies=proxy
                            )
                    continue
                resp.raise_for_status()
                return resp
            except httpx.RequestError as e:
                print(f"DEBUG: IG Request Error on attempt {attempt + 1}: {e}")
                if attempt == settings.max_retries - 1:
                    raise
                await asyncio.sleep(random.uniform(settings.request_delay_min, settings.request_delay_max))
        raise Exception("Max retries exceeded")

    @abstractmethod
    async def scrape(self, **kwargs) -> Dict[str, Any]:
        pass