"""
GENESIS AI - Desktop Application
Use GENESIS for ANYTHING - not just coding!
Save as: backend/desktop_app.py

Run: python desktop_app.py
"""

import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import requests
import json
from datetime import datetime
import threading


class GenesisDesktopApp:
    """Simple desktop interface to use GENESIS AI for anything"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GENESIS AI - Desktop Interface")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a1a')
        
        self.api_url = "http://localhost:8000"
        self.setup_ui()
        
    def setup_ui(self):
        """Create UI"""
        
        # Header
        header = tk.Frame(self.root, bg='#2d2d2d', height=60)
        header.pack(fill='x', padx=0, pady=0)
        
        title = tk.Label(
            header,
            text="🧠 GENESIS AI",
            font=("Arial", 20, "bold"),
            bg='#2d2d2d',
            fg='#a855f7'
        )
        title.pack(pady=15)
        
        # Main container
        main = tk.Frame(self.root, bg='#1a1a1a')
        main.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Mode selector
        mode_frame = tk.Frame(main, bg='#1a1a1a')
        mode_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            mode_frame,
            text="Mode:",
            font=("Arial", 11),
            bg='#1a1a1a',
            fg='#ffffff'
        ).pack(side='left', padx=(0, 10))
        
        self.mode_var = tk.StringVar(value="prompt")
        
        modes = [
            ("💬 Simple Prompt", "prompt"),
            ("🚀 Generate Project", "project"),
            ("💡 Creative Writing", "creative"),
            ("🔍 Research", "research"),
            ("✍️ Rewrite Text", "rewrite")
        ]
        
        for text, value in modes:
            tk.Radiobutton(
                mode_frame,
                text=text,
                variable=self.mode_var,
                value=value,
                font=("Arial", 10),
                bg='#1a1a1a',
                fg='#ffffff',
                selectcolor='#2d2d2d',
                activebackground='#1a1a1a',
                activeforeground='#a855f7'
            ).pack(side='left', padx=5)
        
        # Input area
        tk.Label(
            main,
            text="Your Request:",
            font=("Arial", 11, "bold"),
            bg='#1a1a1a',
            fg='#ffffff'
        ).pack(anchor='w', pady=(0, 5))
        
        self.input_text = scrolledtext.ScrolledText(
            main,
            height=8,
            font=("Consolas", 10),
            bg='#2d2d2d',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief='flat',
            padx=10,
            pady=10
        )
        self.input_text.pack(fill='x', pady=(0, 15))
        
        # Buttons
        button_frame = tk.Frame(main, bg='#1a1a1a')
        button_frame.pack(fill='x', pady=(0, 15))
        
        self.generate_btn = tk.Button(
            button_frame,
            text="▶ Generate",
            command=self.generate,
            font=("Arial", 11, "bold"),
            bg='#a855f7',
            fg='#ffffff',
            activebackground='#9333ea',
            relief='flat',
            padx=30,
            pady=10,
            cursor='hand2'
        )
        self.generate_btn.pack(side='left', padx=(0, 10))
        
        tk.Button(
            button_frame,
            text="Clear",
            command=self.clear,
            font=("Arial", 11),
            bg='#4b5563',
            fg='#ffffff',
            activebackground='#374151',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        ).pack(side='left')
        
        # Status
        self.status_label = tk.Label(
            button_frame,
            text="Ready",
            font=("Arial", 10),
            bg='#1a1a1a',
            fg='#10b981'
        )
        self.status_label.pack(side='right')
        
        # Output area
        tk.Label(
            main,
            text="Response:",
            font=("Arial", 11, "bold"),
            bg='#1a1a1a',
            fg='#ffffff'
        ).pack(anchor='w', pady=(0, 5))
        
        self.output_text = scrolledtext.ScrolledText(
            main,
            height=20,
            font=("Consolas", 10),
            bg='#2d2d2d',
            fg='#ffffff',
            relief='flat',
            padx=10,
            pady=10
        )
        self.output_text.pack(fill='both', expand=True)
        
    def set_status(self, text: str, color: str = '#10b981'):
        """Update status"""
        self.status_label.config(text=text, fg=color)
        
    def generate(self):
        """Generate response"""
        prompt = self.input_text.get("1.0", "end-1c").strip()
        
        if not prompt:
            messagebox.showwarning("Warning", "Please enter a request")
            return
        
        mode = self.mode_var.get()
        
        # Run in thread to avoid freezing UI
        thread = threading.Thread(target=self._generate_thread, args=(prompt, mode))
        thread.start()
        
    def _generate_thread(self, prompt: str, mode: str):
        """Generate in background thread"""
        self.generate_btn.config(state='disabled')
        self.set_status("Generating...", '#f59e0b')
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", "⏳ Waiting for AI...\n\n")
        
        try:
            if mode == "project":
                # Generate full project
                response = requests.post(
                    f"{self.api_url}/api/generate",
                    json={"prompt": prompt, "create_files": True},
                    timeout=120
                )
            else:
                # Simple prompt
                response = requests.post(
                    f"{self.api_url}/api/prompt",
                    json={"prompt": prompt, "task_type": mode},
                    timeout=60
                )
            
            if response.status_code == 200:
                data = response.json()
                
                if mode == "project":
                    # Project response
                    self.display_project_response(data)
                else:
                    # Simple response
                    self.output_text.delete("1.0", "end")
                    self.output_text.insert("1.0", data.get("response", "No response"))
                    self.output_text.insert("end", f"\n\n---\n✅ {data.get('provider', 'unknown')} | Cost: ${data.get('cost', 0):.4f}")
                
                self.set_status("Complete!", '#10b981')
            else:
                self.output_text.delete("1.0", "end")
                self.output_text.insert("1.0", f"❌ Error: {response.text}")
                self.set_status("Error", '#ef4444')
                
        except requests.exceptions.ConnectionError:
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", "❌ Cannot connect to GENESIS AI backend\n\nMake sure backend is running:\npython main.py")
            self.set_status("Connection Error", '#ef4444')
            
        except Exception as e:
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", f"❌ Error: {str(e)}")
            self.set_status("Error", '#ef4444')
        
        finally:
            self.generate_btn.config(state='normal')
    
    def display_project_response(self, data: dict):
        """Display project generation response"""
        self.output_text.delete("1.0", "end")
        
        output = "✅ PROJECT GENERATED!\n\n"
        output += f"📁 Project ID: {data.get('project_id')}\n"
        output += f"📍 Location: {data.get('output_directory', 'In memory')}\n"
        output += f"🔧 Tech Stack: {', '.join(data.get('tech_stack', []))}\n"
        output += f"💰 Cost: {data.get('cost_estimate', '$0.00')}\n"
        output += f"🤖 AI Used: {', '.join(data.get('ai_providers_used', ['unknown']))}\n\n"
        
        output += "📦 FILES CREATED:\n"
        for file in data.get('files_created', []):
            output += f"  - {file}\n"
        
        output += "\n📋 EXECUTION LOG:\n"
        for log in data.get('logs', [])[-10:]:
            output += f"  {log}\n"
        
        if data.get('errors'):
            output += "\n⚠️ ERRORS:\n"
            for error in data['errors']:
                output += f"  - {error}\n"
        
        self.output_text.insert("1.0", output)
    
    def clear(self):
        """Clear input and output"""
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")
        self.set_status("Ready", '#10b981')
    
    def run(self):
        """Start app"""
        print("🚀 Starting GENESIS Desktop App...")
        print("📍 Make sure backend is running on http://localhost:8000")
        self.root.mainloop()


if __name__ == "__main__":
    app = GenesisDesktopApp()
    app.run()