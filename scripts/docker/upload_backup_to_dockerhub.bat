@echo off
setlocal enabledelayedexpansion
echo.
echo ════════════════════════════════════════════════════════════
echo 📤 UPLOADING TO DOCKER HUB
echo ════════════════════════════════════════════════════════════
for /f "tokens=*" %%F in ('dir /B /O:-D backups\*.tar.gz ^| findstr /V "^$"') do (
    set LATEST_BACKUP=%%F
    goto :found
)
:found
if "!LATEST_BACKUP!"=="" (
    echo ❌ No backup found
    pause
    exit /b 1
)
echo 📁 Latest: !LATEST_BACKUP!
echo.
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 🔐 Docker not logged in. Logging in...
    docker login
)
echo 📤 Creating image...
docker create --name temp-backup-container alpine
docker cp "backups\!LATEST_BACKUP!" temp-backup-container:/backup.tar.gz
docker commit temp-backup-container zahidkhandev/notebook-lm-backup:latest
docker push zahidkhandev/notebook-lm-backup:latest
docker rm -f temp-backup-container
echo.
echo ✅ UPLOADED: zahidkhandev/notebook-lm-backup:latest
echo.
pause
