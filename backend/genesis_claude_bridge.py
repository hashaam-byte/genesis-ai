"""
GENESIS AI - Claude Bridge (Anti-Detection Version)
Bypasses Cloudflare "Verify you are human" checks
Save as: backend/genesis_claude_bridge.py
"""

from playwright.sync_api import sync_playwright
import time
import json
from pathlib import Path


class GenesisClaude:
    """
    Bridge between Genesis AI and Claude.ai
    ANTI-DETECTION: Bypasses Cloudflare security checks
    """
    
    def __init__(self, auto_start: bool = True, use_firefox: bool = False):
        self.browser = None
        self.page = None
        self.playwright = None
        self.use_firefox = use_firefox
        
        if auto_start:
            self.start()
    
    def start(self):
        """Start browser with anti-detection settings"""
        print("\n🚀 Starting Genesis <-> Claude Bridge (Stealth Mode)")
        print("=" * 60)
        
        # Setup browser data directory
        data_dir = Path("./browser_data/genesis_claude")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Start playwright
        self.playwright = sync_playwright().start()
        
        # SOLUTION 1: Use Firefox (Cloudflare detection is weaker)
        if self.use_firefox:
            print("🦊 Using Firefox (better for Cloudflare)...")
            self.browser = self.playwright.firefox.launch_persistent_context(
                str(data_dir / "firefox"),
                headless=False,
                viewport={'width': 1400, 'height': 900}
            )
        else:
            # SOLUTION 2: Chrome with anti-detection flags
            print("🌐 Launching Chrome with stealth mode...")
            self.browser = self.playwright.chromium.launch_persistent_context(
                str(data_dir / "chrome"),
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',  # Hide automation
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-web-security',
                    '--disable-features=IsolateOrigins,site-per-process',
                    '--disable-setuid-sandbox',
                    '--disable-accelerated-2d-canvas',
                    '--disable-gpu',
                    '--window-size=1920,1080',
                    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                ],
                viewport={'width': 1400, 'height': 900},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                ignore_default_args=['--enable-automation'],
                bypass_csp=True
            )
        
        # Get page
        if self.browser.pages:
            self.page = self.browser.pages[0]
        else:
            self.page = self.browser.new_page()
        
        # Inject anti-detection scripts
        self._inject_stealth_scripts()
        
        # Open Claude.ai with proper wait
        print("📱 Opening Claude.ai...")
        try:
            self.page.goto("https://claude.ai/new", timeout=60000, wait_until="networkidle")
            time.sleep(3)  # Extra wait for Cloudflare
            print("✅ Claude.ai loaded")
        except Exception as e:
            print(f"⚠️  Initial load: {e}")
            print("👉 Waiting for Cloudflare check...")
            time.sleep(10)
        
        print("\n" + "=" * 60)
        print("✅ READY!")
        print("=" * 60)
        print("👉 If you see 'Verify you are human':")
        print("   - Wait 10-15 seconds (auto-solves sometimes)")
        print("   - Or click the checkbox manually")
        print("   - Then the page will load normally")
        print("=" * 60 + "\n")
    
    def _inject_stealth_scripts(self):
        """Inject JavaScript to hide automation"""
        stealth_js = """
        // Override navigator.webdriver
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        
        // Override plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
        
        // Override languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en']
        });
        
        // Override chrome object
        window.chrome = {
            runtime: {}
        };
        
        // Override permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
        """
        
        try:
            self.page.add_init_script(stealth_js)
            print("🥷 Stealth scripts injected")
        except Exception as e:
            print(f"⚠️  Stealth injection: {e}")
    
    def wait_for_cloudflare(self, timeout: int = 60):
        """Wait for Cloudflare check to complete"""
        print("⏳ Waiting for Cloudflare verification...")
        start = time.time()
        
        while time.time() - start < timeout:
            # Check if we're past Cloudflare
            if self.check_login():
                print("✅ Cloudflare passed!")
                return True
            
            # Check if still on challenge page
            url = self.page.url
            if "challenges.cloudflare.com" in url or "challenge" in url:
                print("🔄 Still on Cloudflare challenge...")
                time.sleep(3)
            else:
                # Might be through
                time.sleep(2)
                if self.check_login():
                    return True
        
        print("⚠️  Cloudflare timeout - may need manual intervention")
        return False
    
    def check_login(self) -> bool:
        """Check if logged in to Claude.ai"""
        try:
            # Look for chat input (means logged in and past Cloudflare)
            textarea = self.page.query_selector('textarea[placeholder*="talk" i]')
            if textarea:
                return True
            
            # Also check for login button
            login_btn = self.page.query_selector('button:has-text("Login")')
            if login_btn:
                return False  # Not logged in but past Cloudflare
            
            return False
        except:
            return False
    
    def wait_for_login(self, timeout: int = 300) -> bool:
        """Wait for user to login"""
        print("⏳ Waiting for login...")
        print("👉 Please login to Claude.ai in the browser window")
        
        start = time.time()
        while time.time() - start < timeout:
            if self.check_login():
                print("✅ Logged in successfully!")
                return True
            time.sleep(2)
        
        print("❌ Login timeout")
        return False
    
    def get_latest_response(self, wait_complete: bool = True, timeout: int = 120) -> dict:
        """
        Get Claude's latest response
        
        Returns:
            {
                'success': bool,
                'response': str,
                'timestamp': float,
                'length': int
            }
        """
        try:
            # Wait for response to complete if requested
            if wait_complete:
                print("⏳ Waiting for Claude to finish responding...")
                start = time.time()
                
                while time.time() - start < timeout:
                    # Check for stop button (still generating)
                    stop_btn = self.page.query_selector('button[aria-label*="stop" i]')
                    if not stop_btn:
                        print("✅ Response complete")
                        break
                    time.sleep(0.5)
                else:
                    print("⚠️  Response timeout - reading partial response")
            
            # Find all message containers
            messages = None
            selectors = [
                'div[data-testid="message-content"]',
                'div[class*="Message"]',
                '[data-testid*="message"]',
                'div[data-is-streaming]'
            ]
            
            for selector in selectors:
                messages = self.page.query_selector_all(selector)
                if messages and len(messages) > 0:
                    break
            
            if not messages or len(messages) == 0:
                return {
                    'success': False,
                    'response': 'Error: No messages found',
                    'timestamp': time.time(),
                    'length': 0
                }
            
            # Get last message
            last_msg = messages[-1]
            text = last_msg.inner_text().strip()
            
            return {
                'success': True,
                'response': text,
                'timestamp': time.time(),
                'length': len(text)
            }
            
        except Exception as e:
            return {
                'success': False,
                'response': f'Error: {str(e)}',
                'timestamp': time.time(),
                'length': 0
            }
    
    def get_conversation_history(self) -> list:
        """Get all messages in current conversation"""
        try:
            messages = []
            msg_elements = self.page.query_selector_all('[data-testid*="message"]')
            
            for i, el in enumerate(msg_elements):
                text = el.inner_text().strip()
                if text:
                    role = "user" if i % 2 == 0 else "assistant"
                    messages.append({
                        'role': role,
                        'content': text
                    })
            
            return messages
            
        except Exception as e:
            print(f"Error getting history: {e}")
            return []
    
    def extract_code_blocks(self, text: str) -> list:
        """Extract code blocks from Claude's response"""
        blocks = []
        lines = text.split('\n')
        
        in_block = False
        current_block = []
        current_lang = 'text'
        
        for line in lines:
            if line.strip().startswith('```'):
                if not in_block:
                    in_block = True
                    current_lang = line.strip()[3:].strip() or 'text'
                    current_block = []
                else:
                    in_block = False
                    blocks.append({
                        'language': current_lang,
                        'code': '\n'.join(current_block)
                    })
                    current_block = []
            elif in_block:
                current_block.append(line)
        
        return blocks
    
    def close(self):
        """Clean shutdown"""
        print("\n🔒 Closing browser...")
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("✅ Closed")


# ============ ALTERNATIVE: USE YOUR REAL BROWSER ============

def use_real_browser_method():
    """
    BEST METHOD: Connect to your real Chrome/Edge browser
    NO Cloudflare issues because it's your real browser!
    """
    print("\n🎯 BEST METHOD: Use Your Real Browser")
    print("=" * 60)
    print("\n1️⃣  Close ALL Chrome/Edge windows")
    print("\n2️⃣  Start Chrome with remote debugging:")
    print("\n   Windows:")
    print('   "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222')
    print("\n   Mac:")
    print('   /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222')
    print("\n   Linux:")
    print('   google-chrome --remote-debugging-port=9222')
    print("\n3️⃣  Run the connection script below")
    print("=" * 60)
    
    input("\nPress ENTER when Chrome is running with debugging enabled...")
    
    playwright = sync_playwright().start()
    
    try:
        print("\n🔌 Connecting to your Chrome browser...")
        browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        
        # Get or create Claude tab
        context = browser.contexts[0]
        
        # Find Claude.ai tab or create new one
        claude_page = None
        for page in context.pages:
            if "claude.ai" in page.url:
                claude_page = page
                break
        
        if not claude_page:
            claude_page = context.new_page()
            claude_page.goto("https://claude.ai/new")
        
        print("✅ Connected to your real browser!")
        print("👉 Now you can use Claude.ai normally")
        print("👉 No Cloudflare issues!")
        
        # Interactive commands
        while True:
            cmd = input("\nCommand [r=read, q=quit]: ").strip().lower()
            
            if cmd == 'r':
                messages = claude_page.query_selector_all('[data-testid*="message"]')
                if messages:
                    last = messages[-1].inner_text()
                    print(f"\n{last[:500]}")
                else:
                    print("No messages yet")
            
            elif cmd == 'q':
                break
        
        print("\n✅ Done! Your browser stays open.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure Chrome is running with --remote-debugging-port=9222")


# ============ INTERACTIVE MODE ============

def interactive_mode(use_firefox=False):
    """Interactive mode with Cloudflare handling"""
    print("\n🎮 GENESIS AI - CLAUDE BRIDGE")
    print("(Anti-Cloudflare Version)\n")
    
    bridge = GenesisClaude(use_firefox=use_firefox)
    
    try:
        # Wait for Cloudflare
        print("\n⏳ Checking for Cloudflare...")
        time.sleep(5)
        
        if not bridge.check_login():
            print("\n👉 Complete Cloudflare check if needed, then login")
            bridge.wait_for_cloudflare()
            bridge.wait_for_login()
        
        print("\n✅ Ready to work!")
        print("\nCommands:")
        print("  [r] Read latest response")
        print("  [h] Get conversation history")
        print("  [c] Extract code from latest")
        print("  [q] Quit\n")
        
        last_response = None
        
        while True:
            cmd = input("Command: ").strip().lower()
            
            if cmd == 'r':
                result = bridge.get_latest_response()
                if result['success']:
                    print(f"\n{'='*60}")
                    print(result['response'])
                    print(f"{'='*60}\n")
                    last_response = result
                else:
                    print(f"❌ {result['response']}\n")
            
            elif cmd == 'h':
                history = bridge.get_conversation_history()
                for i, msg in enumerate(history):
                    print(f"\n--- {i+1} [{msg['role']}] ---")
                    print(msg['content'][:150])
            
            elif cmd == 'c':
                if last_response:
                    blocks = bridge.extract_code_blocks(last_response['response'])
                    if blocks:
                        print(f"\n📦 {len(blocks)} code block(s):")
                        for i, b in enumerate(blocks):
                            print(f"\n{i+1}. [{b['language']}] {len(b['code'])} chars")
                    else:
                        print("\n⚠️  No code blocks")
                else:
                    print("\n⚠️  Read response first")
            
            elif cmd == 'q':
                break
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted")
    finally:
        bridge.close()


if __name__ == "__main__":
    import sys
    
    print("\n🚀 GENESIS CLAUDE BRIDGE\n")
    print("Choose method:")
    print("1. Auto browser (Chrome with anti-detection)")
    print("2. Auto browser (Firefox - better Cloudflare)")
    print("3. Use real browser (BEST - no Cloudflare issues)")
    
    choice = input("\nChoice [1/2/3]: ").strip()
    
    if choice == "1":
        interactive_mode(use_firefox=False)
    elif choice == "2":
        interactive_mode(use_firefox=True)
    elif choice == "3":
        use_real_browser_method()
    else:
        print("Invalid choice")