# YouTube Downloader Backend

Flask HTTP service that accepts download requests from the Chrome extension, fetches the requested YouTube media with `yt-dlp`, saves the result to the user's `Downloads` directory, and reports success or failure back to the extension.

## Requirements

- Python 3.9+
- `ffmpeg` available on `PATH` (needed by `yt-dlp` for muxing/conversion)
- Python dependencies from `requirements.txt`

Install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate   # or source .venv/bin/activate
pip install -r requirements.txt
```

## Running the Server

```bash
python server.py
```

The server listens on `http://localhost:5000` by default.

## API

`POST /download`

```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "format": "MP3"  // or "MP4"
}
```

- Saves the final file to `<user home>/Downloads/<video-title>.mp4|.mp3`.
- Responds with JSON: `{"success": true, "file": "C:\\Users\\...\\Downloads\\video.mp3", "filename": "video.mp3"}`.
- On error, returns `{"success": false, "error": "<message>"}` with an appropriate HTTP status.

`GET /health` can be used by the extension to verify the backend is running.
# yt_extension_
