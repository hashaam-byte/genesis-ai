from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum


class TaskTypeEnum(str, Enum):
    CREATIVE_UI = "creative_ui"
    CODE_GENERATION = "code_generation"
    ARCHITECTURE = "architecture"
    DEBUGGING = "debugging"
    FAST_SIMPLE = "fast_simple"
    MULTIMODAL = "multimodal"
    MODELING_3D = "3d_modeling"
    PLANNING = "planning"
    REFACTORING = "refactoring"


class GenerationRequest(BaseModel):
    prompt: str = Field(..., description="The task prompt for AI generation")
    task_type: Optional[TaskTypeEnum] = Field(None, description="Specific task type (auto-detected if not provided)")
    max_tokens: Optional[int] = Field(4000, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(0.7, description="Generation temperature")
    preferred_model: Optional[str] = Field(None, description="Preferred AI model (auto-selected if not provided)")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for generation")
    files: Optional[List[Dict[str, Any]]] = Field(None, description="Existing files to reference")


class ProjectCreateRequest(BaseModel):
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    framework: Optional[str] = Field(None, description="Target framework (react, vue, nextjs, etc.)")
    template: Optional[str] = Field(None, description="Starting template")


class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, description="New project name")
    description: Optional[str] = Field(None, description="New project description")
    status: Optional[str] = Field(None, description="Project status")


class FileOperationRequest(BaseModel):
    project_id: str = Field(..., description="Project ID")
    file_path: str = Field(..., description="File path within project")
    content: Optional[str] = Field(None, description="File content (for create/update)")
    operation: str = Field(..., description="Operation: create, update, delete")


class APIKeyRequest(BaseModel):
    name: str = Field(..., description="API key name/identifier")
    permissions: List[str] = Field(..., description="List of permissions")
    rate_limit: Optional[int] = Field(None, description="Rate limit per hour")
