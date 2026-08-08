@echo off
cls

net session >nul 2>&1
if %errorLevel% neq 0 (
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

winget install --id Python.Python.3.13 --silent --accept-source-agreements --accept-package-agreements

for /f "tokens=2*" %%A in ('reg query "HKLM\System\CurrentControlSet\Control\Session Manager\Environment" /v Path') do set "SYS_PATH=%%B"
for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v Path') do set "USER_PATH=%%B"
set "PATH=%SYS_PATH%;%USER_PATH%"

:dependencies
py -3.13 -m ensurepip --default-pip
py -3.13 -m pip install --upgrade pip
py -3.13 -m pip install pyautogui mpv python_mpv_jsonipc PySimpleGUI

mkdir "%DOCS_PATH%\YT_trumpet"
mkdir "%DOCS_PATH%\YT_trumpet\insterments"
mkdir "%DOCS_PATH%\YT_trumpet\midis"
mkdir "%DOCS_PATH%\YT_trumpet\songs"
mkdir "%DOCS_PATH%\YT_trumpet\MPV"

set "song_DIR=%DOCS_PATH%\YT_trumpet\insterments"
cd /d "%song_DIR%"
curl -L "https://githubusercontent.com" -o "drum_fast.mp4"
curl -L "https://githubusercontent.com" -o "piano_fast.mp4"
curl -L "https://githubusercontent.com" -o "Trumpet_fast.mp4"
curl -L "https://githubusercontent.com" -o "Guitar_fast.mp4"

set "file_DIR=%DOCS_PATH%\YT_trumpet"
cd /d "%file_DIR%"
curl -L "https://raw.githubusercontent.com/space8debris/youtube-trumpet-auto-player/main/YT_trumpet_GUI.py" -o "YT_trumpet_GUI.py"
curl -L "https://raw.githubusercontent.com/space8debris/youtube-trumpet-auto-player/main/many%20yt%20trumpets%20.py" -o "many yt trumpets.py"
curl -L "https://raw.githubusercontent.com/space8debris/youtube-trumpet-auto-player/main/midi%20maker.py" -o "midi maker.py"

curl -L "https://://githubusercontent.com/space8debris/youtube-trumpet-auto-player/refs/heads/main/logos/Big_Logo.png" -o "Big_Logo.png"
curl -L "https://://githubusercontent.com/space8debris/youtube-trumpet-auto-player/refs/heads/main/logos/Logo.png" -o "Logo.png"
curl -L "https://://githubusercontent.com/space8debris/youtube-trumpet-auto-player/refs/heads/main/logos/Big_Logo_Alt.ico" -o "Big_Logo_Alt.ico"
curl -L "https://://githubusercontent.com/space8debris/youtube-trumpet-auto-player/refs/heads/main/logos/Big_Logo_Alt.png" -o "Big_Logo_Alt.png"


winget install --id=mpv.net --silent --accept-source-agreements --accept-package-agreements >nul 2>&1


start "" "https://sourceforge.net/projects/mpv-player-windows/files/64bit-v3/mpv-x86_64-v3-20260607-git-71ebd08.7z/download"
echo Done go to the link download the newest v3 thing and extract it into the MPV folder in your YT_trumpet.

pause
exit
