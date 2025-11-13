"""Scraper unit tests."""

import pytest
from httpx import Response
from unittest.mock import AsyncMock, patch
import json
from src.instagram_scraper.scrapers.profile import ProfileScraper
from src.instagram_scraper.scrapers.posts import PostsScraper
from src.instagram_scraper.scrapers.media import MediaScraper
from src.instagram_scraper.models.profile import ProfileModel

@pytest.fixture
def mock_response():
    with open("data/samples/sample_profile.json", "r") as f:
        data = json.load(f)
    return data

@pytest.mark.asyncio
async def test_profile_scrape(mock_response):
    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = Response(200, json=mock_response)
        async with ProfileScraper() as scraper:
            profile = await scraper.scrape("nasa")
            assert isinstance(profile, ProfileModel)
            assert profile.username == "nasa"
            assert profile.followers > 0

@pytest.mark.asyncio
async def test_posts_scrape():
    pass 

@pytest.mark.asyncio
async def test_media_scrape():
    pass