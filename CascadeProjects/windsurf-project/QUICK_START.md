# 🚀 GENESIS AI - Quick Start Guide

## 🎯 What We Built

GENESIS AI is a **hybrid orchestrator system** that intelligently routes tasks to the best AI model (Claude, GPT-4, Gemini, Groq) with automatic fallbacks.

## 📋 Current Status: ✅ COMPLETE MVP

The core system is fully implemented and ready to run:

### ✅ Backend (FastAPI)
- Smart routing logic with task classification
- AI model clients for Claude, OpenAI, Gemini, Groq
- REST API with WebSocket support
- Project management system
- External API with key management
- Quality scoring and fallback mechanisms

### ✅ Frontend (Next.js)
- Modern dashboard with Tailwind CSS
- Real-time generation progress
- Project file explorer
- Code viewer with syntax highlighting
- Model selector and task type options
- Error handling and user feedback

### ✅ Architecture
- Multi-model AI routing
- Intelligent task classification
- Automatic fallback system
- Project organization
- API exposure for external apps

## 🛠️ Setup Instructions

### 1. Environment Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

**Frontend:**
```bash
cd frontend
npm install
```

### 2. Add API Keys

Edit `backend/.env` and add at least one:
```env
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
GROQ_API_KEY=your_groq_key_here
```

### 3. Start Services

**Backend (Terminal 1):**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

### 4. Access the App

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🎮 How to Use

1. **Open the Dashboard**: Visit http://localhost:3000
2. **Enter a Prompt**: Describe what you want to create
3. **Optional**: Select a specific task type or AI model
4. **Generate**: Click "Generate" and watch the magic happen
5. **View Results**: See generated code, copy to clipboard, or save to projects

## 🧪 Test the System

Try these example prompts:

```
Create a modern React component for a todo list with TypeScript
Design a beautiful landing page with Tailwind CSS
Build a REST API with FastAPI for user management
Debug this Python function that's not working
Create a simple 3D scene with Three.js
```

## 🔧 Key Features Working

### Smart Routing
- Automatically detects task types (UI, code, debugging, etc.)
- Routes to optimal AI model based on task complexity
- Falls back to other models if primary fails
- Quality scoring to ensure good results

### Multi-Model Support
- **Claude**: Creative tasks, complex reasoning
- **GPT-4**: General coding, tool use
- **Gemini**: Multimodal tasks
- **Groq**: Fast inference

### Project Management
- Create and organize projects
- File explorer with syntax highlighting
- Save generated code to projects
- Track project history

### Real-time Updates
- WebSocket for live generation progress
- Quality indicators and model used
- Error handling with troubleshooting tips

## 📊 API Endpoints

### Generation
- `POST /api/generate/` - Generate content
- `GET /api/generate/models` - Check available models
- `WebSocket /api/generate/ws` - Real-time updates

### Projects
- `GET /api/projects/` - List projects
- `POST /api/projects/` - Create project
- `GET /api/projects/{id}/files` - List files

### External API
- `POST /api/external/generate` - Public endpoint
- `POST /api/external/keys` - Create API keys

## 🚀 Next Steps

The MVP is complete! Here's what you can do next:

### Immediate
1. **Add your API keys** and test generation
2. **Try different task types** to see routing in action
3. **Create projects** and organize generated code
4. **Explore the API** at http://localhost:8000/docs

### Advanced Features
- Add more AI models (Llama, Cohere)
- Implement vector database for memory
- Add code execution sandbox
- Support for more frameworks
- Team collaboration features

## 🎉 Success Metrics

✅ **Hybrid Intelligence**: Multiple AI models working together  
✅ **Smart Routing**: Automatic task classification and model selection  
✅ **Budget-Friendly**: Uses existing API keys, no training costs  
✅ **Full-Stack**: Complete frontend + backend + API  
✅ **Real-time**: WebSocket updates and live progress  
✅ **Project Management**: Organize and save generated work  
✅ **API Exposure**: Public API for external applications  

## 🆘 Troubleshooting

**Backend won't start:**
- Check Python 3.8+ is installed
- Install requirements: `pip install -r requirements.txt`
- Verify .env file exists with API keys

**Frontend errors:**
- Run `npm install` in frontend directory
- Check Node.js 18+ is installed
- Ensure backend is running on port 8000

**Generation fails:**
- Verify API keys are valid
- Check internet connection
- Try a simpler prompt
- Check backend logs for errors

---

**🎯 GENESIS AI is ready to transform your development workflow!**
