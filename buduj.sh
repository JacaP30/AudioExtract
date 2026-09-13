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

rm -rf build dist AudioExtract.spec

echo "Budowanie AudioExtract..."
./.venv/bin/pyinstaller --noconfirm --clean --onefile --console --name AudioExtract \
  --add-data "templates:templates" \
  --add-data "static:static" \
  --add-data "licenses:licenses" \
  --add-data "LICENSE:." \
  --collect-all imageio_ffmpeg app.py

chmod +x dist/AudioExtract

if [ "$(uname -s)" = "Darwin" ]; then
  mkdir -p dist/AudioExtract.app/Contents/MacOS
  mv dist/AudioExtract dist/AudioExtract.app/Contents/MacOS/AudioExtract
  cat > dist/AudioExtract.app/Contents/Info.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleExecutable</key>
  <string>AudioExtract</string>
  <key>CFBundleIdentifier</key>
  <string>com.aiit.audioextract</string>
  <key>CFBundleName</key>
  <string>AudioExtract</string>
  <key>CFBundlePackageType</key>
  <string>APPL</string>
  <key>CFBundleVersion</key>
  <string>1.0</string>
</dict>
</plist>
EOF
  echo
  echo "Gotowe. Aplikacja: $(pwd)/dist/AudioExtract.app"
else
  mv dist/AudioExtract dist/AudioExtract.bin
  cat > dist/AudioExtract.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
chmod +x ./AudioExtract.bin
./AudioExtract.bin
EOF
  chmod +x dist/AudioExtract.sh
  echo
  echo "Gotowe. Uruchom: $(pwd)/dist/AudioExtract.sh"
fi
