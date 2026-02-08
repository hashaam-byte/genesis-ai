from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
import os
import json
import uuid
from datetime import datetime
import aiofiles

from app.schemas.request import ProjectCreateRequest, ProjectUpdateRequest, FileOperationRequest
from app.schemas.response import ProjectResponse, FileResponse
from app.config import settings

router = APIRouter()

# In-memory project storage (replace with database in production)
projects_db: Dict[str, Dict[str, Any]] = {}


@router.post("/", response_model=ProjectResponse)
async def create_project(request: ProjectCreateRequest):
    """Create a new project"""
    project_id = str(uuid.uuid4())
    
    project = {
        "id": project_id,
        "name": request.name,
        "description": request.description,
        "framework": request.framework,
        "template": request.template,
        "status": "created",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "files": {},
        "last_activity": datetime.utcnow()
    }
    
    projects_db[project_id] = project
    
    # Create project directory
    project_dir = os.path.join(settings.PROJECTS_DIR, project_id)
    os.makedirs(project_dir, exist_ok=True)
    
    return ProjectResponse(
        id=project["id"],
        name=project["name"],
        description=project["description"],
        framework=project["framework"],
        status=project["status"],
        created_at=project["created_at"],
        updated_at=project["updated_at"],
        file_count=len(project["files"]),
        last_activity=project["last_activity"]
    )


@router.get("/", response_model=List[ProjectResponse])
async def list_projects():
    """List all projects"""
    projects = []
    
    for project_data in projects_db.values():
        projects.append(ProjectResponse(
            id=project_data["id"],
            name=project_data["name"],
            description=project_data["description"],
            framework=project_data["framework"],
            status=project_data["status"],
            created_at=project_data["created_at"],
            updated_at=project_data["updated_at"],
            file_count=len(project_data["files"]),
            last_activity=project_data["last_activity"]
        ))
    
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """Get project details"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects_db[project_id]
    
    return ProjectResponse(
        id=project["id"],
        name=project["name"],
        description=project["description"],
        framework=project["framework"],
        status=project["status"],
        created_at=project["created_at"],
        updated_at=project["updated_at"],
        file_count=len(project["files"]),
        last_activity=project["last_activity"]
    )


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: str, request: ProjectUpdateRequest):
    """Update project details"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects_db[project_id]
    
    if request.name is not None:
        project["name"] = request.name
    if request.description is not None:
        project["description"] = request.description
    if request.status is not None:
        project["status"] = request.status
    
    project["updated_at"] = datetime.utcnow()
    project["last_activity"] = datetime.utcnow()
    
    return ProjectResponse(
        id=project["id"],
        name=project["name"],
        description=project["description"],
        framework=project["framework"],
        status=project["status"],
        created_at=project["created_at"],
        updated_at=project["updated_at"],
        file_count=len(project["files"]),
        last_activity=project["last_activity"]
    )


@router.delete("/{project_id}")
async def delete_project(project_id: str):
    """Delete a project"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Remove from database
    del projects_db[project_id]
    
    # Remove project directory
    project_dir = os.path.join(settings.PROJECTS_DIR, project_id)
    try:
        import shutil
        shutil.rmtree(project_dir)
    except:
        pass  # Directory might not exist
    
    return {"message": "Project deleted successfully"}


@router.get("/{project_id}/files", response_model=List[FileResponse])
async def list_project_files(project_id: str):
    """List all files in a project"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects_db[project_id]
    files = []
    
    for file_path, file_data in project["files"].items():
        files.append(FileResponse(
            path=file_path,
            name=os.path.basename(file_path),
            size=len(file_data.get("content", "")),
            type=os.path.splitext(file_path)[1],
            content=None,  # Don't return content by default
            created_at=file_data["created_at"],
            updated_at=file_data["updated_at"]
        ))
    
    return files


@router.get("/{project_id}/files/{file_path:path}")
async def get_file_content(project_id: str, file_path: str):
    """Get file content"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects_db[project_id]
    
    if file_path not in project["files"]:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_data = project["files"][file_path]
    
    return {
        "path": file_path,
        "content": file_data["content"],
        "created_at": file_data["created_at"],
        "updated_at": file_data["updated_at"]
    }


@router.post("/{project_id}/files")
async def create_or_update_file(project_id: str, request: FileOperationRequest):
    """Create or update a file in a project"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects_db[project_id]
    
    file_data = {
        "content": request.content or "",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    if request.operation == "create":
        if request.file_path in project["files"]:
            raise HTTPException(status_code=409, detail="File already exists")
        
        file_data["created_at"] = datetime.utcnow()
        project["files"][request.file_path] = file_data
        
    elif request.operation == "update":
        if request.file_path not in project["files"]:
            raise HTTPException(status_code=404, detail="File not found")
        
        file_data["created_at"] = project["files"][request.file_path]["created_at"]
        file_data["updated_at"] = datetime.utcnow()
        project["files"][request.file_path] = file_data
        
    elif request.operation == "delete":
        if request.file_path not in project["files"]:
            raise HTTPException(status_code=404, detail="File not found")
        
        del project["files"][request.file_path]
        
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")
    
    # Update project metadata
    project["updated_at"] = datetime.utcnow()
    project["last_activity"] = datetime.utcnow()
    
    # Write to file system
    project_dir = os.path.join(settings.PROJECTS_DIR, project_id)
    os.makedirs(project_dir, exist_ok=True)
    
    full_path = os.path.join(project_dir, request.file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    if request.operation != "delete":
        async with aiofiles.open(full_path, 'w', encoding='utf-8') as f:
            await f.write(request.content or "")
    else:
        try:
            os.remove(full_path)
        except:
            pass
    
    return {"message": f"File {request.operation}d successfully"}


@router.delete("/{project_id}/files/{file_path:path}")
async def delete_file(project_id: str, file_path: str):
    """Delete a file from a project"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects_db[project_id]
    
    if file_path not in project["files"]:
        raise HTTPException(status_code=404, detail="File not found")
    
    del project["files"][file_path]
    
    # Update project metadata
    project["updated_at"] = datetime.utcnow()
    project["last_activity"] = datetime.utcnow()
    
    # Remove from file system
    project_dir = os.path.join(settings.PROJECTS_DIR, project_id)
    full_path = os.path.join(project_dir, file_path)
    
    try:
        os.remove(full_path)
    except:
        pass
    
    return {"message": "File deleted successfully"}
