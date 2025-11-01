@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0.."

echo.
echo ====================================================================
echo    NotebookLM - Starting Development Environment
echo ====================================================================
echo.

echo [*] Checking Docker containers...
docker-compose -f docker/docker-compose.yml ps | find "notebook-db" >nul
if errorlevel 1 (
    echo [+] Starting Docker containers...
    docker-compose -f docker/docker-compose.yml up -d
    echo [+] Waiting 15 seconds for services to be ready...
    timeout /t 15 /nobreak
) else (
    echo [OK] Docker containers already running
)

echo.
echo [*] Starting backend on http://localhost:8000
cd backend
start "Backend" cmd /k python -m uvicorn app.main:app --reload --port 8000
cd ..

timeout /t 2 /nobreak

if exist "frontend\package.json" (
    echo [*] Starting frontend on http://localhost:5173
    cd frontend
    start "Frontend" cmd /k npm run dev
    cd ..
)

echo.
echo ====================================================================
echo    SERVICES RUNNING
echo ====================================================================
echo.
echo    DOCKER:
echo       PostgreSQL: localhost:5434
echo       Redis:      localhost:6379
echo       LocalStack: localhost:4566
echo.
echo    BACKEND:   http://localhost:8000
echo    API DOCS:  http://localhost:8000/docs
echo    FRONTEND:  http://localhost:5173
echo.
echo    Commands:
echo       docker-compose -f docker/docker-compose.yml ps
echo       docker-compose -f docker/docker-compose.yml logs -f
echo.
echo    Close windows to stop services
echo.
pause
