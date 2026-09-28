from pathlib import Path
import subprocess

root = Path("release")
app_bundle = root / "AudioExtract.app"
app = app_bundle / "Contents"
macos = app / "MacOS"
macos.mkdir(parents=True, exist_ok=True)

source = Path("dist") / "AudioExtract"
target = macos / "AudioExtract"
source.replace(target)
target.chmod(0o755)

(app / "Info.plist").write_text(
    """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleExecutable</key>
  <string>AudioExtract</string>
  <key>CFBundleIdentifier</key>
  <string>com.aiit.audioextract</string>
  <key>CFBundleName</key>
  <string>AudioExtract</string>
  <key>CFBundleDisplayName</key>
  <string>AudioExtract</string>
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

# Ad-hoc signature — bez tego macOS (zwłaszcza Apple Silicon) często
# pokazuje tylko "The application can't be opened".
subprocess.run(
    ["codesign", "--force", "--deep", "--sign", "-", str(app_bundle)],
    check=True,
)

# Zip tworzony na macOS zachowuje bit +x (Compress-Archive na Windows go gubi).
zip_path = root / "AudioExtract-macos.zip"
if zip_path.exists():
    zip_path.unlink()
subprocess.run(
    [
        "ditto",
        "-c",
        "-k",
        "--sequesterRsrc",
        "--keepParent",
        str(app_bundle),
        str(zip_path),
    ],
    check=True,
)
