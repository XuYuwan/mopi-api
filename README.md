# MOPI Music API

YouTube Music backend for MOPI Android app.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python main.py

# Server runs on http://localhost:8000
```

## Endpoints

- `GET /` - Health check
- `GET /search?q=song+name&limit=20` - Search tracks
- `GET /track/{videoId}` - Get track details
- `GET /album/{browseId}` - Get album with tracks

## Deploy to Railway

1. Create account at https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Connect this repo
4. Railway auto-detects Python and deploys!

Your API will be live at: `https://your-app.railway.app`

## Environment Variables

None required for basic usage.

## Notes

- Free tier: 500 hours/month on Railway
- For production: add rate limiting, caching
- Direct audio streaming requires yt-dlp integration
