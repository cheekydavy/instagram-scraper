"""Header generation."""

from typing import Dict, Any
from fake_useragent import UserAgent

ua = UserAgent()

def get_headers(user_agent: UserAgent, csrf_token: str = None) -> Dict[str, str]:
    headers = {
        "User-Agent": user_agent.random,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": "0",  
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest"
    }
    if csrf_token:
        headers["x-csrftoken"] = csrf_token
    return headers