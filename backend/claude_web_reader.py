"""
GENESIS AI - Claude.ai Response Reader
Works with YOUR browser - just reads responses!
Save as: backend/claude_web_reader.py
"""

from playwright.sync_api import sync_playwright
import time
import json
from typing import Optional
import os


class ClaudeWebReader:
    """
    Reads responses from Claude.ai in YOUR browser
    You manually open claude.ai, send prompts, and this reads the responses
    NO AUTOMATION - just monitoring!
    """
    
    def __init__(self, browser_type: str = "chrome"):
        """
        browser_type: "chrome", "firefox", or "edge"
        """
        self.browser_type = browser_type
        self.browser = None
        self.context = None
        self.page = None
        
    def connect_to_browser(self, debugger_url: str):
        """
        Connect to your existing browser
        
        To enable remote debugging:
        
        CHROME:
        1. Close all Chrome windows
        2. Run: chrome.exe --remote-debugging-port=9222
        3. Or on Mac: /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
        
        EDGE:
        msedge.exe --remote-debugging-port=9222
        
        Then call: reader.connect_to_browser("http://localhost:9222")
        """
        print(f"🔌 Connecting to browser at {debugger_url}...")
        
        playwright = sync_playwright().start()
        
        try:
            self.browser = playwright.chromium.connect_over_cdp(debugger_url)
            self.context = self.browser.contexts[0]
            
            # Find or create Claude.ai tab
            claude_page = None
            for page in self.context.pages:
                if "claude.ai" in page.url:
                    claude_page = page
                    break
            
            if claude_page:
                self.page = claude_page
                print(f"✅ Connected to existing Claude.ai tab")
            else:
                self.page = self.context.new_page()
                self.page.goto("https://claude.ai/new")
                print(f"✅ Opened new Claude.ai tab")
                print("👉 Please login if needed")
            
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            print("\nMake sure to:")
            print("1. Close all Chrome windows")
            print("2. Start Chrome with: chrome.exe --remote-debugging-port=9222")
            print("3. Then run this script")
            return False
    
    def start_simple_mode(self):
        """
        Simpler approach - launches browser with debugging enabled
        """
        print("🌐 Starting browser in debug mode...")
        
        playwright = sync_playwright().start()
        
        # Launch browser with persistent context (saves login)
        user_data_dir = "./browser_data/claude_reader"
        os.makedirs(user_data_dir, exist_ok=True)
        
        self.browser = playwright.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            args=[
                '--remote-debugging-port=9222',
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled'
            ],
            viewport={'width': 1280, 'height': 720}
        )
        
        # Get or create page
        if self.browser.pages:
            self.page = self.browser.pages[0]
        else:
            self.page = self.browser.new_page()
        
        # Navigate to Claude
        print("📱 Opening Claude.ai...")
        self.page.goto("https://claude.ai/new", wait_until="domcontentloaded")
        
        print("\n" + "=" * 60)
        print("✅ BROWSER READY!")
        print("=" * 60)
        print("👉 You can now:")
        print("   1. Login to Claude.ai if needed")
        print("   2. Start a conversation manually")
        print("   3. Use read_latest_response() to get Claude's replies")
        print("=" * 60 + "\n")
        
        return True
    
    def wait_for_login(self, timeout: int = 300):
        """
        Wait for user to login manually
        """
        print("⏳ Waiting for you to login...")
        print("👉 Login to Claude.ai in the browser, then this will continue")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Check if chat textarea exists (means logged in)
                textarea = self.page.query_selector('textarea[placeholder*="talk" i]')
                if textarea:
                    print("✅ Login detected!")
                    return True
            except:
                pass
            time.sleep(2)
        
        print("⚠️  Timeout waiting for login")
        return False
    
    def read_latest_response(self, wait_for_completion: bool = True, max_wait: int = 60) -> str:
        """
        Read the latest response from Claude
        
        Args:
            wait_for_completion: Wait for Claude to finish typing
            max_wait: Maximum seconds to wait
        
        Returns:
            Claude's response text
        """
        print("📖 Reading Claude's response...")
        
        try:
            if wait_for_completion:
                print("⏳ Waiting for response to complete...")
                start_time = time.time()
                
                # Wait for response to finish
                while time.time() - start_time < max_wait:
                    # Check if there's a stop button (means still generating)
                    stop_button = self.page.query_selector('button[aria-label*="stop" i]')
                    if not stop_button:
                        break
                    time.sleep(0.5)
            
            # Try multiple selectors to find messages
            selectors = [
                '[data-testid*="message"]',
                '[class*="Message"]',
                '[class*="markdown"]',
                'div[data-is-streaming]',
            ]
            
            messages = []
            for selector in selectors:
                messages = self.page.query_selector_all(selector)
                if messages and len(messages) > 0:
                    break
            
            if not messages or len(messages) == 0:
                print("⚠️  No messages found on page")
                return "Error: No messages found"
            
            # Get the last message (Claude's response)
            last_message = messages[-1]
            response_text = last_message.inner_text().strip()
            
            if response_text:
                print(f"✅ Got response ({len(response_text)} chars)")
                return response_text
            else:
                print("⚠️  Response was empty")
                return "Error: Empty response"
                
        except Exception as e:
            print(f"❌ Error reading response: {e}")
            return f"Error: {str(e)}"
    
    def read_all_messages(self) -> list:
        """
        Read all messages in the current conversation
        Returns list of dicts with 'role' and 'content'
        """
        print("📚 Reading all messages...")
        
        try:
            messages = []
            
            # Get all message elements
            message_elements = self.page.query_selector_all('[data-testid*="message"]')
            
            for msg_el in message_elements:
                text = msg_el.inner_text().strip()
                if text:
                    # Try to determine if it's user or assistant
                    # This is a heuristic - may need adjustment
                    role = "assistant" if "Claude" in text[:50] else "user"
                    messages.append({
                        "role": role,
                        "content": text
                    })
            
            print(f"✅ Found {len(messages)} messages")
            return messages
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def get_page_url(self) -> str:
        """Get current page URL"""
        if self.page:
            return self.page.url
        return "No page"
    
    def close(self):
        """Close browser"""
        if self.browser:
            self.browser.close()
            print("🔒 Browser closed")


# ============ USAGE EXAMPLES ============

def example_simple_usage():
    """
    Simple mode - script opens browser for you
    """
    print("🎯 SIMPLE MODE - Script opens browser\n")
    
    reader = ClaudeWebReader()
    
    try:
        # Start browser
        reader.start_simple_mode()
        
        # Wait for login if needed
        input("\n👉 Press ENTER after you've logged in and started a conversation...")
        
        # Read the latest response
        response = reader.read_latest_response()
        
        print("\n" + "=" * 60)
        print("CLAUDE'S RESPONSE:")
        print("=" * 60)
        print(response)
        print("=" * 60)
        
        # Keep reading
        while True:
            choice = input("\n[R]ead again, [A]ll messages, or [Q]uit? ").strip().upper()
            
            if choice == 'R':
                response = reader.read_latest_response()
                print("\n" + response)
            
            elif choice == 'A':
                messages = reader.read_all_messages()
                for i, msg in enumerate(messages):
                    print(f"\n--- Message {i+1} ({msg['role']}) ---")
                    print(msg['content'][:200] + "..." if len(msg['content']) > 200 else msg['content'])
            
            elif choice == 'Q':
                break
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        input("\n👉 Press ENTER to close browser...")
        reader.close()


def example_connect_mode():
    """
    Advanced mode - connect to your existing browser
    """
    print("🎯 CONNECT MODE - Use your existing browser\n")
    print("First, start Chrome with debugging:")
    print('chrome.exe --remote-debugging-port=9222\n')
    
    input("Press ENTER when Chrome is running with debugging enabled...")
    
    reader = ClaudeWebReader()
    
    try:
        if reader.connect_to_browser("http://localhost:9222"):
            print("✅ Connected!")
            
            input("\n👉 Go to claude.ai and start a chat, then press ENTER...")
            
            response = reader.read_latest_response()
            print("\n" + response)
        
    except Exception as e:
        print(f"❌ Error: {e}")


# ============ QUICK TEST ============

if __name__ == "__main__":
    print("🧪 Testing Claude Web Reader\n")
    
    # Use simple mode (recommended)
    example_simple_usage()
    
    # Or use connect mode (advanced)
    # example_connect_mode()