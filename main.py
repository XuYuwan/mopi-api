"""
MOPI API - YouTube Music Backend
FastAPI server providing music search and streaming URLs
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from ytmusicapi import YTMusic
from typing import Optional, List, Dict, Any
import yt_dlp
import uvicorn

app = FastAPI(
    title="MOPI Music API",
    description="YouTube Music API for MOPI Android App",
    version="1.0.0"
)

# Enable CORS for Android app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize YTMusic client
ytmusic = YTMusic()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "MOPI Music API",
        "version": "1.0.0"
    }


@app.get("/search")
async def search_tracks(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=50, description="Number of results")
) -> Dict[str, Any]:
    """
    Search for tracks on YouTube Music
    
    Returns:
        List of tracks with metadata and stream info
    """
    try:
        results = ytmusic.search(q, filter="songs", limit=limit)
        
        tracks = []
        for item in results:
            track = {
                "id": item.get("videoId", ""),
                "title": item.get("title", ""),
                "artistName": ", ".join([a["name"] for a in item.get("artists", [])]),
                "artistId": item.get("artists", [{}])[0].get("id", "") if item.get("artists") else "",
                "albumName": item.get("album", {}).get("name") if item.get("album") else None,
                "albumId": item.get("album", {}).get("id") if item.get("album") else None,
                "durationMs": (item.get("duration_seconds", 0) * 1000) if item.get("duration_seconds") else 0,
                "thumbnailUrl": item.get("thumbnails", [{}])[-1].get("url") if item.get("thumbnails") else None,
                "streamUrl": f"https://music.youtube.com/watch?v={item.get('videoId', '')}"
            }
            tracks.append(track)
        
        return {
            "success": True,
            "query": q,
            "count": len(tracks),
            "tracks": tracks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.get("/track/{video_id}")
async def get_track(video_id: str) -> Dict[str, Any]:
    """
    Get track with REAL decrypted audio stream URL using yt-dlp!
    
    Note: Stream URLs expire after ~6 hours. Call right before playback.
    """
    try:
        # Use yt-dlp to extract stream URL (handles signatureCipher decryption)
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False
        }
        
        video_url = f"https://music.youtube.com/watch?v={video_id}"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # Get best audio format
            formats = info.get('formats', [])
            audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
            
            if not audio_formats:
                # Fallback to any format with audio
                audio_formats = [f for f in formats if f.get('acodec') != 'none']
            
            if not audio_formats:
                raise HTTPException(status_code=404, detail="No audio stream found")
            
            # Pick highest bitrate
            best_audio = max(audio_formats, key=lambda x: x.get('abr', 0) or x.get('tbr', 0))
            stream_url = best_audio.get('url')
            
            if not stream_url:
                raise HTTPException(status_code=404, detail="Stream URL not found")
            
            # Get thumbnail
            thumbnails = info.get('thumbnails', [])
            thumb_url = thumbnails[-1].get('url') if thumbnails else None
            
            track = {
                "id": video_id,
                "title": info.get('title', ''),
                "artistName": info.get('artist') or info.get('uploader', ''),
                "durationMs": int(info.get('duration', 0)) * 1000,
                "thumbnailUrl": thumb_url,
                "streamUrl": stream_url  # REAL DECRYPTED STREAM! 🎵
            }
            
            return {
                "success": True,
                "track": track
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get track: {str(e)}")


@app.get("/album/{browse_id}")
async def get_album(browse_id: str) -> Dict[str, Any]:
    """Get album with all tracks"""
    try:
        album = ytmusic.get_album(browse_id)
        
        if not album:
            raise HTTPException(status_code=404, detail="Album not found")
        
        tracks = []
        for track in album.get("tracks", []):
            tracks.append({
                "id": track.get("videoId", ""),
                "title": track.get("title", ""),
                "artistName": ", ".join([a["name"] for a in track.get("artists", [])]),
                "durationMs": (track.get("duration_seconds", 0) * 1000) if track.get("duration_seconds") else 0,
                "streamUrl": f"https://music.youtube.com/watch?v={track.get('videoId', '')}"
            })
        
        return {
            "success": True,
            "album": {
                "id": browse_id,
                "title": album.get("title", ""),
                "artist": album.get("artists", [{}])[0].get("name", ""),
                "year": album.get("year"),
                "trackCount": album.get("trackCount", len(tracks)),
                "thumbnailUrl": album.get("thumbnails", [{}])[-1].get("url") if album.get("thumbnails") else None,
            },
            "tracks": tracks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get album: {str(e)}")


if __name__ == "__main__":
    # Run locally for testing
    uvicorn.run(app, host="0.0.0.0", port=8000)
