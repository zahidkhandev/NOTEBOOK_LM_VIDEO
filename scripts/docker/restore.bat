@echo off
setlocal enabledelayedexpansion
echo.
echo ════════════════════════════════════════════════════════════
echo 🔄 DATABASE RESTORE
echo ════════════════════════════════════════════════════════════
if "%~1"=="" (
    echo Usage: restore.bat path\to\backup.sql
    echo.
    echo Available backups:
    dir /B backups\*.sql 2>nul
    dir /B backups\*.tar.gz 2>nul
    echo.
    pause
    exit /b 1
)
set BACKUP_FILE=%~1
if not exist "%BACKUP_FILE%" (
    echo ❌ File not found: %BACKUP_FILE%
    pause
    exit /b 1
)
echo 📁 Restoring: %BACKUP_FILE%
if "%BACKUP_FILE:~-7%"==".tar.gz" (
    echo 📦 Extracting...
    tar -xzf "%BACKUP_FILE%" -C backups
    for %%f in (backups\*.sql) do set BACKUP_FILE=%%f
)
docker-compose ps | find "notebook-db" >nul
if %ERRORLEVEL% NEQ 0 (
    echo ⏳ Starting containers...
    docker-compose up -d
    timeout /t 10 /nobreak
)
echo ⏳ Waiting for PostgreSQL...
timeout /t 5 /nobreak
echo 🔄 Restoring database...
docker-compose exec -T notebook-db psql -U postgres notebook_lm_db < "%BACKUP_FILE%"
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ RESTORE COMPLETE
    echo.
) else (
    echo ❌ RESTORE FAILED
)
pause
