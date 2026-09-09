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
./.venv/bin/pyinstaller --noconfirm --clean --onefile --console --name Audioyt \
  --add-data "templates:templates" \
  --add-data "static:static" \
  --collect-all imageio_ffmpeg app.py

chmod +x dist/Audioyt

if [ "$(uname -s)" = "Darwin" ]; then
  mkdir -p dist/Audioyt.app/Contents/MacOS
  mv dist/Audioyt dist/Audioyt.app/Contents/MacOS/Audioyt
  cat > dist/Audioyt.app/Contents/Info.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleExecutable</key>
  <string>Audioyt</string>
  <key>CFBundleIdentifier</key>
  <string>com.aiit.audioyt</string>
  <key>CFBundleName</key>
  <string>Audioyt</string>
  <key>CFBundlePackageType</key>
  <string>APPL</string>
  <key>CFBundleVersion</key>
  <string>1.0</string>
</dict>
</plist>
EOF
  echo
  echo "Gotowe. Aplikacja: $(pwd)/dist/Audioyt.app"
else
  mv dist/Audioyt dist/Audioyt.bin
  cat > dist/Audioyt.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
chmod +x ./Audioyt.bin
./Audioyt.bin
EOF
  chmod +x dist/Audioyt.sh
  echo
  echo "Gotowe. Uruchom: $(pwd)/dist/Audioyt.sh"
fi