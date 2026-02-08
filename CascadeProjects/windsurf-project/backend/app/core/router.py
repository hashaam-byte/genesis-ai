from typing import Dict, Any, List, Optional
import re
import asyncio
from enum import Enum

from app.models.claude_client import ClaudeClient
from app.models.openai_client import OpenAIClient
from app.models.gemini_client import GeminiClient
from app.models.groq_client import GroqClient


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


class SmartRouter:
    def __init__(self):
        self.claude = ClaudeClient()
        self.openai = OpenAIClient()
        self.gemini = GeminiClient()
        self.groq = GroqClient()
        
        # Model preferences for different task types
        self.model_preferences = {
            TaskType.CREATIVE_UI: ["claude", "gpt-4", "gemini"],
            TaskType.CODE_GENERATION: ["claude", "gpt-4", "gemini"],
            TaskType.ARCHITECTURE: ["claude", "gpt-4"],
            TaskType.DEBUGGING: ["gpt-4", "claude"],
            TaskType.FAST_SIMPLE: ["groq", "claude"],
            TaskType.MULTIMODAL: ["gemini", "gpt-4"],
            TaskType.MODELING_3D: ["claude", "gpt-4"],
            TaskType.PLANNING: ["claude", "gpt-4"],
            TaskType.REFACTORING: ["claude", "gpt-4"]
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
    
    def quality_check(self, result: Dict[str, Any]) -> float:
        """Simple quality check for generated content"""
        if not result.get("success"):
            return 0.0
        
        content = result.get("content", "")
        
        # Basic quality metrics
        quality_score = 0.5  # Base score
        
        # Length check (not too short, not too long)
        if 100 <= len(content) <= 2000:
            quality_score += 0.2
        
        # Code block presence
        if "```" in content:
            quality_score += 0.2
        
        # Explanation presence
        if any(word in content.lower() for word in ["explain", "because", "reason", "here's"]):
            quality_score += 0.1
        
        return min(quality_score, 1.0)
    
    async def route_task(
        self, 
        prompt: str, 
        task_type: Optional[TaskType] = None,
        max_attempts: int = 2
    ) -> Dict[str, Any]:
        """Route task to the best available model with fallback"""
        
        # Classify task if not provided
        if not task_type:
            task_type = self.classify_task(prompt)
        
        # Get preferred models for this task type
        preferred_models = self.model_preferences.get(task_type, ["claude", "gpt-4"])
        
        last_error = None
        
        for attempt in range(max_attempts):
            for model_name in preferred_models:
                try:
                    result = await self._call_model(model_name, prompt, task_type)
                    
                    if result["success"]:
                        quality = self.quality_check(result)
                        
                        # If quality is good, return result
                        if quality >= 0.7:
                            return {
                                "success": True,
                                "content": result["content"],
                                "model": result["model"],
                                "task_type": task_type.value,
                                "quality_score": quality,
                                "attempts": attempt + 1,
                                "usage": result.get("usage", {})
                            }
                        # If quality is low but we have attempts left, try next model
                        elif attempt < max_attempts - 1:
                            continue
                        else:
                            # Last attempt, return what we have
                            return {
                                "success": True,
                                "content": result["content"],
                                "model": result["model"],
                                "task_type": task_type.value,
                                "quality_score": quality,
                                "attempts": attempt + 1,
                                "usage": result.get("usage", {})
                            }
                    else:
                        last_error = result.get("error", "Unknown error")
                        
                except Exception as e:
                    last_error = str(e)
                    continue
        
        # All models failed
        return {
            "success": False,
            "error": f"All models failed. Last error: {last_error}",
            "task_type": task_type.value,
            "attempts": max_attempts
        }
    
    async def _call_model(
        self, 
        model_name: str, 
        prompt: str, 
        task_type: TaskType
    ) -> Dict[str, Any]:
        """Call the specific model"""
        
        # Adjust prompt based on task type
        enhanced_prompt = self._enhance_prompt(prompt, task_type)
        
        if model_name == "claude":
            return await self.claude.generate(enhanced_prompt)
        elif model_name == "gpt-4":
            return await self.openai.generate(enhanced_prompt)
        elif model_name == "gemini":
            return await self.gemini.generate(enhanced_prompt)
        elif model_name == "groq":
            return await self.groq.generate(enhanced_prompt)
        else:
            raise ValueError(f"Unknown model: {model_name}")
    
    def _enhance_prompt(self, prompt: str, task_type: TaskType) -> str:
        """Enhance prompt based on task type"""
        
        enhancers = {
            TaskType.CREATIVE_UI: """
            Focus on creating modern, beautiful, and responsive UI/UX designs.
            Use contemporary design patterns and best practices.
            Include accessibility considerations.
            """,
            
            TaskType.CODE_GENERATION: """
            Write clean, maintainable, and well-documented code.
            Follow best practices and design patterns.
            Include error handling where appropriate.
            """,
            
            TaskType.ARCHITECTURE: """
            Focus on scalable, maintainable architecture.
            Consider performance, security, and extensibility.
            Explain your architectural decisions.
            """,
            
            TaskType.DEBUGGING: """
            Analyze the problem systematically.
            Provide clear explanations of the root cause.
            Offer multiple solutions when applicable.
            """,
            
            TaskType.PLANNING: """
            Break down the task into clear, actionable steps.
            Consider dependencies and potential challenges.
            Provide a realistic implementation roadmap.
            """
        }
        
        enhancer = enhancers.get(task_type, "")
        return f"{prompt}\n\n{enhancer}"
