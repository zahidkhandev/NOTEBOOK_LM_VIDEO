# Project Plan: NotebookLM Video Generator

## Project Overview

**Goal**: Build a production-ready system to generate NotebookLM-style educational videos from uploaded sources.

**Timeline**: 2-3 weeks for MVP

**Target Users**: Content creators, educators, YouTubers

## Phases

### Phase 1: Core Backend (Week 1)

#### Milestone 1.1: Project Setup ✅

- [x] Initialize monorepo structure
- [x] Set up FastAPI backend
- [x] Configure development environment
- [x] Install FFmpeg dependency
- [x] Create all router files (sources, videos, generation)
- [x] Set up package.json for frontend and Remotion
- [x] Configure Python virtual environment
- [x] Install all dependencies (latest versions)

#### Milestone 1.2: Source Processing

- [x] Implement document upload endpoint (basic)
- [ ] Build PDF text extraction
- [ ] Build DOCX text extraction
- [ ] Build URL/web scraping
- [ ] Implement source storage system
- [ ] Add database integration

#### Milestone 1.3: Gemini Integration

- [ ] Set up Gemini API client
- [ ] Implement script analysis service
- [ ] Build slide structure generator
- [ ] Create image prompt generator
- [ ] Add narration script generator

#### Milestone 1.4: Asset Generation

- [ ] Integrate Nano Banana image generation
- [ ] Implement Google Cloud TTS
- [ ] Build asset storage system
- [ ] Create batch processing pipeline

### Phase 2: Frontend & Remotion (Week 2)

#### Milestone 2.1: React Frontend

- [x] Set up Vite + React + TypeScript
- [ ] Create source upload UI
- [ ] Build video configuration form
- [ ] Implement progress tracking
- [ ] Add video history/library

#### Milestone 2.2: Remotion Components

- [ ] Create base NotebookLM slide component
- [ ] Implement all slide variations (data, quote, etc.)
- [ ] Build section dividers
- [ ] Add animations and transitions
- [ ] Create style themes (Classic, Whiteboard, etc.)

#### Milestone 2.3: Integration

- [ ] Connect frontend to backend API
- [ ] Implement WebSocket for progress updates
- [ ] Build preview functionality
- [ ] Add video playback

### Phase 3: Rendering & Polish (Week 3)

#### Milestone 3.1: Video Rendering

- [ ] Integrate Remotion renderer with backend
- [ ] Implement queue system for rendering
- [ ] Add render progress tracking
- [ ] Build error handling and retry logic

#### Milestone 3.2: Optimization

- [ ] Add caching for generated assets
- [ ] Optimize image generation batching
- [ ] Implement concurrent rendering
- [ ] Add video compression options

#### Milestone 3.3: Testing & Documentation

- [ ] Write API tests
- [ ] Create integration tests
- [ ] Write user documentation
- [ ] Add code examples
- [ ] Record demo video

### Phase 4: Deployment (Ongoing)

#### Milestone 4.1: Production Setup

- [ ] Configure production environment
- [ ] Set up CI/CD pipeline
- [ ] Deploy to cloud platform
- [ ] Configure monitoring

#### Milestone 4.2: Scaling

- [ ] Implement Redis for job queue
- [ ] Add PostgreSQL database
- [ ] Configure S3 for storage
- [ ] Set up CDN for assets

## Technical Decisions

### Architecture Choices

**Monorepo**: Single repository for backend, frontend, and Remotion

- Pros: Easier development, shared types, single deployment
- Cons: Larger repo size

**FastAPI Backend**: High-performance async Python framework

- Pros: Fast, great docs, type safety, async support
- Cons: Python dependency management

**Remotion**: Programmatic video generation with React

- Pros: Full control, TypeScript support, maintainable
- Cons: Rendering time, complexity

**SQLite → PostgreSQL**: Start simple, scale later

- Pros: Zero setup, file-based, good for MVP
- Cons: No concurrent writes (will migrate to Postgres)

### API Design

**RESTful endpoints** for CRUD operations
**WebSocket** for real-time progress updates
**Async processing** for long-running tasks

### Latest Dependencies (Oct 24, 2025)

- **Python**: Latest versions without pinning (fastapi, uvicorn, google-generativeai 0.8.3)
- **React**: 18.3.1
- **Remotion**: 4.0.246
- **Vite**: 5.4.10
- **TypeScript**: 5.6.3

## Success Criteria

### MVP Success

- [ ] Generate 5-minute video from PDF in under 20 minutes
- [ ] Support 3+ visual styles
- [ ] Cost per video under $0.50
- [ ] Clean UI with <5 clicks to start generation
- [ ] 95%+ uptime

### Future Enhancements

- Multi-language support
- Voice cloning integration
- Custom branding options
- Batch video generation
- Template library
- Analytics dashboard

## Risk Management

| Risk                          | Impact | Mitigation                                |
| ----------------------------- | ------ | ----------------------------------------- |
| Gemini API rate limits        | High   | Implement queue, caching, retries         |
| Rendering time too long       | Medium | Use cloud rendering, optimize code        |
| Asset storage costs           | Medium | Implement cleanup, use compression        |
| Complex UI learning curve     | Low    | Add tutorials, tooltips, examples         |
| Windows-specific setup issues | Medium | Provide PowerShell scripts, detailed docs |

## Resource Requirements

**Development**: 1-2 developers
**APIs**: Google Cloud account with billing
**Infrastructure**: Local development initially
**Storage**: 10GB+ for generated assets

## Next Steps

1. **Immediate**: Create service files for document processing
2. **Today**: Implement PDF/DOCX extraction
3. **This Week**: Gemini API integration for script analysis
4. **Next Week**: Frontend UI and Remotion components
