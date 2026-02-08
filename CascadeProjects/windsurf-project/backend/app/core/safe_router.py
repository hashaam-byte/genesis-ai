from typing import Dict, Any, Optional
import asyncio
from enum import Enum

class TaskType(Enum):
    CREATIVE_UI = "creative_ui"
    CODE_GENERATION = "code_generation"
    ARCHITECTURE = "architecture"
    DEBUGGING = "debugging"
    FAST_SIMPLE = "fast_simple"
    MULTIMODAL = "multimodal"
    MODELING_3D = "3d_modeling"
    PLANNING = "planning"
    REFACTORING = "refactoring"


class SafeSmartRouter:
    """Safe router that works without API keys for testing"""
    
    def __init__(self):
        self.models_available = {
            "claude": False,
            "openai": False,
            "gemini": False,
            "groq": False
        }
    
    def classify_task(self, prompt: str) -> TaskType:
        """Classify the task type based on the prompt"""
        prompt_lower = prompt.lower()
        
        # Check for creative/UI tasks
        if any(keyword in prompt_lower for keyword in [
            "design", "ui", "ux", "interface", "layout", "styling", 
            "beautiful", "modern", "responsive", "frontend"
        ]):
            return TaskType.CREATIVE_UI
        
        # Check for 3D/modeling tasks
        if any(keyword in prompt_lower for keyword in [
            "3d", "blender", "unity", "model", "animation", "game"
        ]):
            return TaskType.MODELING_3D
        
        # Check for multimodal tasks
        if any(keyword in prompt_lower for keyword in [
            "image", "picture", "visual", "screenshot", "diagram"
        ]):
            return TaskType.MULTIMODAL
        
        # Check for architecture tasks
        if any(keyword in prompt_lower for keyword in [
            "architecture", "structure", "design pattern", "scalable",
            "system design", "database schema"
        ]):
            return TaskType.ARCHITECTURE
        
        # Check for debugging tasks
        if any(keyword in prompt_lower for keyword in [
            "debug", "fix", "error", "bug", "issue", "problem",
            "not working", "broken"
        ]):
            return TaskType.DEBUGGING
        
        # Check for planning tasks
        if any(keyword in prompt_lower for keyword in [
            "plan", "breakdown", "steps", "how to", "implement",
            "build", "create project"
        ]):
            return TaskType.PLANNING
        
        # Check for refactoring tasks
        if any(keyword in prompt_lower for keyword in [
            "refactor", "improve", "optimize", "clean", "rewrite"
        ]):
            return TaskType.REFACTORING
        
        # Check for simple/fast tasks
        if len(prompt.split()) < 20 and any(keyword in prompt_lower for keyword in [
            "simple", "basic", "quick", "small"
        ]):
            return TaskType.FAST_SIMPLE
        
        # Default to code generation
        return TaskType.CODE_GENERATION
    
    async def route_task(
        self, 
        prompt: str, 
        task_type: Optional[TaskType] = None,
        max_attempts: int = 2
    ) -> Dict[str, Any]:
        """Mock routing that returns demo response"""
        
        # Classify task if not provided
        if not task_type:
            task_type = self.classify_task(prompt)
        
        # Return mock response for testing
        mock_response = self._generate_mock_response(prompt, task_type)
        
        return {
            "success": True,
            "content": mock_response,
            "model": "demo",
            "task_type": task_type.value,
            "quality_score": 0.85,
            "attempts": 1,
            "usage": {"demo": True},
            "note": "This is a demo response. Configure API keys to get real AI responses."
        }
    
    def _generate_mock_response(self, prompt: str, task_type: TaskType) -> str:
        """Generate mock response based on task type"""
        
        if task_type == TaskType.CODE_GENERATION:
            return f"""// Generated code for: {prompt}
function generateResponse() {{
    console.log("This is a demo response");
    return "Configure your API keys to get real AI-generated code";
}}

export default generateResponse;"""
        
        elif task_type == TaskType.CREATIVE_UI:
            return f"""<!-- Generated UI for: {prompt} -->
<div className="p-6 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
    <h2 className="text-2xl font-bold text-white mb-4">Demo Component</h2>
    <p className="text-white opacity-90">
        This is a demo UI component. Add your API keys to get real AI-generated designs.
    </p>
    <button className="mt-4 px-4 py-2 bg-white text-blue-600 rounded-md hover:bg-gray-100">
        Configure API Keys
    </button>
</div>"""
        
        elif task_type == TaskType.ARCHITECTURE:
            return f"""# Architecture for: {prompt}

## System Design (Demo)

### Components
- **Frontend**: React/Next.js (Demo)
- **Backend**: FastAPI (Demo)  
- **Database**: PostgreSQL (Demo)
- **AI Models**: Claude, GPT-4, Gemini, Groq (Configure API keys)

### Features
- Smart routing system
- Multi-model fallback
- Real-time updates
- Project management

*This is demo architecture. Configure API keys for real AI-generated designs.*"""
        
        else:
            return f"""# Generated Response for: {prompt}

This is a demo response from GENESIS AI.

## Task Type: {task_type.value}

To get real AI-generated content:
1. Open `backend/.env`
2. Add your API keys (Claude, OpenAI, Gemini, or Groq)
3. Restart the backend server

## Current Status
- Backend: Running (Demo Mode)
- Frontend: Connected
- AI Models: Not configured

The system is working - just add API keys to enable real AI generation!"""

# Create safe router instance
safe_router = SafeSmartRouter()
