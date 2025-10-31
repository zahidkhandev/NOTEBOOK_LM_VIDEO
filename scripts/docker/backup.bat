@echo off
setlocal enabledelayedexpansion
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set BACKUP_FILE=backups\notebook_backup_%mydate%_%mytime%.sql
if not exist backups mkdir backups
echo.
echo ════════════════════════════════════════════════════════════
echo 📦 BACKING UP POSTGRESQL
echo ════════════════════════════════════════════════════════════
echo 🔄 Dumping to: %BACKUP_FILE%
echo.
docker-compose exec -T notebook-db pg_dump -U postgres notebook_lm_db > %BACKUP_FILE%
if %ERRORLEVEL% EQU 0 (
    for %%A in (%BACKUP_FILE%) do set size=%%~zA
    echo ✅ Backup complete: !size! bytes
    echo 🗜️ Compressing...
    tar -czf "%BACKUP_FILE%.tar.gz" "%BACKUP_FILE%"
    if exist "%BACKUP_FILE%.tar.gz" (
        del %BACKUP_FILE%
        echo ✅ Compressed: %BACKUP_FILE%.tar.gz
    )
) else (
    echo ❌ Backup failed! Check containers: docker-compose up -d
)
echo.
pause
