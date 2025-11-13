"""CLI for standalone scraping."""

import asyncio
import argparse
import json
from src.instagram_scraper.scrapers.profile import ProfileScraper  # IG
from src.tiktok_scraper.scrapers.profile import TiktokProfileScraper  # TT

async def main():
    parser = argparse.ArgumentParser(description="Run Social Media scraper CLI")
    parser.add_argument("type", choices=["profile", "videos", "media"], help="Scraper type")
    parser.add_argument("--platform", choices=["ig", "tt"], default="ig", help="Platform")
    parser.add_argument("--username", help="For profile/videos (IG username or TT uniqueId)")
    parser.add_argument("--shortcode", "--video-id", help="For media")
    parser.add_argument("--max-items", type=int, default=50, help="For videos")
    parser.add_argument("--output", choices=["json", "csv"], default="json")
    args = parser.parse_args()

    if args.platform == "ig":
        pass
    elif args.platform == "tt":
        if args.type == "profile":
            if not args.username:
                args.username = input("Enter TT uniqueId: ")
            async with TiktokProfileScraper() as scraper:
                data = await scraper.scrape(args.username)
                output = data.dict()

    if args.output == "json":
        print(json.dumps(output, indent=2))
    else:
        import csv
        import io
        pass

if __name__ == "__main__":
    asyncio.run(main())