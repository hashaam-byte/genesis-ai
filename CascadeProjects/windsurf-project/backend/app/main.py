from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from app.config import settings
from app.api.routes import generate, projects, external

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

# Include API routes
app.include_router(generate.router, prefix="/api/generate", tags=["generate"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(external.router, prefix="/api/external", tags=["external"])

# Serve generated projects statically
if os.path.exists(settings.PROJECTS_DIR):
    app.mount("/projects", StaticFiles(directory=settings.PROJECTS_DIR), name="projects")


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
