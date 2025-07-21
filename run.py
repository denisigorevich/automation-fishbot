#!/usr/bin/env python3
"""
WoW Fishbot Launcher
Simple menu to run different components of the fishbot
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

class FishbotLauncher:
    """Simple launcher for fishbot components"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WoW Fishbot Launcher")
        self.root.geometry("500x400")
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the launcher GUI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="WoW Fishbot Launcher", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Educational disclaimer
        disclaimer_frame = ttk.LabelFrame(main_frame, text="⚠️ Educational Purpose Only", padding="10")
        disclaimer_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        disclaimer_text = """This fishbot is for educational purposes only.
Use only on private servers or for learning programming concepts.
Always respect game terms of service and local laws."""
        
        ttk.Label(disclaimer_frame, text=disclaimer_text, justify=tk.CENTER, foreground="red").grid(row=0, column=0)
        
        # Launch buttons
        buttons_frame = ttk.LabelFrame(main_frame, text="Launch Components", padding="10")
        buttons_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Main bot
        ttk.Button(buttons_frame, text="🎣 Main Fishbot (GUI)", 
                  command=self.launch_main_gui, width=30).grid(row=0, column=0, pady=5)
        
        ttk.Button(buttons_frame, text="🖥️ Main Fishbot (CLI)", 
                  command=self.launch_main_cli, width=30).grid(row=1, column=0, pady=5)
        
        # Setup utility
        ttk.Button(buttons_frame, text="⚙️ Setup & Configuration", 
                  command=self.launch_setup, width=30).grid(row=2, column=0, pady=5)
        
        # Detection tester
        ttk.Button(buttons_frame, text="🧪 Detection Tester", 
                  command=self.launch_tester, width=30).grid(row=3, column=0, pady=5)
        
        # Documentation
        docs_frame = ttk.LabelFrame(main_frame, text="Documentation & Help", padding="10")
        docs_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Button(docs_frame, text="📖 Open README", 
                  command=self.open_readme, width=30).grid(row=0, column=0, pady=5)
        
        ttk.Button(docs_frame, text="📁 Open Project Folder", 
                  command=self.open_folder, width=30).grid(row=1, column=0, pady=5)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Ready to launch", foreground="green")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        
        # Quick setup instructions
        instructions_frame = ttk.LabelFrame(main_frame, text="Quick Start", padding="10")
        instructions_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))
        
        instructions_text = """1. First time? Run 'Setup & Configuration' to configure detection areas
2. Test your setup with 'Detection Tester'
3. Launch the main fishbot when ready
4. Use F9 to start/stop, F10 to pause, F11 for emergency stop"""
        
        ttk.Label(instructions_frame, text=instructions_text, justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
    
    def update_status(self, message, color="black"):
        """Update status message"""
        self.status_label.config(text=message, foreground=color)
        self.root.update()
    
    def launch_main_gui(self):
        """Launch main fishbot in GUI mode"""
        try:
            self.update_status("Launching Main Fishbot (GUI)...", "blue")
            subprocess.Popen([sys.executable, "main.py", "--gui"])
            self.update_status("Main Fishbot (GUI) launched", "green")
        except Exception as e:
            self.update_status(f"Error launching main bot: {e}", "red")
            messagebox.showerror("Error", f"Failed to launch main bot: {e}")
    
    def launch_main_cli(self):
        """Launch main fishbot in CLI mode"""
        try:
            self.update_status("Launching Main Fishbot (CLI)...", "blue")
            subprocess.Popen([sys.executable, "main.py", "--cli"])
            self.update_status("Main Fishbot (CLI) launched", "green")
        except Exception as e:
            self.update_status(f"Error launching main bot: {e}", "red")
            messagebox.showerror("Error", f"Failed to launch main bot: {e}")
    
    def launch_setup(self):
        """Launch setup utility"""
        try:
            self.update_status("Launching Setup Utility...", "blue")
            subprocess.Popen([sys.executable, "setup_detector.py"])
            self.update_status("Setup Utility launched", "green")
        except Exception as e:
            self.update_status(f"Error launching setup: {e}", "red")
            messagebox.showerror("Error", f"Failed to launch setup: {e}")
    
    def launch_tester(self):
        """Launch detection tester"""
        try:
            self.update_status("Launching Detection Tester...", "blue")
            subprocess.Popen([sys.executable, "test_detection.py"])
            self.update_status("Detection Tester launched", "green")
        except Exception as e:
            self.update_status(f"Error launching tester: {e}", "red")
            messagebox.showerror("Error", f"Failed to launch tester: {e}")
    
    def open_readme(self):
        """Open README file"""
        try:
            if os.path.exists("README.md"):
                if sys.platform.startswith('win'):
                    os.startfile("README.md")
                elif sys.platform.startswith('darwin'):
                    subprocess.call(["open", "README.md"])
                else:
                    subprocess.call(["xdg-open", "README.md"])
                self.update_status("README opened", "green")
            else:
                messagebox.showwarning("Warning", "README.md not found")
        except Exception as e:
            self.update_status(f"Error opening README: {e}", "red")
            messagebox.showerror("Error", f"Failed to open README: {e}")
    
    def open_folder(self):
        """Open project folder"""
        try:
            current_dir = os.getcwd()
            if sys.platform.startswith('win'):
                os.startfile(current_dir)
            elif sys.platform.startswith('darwin'):
                subprocess.call(["open", current_dir])
            else:
                subprocess.call(["xdg-open", current_dir])
            self.update_status("Project folder opened", "green")
        except Exception as e:
            self.update_status(f"Error opening folder: {e}", "red")
            messagebox.showerror("Error", f"Failed to open folder: {e}")
    
    def run(self):
        """Run the launcher"""
        self.root.mainloop()

def check_dependencies():
    """Check if required files exist"""
    required_files = ["main.py", "setup_detector.py", "test_detection.py", "requirements.txt"]
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure all fishbot files are in the current directory.")
        return False
    
    return True

def main():
    """Main entry point"""
    print("WoW Fishbot Launcher")
    print("===================")
    
    # Check dependencies
    if not check_dependencies():
        input("Press Enter to exit...")
        return
    
    # Check if in correct directory
    if not os.path.exists("main.py"):
        print("❌ Please run this launcher from the fishbot directory")
        input("Press Enter to exit...")
        return
    
    print("✅ All required files found")
    print("🚀 Starting launcher GUI...")
    
    try:
        app = FishbotLauncher()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Launcher closed by user")
    except Exception as e:
        print(f"❌ Launcher error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()