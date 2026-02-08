from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class GenerationResponse(BaseModel):
    success: bool = Field(..., description="Whether generation was successful")
    content: Optional[str] = Field(None, description="Generated content")
    model: Optional[str] = Field(None, description="AI model used")
    task_type: Optional[str] = Field(None, description="Detected task type")
    quality_score: Optional[float] = Field(None, description="Quality score (0-1)")
    attempts: Optional[int] = Field(None, description="Number of attempts made")
    usage: Optional[Dict[str, Any]] = Field(None, description="Token usage information")
    error: Optional[str] = Field(None, description="Error message if failed")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ProjectResponse(BaseModel):
    id: str = Field(..., description="Project unique identifier")
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    framework: Optional[str] = Field(None, description="Target framework")
    status: str = Field(..., description="Project status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    file_count: int = Field(..., description="Number of files in project")
    last_activity: Optional[datetime] = Field(None, description="Last activity timestamp")


class FileResponse(BaseModel):
    path: str = Field(..., description="File path")
    name: str = Field(..., description="File name")
    size: int = Field(..., description="File size in bytes")
    type: str = Field(..., description="File type/extension")
    content: Optional[str] = Field(None, description="File content (if requested)")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class APIKeyResponse(BaseModel):
    key: str = Field(..., description="Generated API key")
    name: str = Field(..., description="API key name")
    permissions: List[str] = Field(..., description="Granted permissions")
    rate_limit: Optional[int] = Field(None, description="Rate limit per hour")
    created_at: datetime = Field(..., description="Creation timestamp")
    expires_at: Optional[datetime] = Field(None, description="Expiration timestamp")
    usage_count: int = Field(0, description="Number of times used")


class HealthResponse(BaseModel):
    status: str = Field(..., description="Service health status")
    version: str = Field(..., description="API version")
    models: Dict[str, bool] = Field(..., description="Available AI models status")
    uptime: float = Field(..., description="Service uptime in seconds")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
