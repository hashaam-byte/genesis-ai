import anthropic
from typing import Dict, Any, Optional
import asyncio
from app.config import settings


class ClaudeClient:
    def __init__(self):
        self.client = anthropic.AsyncAnthropic(
            api_key=settings.ANTHROPIC_API_KEY
        )
    
    async def generate(
        self,
        prompt: str,
        max_tokens: int = 4000,
        temperature: float = 0.7,
        model: str = "claude-3-sonnet-20240229"
    ) -> Dict[str, Any]:
        """Generate response using Claude"""
        try:
            response = await self.client.messages.create(
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
                "content": response.content[0].text,
                "model": model,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
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
        """Generate structured response using Claude"""
        structured_prompt = f"""
        {prompt}
        
        Please respond with valid JSON that matches this schema:
        {schema}
        
        Your response should be ONLY the JSON, no other text.
        """
        
        result = await self.generate(
            prompt=structured_prompt,
            max_tokens=max_tokens,
            temperature=0.3
        )
        
        if result["success"]:
            try:
                import json
                parsed_content = json.loads(result["content"])
                result["structured_data"] = parsed_content
            except json.JSONDecodeError:
                result["success"] = False
                result["error"] = "Failed to parse structured response"
        
        return result
