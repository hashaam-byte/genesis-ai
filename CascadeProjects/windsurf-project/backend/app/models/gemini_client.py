import google.generativeai as genai
from typing import Dict, Any, Optional
import asyncio
from app.config import settings


class GeminiClient:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    async def generate(
        self,
        prompt: str,
        max_tokens: int = 4000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Generate response using Gemini"""
        if not self.model:
            return {
                "success": False,
                "error": "Gemini API key not configured",
                "model": "gemini-pro"
            }
        
        try:
            # Run in thread pool since Gemini doesn't have async support
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=max_tokens,
                        temperature=temperature
                    )
                )
            )
            
            return {
                "success": True,
                "content": response.text,
                "model": "gemini-pro",
                "usage": {}  # Gemini doesn't provide token usage
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": "gemini-pro"
            }
    
    async def generate_multimodal(
        self,
        prompt: str,
        image_data: bytes,
        image_mime_type: str = "image/jpeg"
    ) -> Dict[str, Any]:
        """Generate response using Gemini with image input"""
        if not self.model:
            return {
                "success": False,
                "error": "Gemini API key not configured",
                "model": "gemini-pro-vision"
            }
        
        try:
            import PIL.Image
            import io
            
            # Create PIL Image from bytes
            image = PIL.Image.open(io.BytesIO(image_data))
            
            vision_model = genai.GenerativeModel('gemini-pro-vision')
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: vision_model.generate_content([prompt, image])
            )
            
            return {
                "success": True,
                "content": response.text,
                "model": "gemini-pro-vision",
                "usage": {}
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": "gemini-pro-vision"
            }
