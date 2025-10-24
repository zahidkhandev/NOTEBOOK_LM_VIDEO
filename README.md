# NotebookLM Video Generator

A production-ready system for generating NotebookLM-style educational videos using AI. Upload sources, configure your video, and generate professional content automatically.

## Features

- 📄 **Multi-Source Support**: PDF, DOCX, TXT, URLs, YouTube videos
- 🎨 **NotebookLM Styles**: Classic, Whiteboard, Watercolor, Retro, Heritage, Papercraft, Anime
- ⏱️ **Custom Durations**: 1-10 minute videos with automatic pacing
- 🤖 **AI-Powered**: Gemini 2.0 for analysis, Nano Banana for images, Google TTS for voice
- 🎥 **Remotion Rendering**: Programmatic video generation with React
- 🚀 **FastAPI Backend**: High-performance async API
- 💅 **React Frontend**: Clean, intuitive UI

## Tech Stack

**Backend:**

- FastAPI (Python 3.11+)
- Google Gemini API
- Google Cloud Text-to-Speech
- PyPDF2, python-docx, BeautifulSoup4
- SQLite (can upgrade to PostgreSQL)

**Frontend:**

- React 18 + TypeScript
- Vite
- TanStack Query
- Tailwind CSS

**Video Generation:**

- Remotion 4.x
- FFmpeg

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- FFmpeg installed
- Google Cloud API credentials

### Installation

Clone repository
git clone <repo-url>
cd notebooklm-video-generato

Run setup script
chmod +x scripts/setup.sh
./scripts/

### Configuration

Backend
cd backend
cp .env.e

Edit .env with your API keys

### Development

Start all services
chmod +x scripts/dev.sh
./scripts/dev.sh

Access:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Project Structure

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed documentation.

## Usage

1. **Upload Sources**: Add PDFs, documents, or URLs
2. **Configure Video**: Set duration, style, and preferences
3. **Generate**: AI analyzes content and creates video structure
4. **Review**: Preview slides and narration
5. **Render**: Generate final video (5-20 minutes)
6. **Download**: Get your MP4 file

## API Documentation

See [API.md](docs/API.md) for complete API reference.

## Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for production deployment guide.

## Cost Estimation

**Per 5-minute video:**

- Gemini API: ~$0.40
- Google Cloud TTS: ~$0.01
- Total: **~$0.41**

No rendering costs (runs locally or on Colab free tier).

## License

MIT

## Support

Open an issue or contact the maintainers.
