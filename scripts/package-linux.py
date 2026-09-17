from pathlib import Path

root = Path("release")
root.mkdir(parents=True, exist_ok=True)

binary = root / "AudioExtract"
Path("dist/AudioExtract").replace(binary)
binary.chmod(0o755)

(root / "CZYTAJ.txt").write_text(
    "Uruchom w terminalu:\n"
    "chmod +x AudioExtract\n"
    "./AudioExtract\n"
    "\n"
    "Zip czasem gubi prawo uruchamiania — stąd chmod.\n",
    encoding="utf-8",
)
