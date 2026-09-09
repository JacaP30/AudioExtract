from pathlib import Path

root = Path("release")
app = root / "Audioyt.app" / "Contents"
macos = app / "MacOS"
macos.mkdir(parents=True, exist_ok=True)

source = Path("dist") / "Audioyt"
target = macos / "Audioyt"
source.replace(target)
target.chmod(0o755)

(app / "Info.plist").write_text(
    """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleExecutable</key>
  <string>Audioyt</string>
  <key>CFBundleIdentifier</key>
  <string>com.aiit.audioyt</string>
  <key>CFBundleName</key>
  <string>Audioyt</string>
  <key>CFBundleDisplayName</key>
  <string>Audioyt</string>
  <key>CFBundlePackageType</key>
  <string>APPL</string>
  <key>CFBundleVersion</key>
  <string>1.0</string>
  <key>CFBundleShortVersionString</key>
  <string>1.0</string>
  <key>LSMinimumSystemVersion</key>
  <string>11.0</string>
  <key>NSHighResolutionCapable</key>
  <true/>
</dict>
</plist>
""",
    encoding="utf-8",
)
