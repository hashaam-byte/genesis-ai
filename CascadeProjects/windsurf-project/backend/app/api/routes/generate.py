from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import Dict, Any, List
import asyncio
import json
import uuid
from datetime import datetime

from app.schemas.request import GenerationRequest
from app.schemas.response import GenerationResponse
from app.core.router import SmartRouter

router = APIRouter()
smart_router = SmartRouter()

# WebSocket connections for real-time updates
active_connections: List[WebSocket] = []


@router.post("/", response_model=GenerationResponse)
async def generate_content(request: GenerationRequest):
    """Generate content using AI models with smart routing"""
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
        
        # Broadcast update to WebSocket clients
        await broadcast_update({
            "type": "generation_complete",
            "data": {
                "success": result["success"],
                "model": result.get("model"),
                "task_type": result.get("task_type"),
                "quality_score": result.get("quality_score"),
                "timestamp": datetime.utcnow().isoformat()
            }
        })
        
        return GenerationResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def generate_stream(request: GenerationRequest):
    """Generate content with streaming response"""
    async def generate():
        try:
            # Send initial status
            yield f"data: {json.dumps({'type': 'start', 'message': 'Starting generation...'})}\n\n"
            
            # Convert task type if provided
            task_type = None
            if request.task_type:
                from app.core.router import TaskType
                task_type = TaskType(request.task_type.value)
            
            # Route the task
            result = await smart_router.route_task(
                prompt=request.prompt,
                task_type=task_type,
                max_attempts=2
            )
            
            # Send result
            yield f"data: {json.dumps({'type': 'complete', 'data': result})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
    
    return generate()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time generation updates"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "generate":
                # Handle generation request
                request_data = message.get("data", {})
                request = GenerationRequest(**request_data)
                
                # Send status update
                await websocket.send_text(json.dumps({
                    "type": "status",
                    "message": "Processing your request..."
                }))
                
                # Generate content
                task_type = None
                if request.task_type:
                    from app.core.router import TaskType
                    task_type = TaskType(request.task_type.value)
                
                result = await smart_router.route_task(
                    prompt=request.prompt,
                    task_type=task_type,
                    max_attempts=2
                )
                
                # Send result
                await websocket.send_text(json.dumps({
                    "type": "result",
                    "data": result
                }))
            
            elif message.get("type") == "ping":
                # Respond to ping
                await websocket.send_text(json.dumps({"type": "pong"}))
                
    except WebSocketDisconnect:
        active_connections.remove(websocket)


async def broadcast_update(message: Dict[str, Any]):
    """Broadcast message to all connected WebSocket clients"""
    if active_connections:
        message_str = json.dumps(message)
        disconnected = []
        
        for connection in active_connections:
            try:
                await connection.send_text(message_str)
            except:
                disconnected.append(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            if conn in active_connections:
                active_connections.remove(conn)


@router.get("/models")
async def get_available_models():
    """Get list of available AI models and their status"""
    models_status = {}
    
    # Check Claude
    try:
        claude_client = smart_router.claude
        if claude_client.client.api_key:
            models_status["claude"] = True
        else:
            models_status["claude"] = False
    except:
        models_status["claude"] = False
    
    # Check OpenAI
    try:
        openai_client = smart_router.openai
        if openai_client.client.api_key:
            models_status["openai"] = True
        else:
            models_status["openai"] = False
    except:
        models_status["openai"] = False
    
    # Check Gemini
    try:
        gemini_client = smart_router.gemini
        if gemini_client.model:
            models_status["gemini"] = True
        else:
            models_status["gemini"] = False
    except:
        models_status["gemini"] = False
    
    # Check Groq
    try:
        groq_client = smart_router.groq
        if groq_client.client:
            models_status["groq"] = True
        else:
            models_status["groq"] = False
    except:
        models_status["groq"] = False
    
    return {
        "models": models_status,
        "total_available": sum(models_status.values()),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/task-types")
async def get_task_types():
    """Get list of supported task types"""
    from app.core.router import TaskType
    
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
