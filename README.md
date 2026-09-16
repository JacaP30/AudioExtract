# AudioExtract

Lokalne narzędzie do wyciągania audio z własnych nagrań — wykładów, konferencji, rekolekcji i podobnych materiałów, do których masz prawa. Działa na Twoim komputerze: bez chmury, bez konta i bez zbierania danych. Wynik to plik MP3 192 kbps.

Możesz wkleić adres http/https albo wybrać plik wideo/audio z dysku. Wolny datek (Buycoffee) jest opcjonalny.

Używaj wyłącznie z materiałami, do których masz prawo. AudioExtract nie jest powiązane z żadną platformą wideo.

## Pobieranie gotowej aplikacji

Najnowsza wersja (strona z plikami):  
https://github.com/JacaP30/AudioExtract/releases/latest

Bezpośrednie pobrania (v1.0.0):

- Windows: https://github.com/JacaP30/AudioExtract/releases/download/v1.0.0/AudioExtract-windows.zip
- macOS: https://github.com/JacaP30/AudioExtract/releases/download/v1.0.0/AudioExtract-macos.zip
- Linux: https://github.com/JacaP30/AudioExtract/releases/download/v1.0.0/AudioExtract-linux.zip

Po rozpakowaniu:

- Windows: uruchom `AudioExtract.exe`
- macOS: uruchom `AudioExtract.app` (przy pierwszym starcie: prawy przycisk → **Otwórz**)
- Linux: `chmod +x AudioExtract.sh AudioExtract.bin && ./AudioExtract.sh`  
  Wymaga glibc ≥ 2.35 (np. Ubuntu 22.04+, Debian 12+, Fedora nowsze). Build CI jest na Ubuntu 22.04, żeby uniknąć błędu `GLIBC_2.38 not found` na starszych dystrybucjach.

## Samodzielna wersja dla laika

Najwygodniejsza wersja to pojedynczy plik aplikacji. Odbiorca nie musi instalować Pythona, bibliotek ani FFmpeg.

Na Windows uruchom `buduj.bat`, a na macOS/Linux uruchom `buduj.sh`. Gotowy plik pojawi się w folderze `dist`. Wyślij odbiorcy tylko plik z tego folderu. Po uruchomieniu aplikacja sama otworzy przeglądarkę.

PyInstaller buduje aplikację dla systemu, na którym jest uruchomiony. Wersje Windows, macOS i Linux trzeba zbudować osobno na odpowiednich systemach. Na macOS rezultat może być pojedynczym plikiem `AudioExtract` albo aplikacją `.app`.

### Budowanie wszystkich wersji z Windows

Nie da się natywnie zbudować wersji macOS na Windows. W repozytorium znajduje się workflow `.github/workflows/build-release.yml`, który robi to automatycznie na maszynach GitHub dla Windows, macOS i Linux.

Po wysłaniu projektu do GitHub:

1. Otwórz zakładkę **Actions**.
2. Wybierz **Build AudioExtract**.
3. Kliknij **Run workflow**.
4. Po zakończeniu pobierz artefakty `AudioExtract-windows`, `AudioExtract-macos` i `AudioExtract-linux`.
5. Rozpakuj archiwum. W środku są pliki z rozszerzeniami, które system rozpoznaje:

   - Windows: `AudioExtract.exe` — uruchom podwójnym kliknięciem.
   - macOS: `AudioExtract.app` — uruchom podwójnym kliknięciem. Przy pierwszym starcie kliknij aplikację prawym przyciskiem i wybierz **Otwórz**.
   - Linux: `AudioExtract.sh` — uruchom podwójnym kliknięciem albo w terminalu: `chmod +x AudioExtract.sh AudioExtract.bin && ./AudioExtract.sh`.

### Instalacja FFmpeg podczas budowania

FFmpeg jest dołączany przez pakiet `imageio-ffmpeg` podczas budowania, więc odbiorca nie musi instalować go osobno. Na macOS/Linux nadaj skryptowi prawo uruchamiania poleceniem `chmod +x buduj.sh`.

Licencje zależności są w folderze `licenses`. Licencja AudioExtract: MIT (`LICENSE`).

## Uruchomienie ręczne

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

Aplikacja przetwarza jeden materiał naraz i usuwa tymczasowy plik po wysłaniu go do przeglądarki.
