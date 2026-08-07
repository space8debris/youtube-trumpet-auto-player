@echo off
cls

if exist "%USERPROFILE%\OneDrive\Documents" (
    set "DOCS_PATH=%USERPROFILE%\OneDrive\Documents"
) else (
    set "DOCS_PATH=%USERPROFILE%\Documents"
)

mkdir "%USERPROFILE%\Documents\YT_trumpet"
mkdir "%USERPROFILE%\Documents\YT_trumpet\insterments"
mkdir "%USERPROFILE%\Documents\YT_trumpet\midis"
mkdir "%USERPROFILE%\Documents\YT_trumpet\songs"

set "song_DIR=%USERPROFILE%\Documents\YT_trumpet\insterments"

cd /d "%song_DIR%"

curl -L "https://github.com/space8debris/youtube-trumpet-auto-player/raw/refs/heads/main/drum_fast.mp4" -o "drum_fast.mp4"
curl -L "https://github.com/space8debris/youtube-trumpet-auto-player/raw/refs/heads/main/piano_fast.mp4" -o "piano_fast.mp4"
curl -L "https://github.com/space8debris/youtube-trumpet-auto-player/raw/refs/heads/main/trumpet_fast.mp4" -o "Trumpet_fast.mp4"

set "file_DIR=%USERPROFILE%\Documents\YT_trumpet"

cd /d "%file_DIR%"

curl -L "https://github.com/space8debris/youtube-trumpet-auto-player/raw/refs/heads/main/many%20yt%20trumpets.py" -o "many yt trumpets.py"
curl -L "https://github.com/space8debris/youtube-trumpet-auto-player/raw/refs/heads/main/midi%20thing%20hopfly.py" -o "midi thing hopfly.py"


py -3.13 --version >nul 2>&1

winget install --id=mpv.net --silent --accept-source-agreements --accept-package-agreements >nul 2>&1
winget install --id Python.Python.3.13 --silent --accept-source-agreements --accept-package-agreements

for /f "tokens=2*" %%A in ('reg query "HKLM\System\CurrentControlSet\Control\Session Manager\Environment" /v Path') do set "SYS_PATH=%%B"
for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v Path') do set "USER_PATH=%%B"
set "PATH=%SYS_PATH%;%USER_PATH%"

py -m ensurepip --default-pip
py -m pip install --upgrade pip

py -m pip install pyautogui
py -m pip install mpv
py -m pip install python_mpv_jsonipc

start "" "https://sourceforge.net/projects/mpv-player-windows/files/64bit-v3/"

echo done now go to the link dowload the newest 3v if on new hardwere and then extract to sytem root

pause
exit

