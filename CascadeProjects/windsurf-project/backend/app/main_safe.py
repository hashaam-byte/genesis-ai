from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import uvicorn

from app.config import settings
from app.core.safe_router import safe_router

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock API routes using safe router
@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} (Safe Mode)",
        "version": settings.VERSION,
        "status": "running",
        "mode": "demo - configure API keys for full functionality"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}

@app.post("/api/generate/")
async def generate_content(request: dict):
    """Generate content using safe demo router"""
    try:
        prompt = request.get("prompt", "")
        task_type = request.get("task_type")
        
        result = await safe_router.route_task(
            prompt=prompt,
            task_type=None,  # Let router classify
            max_attempts=1
        )
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "content": "Demo error - configure API keys for full functionality"
        }

@app.get("/api/generate/models")
async def get_available_models():
    """Get list of available AI models and their status"""
    return {
        "models": {
            "claude": {"available": False, "description": "Creative tasks, complex reasoning"},
            "openai": {"available": False, "description": "General tasks, tool use"},
            "gemini": {"available": False, "description": "Multimodal tasks"},
            "groq": {"available": False, "description": "Fast inference"}
        },
        "total_available": 0,
        "message": "Configure API keys in .env to enable models",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/api/generate/task-types")
async def get_task_types():
    """Get list of supported task types"""
    from app.core.safe_router import TaskType
    
    return {
        "task_types": [task_type.value for task_type in TaskType],
        "descriptions": {
            "creative_ui": "UI/UX design and frontend development",
            "code_generation": "General code generation and programming",
            "architecture": "System architecture and design patterns",
            "debugging": "Bug fixing and troubleshooting",
            "fast_simple": "Quick, simple tasks using fast models",
            "multimodal": "Tasks involving images or visual content",
            "3d_modeling": "3D modeling, Unity, and Blender tasks",
            "planning": "Project planning and task breakdown",
            "refactoring": "Code improvement and optimization"
        }
    }

@app.get("/api/projects/")
async def list_projects():
    """List all projects (mock)"""
    return []

@app.post("/api/projects/")
async def create_project(request: dict):
    """Create a new project (mock)"""
    return {
        "id": "demo-project-id",
        "name": request.get("name", "Demo Project"),
        "description": request.get("description", ""),
        "status": "created",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "file_count": 0,
        "note": "Demo project - configure API keys for full functionality"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main_safe:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
