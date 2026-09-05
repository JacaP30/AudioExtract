from pathlib import Path
import re
import shutil
import tempfile
import threading
import webbrowser

from flask import Flask, after_this_request, jsonify, render_template, request, send_file
import imageio_ffmpeg
import yt_dlp


app = Flask(__name__)
DOWNLOAD_DIR = Path(tempfile.gettempdir()) / "audioyt-downloads"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


def get_ffmpeg_path() -> str | None:
    try:
        return imageio_ffmpeg.get_ffmpeg_exe()
    except RuntimeError:
        return shutil.which("ffmpeg")


def is_youtube_url(value: str) -> bool:
    return bool(
        re.match(
            r"^https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[^\s&]+",
            value,
            re.IGNORECASE,
        )
    )


@app.get("/")
def index():
    return render_template("index.html", ffmpeg_available=get_ffmpeg_path() is not None)


@app.post("/api/download")
def download_audio():
    url = request.form.get("url", "").strip()

    if not is_youtube_url(url):
        return jsonify(error="Wklej poprawny adres filmu z YouTube."), 400

    ffmpeg_path = get_ffmpeg_path()
    if ffmpeg_path is None:
        return jsonify(error="Brakuje składnika FFmpeg. Uruchom ponownie gotową aplikację lub skontaktuj się z autorem."), 500

    output_template = str(DOWNLOAD_DIR / "%(title)s.%(ext)s")
    options = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "restrictfilenames": True,
        "ffmpeg_location": ffmpeg_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    try:
        with yt_dlp.YoutubeDL(options) as downloader:
            info = downloader.extract_info(url, download=True)
            filename = Path(downloader.prepare_filename(info)).with_suffix(".mp3")
    except Exception as error:
        app.logger.exception("Audio download failed")
        return jsonify(error=f"Nie udało się pobrać audio: {error}"), 500

    if not filename.exists():
        return jsonify(error="Pobrano materiał, ale nie znaleziono gotowego pliku audio."), 500

    @after_this_request
    def remove_file(response):
        try:
            filename.unlink(missing_ok=True)
        except OSError:
            app.logger.warning("Could not remove temporary file %s", filename)
        return response

    return send_file(filename, as_attachment=True, download_name=f"{filename.stem}.mp3", mimetype="audio/mpeg")


if __name__ == "__main__":
    threading.Timer(1.2, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=False, port=5000)