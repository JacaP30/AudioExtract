# Audioyt

Lokalna aplikacja Flask do pobierania audio z pojedynczego filmu YouTube i konwersji do MP3.

## Uruchomienie na Windows

1. Zainstaluj Python 3.11+ oraz FFmpeg. Po instalacji sprawdź w PowerShell:

   ```powershell
   ffmpeg -version
   ```

2. Utwórz środowisko i zainstaluj zależności:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. Uruchom aplikację:

   ```powershell
   py app.py
   ```

4. Otwórz `http://127.0.0.1:5000`.

Aplikacja przetwarza jeden film naraz i usuwa tymczasowy plik z serwera po wysłaniu go do przeglądarki. Używaj jej wyłącznie z materiałami, do których masz prawo pobierania.