import openai
from typing import Dict, Any, Optional
import asyncio
from app.config import settings


class OpenAIClient:
    def __init__(self):
        self.client = openai.AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY
        )
    
    async def generate(
        self,
        prompt: str,
        max_tokens: int = 4000,
        temperature: float = 0.7,
        model: str = "gpt-4-turbo-preview"
    ) -> Dict[str, Any]:
        """Generate response using OpenAI GPT"""
        try:
            response = await self.client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return {
                "success": True,
                "content": response.choices[0].message.content,
                "model": model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": model
            }
    
    async def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        max_tokens: int = 4000
    ) -> Dict[str, Any]:
        """Generate structured response using OpenAI with function calling"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                max_tokens=max_tokens,
                temperature=0.3,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                functions=[
                    {
                        "name": "generate_response",
                        "description": "Generate structured response",
                        "parameters": schema
                    }
                ],
                function_call={"name": "generate_response"}
            )
            
            function_call = response.choices[0].message.function_call
            if function_call:
                import json
                structured_data = json.loads(function_call.arguments)
                
                return {
                    "success": True,
                    "content": response.choices[0].message.content,
                    "structured_data": structured_data,
                    "model": "gpt-4-turbo-preview",
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "No function call in response",
                    "model": "gpt-4-turbo-preview"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": "gpt-4-turbo-preview"
            }
    
    async def generate_with_tools(
        self,
        prompt: str,
        tools: list,
        max_tokens: int = 4000
    ) -> Dict[str, Any]:
        """Generate response with tool calling capabilities"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                max_tokens=max_tokens,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                tools=tools,
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            
            return {
                "success": True,
                "content": message.content,
                "tool_calls": message.tool_calls,
                "model": "gpt-4-turbo-preview",
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": "gpt-4-turbo-preview"
            }
