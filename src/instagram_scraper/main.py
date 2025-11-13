"""FastAPI entry point for Social Media Scraper."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router


app = FastAPI(
    title="Mbuvi Tech IG Downloader API",
    description="Scrape and download public IG data without login.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

app.mount("/downloads", StaticFiles(directory="data/outputs/downloads"), name="downloads")

app.mount("/", StaticFiles(directory="web", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)