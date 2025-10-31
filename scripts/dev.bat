@echo off
cd /d "%~dp0.."

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  🚀 NotebookLM - Starting Development Environment          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo 🐳 Checking Docker containers...
docker-compose -f docker/docker-compose.yml ps | find "notebook-db" >nul
if %ERRORLEVEL% NEQ 0 (
    echo ⏳ Starting Docker containers...
    docker-compose -f docker/docker-compose.yml up -d
    timeout /t 10 /nobreak
) else (
    echo ✅ Docker containers already running
)

echo.
echo 🔧 Starting backend on http://localhost:8000
cd backend
start "Backend" python -m uvicorn app.main:app --reload --port 8000
cd ..

timeout /t 2 /nobreak

if exist frontend\package.json (
    echo 🎨 Starting frontend on http://localhost:5173
    cd frontend
    start "Frontend" cmd /k npm run dev
    cd ..
)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  ✅ Services Running                                       ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo    Backend:  http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo    Frontend: http://localhost:5173
echo.
pause
