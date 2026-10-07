@echo off
cls
setlocal enabledelayedexpansion

:: Request administrative 
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrative privileges
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

if exist "%USERPROFILE%\OneDrive\Documents" (
    set "DOCS_PATH=%USERPROFILE%\OneDrive\Documents"
) else (
    set "DOCS_PATH=%USERPROFILE%\Documents"
)

py -3.13 --version >nul 2>&1
if %errorLevel%==0 (
    goto :dependencies
)

echo Python 3.13 not found. Installing
winget install --id Python.Python.3.13 --silent --accept-source-agreements --accept-package-agreements

for /f "tokens=2*" %%A in ('reg query "HKLM\System\CurrentControlSet\Control\Session Manager\Environment" /v Path') do set "SYS_PATH=%%B"
for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v Path') do set "USER_PATH=%%B"
set "PATH=%SYS_PATH%;%USER_PATH%"

:dependencies
echo Upgrading pip and setting up environment
py -3.13 -m ensurepip --default-pip
py -3.13 -m pip install --upgrade pip

py -3.13 -m pip install pyautogui python-mpv python-mpv-jsonipc PySimpleGUI mido

mkdir "!DOCS_PATH!\YT_trumpet" 2>nul
mkdir "!DOCS_PATH!\YT_trumpet\insterments" 2>nul
mkdir "!DOCS_PATH!\YT_trumpet\midis" 2>nul
mkdir "!DOCS_PATH!\YT_trumpet\songs" 2>nul
mkdir "!DOCS_PATH!\YT_trumpet\MPV" 2>nul

set "song_DIR=!DOCS_PATH!\YT_trumpet\insterments"
cd /d "!song_DIR!"

echo Downloading instruments
curl -L "https://github.com/space8debris/youtube-trumpet-auto-player/raw/refs/heads/main/insterments/drum_fast.mp4" -o "drum_fast.mp4"
curl -L "https://github.com/space8debris/youtube-trumpet-auto-player/raw/refs/heads/main/insterments/piano_fast.mp4" -o "piano_fast.mp4"
curl -L "https://github.com/space8debris/youtube-trumpet-auto-player/raw/refs/heads/main/insterments/trumpet_fast.mp4" -o "Trumpet_fast.mp4"
curl -L "https://github.com/space8debris/youtube-trumpet-auto-player/raw/refs/heads/main/insterments/Guitar_fast.mp4" -o "Guitar_fast.mp4"

set "file_DIR=!DOCS_PATH!\YT_trumpet"
cd /d "!file_DIR!"

curl -L "https://github.com/space8debris/youtube-trumpet-auto-player/raw/refs/heads/main/YT_trumpet_GUI.py" -o "YT_trumpet_GUI.py"
curl -L "https://github.com/space8debris/youtube-trumpet-auto-player/raw/refs/heads/main/many_yt_trumpets.py" -o "many yt trumpets.py"
curl -L "https://github.com/space8debris/youtube-trumpet-auto-player/raw/refs/heads/main/midi_maker.py" -o "midi maker.py"
curl -L "https://github.com/space8debris/youtube-trumpet-auto-player/blob/main/logos/Big_Logo.png?raw=true" -o "Big_Logo.png"
curl -L "https://github.com/space8debris/youtube-trumpet-auto-player/blob/main/logos/Logo.png?raw=true" -o "Logo.png"
curl -L "https://github.com/space8debris/youtube-trumpet-auto-player/raw/refs/heads/main/logos/Big_Logo_Alt.ico" -o "Big_Logo_Alt.ico"
curl -L "https://github.com/space8debris/youtube-trumpet-auto-player/blob/main/logos/Big_Logo_Alt.png?raw=true" -o "Big_Logo_Alt.png"

start "" "https://sourceforge.net/projects/mpv-player-windows/files/64bit-v3/"

echo done now go to the link dowload the newest 3v if on new hardwere and then extract to MPV folder in the yt trumpet folder

pause
exit
