# Instagram Scraper

A modern, web-based Instagram media downloader that allows you to download posts, reels, and carousel media from Instagram without requiring login. Built with FastAPI and featuring a clean, responsive web interface.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.120.1-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

- 🎯 **No Login Required** - Download public Instagram content without authentication
- 🖼️ **Multiple Media Support** - Download images, videos, and carousel posts
- 🎬 **Video Thumbnails** - Automatic thumbnail preview for videos
- ⚡ **Smart Caching** - Reuses previously downloaded files for faster access
- 🧹 **Auto Cleanup** - Automatically manages disk space by cleaning old downloads
- 🎨 **Modern UI** - Clean, responsive web interface with paste-from-clipboard support
- 📱 **Carousel Support** - Download all media from multi-image/video posts
- 🔄 **RESTful API** - Full API access for programmatic use

## Installation

### Prerequisites

- Python 3.10 or higher
- pip or poetry

### Setup

1. Clone the repository:
```bash
git clone https://github.com/cheekydavy/instagram-scraper.git
cd instagram-scraper
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Web Interface

1. Start the server:
```bash
uvicorn src.instagram_scraper.main:app --reload
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

3. Paste an Instagram post or reel URL and click "Download Media"

### API Endpoints

#### Download Media
```http
GET /api/v1/download?shortcode={shortcode}
GET /api/v1/download?url={instagram_url}
```

**Example:**
```bash
curl "http://localhost:8000/api/v1/download?url=https://www.instagram.com/p/ABC123/"
```

**Response:**
```json
{
  "shortcode": "ABC123",
  "files": [
    {
      "name": "ABC123_001.jpg",
      "path": "/downloads/20251113_120000/ABC123_001.jpg",
      "type": "jpg"
    }
  ],
  "preview_thumbnail": "https://...",
  "cached": false
}
```

#### Get Profile
```http
GET /api/v1/profile/{username}
```

#### Get Posts
```http
GET /api/v1/posts/{username}?max_posts=50
```

#### Get Media Info
```http
GET /api/v1/media/{shortcode}
```

#### Preview Media
```http
GET /api/v1/preview/{shortcode}
```

## Project Structure

```
instagram-scraper/
├── src/
│   └── instagram_scraper/
│       ├── api/
│       │   └── routes.py          # API endpoints
│       ├── config/
│       │   └── settings.py        # Configuration
│       ├── models/                # Pydantic models
│       ├── scrapers/              # Scraping logic
│       ├── utils/                 # Utility functions
│       └── main.py                # FastAPI app entry point
├── web/
│   ├── index.html                 # Web UI
│   ├── script.js                  # Frontend logic
│   └── style.css                  # Styling
├── data/
│   └── outputs/
│       └── downloads/             # Downloaded media
├── tests/                         # Test files
├── requirements.txt               # Python dependencies
└── README.md
```

## Technologies Used

- **FastAPI** - Modern, fast web framework for building APIs
- **httpx** - Async HTTP client
- **yt-dlp** - Media downloader
- **Pydantic** - Data validation
- **Vanilla JavaScript** - Frontend (no frameworks)

## Features in Detail

### Smart Caching
The scraper automatically checks if a post has been downloaded before. If found, it returns the cached files instantly without re-downloading.


### Video Support
- Automatic video detection
- Thumbnail preview using Instagram's thumbnail URLs
- Native HTML5 video player with controls

### User Experience
- One-click paste from clipboard
- "Download Another" button for quick successive downloads

## API Documentation

Once the server is running, visit:
```
http://localhost:8000/docs
```

This provides interactive API documentation powered by Swagger UI.

## Development

### Running Tests
```bash
pytest
```

### Code Structure
- **Scrapers** - Handle Instagram data extraction
- **Models** - Define data structures using Pydantic
- **API Routes** - FastAPI endpoints
- **Utils** - Helper functions for headers, parsing, etc.

## Limitations

- Rate limiting may apply (Instagram's anti-scraping measures)
- Instagram's API structure may change, requiring updates

## Ethical Use

This tool is intended for:
- ✅ Downloading your own content
- ✅ Downloading public content for personal use
- ✅ Educational purposes

Please respect:
- ❌ Copyright laws
- ❌ Instagram's Terms of Service
- ❌ Content creators' rights
- ❌ Rate limits and server resources

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Author

**Cheeky Davy**

- GitHub: [@cheekydavy](https://github.com/cheekydavy)
- Telegram: [@mbuvi](https://t.me/mbuvi)
- Instagram: [@_mbuvi](https://instagram.com/_mbuvi)

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Media downloading powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- Inspired by the need for a simple, no-login Instagram downloader

## Disclaimer

This tool is for educational purposes only. Use responsibly and in accordance with Instagram's Terms of Service and applicable laws. The authors are not responsible for any misuse of this software.

