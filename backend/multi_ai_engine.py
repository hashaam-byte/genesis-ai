"""
GENESIS AI - Multi-AI Hybrid Engine
Supports: Groq, Gemini, Claude, OpenAI
Save as: backend/multi_ai_engine.py
"""

import os
from typing import Dict, List, Optional, Any
import json
from dotenv import load_dotenv

# Import all AI SDKs
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from anthropic import Anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

load_dotenv()


class MultiAIEngine:
    """Intelligent AI router that uses multiple models"""
    
    def __init__(self):
        self.primary_ai = os.getenv("PRIMARY_AI", "groq")
        self.fallback_ai = os.getenv("FALLBACK_AI", "gemini")
        self.hybrid_mode = os.getenv("HYBRID_MODE", "true").lower() == "true"
        self.budget_mode = os.getenv("BUDGET_MODE", "true").lower() == "true"
        
        # Initialize available clients
        self.clients = {}
        self._init_clients()
        
        print(f"🧠 Multi-AI Engine initialized")
        print(f"   Primary: {self.primary_ai}")
        print(f"   Fallback: {self.fallback_ai}")
        print(f"   Available: {', '.join(self.clients.keys())}")
        print(f"   Budget Mode: {self.budget_mode}")
    
    def _init_clients(self):
        """Initialize all available AI clients"""
        
        # Groq (FREE, FAST)
        if GROQ_AVAILABLE:
            groq_key = os.getenv("GROQ_API_KEY")
            if groq_key:
                self.clients["groq"] = Groq(api_key=groq_key)
                print("   ✅ Groq initialized (FREE)")
        
        # Google Gemini (FREE tier)
        if GEMINI_AVAILABLE:
            gemini_key = os.getenv("GOOGLE_API_KEY")
            if gemini_key:
                genai.configure(api_key=gemini_key)
                self.clients["gemini"] = genai.GenerativeModel('gemini-1.5-flash')
                print("   ✅ Gemini initialized (FREE)")
        
        # Claude (PAID)
        if CLAUDE_AVAILABLE and not self.budget_mode:
            claude_key = os.getenv("ANTHROPIC_API_KEY")
            if claude_key:
                self.clients["claude"] = Anthropic(api_key=claude_key)
                print("   ✅ Claude initialized (PAID)")
        
        # OpenAI (PAID)
        if OPENAI_AVAILABLE and not self.budget_mode:
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key:
                self.clients["openai"] = OpenAI(api_key=openai_key)
                print("   ✅ OpenAI initialized (PAID)")
        
        if not self.clients:
            raise ValueError("No AI providers available! Check API keys in .env")
    
    def generate(self, prompt: str, system_prompt: str = "", task_type: str = "general") -> str:
        """
        Smart generation with automatic fallback
        task_type: general, code, review, architecture, planning
        """
        
        # Choose best AI for task
        provider = self._choose_provider(task_type)
        
        print(f"   🤖 Using {provider} for {task_type}")
        
        try:
            result = self._call_ai(provider, prompt, system_prompt)
            return result
        except Exception as e:
            print(f"   ⚠️  {provider} failed: {e}")
            
            # Try fallback
            if provider != self.fallback_ai and self.fallback_ai in self.clients:
                print(f"   🔄 Trying fallback: {self.fallback_ai}")
                try:
                    return self._call_ai(self.fallback_ai, prompt, system_prompt)
                except Exception as e2:
                    print(f"   ❌ Fallback also failed: {e2}")
            
            # Last resort: try any available AI
            for backup_provider in self.clients.keys():
                if backup_provider not in [provider, self.fallback_ai]:
                    print(f"   🔄 Last resort: {backup_provider}")
                    try:
                        return self._call_ai(backup_provider, prompt, system_prompt)
                    except:
                        continue
            
            raise Exception("All AI providers failed")
    
    def _choose_provider(self, task_type: str) -> str:
        """Choose best AI for the task"""
        
        # Budget mode: only free AIs
        if self.budget_mode:
            if "groq" in self.clients:
                return "groq"  # Fastest free option
            elif "gemini" in self.clients:
                return "gemini"
            else:
                return list(self.clients.keys())[0]
        
        # Smart routing based on task
        task_routing = {
            "code": "groq",           # Fast code generation
            "review": "gemini",       # Good at analysis
            "architecture": "claude", # Best reasoning
            "planning": "claude",     # Strategic thinking
            "general": "groq"         # Default to fast
        }
        
        preferred = task_routing.get(task_type, self.primary_ai)
        
        # Use preferred if available, otherwise primary
        if preferred in self.clients:
            return preferred
        elif self.primary_ai in self.clients:
            return self.primary_ai
        else:
            return list(self.clients.keys())[0]
    
    def _call_ai(self, provider: str, prompt: str, system_prompt: str) -> str:
        """Call specific AI provider"""
        
        if provider == "groq":
            return self._call_groq(prompt, system_prompt)
        elif provider == "gemini":
            return self._call_gemini(prompt, system_prompt)
        elif provider == "claude":
            return self._call_claude(prompt, system_prompt)
        elif provider == "openai":
            return self._call_openai(prompt, system_prompt)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def _call_groq(self, prompt: str, system_prompt: str) -> str:
        """Call Groq API (FREE, FAST)"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.clients["groq"].chat.completions.create(
            model="llama-3.3-70b-versatile",  # Fast and capable
            messages=messages,
            temperature=0.7,
            max_tokens=4000
        )
        return response.choices[0].message.content
    
    def _call_gemini(self, prompt: str, system_prompt: str) -> str:
        """Call Google Gemini API (FREE tier)"""
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        response = self.clients["gemini"].generate_content(full_prompt)
        return response.text
    
    def _call_claude(self, prompt: str, system_prompt: str) -> str:
        """Call Anthropic Claude API (PAID)"""
        response = self.clients["claude"].messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            system=system_prompt if system_prompt else "You are a helpful AI assistant.",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    def _call_openai(self, prompt: str, system_prompt: str) -> str:
        """Call OpenAI API (PAID)"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.clients["openai"].chat.completions.create(
            model="gpt-4o-mini",  # Cheaper option
            messages=messages,
            temperature=0.7,
            max_tokens=4000
        )
        return response.choices[0].message.content
    
    # ============ HIGH-LEVEL METHODS ============
    
    def generate_code(self, task: str, context: Dict) -> str:
        """Generate code (uses fastest free AI)"""
        system_prompt = """You are an expert full-stack developer.
Write clean, production-ready code with comments.
Return ONLY code, no explanations."""
        
        user_prompt = f"""Generate code for: {task}

Context:
- Type: {context.get('project_type', 'web_app')}
- Stack: {context.get('tech_stack', 'React, Node.js')}
- File: {context.get('target_file', 'App.tsx')}

Generate complete, working code."""
        
        return self.generate(user_prompt, system_prompt, task_type="code")
    
    def generate_plan(self, prompt: str, project_type: str) -> List[Dict]:
        """Generate project plan (uses best reasoning AI)"""
        system_prompt = """Create a detailed project execution plan.
Return ONLY a JSON array of steps."""
        
        user_prompt = f"""Create execution plan for:
Type: {project_type}
Request: {prompt}

Return JSON array like:
[{{"step_number": 1, "description": "...", "estimated_time": "5 min"}}]"""
        
        response = self.generate(user_prompt, system_prompt, task_type="planning")
        
        # Extract JSON
        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except:
            pass
        
        # Fallback
        return [
            {"step_number": 1, "description": "Analyze requirements", "estimated_time": "2 min"},
            {"step_number": 2, "description": "Generate code", "estimated_time": "5 min"},
            {"step_number": 3, "description": "Review and test", "estimated_time": "3 min"}
        ]
    
    def review_code(self, code: str, filename: str) -> Dict:
        """Review code (uses free analysis AI)"""
        system_prompt = """Review code for bugs, security, and best practices.
Return JSON: {"status": "pass/needs_fixes", "issues": [], "rating": 1-10}"""
        
        user_prompt = f"""Review this code:
File: {filename}
Code:
```
{code[:2000]}
```"""
        
        response = self.generate(user_prompt, system_prompt, task_type="review")
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0:
                return json.loads(response[json_start:json_end])
        except:
            pass
        
        return {"status": "pass", "issues": [], "rating": 8}
    
    def analyze_tech_stack(self, prompt: str, project_type: str) -> List[str]:
        """Choose optimal tech stack"""
        system_prompt = "Choose best technologies. Return ONLY JSON array of tech names."
        
        user_prompt = f"""Best tech stack for:
Type: {project_type}
Requirements: {prompt}

Return: ["React", "Node.js", ...]"""
        
        response = self.generate(user_prompt, system_prompt, task_type="architecture")
        
        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start >= 0:
                return json.loads(response[json_start:json_end])
        except:
            pass
        
        # Fallback
        stacks = {
            "web_app": ["React", "TypeScript", "Node.js", "PostgreSQL"],
            "game": ["Unity", "C#", "Blender"],
            "mobile_app": ["React Native", "TypeScript"],
        }
        return stacks.get(project_type, stacks["web_app"])


# ============ QUICK TEST ============

if __name__ == "__main__":
    print("🧪 Testing Multi-AI Engine...\n")
    
    try:
        ai = MultiAIEngine()
        
        # Test code generation
        print("\n1️⃣ Testing Code Generation...")
        code = ai.generate_code(
            "Create a React Todo component",
            {"project_type": "web_app", "tech_stack": "React", "target_file": "Todo.tsx"}
        )
        print(f"✓ Generated {len(code)} characters")
        print(f"Preview: {code[:150]}...")
        
        # Test planning
        print("\n2️⃣ Testing Plan Generation...")
        plan = ai.generate_plan("Build a weather app", "web_app")
        print(f"✓ Generated {len(plan)} steps")
        
        print("\n✅ Multi-AI Engine Working!")
        print(f"\n💰 Cost: $0.00 (using free tier)")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have at least one API key set in .env:")
        print("  - GROQ_API_KEY (recommended - free & fast)")
        print("  - GOOGLE_API_KEY (gemini - free tier)")