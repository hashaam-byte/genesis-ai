from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Dict, Any, List
import secrets
import hashlib
from datetime import datetime, timedelta
import json

from app.schemas.request import APIKeyRequest, GenerationRequest
from app.schemas.response import APIKeyResponse, GenerationResponse
from app.core.router import SmartRouter

router = APIRouter()
smart_router = SmartRouter()

# In-memory API key storage (replace with database in production)
api_keys_db: Dict[str, Dict[str, Any]] = {}


def verify_api_key(api_key: str = Header(None, alias="X-API-Key")):
    """Verify API key and return key data"""
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    
    if key_hash not in api_keys_db:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    key_data = api_keys_db[key_hash]
    
    # Check if key is expired
    if key_data.get("expires_at") and key_data["expires_at"] < datetime.utcnow():
        raise HTTPException(status_code=401, detail="API key expired")
    
    # Check rate limit
    current_hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    if key_data["last_reset"] < current_hour:
        key_data["usage_count"] = 0
        key_data["last_reset"] = current_hour
    
    if key_data["rate_limit"] and key_data["usage_count"] >= key_data["rate_limit"]:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    # Update usage
    key_data["usage_count"] += 1
    key_data["last_used"] = datetime.utcnow()
    
    return key_data


@router.post("/keys", response_model=APIKeyResponse)
async def create_api_key(request: APIKeyRequest):
    """Create a new API key"""
    # Generate secure API key
    api_key = f"genesis_{secrets.token_urlsafe(32)}"
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    
    # Set expiration (default 1 year)
    expires_at = datetime.utcnow() + timedelta(days=365)
    
    key_data = {
        "key": api_key,
        "name": request.name,
        "permissions": request.permissions,
        "rate_limit": request.rate_limit,
        "created_at": datetime.utcnow(),
        "expires_at": expires_at,
        "usage_count": 0,
        "last_used": None,
        "last_reset": datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    }
    
    api_keys_db[key_hash] = key_data
    
    return APIKeyResponse(
        key=api_key,
        name=key_data["name"],
        permissions=key_data["permissions"],
        rate_limit=key_data["rate_limit"],
        created_at=key_data["created_at"],
        expires_at=key_data["expires_at"],
        usage_count=key_data["usage_count"]
    )


@router.get("/keys")
async def list_api_keys():
    """List all API keys (admin endpoint)"""
    keys = []
    
    for key_hash, key_data in api_keys_db.items():
        # Don't return the actual key hash
        keys.append({
            "name": key_data["name"],
            "permissions": key_data["permissions"],
            "rate_limit": key_data["rate_limit"],
            "created_at": key_data["created_at"],
            "expires_at": key_data["expires_at"],
            "usage_count": key_data["usage_count"],
            "last_used": key_data["last_used"]
        })
    
    return {"keys": keys}


@router.delete("/keys/{key_name}")
async def delete_api_key(key_name: str):
    """Delete an API key"""
    keys_to_delete = []
    
    for key_hash, key_data in api_keys_db.items():
        if key_data["name"] == key_name:
            keys_to_delete.append(key_hash)
    
    if not keys_to_delete:
        raise HTTPException(status_code=404, detail="API key not found")
    
    for key_hash in keys_to_delete:
        del api_keys_db[key_hash]
    
    return {"message": "API key deleted successfully"}


@router.post("/generate", response_model=GenerationResponse)
async def external_generate(
    request: GenerationRequest,
    key_data: Dict[str, Any] = Depends(verify_api_key)
):
    """Generate content using API key authentication"""
    
    # Check permissions
    if "generate" not in key_data["permissions"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    try:
        # Convert task type if provided
        task_type = None
        if request.task_type:
            from app.core.router import TaskType
            task_type = TaskType(request.task_type.value)
        
        # Route the task to the best model
        result = await smart_router.route_task(
            prompt=request.prompt,
            task_type=task_type,
            max_attempts=2
        )
        
        # Add API usage metadata
        result["api_key"] = key_data["name"]
        result["generated_at"] = datetime.utcnow().isoformat()
        
        return GenerationResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usage")
async def get_usage_stats(key_data: Dict[str, Any] = Depends(verify_api_key)):
    """Get usage statistics for API key"""
    current_hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    
    # Reset counter if needed
    if key_data["last_reset"] < current_hour:
        key_data["usage_count"] = 0
        key_data["last_reset"] = current_hour
    
    return {
        "api_key": key_data["name"],
        "usage_count": key_data["usage_count"],
        "rate_limit": key_data["rate_limit"],
        "remaining": (
            key_data["rate_limit"] - key_data["usage_count"]
            if key_data["rate_limit"] else None
        ),
        "last_used": key_data["last_used"],
        "created_at": key_data["created_at"],
        "expires_at": key_data["expires_at"]
    }


@router.get("/models")
async def get_available_models_external(key_data: Dict[str, Any] = Depends(verify_api_key)):
    """Get available models for external API users"""
    
    # Check permissions
    if "read" not in key_data["permissions"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    models_status = {}
    
    # Check Claude
    try:
        claude_client = smart_router.claude
        if claude_client.client.api_key:
            models_status["claude"] = {
                "available": True,
                "description": "Creative tasks, complex reasoning"
            }
        else:
            models_status["claude"] = {"available": False}
    except:
        models_status["claude"] = {"available": False}
    
    # Check OpenAI
    try:
        openai_client = smart_router.openai
        if openai_client.client.api_key:
            models_status["openai"] = {
                "available": True,
                "description": "General tasks, tool use"
            }
        else:
            models_status["openai"] = {"available": False}
    except:
        models_status["openai"] = {"available": False}
    
    # Check Gemini
    try:
        gemini_client = smart_router.gemini
        if gemini_client.model:
            models_status["gemini"] = {
                "available": True,
                "description": "Multimodal tasks"
            }
        else:
            models_status["gemini"] = {"available": False}
    except:
        models_status["gemini"] = {"available": False}
    
    # Check Groq
    try:
        groq_client = smart_router.groq
        if groq_client.client:
            models_status["groq"] = {
                "available": True,
                "description": "Fast inference"
            }
        else:
            models_status["groq"] = {"available": False}
    except:
        models_status["groq"] = {"available": False}
    
    return {
        "models": models_status,
        "total_available": sum(1 for model in models_status.values() if model.get("available", False))
    }
