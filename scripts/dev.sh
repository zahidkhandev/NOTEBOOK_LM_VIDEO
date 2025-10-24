#!/bin/bash

echo "🚀 Starting development servers..."

# Start backend
echo "Starting backend on http://localhost:8000"
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

cd ..

# Start frontend
echo "Starting frontend on http://localhost:5173"
cd frontend
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "✅ Services running:"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Trap Ctrl+C to kill all processes
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT

wait
