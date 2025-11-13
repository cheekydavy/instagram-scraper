"""Proxy rotation."""

import random
from typing import Optional, Dict, Any

def get_proxy(proxies_list: list) -> Optional[str]:
    """
    Get a random proxy from the list.
    Returns proxy URL string for httpx, or None if no proxies available.
    httpx accepts: "http://proxy:port" or "socks5://proxy:port"
    """
    if not proxies_list:
        return None
    proxy_url = random.choice(proxies_list)
    proxy_url = proxy_url.strip()
    if not proxy_url.startswith(("http://", "https://", "socks5://", "socks4://")):
        proxy_url = f"http://{proxy_url}"
    return proxy_url