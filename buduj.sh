#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

PYTHON="${PYTHON:-python3}"
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "Nie znaleziono Python 3. Zainstaluj Python 3.11 lub nowszy."
  exit 1
fi

if [ ! -x ".venv/bin/python" ]; then
  echo "Tworzenie srodowiska budowania..."
  "$PYTHON" -m venv .venv
fi

echo "Instalowanie bibliotek aplikacji i PyInstaller..."
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r requirements.txt pyinstaller

rm -rf build dist Audioyt.spec

echo "Budowanie Audioyt..."
./.venv/bin/pyinstaller --noconfirm --clean --onefile --name Audioyt \
  --add-data "templates:templates" \
  --add-data "static:static" \
  --collect-all imageio_ffmpeg app.py

echo
echo "Gotowe. Plik znajduje sie w: $(pwd)/dist/Audioyt"