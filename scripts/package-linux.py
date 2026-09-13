from pathlib import Path

root = Path("release")
root.mkdir(parents=True, exist_ok=True)

binary = root / "AudioExtract.bin"
Path("dist/AudioExtract").replace(binary)
binary.chmod(0o755)

launcher = root / "AudioExtract.sh"
launcher.write_text(
    "#!/usr/bin/env bash\n"
    "set -euo pipefail\n"
    'cd "$(dirname "$0")"\n'
    "chmod +x ./AudioExtract.bin\n"
    "./AudioExtract.bin\n",
    encoding="utf-8",
)
launcher.chmod(0o755)

(root / "CZYTAJ.txt").write_text(
    "Uruchom AudioExtract.sh (podwojne klikniecie albo: ./AudioExtract.sh).\n"
    "Jesli system nie pozwala uruchomic pliku, w terminalu wpisz:\n"
    "chmod +x AudioExtract.sh AudioExtract.bin\n"
    "./AudioExtract.sh\n",
    encoding="utf-8",
)
