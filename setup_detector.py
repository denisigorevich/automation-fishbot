#!/usr/bin/env python3
"""
Setup script for Fishbot - helps configure detection areas and capture templates
"""

import cv2
import numpy as np
import pyautogui
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from PIL import Image, ImageTk

class FishbotSetup:
    """Setup utility for configuring the fishbot"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fishbot Setup")
        self.root.geometry("800x600")
        
        self.detection_area = (400, 200, 800, 600)  # x, y, width, height
        self.screenshot = None
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the GUI elements"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Fishbot Setup & Configuration", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Detection area frame
        area_frame = ttk.LabelFrame(main_frame, text="Detection Area Configuration", padding="10")
        area_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Current area display
        ttk.Label(area_frame, text="Current Detection Area:").grid(row=0, column=0, sticky=tk.W)
        self.area_label = ttk.Label(area_frame, text=str(self.detection_area))
        self.area_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Area adjustment controls
        ttk.Label(area_frame, text="X:").grid(row=1, column=0, sticky=tk.W)
        self.x_var = tk.IntVar(value=self.detection_area[0])
        ttk.Entry(area_frame, textvariable=self.x_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(area_frame, text="Y:").grid(row=1, column=2, sticky=tk.W, padx=(20, 0))
        self.y_var = tk.IntVar(value=self.detection_area[1])
        ttk.Entry(area_frame, textvariable=self.y_var, width=10).grid(row=1, column=3, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(area_frame, text="Width:").grid(row=2, column=0, sticky=tk.W)
        self.width_var = tk.IntVar(value=self.detection_area[2])
        ttk.Entry(area_frame, textvariable=self.width_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(area_frame, text="Height:").grid(row=2, column=2, sticky=tk.W, padx=(20, 0))
        self.height_var = tk.IntVar(value=self.detection_area[3])
        ttk.Entry(area_frame, textvariable=self.height_var, width=10).grid(row=2, column=3, sticky=tk.W, padx=(5, 0))
        
        ttk.Button(area_frame, text="Update Area", command=self.update_detection_area).grid(row=3, column=0, pady=(10, 0))
        ttk.Button(area_frame, text="Preview Area", command=self.preview_area).grid(row=3, column=1, pady=(10, 0))
        
        # Screenshot frame
        screenshot_frame = ttk.LabelFrame(main_frame, text="Screen Capture", padding="10")
        screenshot_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(screenshot_frame, text="Take Screenshot", command=self.take_screenshot).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(screenshot_frame, text="Capture Detection Area", command=self.capture_detection_area).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(screenshot_frame, text="Save Bobber Template", command=self.save_bobber_template).grid(row=0, column=2)
        
        # Preview canvas
        self.canvas = tk.Canvas(main_frame, width=600, height=300, bg='lightgray')
        self.canvas.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        # Instructions
        instructions_frame = ttk.LabelFrame(main_frame, text="Instructions", padding="10")
        instructions_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        instructions_text = """1. Position your Game window and cast your fishing line
2. Adjust the detection area to cover the water where your bobber appears
3. Take a screenshot to preview the area
4. Capture the detection area when your bobber is visible
5. Save the bobber template for better detection
6. The bot will use this configuration for automated fishing"""
        
        ttk.Label(instructions_frame, text=instructions_text, justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
        
        # Save/Load buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(button_frame, text="Save Configuration", command=self.save_config).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Load Configuration", command=self.load_config).grid(row=0, column=1)
    
    def update_detection_area(self):
        """Update the detection area from GUI inputs"""
        self.detection_area = (
            self.x_var.get(),
            self.y_var.get(),
            self.width_var.get(),
            self.height_var.get()
        )
        self.area_label.config(text=str(self.detection_area))
    
    def preview_area(self):
        """Preview the detection area on screen"""
        try:
            # Take a screenshot of the entire screen
            screenshot = pyautogui.screenshot()
            
            # Draw a red rectangle over the detection area
            import PIL.ImageDraw as ImageDraw
            draw = ImageDraw.Draw(screenshot)
            x, y, w, h = self.detection_area
            draw.rectangle([x, y, x+w, y+h], outline="red", width=3)
            
            # Show preview window
            preview_window = tk.Toplevel(self.root)
            preview_window.title("Detection Area Preview")
            
            # Resize for display
            display_width = 800
            display_height = 600
            screenshot_resized = screenshot.resize((display_width, display_height), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(screenshot_resized)
            label = ttk.Label(preview_window, image=photo)
            label.image = photo  # Keep a reference
            label.pack()
            
            ttk.Button(preview_window, text="Close", command=preview_window.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview area: {e}")
    
    def take_screenshot(self):
        """Take a screenshot and display it"""
        try:
            self.screenshot = pyautogui.screenshot()
            
            # Resize for canvas display
            canvas_width = 600
            canvas_height = 300
            screenshot_resized = self.screenshot.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
            
            self.photo = ImageTk.PhotoImage(screenshot_resized)
            self.canvas.delete("all")
            self.canvas.create_image(canvas_width//2, canvas_height//2, image=self.photo)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to take screenshot: {e}")
    
    def capture_detection_area(self):
        """Capture just the detection area"""
        try:
            x, y, w, h = self.detection_area
            area_screenshot = pyautogui.screenshot(region=(x, y, w, h))
            
            # Display in canvas
            canvas_width = 600
            canvas_height = 300
            area_resized = area_screenshot.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
            
            self.photo = ImageTk.PhotoImage(area_resized)
            self.canvas.delete("all")
            self.canvas.create_image(canvas_width//2, canvas_height//2, image=self.photo)
            
            # Save for template creation
            self.area_screenshot = area_screenshot
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture detection area: {e}")
    
    def save_bobber_template(self):
        """Save a bobber template from the current area screenshot"""
        if not hasattr(self, 'area_screenshot'):
            messagebox.showwarning("Warning", "Please capture the detection area first")
            return
        
        try:
            # Create templates directory if it doesn't exist
            os.makedirs('templates', exist_ok=True)
            
            # Save the area screenshot as bobber template
            template_path = 'templates/bobber.png'
            self.area_screenshot.save(template_path)
            
            # Also save as numpy array for OpenCV
            import cv2
            cv_image = cv2.cvtColor(np.array(self.area_screenshot), cv2.COLOR_RGB2BGR)
            cv2.imwrite('templates/bobber_cv.png', cv_image)
            
            messagebox.showinfo("Success", f"Bobber template saved to {template_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save template: {e}")
    
    def save_config(self):
        """Save the current configuration"""
        try:
            config = {
                "bobber_detection_area": self.detection_area,
                "fishing_key": "1",
                "loot_key": "shift+right",
                "splash_threshold": 0.7,
                "reaction_delay_min": 0.1,
                "reaction_delay_max": 0.3,
                "cast_delay": 2.0,
                "timeout_duration": 30.0,
                "enable_sound_detection": True,
                "enable_visual_detection": True,
                "auto_loot": True
            }
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialvalue="fishbot_config.json"
            )
            
            if filename:
                with open(filename, 'w') as f:
                    json.dump(config, f, indent=4)
                messagebox.showinfo("Success", f"Configuration saved to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
    
    def load_config(self):
        """Load configuration from file"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'r') as f:
                    config = json.load(f)
                
                if "bobber_detection_area" in config:
                    self.detection_area = tuple(config["bobber_detection_area"])
                    self.x_var.set(self.detection_area[0])
                    self.y_var.set(self.detection_area[1])
                    self.width_var.set(self.detection_area[2])
                    self.height_var.set(self.detection_area[3])
                    self.area_label.config(text=str(self.detection_area))
                
                messagebox.showinfo("Success", f"Configuration loaded from {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {e}")
    
    def run(self):
        """Run the setup GUI"""
        self.root.mainloop()

def main():
    """Main entry point"""
    print("Fishbot Setup Utility")
    print("========================")
    print("This utility helps you configure the fishbot detection areas and templates.")
    print()
    
    app = FishbotSetup()
    app.run()

if __name__ == "__main__":
    main()