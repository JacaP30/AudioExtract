from pathlib import Path

root = Path("release")
root.mkdir(parents=True, exist_ok=True)

binary = root / "Audioyt.bin"
Path("dist/Audioyt").replace(binary)
binary.chmod(0o755)

launcher = root / "Audioyt.sh"
launcher.write_text(
    "#!/usr/bin/env bash\n"
    "set -euo pipefail\n"
    'cd "$(dirname "$0")"\n'
    "chmod +x ./Audioyt.bin\n"
    "./Audioyt.bin\n",
    encoding="utf-8",
)
launcher.chmod(0o755)

(root / "CZYTAJ.txt").write_text(
    "Uruchom Audioyt.sh (podwojne klikniecie albo: ./Audioyt.sh).\n"
    "Jesli system nie pozwala uruchomic pliku, w terminalu wpisz:\n"
    "chmod +x Audioyt.sh Audioyt.bin\n"
    "./Audioyt.sh\n",
    encoding="utf-8",
)
