@echo off
setlocal enabledelayedexpansion
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set BACKUP_FILE=backups\notebook_backup_%mydate%_%mytime%.sql
set LOG_FILE=backups\backup_log.txt
if not exist backups mkdir backups
echo [%date% %time%] Starting backup >> %LOG_FILE%
docker-compose ps | find "notebook-db" >nul
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] ERROR: Containers not running >> %LOG_FILE%
    exit /b 1
)
docker-compose exec -T notebook-db pg_dump -U postgres notebook_lm_db > %BACKUP_FILE%
if %ERRORLEVEL% EQU 0 (
    tar -czf "%BACKUP_FILE%.tar.gz" "%BACKUP_FILE%"
    del %BACKUP_FILE%
    for %%A in ("%BACKUP_FILE%.tar.gz") do set size=%%~zA
    echo [%date% %time%] SUCCESS: !size! >> %LOG_FILE%
) else (
    echo [%date% %time%] FAILED >> %LOG_FILE%
)
