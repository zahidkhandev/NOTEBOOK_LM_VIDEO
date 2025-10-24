#!/bin/bash

echo "🚀 Setting up NotebookLM Video Generator..."

# Check prerequisites
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required but not installed. Aborting." >&2; exit 1; }
command -v node >/dev/null 2>&1 || { echo "Node.js is required but not installed. Aborting." >&2; exit 1; }
command -v ffmpeg >/dev/null 2>&1 || { echo "FFmpeg is required but not installed. Aborting." >&2; exit 1; }

# Backend setup
echo "📦 Setting up backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create directories
mkdir -p data/sources data/generated/images data/generated/audio data/generated/videos data/temp

# Copy env file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Please edit backend/.env with your API keys"
fi

cd ..

# Frontend setup
echo "📦 Setting up frontend..."
cd frontend
npm install
cd ..

# Remotion setup
echo "📦 Setting up Remotion..."
cd remotion
npm install
cd ..

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your API keys"
echo "2. Run ./scripts/dev.sh to start development servers"
