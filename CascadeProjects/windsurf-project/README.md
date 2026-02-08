# GENESIS AI - Hybrid Orchestrator System

A intelligent AI-powered code generation system that uses multiple AI models with smart routing to provide the best possible results for any task.

## 🚀 Features

- **Multi-Model AI Routing**: Automatically routes tasks to the best AI model (Claude, GPT-4, Gemini, Groq)
- **Intelligent Fallback**: If one model fails, automatically tries the next best option
- **Task Classification**: Automatically detects task types (UI design, code generation, debugging, etc.)
- **Real-time Updates**: WebSocket support for live generation progress
- **Project Management**: Complete project organization and file management
- **API Exposure**: Public API for external applications
- **Budget-Friendly**: Uses your existing AI API keys, no training costs

## 🏗️ Architecture

```
Next.js Dashboard (Frontend)
         ↓
FastAPI Backend (Python)
         ↓
Smart Router (Hybrid AI)
         ↓
┌───────┴───────┬──────────┬──────────┐
↓               ↓          ↓          ↓
Claude      OpenAI GPT    Gemini     Groq
(via API)   (via API)   (via API)  (via API)
```

## 📋 Quick Start

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.8+
- API keys for at least one AI service:
  - Anthropic Claude
  - OpenAI GPT
  - Google Gemini
  - Groq

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd genesis-ai
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Start the services**
   
   Backend (Terminal 1):
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   Frontend (Terminal 2):
   ```bash
   cd frontend
   npm run dev
   ```

5. **Open your browser**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables (.env)

```env
# AI Model API Keys
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# App Settings
APP_NAME=GENESIS AI
VERSION=1.0.0
DEBUG=true

# CORS Settings
ALLOWED_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]

# File Storage
PROJECTS_DIR=./sandbox/projects
```

## 📖 Usage

### Web Interface

1. Open http://localhost:3000
2. Enter your prompt in the text area
3. Optionally select a specific task type
4. Click "Generate" and watch the AI work its magic
5. View results, copy code, or save to projects

### API Usage

```bash
# Generate content
curl -X POST "http://localhost:8000/api/generate/" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a React component for a todo list"}'

# List projects
curl "http://localhost:8000/api/projects/"

# Get available models
curl "http://localhost:8000/api/generate/models"
```

## 🎯 Task Types

GENESIS AI automatically classifies your requests:

- **Creative UI**: Design beautiful interfaces and layouts
- **Code Generation**: Generate clean, maintainable code
- **Architecture**: Design scalable systems and patterns
- **Debugging**: Fix bugs and troubleshoot issues
- **Fast Simple**: Quick tasks using fast models
- **Multimodal**: Tasks involving images or visual content
- **3D Modeling**: Unity, Blender, and game development
- **Planning**: Project planning and task breakdown
- **Refactoring**: Code improvement and optimization

## 🤖 AI Model Routing

The smart router automatically selects the best model:

- **Claude**: Creative tasks, complex reasoning, architecture
- **GPT-4**: General coding, tool use, debugging
- **Gemini**: Multimodal tasks, image processing
- **Groq**: Fast inference for simple tasks

## 📁 Project Structure

```
genesis-ai/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Settings
│   │   ├── core/
│   │   │   └── router.py        # Smart routing logic
│   │   ├── models/              # AI model clients
│   │   ├── api/routes/          # API endpoints
│   │   └── schemas/             # Data models
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx             # Main dashboard
│   │   ├── components/          # React components
│   │   ├── hooks/               # Custom hooks
│   │   └── lib/                 # Utilities
│   └── package.json
└── sandbox/projects/             # Generated projects
```

## 🔌 API Endpoints

### Generation
- `POST /api/generate/` - Generate content
- `GET /api/generate/models` - List available models
- `GET /api/generate/task-types` - List task types
- `WebSocket /api/generate/ws` - Real-time updates

### Projects
- `GET /api/projects/` - List projects
- `POST /api/projects/` - Create project
- `GET /api/projects/{id}` - Get project details
- `GET /api/projects/{id}/files` - List project files

### External API
- `POST /api/external/generate` - Public generation endpoint
- `POST /api/external/keys` - Create API key
- `GET /api/external/usage` - Get usage stats

## 🛠️ Development

### Adding New AI Models

1. Create a client in `backend/app/models/`
2. Add to `SmartRouter` in `backend/app/core/router.py`
3. Update model preferences and task classification

### Custom Task Types

1. Add to `TaskType` enum in `router.py`
2. Update classification logic
3. Add model preferences

### Frontend Components

- Use Tailwind CSS for styling
- Follow the existing component patterns
- Add TypeScript types for props

## 📊 Monitoring

- Health check: `GET /health`
- Model status: `GET /api/generate/models`
- Usage statistics: Available through the dashboard

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter issues:

1. Check the API key configuration
2. Verify all services are running
3. Check browser console for errors
4. Review backend logs
5. Open an issue on GitHub

## 🎉 What's Next?

- [ ] Add more AI models (Llama, Cohere)
- [ ] Implement vector database for memory
- [ ] Add code execution sandbox
- [ ] Support for more frameworks
- [ ] Mobile app companion
- [ ] Team collaboration features

---

Built with ❤️ by the GENESIS AI team
