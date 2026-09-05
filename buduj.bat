@echo off
setlocal
cd /d "%~dp0"
title Audioyt - budowanie pliku EXE

where py >nul 2>&1
if %errorlevel% equ 0 (set "PYTHON=py") else (set "PYTHON=python")

if not exist ".venv\Scripts\python.exe" (
    echo Tworzenie srodowiska budowania...
    %PYTHON% -m venv .venv
    if errorlevel 1 goto :error
)

echo Instalowanie bibliotek aplikacji i PyInstaller...
".venv\Scripts\python.exe" -m pip install -r requirements.txt pyinstaller
if errorlevel 1 goto :error

echo Czyszczenie poprzedniego buildu...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist Audioyt.spec del /q Audioyt.spec

echo Budowanie Audioyt.exe...
".venv\Scripts\pyinstaller.exe" --noconfirm --clean --onefile --console --name Audioyt --add-data "templates;templates" --add-data "static;static" --collect-all imageio_ffmpeg app.py
if errorlevel 1 goto :error

echo.
echo Gotowe. Wyslij plik:
echo %cd%\dist\Audioyt.exe
echo.
echo Odbiorca nie potrzebuje Pythona ani FFmpeg - wszystko jest w jednym pliku.
pause
exit /b 0

:error
echo.
echo Budowanie nie powiodlo sie.
pause
exit /b 1