"""Proxy rotation."""

import random
from typing import Optional, Dict, Any

def get_proxy(proxies_list: list) -> Optional[Dict[str, str]]:
    if not proxies_list:
        return None
    proxy_url = random.choice(proxies_list)
    return {"http://": proxy_url, "https://": proxy_url}