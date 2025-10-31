@echo off
setlocal enabledelayedexpansion
echo.
echo ════════════════════════════════════════════════════════════
echo 📥 DOWNLOADING FROM DOCKER HUB
echo ════════════════════════════════════════════════════════════
echo.
if not exist backups mkdir backups
echo 🐳 Pulling image...
docker pull zahidkhandev/notebook-lm-backup:latest
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to pull image
    pause
    exit /b 1
)
echo ✅ Image pulled
echo 📦 Extracting...
docker create --name temp-backup zahidkhandev/notebook-lm-backup:latest
docker cp temp-backup:/backup.tar.gz backups/downloaded_backup.tar.gz
docker rm temp-backup
if exist backups\downloaded_backup.tar.gz (
    echo ✅ Downloaded: backups\downloaded_backup.tar.gz
    echo.
    echo 🔄 To restore: restore.bat backups\downloaded_backup.tar.gz
) else (
    echo ❌ Failed to extract
)
echo.
pause
