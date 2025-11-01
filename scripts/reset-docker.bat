@echo off
cd /d "%~dp0.."

echo.
echo ====================================================================
echo    SAFE RESET - Only NotebookLM Project Data
echo ====================================================================
echo.

echo [!] WARNING: This will DELETE only NotebookLM containers and volumes!
echo.
set /p confirm="Type 'YES' to confirm: "
if /i not "%confirm%"=="YES" (
    echo [X] Cancelled
    exit /b 1
)

echo.
echo [*] Stopping only NotebookLM containers...
docker-compose -f docker/docker-compose.yml down

echo.
echo [*] Removing ONLY NotebookLM volumes...
docker volume rm notebook_db_data 2>nul
docker volume rm notebook_redis_data 2>nul
docker volume rm notebook_localstack_data 2>nul

echo.
echo [OK] RESET COMPLETE!
echo.
echo [+] Now run: scripts\dev.bat
echo.
pause
