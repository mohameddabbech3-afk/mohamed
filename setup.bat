@echo off
REM Setup script for The Well That Heard the Same Wish cartoon short
REM Run this from the project directory: shorts/well-wishes

set PROJECT_DIR=%~dp0
cd /d "%PROJECT_DIR%"

echo ========================================
echo Setting up: The Well That Heard the Same Wish
echo ========================================
echo.

REM 1. Create directories
echo [1/6] Creating directories...
if not exist web\lib mkdir web\lib
if not exist web\fonts mkdir web\fonts
if not exist work mkdir work
if not exist stills mkdir stills
if not exist out mkdir out
echo Done.
echo.

REM 2. Copy kit files
echo [2/6] Copying kit files...
set KIT_DIR=C:\Users\Adem\Desktop\cartoon-short-kit

copy "%KIT_DIR%\fonts\*.ttf" "web\fonts\"
copy "%KIT_DIR%\engine\*.js" "web\"
copy "%KIT_DIR%\engine\index.html" "web\"
copy "%KIT_DIR%\vendor\three.module.js" "web\lib\"
copy "%KIT_DIR%\vendor\toonbase.js" "web\"
copy "%KIT_DIR%\engine\roman.js" "web\"
copy "%KIT_DIR%\tools\timing.py" "."
copy "%KIT_DIR%\tools\render.mjs" "."
copy "%KIT_DIR%\tools\sheet.py" "."
copy "%KIT_DIR%\tools\mix.py" "."
copy "%KIT_DIR%\tools\finish.sh" "."

REM Combine toonbase + roman into toon.js
type "web\toonbase.js" "web\roman.js" > "web\toon.js"
echo Kit files copied.
echo.

REM 3. Install Node dependencies
echo [3/6] Installing Playwright...
npm install playwright --no-audit --no-fund
if errorlevel 1 (
    echo ERROR: npm install failed
    pause
    exit /b 1
)
echo.

REM 4. Install Playwright Chromium
echo [4/6] Installing Playwright Chromium...
npx playwright install chromium
if errorlevel 1 (
    echo ERROR: Playwright install failed
    pause
    exit /b 1
)
echo.

REM 5. Install Python dependencies
echo [5/6] Installing Python packages...
pip install numpy pillow --break-system-packages
if errorlevel 1 (
    echo ERROR: pip install failed
    pause
    exit /b 1
)
echo.

REM 6. Copy voice.mp3 (user needs to provide)
echo [6/6] Checking for voice.mp3...
if exist voice.mp3 (
    echo voice.mp3 found - ready to render!
) else (
    echo WARNING: voice.mp3 not found!
    echo Please record the script and save as voice.mp3 in this folder
    echo Or copy from: C:\Users\Adem\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Local\Claude-3p\local-agent-mode-sessions\b1d93b46\00000000\e97e86d3\uploads\voice_preview_mike - animation, explainers ^& gaming.mp3
)
echo.

echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure voice.mp3 is in this folder (record your narration matching script.txt)
echo 2. Run timing extraction:
echo    python timing.py voice.mp3 script.txt --out work --lang ar
echo.
echo 3. Check work/phrases.json and update web/story.js SHOTS with actual frames
echo.
echo 4. Generate look-check stills:
echo    node render.mjs stills/a "0,90,210,330,450,570,690,809"
echo    python sheet.py stills/a stills/sheet_a.jpg
echo.
echo 5. Render frames:
echo    node render.mjs frames "0-809"
echo.
echo 6. Generate audio:
echo    python audio.py
echo    python mix.py voice.mp3 music.wav sfx.wav
echo.
echo 7. Final encode:
echo    bash finish.sh "The Well That Heard the Same Wish"
echo.
pause