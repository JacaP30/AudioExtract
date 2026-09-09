# Audioyt

Lokalna aplikacja Flask do pobierania audio z pojedynczego filmu YouTube i konwersji do MP3.

## Samodzielna wersja dla laika

Najwygodniejsza wersja to pojedynczy plik aplikacji. Odbiorca nie musi instalowac Pythona, bibliotek ani FFmpeg.

Na Windows uruchom `buduj.bat`, a na macOS/Linux uruchom `buduj.sh`. Gotowy plik pojawi sie w folderze `dist`. Wyslij odbiorcy tylko plik z tego folderu. Po uruchomieniu aplikacja sama otworzy przegladarke i uruchomi wlasne okno terminala w tle. Terminal zamknie sie automatycznie, gdy aplikacja zostanie zakonczona.

PyInstaller buduje aplikacje dla systemu, na ktorym jest uruchomiony. Wersje Windows, macOS i Linux trzeba zbudowac osobno na odpowiednich systemach. Na macOS rezultat moze byc pojedynczym plikiem `Audioyt` albo aplikacja `.app`, zależnie od sposobu dystrybucji.

### Budowanie wszystkich wersji z Windows

Nie da sie natywnie zbudowac wersji macOS na Windows. W repozytorium znajduje sie workflow `.github/workflows/build-release.yml`, ktory robi to automatycznie na maszynach GitHub dla Windows, macOS i Linux.

Po wyslaniu projektu do GitHub:

1. Otworz zakladke **Actions**.
2. Wybierz **Build Audioyt**.
3. Kliknij **Run workflow**.
4. Po zakonczeniu pobierz artefakty `Audioyt-windows`, `Audioyt-macos` i `Audioyt-linux`.
5. Rozpakuj archiwum. W srodku sa pliki z rozszerzeniami, ktore system rozpoznaje:

   - Windows: `Audioyt.exe` — uruchom podwojnym kliknieciem.
   - macOS: `Audioyt.app` — uruchom podwojnym kliknieciem. Przy pierwszym starcie kliknij aplikacje prawym przyciskiem i wybierz **Otworz**.
   - Linux: `Audioyt.sh` — uruchom podwojnym kliknieciem albo w terminalu: `chmod +x Audioyt.sh Audioyt.bin && ./Audioyt.sh`.

### Instalacja FFmpeg podczas budowania

FFmpeg jest dołączany przez pakiet `imageio-ffmpeg` podczas budowania, więc odbiorca nie musi instalować go osobno. Na macOS/Linux nadaj skryptowi prawo uruchamiania poleceniem `chmod +x buduj.sh`.

## Uruchomienie reczne

Aplikacja korzysta ze środowiska wirtualnego w folderze `.venv`. Bez jego włączenia `python app.py` może użyć systemowego Pythona i zgłosić brak bibliotek.

1. Zainstaluj Python 3.11+ oraz FFmpeg. Po instalacji sprawdź w PowerShell:

   ```powershell
   ffmpeg -version
   ```

2. Utwórz środowisko `.venv` i zainstaluj zależności (wystarczy raz):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

   Na macOS i Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. W każdym nowym terminalu najpierw włącz `.venv`, potem uruchom aplikację.

   Windows (PowerShell):

   ```powershell
   .\.venv\Scripts\Activate.ps1
   python app.py
   ```

   macOS i Linux:

   ```bash
   source .venv/bin/activate
   python app.py
   ```

   Bez aktywacji możesz też uruchomić Pythona bezpośrednio ze środowiska:

   ```powershell
   .\.venv\Scripts\python.exe app.py
   ```

4. Otwórz `http://127.0.0.1:5000`.

Aktywne `.venv` poznasz po przedrostku `(.venv)` w wierszu poleceń. Aby je wyłączyć, wpisz `deactivate`.

Aplikacja przetwarza jeden film naraz i usuwa tymczasowy plik z serwera po wysłaniu go do przeglądarki. Używaj jej wyłącznie z materiałami, do których masz prawo pobierania.