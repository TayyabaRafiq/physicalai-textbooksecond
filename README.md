# AI-Native Physical AI & Humanoid Robotics Textbook

A comprehensive interactive textbook with an integrated RAG (Retrieval-Augmented Generation) chatbot for learning Physical AI and Humanoid Robotics from ROS 2 to Vision-Language-Action systems.

## Project Overview

This project combines:
- **Interactive Textbook**: Built with Docusaurus, featuring structured content on Physical AI topics including ROS 2, computer vision, motion planning, and VLA systems
- **RAG Chatbot**: Intelligent question-answering system that retrieves relevant content from the textbook and provides accurate, citation-backed answers
- **Floating AI Assistant**: Accessible from any docs page, allowing students to ask questions while reading

## Tech Stack

### Frontend
- **Docusaurus 3.9.2** - Static site generator with React
- **React 19** - UI components and interactivity
- **MDX** - Enhanced markdown for rich content

### Backend
- **FastAPI** - High-performance Python web framework
- **Cohere** - Embeddings (embed-english-v3.0) and LLM (Command)
- **Qdrant Cloud** - Vector database for semantic search
- **Neon Postgres** - Serverless database for content storage
- **SQLAlchemy + Alembic** - ORM and migrations
- **UV** - Fast Python package manager

## Features

### Content Ingestion
- Markdown-to-database pipeline
- Automatic text chunking with metadata preservation
- Vector embeddings generation
- Dual storage (Postgres + Qdrant)

### Semantic Search
- Vector similarity search using Qdrant
- Metadata filtering (module, chapter, section)
- Top-k retrieval with configurable limits

### Question Answering
- Source-grounded answers with citations
- Context-aware responses using RAG
- Module/chapter/section filtering support
- Fallback handling for out-of-scope questions

### Frontend Integration
- Floating "Ask AI" button on all `/docs` pages
- Opens chat in new tab for seamless multitasking
- Clean, professional UI with gradient styling
- Mobile-responsive design

## Running the Project

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   ```
   Fill in your API keys:
   - `COHERE_API_KEY` - Get from https://cohere.com
   - `QDRANT_URL` and `QDRANT_API_KEY` - Get from https://qdrant.tech
   - `DATABASE_URL` - Get from https://neon.tech

3. **Install dependencies** (using uv):
   ```bash
   uv sync
   ```

4. **Run database migrations**:
   ```bash
   uv run alembic upgrade head
   ```

5. **Start the server**:
   ```bash
   uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

   Backend will be available at: http://localhost:8000
   API docs at: http://localhost:8000/docs

### Frontend Setup

1. **Navigate to project root**:
   ```bash
   cd ..
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm start
   ```

   Frontend will be available at: http://localhost:3000

4. **Build for production**:
   ```bash
   npm run build
   ```

## API Overview

### Health Check
- **GET** `/health` - Server health status
- **GET** `/health/dependencies` - Check all external services (Qdrant, Neon, Cohere)

### Content Ingestion
- **POST** `/api/v1/ingest` - Ingest markdown content
  ```json
  {
    "file_path": "string",
    "module": "string",
    "chapter": "string",
    "section": "string"
  }
  ```

### Question Answering
- **POST** `/api/v1/question` - Ask a question
  ```json
  {
    "question": "string",
    "module": "optional",
    "chapter": "optional",
    "section": "optional"
  }
  ```
  Response includes answer and source citations.

### Interactive API Documentation
Visit http://localhost:8000/docs for full Swagger UI documentation with request/response schemas.

## Deployment

### Frontend (Vercel)
The frontend is optimized for Vercel deployment:
```bash
npm run build
# Deploy to Vercel
```

### Backend (Railway/Render/Fly.io)
The backend is compatible with major cloud platforms:
- Set environment variables in platform dashboard
- Deploy from `backend/` directory
- Ensure `DATABASE_URL`, `QDRANT_URL`, and `COHERE_API_KEY` are configured

**Note**: Frontend and backend must be deployed separately. Update the `API_URL` in `src/pages/chat.jsx` to point to your deployed backend.

## Project Structure

```
.
├── backend/                 # FastAPI backend
│   ├── app/                # Application code
│   ├── alembic/            # Database migrations
│   ├── content/            # Sample markdown content
│   ├── main.py             # FastAPI entry point
│   └── pyproject.toml      # Python dependencies
├── content/                # Docusaurus textbook content
│   ├── intro.md           # Landing page
│   └── modules/           # Organized by modules
├── src/
│   ├── components/        # React components
│   ├── css/               # Global styles
│   ├── pages/             # Custom pages (homepage, chat)
│   └── theme/             # Docusaurus theme overrides
├── static/                # Static assets
├── docusaurus.config.ts   # Docusaurus configuration
└── package.json           # Frontend dependencies
```

## Status

**✅ Submission Ready**

This project is complete and ready for submission with:
- Fully functional RAG backend with Cohere, Qdrant, and Neon
- Interactive Docusaurus frontend with integrated chatbot
- Comprehensive API documentation
- Professional UI/UX with floating AI assistant
- Source-grounded answers with citations
- Production-ready deployment configuration

---

**License**: MIT | **Created**: 2025 | **Built with**: FastAPI, Docusaurus, Cohere, Qdrant, Neon
