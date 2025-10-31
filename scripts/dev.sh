#!/bin/bash

set -e

cd "$(dirname "$0")/.."

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🚀 NotebookLM - Starting Development Environment          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if Docker containers are running
echo "🐳 Checking Docker containers..."
if ! docker-compose -f docker/docker-compose.yml ps | grep -q "notebook-db"; then
    echo "⏳ Starting Docker containers..."
    docker-compose -f docker/docker-compose.yml up -d
    echo "⏳ Waiting 10 seconds..."
    sleep 10
else
    echo "✅ Docker containers already running"
fi

echo ""
echo "🔧 Starting backend on http://localhost:8000"
cd backend
python -m uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

sleep 2

# Start frontend if exists
if [ -d "frontend" ] && [ -f "frontend/package.json" ]; then
    echo "🎨 Starting frontend on http://localhost:5173"
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    cd ..
else
    FRONTEND_PID=""
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ Services Running                                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "   🐳 Docker:"
echo "      PostgreSQL: localhost:5434"
echo "      Redis:      localhost:6379"
echo "      LocalStack: localhost:4566"
echo ""
echo "   🔧 Backend:     http://localhost:8000"
echo "   📍 API Docs:    http://localhost:8000/docs"
echo ""
if [ ! -z "$FRONTEND_PID" ]; then
    echo "   🎨 Frontend:    http://localhost:5173"
fi
echo ""
echo "   Press Ctrl+C to stop"
echo ""

# Clean up on exit
cleanup() {
    echo ""
    echo "🛑 Stopping..."
    kill $BACKEND_PID 2>/dev/null || true
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    exit 0
}

trap cleanup INT TERM

wait
