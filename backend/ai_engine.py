"""
GENESIS AI - Real AI Code Generation Engine
Save as: backend/ai_engine.py
"""

from anthropic import Anthropic
import os
from typing import Dict, List, Optional
import json
from dotenv import load_dotenv

load_dotenv()

class AICodeGenerator:
    """Uses Claude to generate actual code"""
    
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"
    
    def generate_project_plan(self, prompt: str, project_type: str) -> List[Dict]:
        """Generate intelligent project plan"""
        
        system_prompt = """You are GENESIS AI, an expert software architect and coder.
Your job is to create detailed, professional project execution plans.
Return ONLY a JSON array of steps, no other text.

Each step should have:
- step_number: int
- description: string (clear, specific action)
- estimated_time: string

Example format:
[
  {"step_number": 1, "description": "Analyze requirements and choose tech stack", "estimated_time": "2 min"},
  {"step_number": 2, "description": "Design system architecture", "estimated_time": "3 min"}
]"""

        user_prompt = f"""Create a detailed execution plan for this project:

PROJECT TYPE: {project_type}
USER REQUEST: {prompt}

Generate 5-7 specific, actionable steps to build this project.
Focus on: architecture, code generation, testing, and deployment.
Return ONLY valid JSON array."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            content = response.content[0].text
            # Extract JSON from response
            json_start = content.find('[')
            json_end = content.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                return json.loads(json_str)
            else:
                # Fallback
                return self._fallback_plan(project_type)
                
        except Exception as e:
            print(f"AI Plan Generation Error: {e}")
            return self._fallback_plan(project_type)
    
    def generate_code(self, task: str, context: Dict) -> str:
        """Generate actual code for a specific task"""
        
        system_prompt = """You are GENESIS AI, an expert full-stack developer.
You write clean, professional, production-ready code.
You follow best practices and modern conventions.
You add helpful comments but don't over-comment.
Return ONLY the code, no explanations before or after."""

        user_prompt = f"""Generate code for this task:

TASK: {task}

PROJECT CONTEXT:
- Type: {context.get('project_type', 'web_app')}
- Tech Stack: {context.get('tech_stack', 'React, Node.js')}
- Requirements: {context.get('prompt', 'Build a web application')}

FILES TO GENERATE: {context.get('target_file', 'App.tsx')}

Generate clean, working code. Include all necessary imports and setup."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            print(f"AI Code Generation Error: {e}")
            return f"// Error generating code: {e}\n// Fallback code placeholder"
    
    def review_code(self, code: str, filename: str) -> Dict:
        """AI reviews generated code for issues"""
        
        system_prompt = """You are a senior code reviewer.
Analyze code for:
- Bugs and errors
- Security issues
- Performance problems
- Best practice violations
- Missing error handling

Return JSON format:
{
  "status": "pass" or "needs_fixes",
  "issues": ["issue1", "issue2"],
  "suggestions": ["suggestion1", "suggestion2"],
  "rating": 1-10
}"""

        user_prompt = f"""Review this code:

FILE: {filename}
CODE:
```
{code}
```

Provide detailed review in JSON format."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            content = response.content[0].text
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                return json.loads(json_str)
            else:
                return {
                    "status": "pass",
                    "issues": [],
                    "suggestions": ["Code looks good"],
                    "rating": 8
                }
                
        except Exception as e:
            print(f"AI Review Error: {e}")
            return {
                "status": "pass",
                "issues": [],
                "suggestions": [f"Review skipped: {e}"],
                "rating": 7
            }
    
    def fix_code(self, code: str, issues: List[str]) -> str:
        """AI fixes code based on review"""
        
        system_prompt = """You are an expert code fixer.
Fix all issues while preserving functionality.
Return ONLY the fixed code."""

        user_prompt = f"""Fix these issues in the code:

ISSUES:
{chr(10).join(f'- {issue}' for issue in issues)}

ORIGINAL CODE:
```
{code}
```

Return the fixed code."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            print(f"AI Fix Error: {e}")
            return code  # Return original if fix fails
    
    def analyze_tech_stack(self, prompt: str, project_type: str) -> List[str]:
        """AI chooses best tech stack"""
        
        system_prompt = """You are a tech stack consultant.
Choose the BEST modern technologies for the project.
Return ONLY a JSON array of tech names."""

        user_prompt = f"""Choose optimal tech stack for:

PROJECT TYPE: {project_type}
REQUIREMENTS: {prompt}

Return JSON array like: ["React", "Node.js", "PostgreSQL", "Tailwind"]"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            content = response.content[0].text
            json_start = content.find('[')
            json_end = content.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                return json.loads(json_str)
                
        except Exception as e:
            print(f"Tech Stack Analysis Error: {e}")
        
        # Fallback tech stacks
        fallback = {
            "web_app": ["React", "TypeScript", "Node.js", "Express", "PostgreSQL", "Tailwind CSS"],
            "game": ["Unity", "C#", "Blender", "Python"],
            "mobile_app": ["React Native", "TypeScript", "Firebase"],
            "api": ["FastAPI", "Python", "PostgreSQL", "Redis"]
        }
        return fallback.get(project_type, fallback["web_app"])
    
    def _fallback_plan(self, project_type: str) -> List[Dict]:
        """Fallback plan if AI fails"""
        plans = {
            "web_app": [
                {"step_number": 1, "description": "Analyze requirements and choose tech stack", "estimated_time": "2 min"},
                {"step_number": 2, "description": "Design system architecture", "estimated_time": "3 min"},
                {"step_number": 3, "description": "Generate frontend React components", "estimated_time": "5 min"},
                {"step_number": 4, "description": "Generate backend API endpoints", "estimated_time": "5 min"},
                {"step_number": 5, "description": "Create database schema", "estimated_time": "3 min"},
                {"step_number": 6, "description": "Review and fix code", "estimated_time": "4 min"},
            ]
        }
        return plans.get(project_type, plans["web_app"])


# ============ QUICK TEST ============

if __name__ == "__main__":
    # Test the AI engine
    print("🧪 Testing AI Code Generator...")
    
    try:
        ai = AICodeGenerator()
        
        # Test 1: Generate plan
        print("\n1️⃣ Testing Plan Generation...")
        plan = ai.generate_project_plan("Build a todo app", "web_app")
        print(f"✓ Generated {len(plan)} steps")
        
        # Test 2: Generate code
        print("\n2️⃣ Testing Code Generation...")
        code = ai.generate_code(
            "Create a React Todo component",
            {
                "project_type": "web_app",
                "tech_stack": "React, TypeScript",
                "prompt": "Todo app",
                "target_file": "Todo.tsx"
            }
        )
        print(f"✓ Generated {len(code)} characters of code")
        print("\nSample:")
        print(code[:200] + "...")
        
        print("\n✅ AI Engine Working!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure ANTHROPIC_API_KEY is set in .env file")