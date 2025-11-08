#!/usr/bin/env python3
"""
Flask-based backend service for downloading YouTube videos or audio via yt-dlp.
"""

from __future__ import annotations

import logging
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

app = Flask(__name__)
CORS(app)

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
)


def get_download_directory() -> Path:
    """Return temp directory for downloads."""
    temp_dir = Path(tempfile.gettempdir()) / "yt_downloads"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir


def build_yt_dlp_options(download_dir: Path, target_format: str) -> Dict[str, Any]:
    """Create yt-dlp configuration based on the requested output format."""
    base_options: Dict[str, Any] = {
        "outtmpl": str(download_dir / "%(title)s.%(ext)s"),
        "restrictfilenames": True,
        "noplaylist": True,
        "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
    }

    if target_format == "MP4":
        return {
            **base_options,
            "format": "18/best[ext=mp4]/best",
        }

    if target_format == "MP3":
        return {
            **base_options,
            "format": "bestaudio[ext=m4a]/bestaudio",
        }

    raise ValueError("Unsupported format. Use either 'MP4' or 'MP3'.")


def download_media(url: str, target_format: str) -> Path:
    """Download the specified URL and return the resulting file path."""
    target_format = target_format.strip().upper()
    download_dir = get_download_directory()
    ydl_opts = build_yt_dlp_options(download_dir, target_format)

    logging.info("Starting download for %s as %s", url, target_format)

    with YoutubeDL(ydl_opts) as ydl:
        info: Dict[str, Any] = ydl.extract_info(url, download=True)

    if info.get("entries"):
        info = info["entries"][0]

    prepared = Path(ydl.prepare_filename(info))
    
    if target_format == "MP3":
        m4a_path = prepared.with_suffix(".m4a")
        if m4a_path.exists():
            final_path = m4a_path
        else:
            final_path = prepared
    else:
        final_path = prepared.with_suffix(".mp4")

    if not final_path.exists():
        raise FileNotFoundError(
            f"Download completed but {final_path.name} was not found in {final_path.parent}"
        )

    logging.info("Download finished: %s", final_path)
    return final_path


@app.route("/download", methods=["POST"])
def handle_download():
    """Handle download requests from the Chrome extension."""
    payload = request.get_json(silent=True) or {}
    url = (payload.get("url") or "").strip()
    requested_format = (payload.get("format") or "MP4").strip().upper()

    if not url:
        return jsonify({"success": False, "error": "Missing 'url' in request body."}), 400

    if requested_format not in {"MP4", "MP3"}:
        return (
            jsonify(
                {"success": False, "error": "Invalid format. Valid options are 'MP4' or 'MP3'."}
            ),
            400,
        )

    try:
        downloaded_path = download_media(url, requested_format)
        response = send_file(
            downloaded_path,
            as_attachment=True,
            download_name=downloaded_path.name
        )
        
        @response.call_on_close
        def cleanup():
            try:
                if downloaded_path.exists():
                    downloaded_path.unlink()
            except Exception:
                pass
        
        return response
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except DownloadError as exc:
        logging.exception("yt-dlp failed to download %s", url)
        return jsonify({"success": False, "error": f"Download failed: {exc}"}), 502
    except FileNotFoundError as exc:
        logging.exception("Post-processing failed for %s", url)
        return jsonify({"success": False, "error": str(exc)}), 500
    except Exception as exc:  # pylint: disable=broad-except
        logging.exception("Unexpected error while downloading %s", url)
        return jsonify({"success": False, "error": f"Unexpected error: {exc}"}), 500


@app.route("/")
def index():
    """Root endpoint."""
    return jsonify({"message": "YouTube Downloader API", "endpoints": ["/download", "/health"]})


@app.route("/health")
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
