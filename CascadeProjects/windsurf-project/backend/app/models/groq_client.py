from groq import Groq
from typing import Dict, Any, Optional
import asyncio
from app.config import settings


class GroqClient:
    def __init__(self):
        if settings.GROQ_API_KEY:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
        else:
            self.client = None
    
    async def generate(
        self,
        prompt: str,
        max_tokens: int = 4000,
        temperature: float = 0.7,
        model: str = "mixtral-8x7b-32768"
    ) -> Dict[str, Any]:
        """Generate response using Groq (fast inference)"""
        if not self.client:
            return {
                "success": False,
                "error": "Groq API key not configured",
                "model": model
            }
        
        try:
            # Run in thread pool since Groq doesn't have async support
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
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
    
    async def generate_fast(
        self,
        prompt: str,
        model: str = "llama2-70b-4096"
    ) -> Dict[str, Any]:
        """Generate fast response using Groq's fastest models"""
        return await self.generate(
            prompt=prompt,
            max_tokens=1000,
            temperature=0.5,
            model=model
        )
