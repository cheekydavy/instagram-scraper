"""Setup script."""

import os

dirs = [
    "src/instagram_scraper/config",
    "src/instagram_scraper/scrapers",
    "src/instagram_scraper/models",
    "src/instagram_scraper/utils",
    "src/instagram_scraper/api",
    "tests",
    "data/samples",
    "data/outputs",
    "scripts"
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

print("Project structure created!")