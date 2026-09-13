from pathlib import Path
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import uuid
import webbrowser
from urllib.parse import urlparse

from flask import Flask, after_this_request, jsonify, render_template, request, send_file
import imageio_ffmpeg
import yt_dlp


def resource_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


app = Flask(
    __name__,
    template_folder=str(resource_root() / "templates"),
    static_folder=str(resource_root() / "static"),
)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024 * 1024
app.jinja_env.auto_reload = True
app.jinja_env.cache = None
DOWNLOAD_DIR = Path(tempfile.gettempdir()) / "audioextract-downloads"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_SUFFIXES = {
    ".mp4",
    ".mkv",
    ".webm",
    ".mov",
    ".avi",
    ".m4v",
    ".mpeg",
    ".mpg",
    ".wmv",
    ".3gp",
    ".m4a",
    ".wav",
    ".ogg",
    ".mp3",
    ".flac",
    ".aac",
    ".wma",
}


def get_ffmpeg_path() -> str | None:
    try:
        return imageio_ffmpeg.get_ffmpeg_exe()
    except RuntimeError:
        return shutil.which("ffmpeg")


def is_http_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def port_is_busy(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex(("127.0.0.1", port)) == 0


def safe_stem(filename: str) -> str:
    stem = Path(filename).stem.strip() or "audio"
    cleaned = re.sub(r"[^\w\-]+", "_", stem)[:80].strip("._")
    return cleaned or "audio"


def uploaded_file():
    upload = request.files.get("file")
    if upload is None or not (upload.filename or "").strip():
        return None
    return upload


def convert_local_file(upload, ffmpeg_path: str) -> Path:
    suffix = Path(upload.filename or "").suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise ValueError("Nieobsługiwany format pliku.")

    token = uuid.uuid4().hex[:12]
    source = DOWNLOAD_DIR / f"src-{token}{suffix}"
    output = DOWNLOAD_DIR / f"{safe_stem(upload.filename)}.mp3"
    upload.save(source)

    command = [
        ffmpeg_path,
        "-y",
        "-i",
        str(source),
        "-vn",
        "-acodec",
        "libmp3lame",
        "-b:a",
        "192k",
        str(output),
    ]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=3600,
            check=False,
        )
        if result.returncode != 0 or not output.exists():
            detail = (result.stderr or result.stdout or "FFmpeg nie przekonwertował pliku.").strip()
            raise RuntimeError(detail[-800:])
        return output
    finally:
        source.unlink(missing_ok=True)


def send_mp3(path: Path):
    @after_this_request
    def remove_file(response):
        try:
            path.unlink(missing_ok=True)
        except OSError:
            app.logger.warning("Could not remove temporary file %s", path)
        return response

    return send_file(path, as_attachment=True, download_name=f"{path.stem}.mp3", mimetype="audio/mpeg")


@app.after_request
def disable_cache(response):
    response.headers["Cache-Control"] = "no-store, max-age=0"
    return response


@app.get("/")
def index():
    return render_template("index.html", ffmpeg_available=get_ffmpeg_path() is not None)


@app.get("/licencje")
def licenses_page():
    return render_template("licenses.html")


@app.post("/api/download")
def download_audio():
    url = request.form.get("url", "").strip()
    upload = uploaded_file()

    ffmpeg_path = get_ffmpeg_path()
    if ffmpeg_path is None:
        return jsonify(error="Brakuje składnika FFmpeg. Uruchom ponownie gotową aplikację lub skontaktuj się z autorem."), 500

    if upload is not None:
        try:
            filename = convert_local_file(upload, ffmpeg_path)
        except ValueError as error:
            return jsonify(error=str(error)), 400
        except Exception as error:
            app.logger.exception("Local audio conversion failed")
            return jsonify(error=f"Nie udało się wyciągnąć audio: {error}"), 500
        return send_mp3(filename)

    if not is_http_url(url):
        return jsonify(error="Wklej poprawny adres http lub https albo wybierz plik z komputera."), 400

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
        return jsonify(error=f"Nie udało się wyciągnąć audio: {error}"), 500

    if not filename.exists():
        return jsonify(error="Pobrano materiał, ale nie znaleziono gotowego pliku audio."), 500

    return send_mp3(filename)


if __name__ == "__main__":
    if port_is_busy(5000):
        raise SystemExit(
            "Port 5000 jest juz zajety przez inna instancje AudioExtract. "
            "Zamknij poprzednie okno z python app.py (Ctrl+C) i uruchom ponownie."
        )

    print(f"Szablony: {Path(app.root_path) / 'templates' / 'index.html'}")
    threading.Timer(1.2, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=False, port=5000)
