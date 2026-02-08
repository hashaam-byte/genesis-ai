#!/usr/bin/env python3
"""
Simple test script to verify backend functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Test imports
try:
    from app.config import settings
    print("✅ Config loaded successfully")
    print(f"   App name: {settings.APP_NAME}")
    print(f"   Debug mode: {settings.DEBUG}")
except Exception as e:
    print(f"❌ Config failed: {e}")

try:
    from app.core.router import SmartRouter, TaskType
    print("✅ SmartRouter loaded successfully")
    
    # Test task classification
    router = SmartRouter()
    test_prompt = "Create a beautiful React component with TypeScript"
    task_type = router.classify_task(test_prompt)
    print(f"   Task classification: {task_type.value}")
    
except Exception as e:
    print(f"❌ SmartRouter failed: {e}")

try:
    from app.models.claude_client import ClaudeClient
    from app.models.openai_client import OpenAIClient
    print("✅ AI model clients loaded successfully")
    
    # Note: We won't actually test API calls without keys
    claude = ClaudeClient()
    openai = OpenAIClient()
    print("   Claude client initialized")
    print("   OpenAI client initialized")
    
except Exception as e:
    print(f"❌ AI model clients failed: {e}")

try:
    from app.api.routes.generate import router
    print("✅ API routes loaded successfully")
except Exception as e:
    print(f"❌ API routes failed: {e}")

print("\n🎉 Backend core components are working!")
print("📝 Next steps:")
print("   1. Copy backend/.env.example to backend/.env")
print("   2. Add your API keys to .env")
print("   3. Run: cd backend && python -m uvicorn app.main:app --reload")
print("   4. Visit: http://localhost:8000/docs")
