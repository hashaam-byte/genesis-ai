"""
GENESIS AI - ULTIMATE Hybrid AI Engine
Combines: Free APIs + Your Claude/OpenAI Subscriptions
Save as: backend/ultimate_ai.py
"""

import os
from typing import Dict, List, Optional
import json
from dotenv import load_dotenv

# Free AI imports
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

# Web interface imports (YOUR accounts)
try:
    from backend.claude_web_reader import ClaudeWebInterface
    CLAUDE_WEB_AVAILABLE = True
except ImportError:
    CLAUDE_WEB_AVAILABLE = False

try:
    from backend.claude_web_reader import ChatGPTWebInterface
    CHATGPT_WEB_AVAILABLE = True
except ImportError:
    CHATGPT_WEB_AVAILABLE = False

load_dotenv()


class UltimateAI:
    """
    The smartest AI routing system:
    - FREE tasks → Groq/Gemini (fast, unlimited)
    - COMPLEX tasks → Your Claude/ChatGPT subscription (via browser)
    - ZERO API costs
    """
    
    def __init__(self):
        self.use_web_interfaces = os.getenv("USE_WEB_INTERFACES", "true").lower() == "true"
        self.prefer_free = os.getenv("PREFER_FREE_AI", "true").lower() == "true"
        
        self.free_clients = {}
        self.web_clients = {}
        self.stats = {
            "free_calls": 0,
            "web_calls": 0,
            "total_cost": 0.0
        }
        
        self._init_all_clients()
        self._print_status()
    
    def _init_all_clients(self):
        """Initialize all available AI clients"""
        
        # ========== FREE APIs (UNLIMITED) ==========
        
        if GROQ_AVAILABLE:
            groq_key = os.getenv("GROQ_API_KEY")
            if groq_key:
                self.free_clients["groq"] = Groq(api_key=groq_key)
                print("   ✅ Groq (FREE, FAST)")
        
        if GEMINI_AVAILABLE:
            gemini_key = os.getenv("GOOGLE_API_KEY")
            if gemini_key:
                genai.configure(api_key=gemini_key)
                self.free_clients["gemini"] = genai.GenerativeModel('gemini-1.5-flash')
                print("   ✅ Gemini (FREE)")
        
        # ========== WEB INTERFACES (YOUR SUBSCRIPTIONS) ==========
        
        if self.use_web_interfaces:
            if CLAUDE_WEB_AVAILABLE:
                try:
                    self.web_clients["claude_web"] = ClaudeWebInterface()
                    print("   ✅ Claude.ai (YOUR ACCOUNT)")
                except Exception as e:
                    print(f"   ⚠️  Claude.ai: {e}")
            
            if CHATGPT_WEB_AVAILABLE:
                try:
                    self.web_clients["chatgpt_web"] = ChatGPTWebInterface()
                    print("   ✅ ChatGPT (YOUR ACCOUNT)")
                except Exception as e:
                    print(f"   ⚠️  ChatGPT: {e}")
    
    def _print_status(self):
        """Print available services"""
        print("\n" + "=" * 60)
        print("🧠 ULTIMATE AI ENGINE STATUS")
        print("=" * 60)
        print(f"FREE APIs: {len(self.free_clients)} available")
        print(f"WEB Interfaces: {len(self.web_clients)} available")
        print(f"Strategy: {'Prefer FREE' if self.prefer_free else 'Balanced'}")
        print("=" * 60 + "\n")
    
    def generate(self, prompt: str, system_prompt: str = "", task_type: str = "general") -> Dict:
        """
        Smart generation with cost optimization
        Returns: {"text": str, "provider": str, "cost": float}
        """
        
        # Determine which AI to use
        provider = self._choose_provider(task_type)
        
        print(f"   🤖 Using: {provider} for {task_type}")
        
        try:
            if provider in self.free_clients:
                # FREE API
                result = self._call_free_ai(provider, prompt, system_prompt)
                self.stats["free_calls"] += 1
                cost = 0.0
                
            elif provider in self.web_clients:
                # YOUR SUBSCRIPTION (via browser)
                result = self._call_web_interface(provider, prompt, system_prompt)
                self.stats["web_calls"] += 1
                cost = 0.0  # Uses your subscription
                
            else:
                raise Exception("No AI provider available")
            
            return {
                "text": result,
                "provider": provider,
                "cost": cost
            }
            
        except Exception as e:
            print(f"   ❌ {provider} failed: {e}")
            
            # Try fallback
            fallback = self._get_fallback(provider)
            if fallback:
                print(f"   🔄 Trying fallback: {fallback}")
                return self.generate(prompt, system_prompt, task_type)
            
            raise Exception("All AI providers failed")
    
    def _choose_provider(self, task_type: str) -> str:
        """Choose best provider based on task complexity"""
        
        # Simple tasks → FREE APIs (fast)
        simple_tasks = ["code", "general", "review"]
        
        # Complex tasks → Web interfaces (your subscriptions, better quality)
        complex_tasks = ["architecture", "planning", "complex_code"]
        
        if task_type in simple_tasks and self.prefer_free:
            # Use free APIs
            if "groq" in self.free_clients:
                return "groq"
            elif "gemini" in self.free_clients:
                return "gemini"
        
        if task_type in complex_tasks:
            # Use web interfaces for better quality
            if "claude_web" in self.web_clients:
                return "claude_web"
            elif "chatgpt_web" in self.web_clients:
                return "chatgpt_web"
        
        # Default: use whatever is available
        if self.free_clients:
            return list(self.free_clients.keys())[0]
        elif self.web_clients:
            return list(self.web_clients.keys())[0]
        
        raise Exception("No AI providers available")
    
    def _get_fallback(self, failed_provider: str) -> Optional[str]:
        """Get fallback provider"""
        all_providers = list(self.free_clients.keys()) + list(self.web_clients.keys())
        all_providers = [p for p in all_providers if p != failed_provider]
        return all_providers[0] if all_providers else None
    
    def _call_free_ai(self, provider: str, prompt: str, system_prompt: str) -> str:
        """Call free API"""
        
        if provider == "groq":
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.free_clients["groq"].chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=4000
            )
            return response.choices[0].message.content
        
        elif provider == "gemini":
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = self.free_clients["gemini"].generate_content(full_prompt)
            return response.text
    
    def _call_web_interface(self, provider: str, prompt: str, system_prompt: str) -> str:
        """Call web interface (YOUR subscription)"""
        
        # Combine system + user prompt
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        
        client = self.web_clients[provider]
        
        # Initialize browser if needed
        if not client.is_logged_in:
            client.initialize()
            if not client.check_login_status():
                client.login_manually()
        
        # Send prompt
        response = client.send_prompt(full_prompt)
        return response
    
    # ============ HIGH-LEVEL METHODS ============
    
    def generate_code(self, task: str, context: Dict) -> Dict:
        """Generate code (uses FREE AI by default)"""
        system_prompt = """You are an expert developer.
Write clean, production code with comments.
Return ONLY code, no explanations."""
        
        prompt = f"""Generate code for: {task}

Context:
- Type: {context.get('project_type')}
- Stack: {context.get('tech_stack')}
- File: {context.get('target_file')}

Generate complete, working code."""
        
        return self.generate(prompt, system_prompt, task_type="code")
    
    def generate_plan(self, user_prompt: str, project_type: str) -> Dict:
        """Generate plan (uses web interface for better quality)"""
        system_prompt = """Create detailed project execution plan.
Return ONLY JSON array of steps."""
        
        prompt = f"""Create plan for:
Type: {project_type}
Request: {user_prompt}

Return JSON: [{{"step_number": 1, "description": "...", "estimated_time": "5 min"}}]"""
        
        result = self.generate(prompt, system_prompt, task_type="planning")
        
        # Parse JSON from response
        try:
            text = result["text"]
            json_start = text.find('[')
            json_end = text.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                plan = json.loads(text[json_start:json_end])
                result["plan"] = plan
        except:
            result["plan"] = [
                {"step_number": 1, "description": "Generate code", "estimated_time": "5 min"}
            ]
        
        return result
    
    def get_stats(self) -> Dict:
        """Get usage statistics"""
        return {
            **self.stats,
            "free_providers": list(self.free_clients.keys()),
            "web_providers": list(self.web_clients.keys()),
            "total_providers": len(self.free_clients) + len(self.web_clients)
        }
    
    def cleanup(self):
        """Close browser sessions"""
        for client in self.web_clients.values():
            try:
                client.close()
            except:
                pass


# ============ QUICK TEST ============

if __name__ == "__main__":
    print("🧪 Testing Ultimate AI Engine...\n")
    
    try:
        ai = UltimateAI()
        
        # Test 1: Simple code (should use FREE API)
        print("\n1️⃣ Testing simple code generation (FREE API)...")
        result = ai.generate_code(
            "Create a React button",
            {"project_type": "web", "tech_stack": "React", "target_file": "Button.tsx"}
        )
        print(f"   Provider: {result['provider']}")
        print(f"   Cost: ${result['cost']}")
        print(f"   Code preview: {result['text'][:100]}...")
        
        # Test 2: Complex planning (should use web interface if available)
        print("\n2️⃣ Testing complex planning...")
        result = ai.generate_plan("Build a social media app", "web_app")
        print(f"   Provider: {result['provider']}")
        print(f"   Cost: ${result['cost']}")
        
        # Show stats
        print("\n📊 Usage Statistics:")
        stats = ai.get_stats()
        print(f"   FREE API calls: {stats['free_calls']}")
        print(f"   Web interface calls: {stats['web_calls']}")
        print(f"   Total cost: ${stats['total_cost']}")
        
        print("\n✅ Ultimate AI Engine Working!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    finally:
        print("\n🔒 Cleaning up...")
        ai.cleanup()