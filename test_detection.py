#!/usr/bin/env python3
"""
Test script for WoW Fishbot detection methods
This script helps verify that visual and audio detection are working correctly
"""

import cv2
import numpy as np
import pyautogui
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import json

class DetectionTester:
    """Test utility for verifying detection methods"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fishbot Detection Tester")
        self.root.geometry("900x700")
        
        self.detection_area = (400, 200, 800, 600)
        self.is_testing = False
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the test GUI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Detection Method Tester", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Configuration frame
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Detection area
        ttk.Label(config_frame, text="Detection Area (x, y, w, h):").grid(row=0, column=0, sticky=tk.W)
        self.area_entry = ttk.Entry(config_frame, width=30)
        self.area_entry.insert(0, f"{self.detection_area[0]}, {self.detection_area[1]}, {self.detection_area[2]}, {self.detection_area[3]}")
        self.area_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Button(config_frame, text="Update", command=self.update_area).grid(row=0, column=2, padx=(10, 0))
        
        # Test controls
        test_frame = ttk.LabelFrame(main_frame, text="Tests", padding="10")
        test_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(test_frame, text="Test Visual Detection", command=self.test_visual).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(test_frame, text="Test Audio Detection", command=self.test_audio).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(test_frame, text="Test Motion Detection", command=self.test_motion).grid(row=0, column=2)
        
        ttk.Button(test_frame, text="Continuous Test", command=self.start_continuous_test).grid(row=1, column=0, pady=(10, 0))
        ttk.Button(test_frame, text="Stop Test", command=self.stop_test).grid(row=1, column=1, pady=(10, 0))
        ttk.Button(test_frame, text="Capture Screenshot", command=self.capture_screenshot).grid(row=1, column=2, pady=(10, 0))
        
        # Results display
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Canvas for image display
        self.canvas = tk.Canvas(results_frame, width=600, height=300, bg='lightgray')
        self.canvas.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Text output
        self.output_text = tk.Text(results_frame, height=10, width=80)
        self.output_text.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
    def log(self, message):
        """Log message to output text"""
        timestamp = time.strftime("%H:%M:%S")
        self.output_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.output_text.see(tk.END)
        self.root.update()
        
    def update_area(self):
        """Update detection area from entry"""
        try:
            coords = [int(x.strip()) for x in self.area_entry.get().split(',')]
            if len(coords) == 4:
                self.detection_area = tuple(coords)
                self.log(f"Detection area updated to: {self.detection_area}")
            else:
                raise ValueError("Need 4 coordinates")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid coordinates: {e}")
    
    def capture_area(self):
        """Capture the detection area"""
        x, y, w, h = self.detection_area
        screenshot = pyautogui.screenshot(region=(x, y, w, h))
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    def test_visual(self):
        """Test visual splash detection"""
        self.log("Testing visual detection...")
        
        try:
            screen = self.capture_area()
            
            # Convert to HSV for color detection
            hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
            
            # Define color ranges for splash (white/light blue)
            lower_splash = np.array([0, 0, 200])
            upper_splash = np.array([180, 30, 255])
            
            mask = cv2.inRange(hsv, lower_splash, upper_splash)
            
            # Count white pixels
            white_pixels = np.sum(mask == 255)
            total_pixels = mask.shape[0] * mask.shape[1]
            splash_ratio = white_pixels / total_pixels
            
            self.log(f"Splash ratio: {splash_ratio:.4f}")
            self.log(f"White pixels: {white_pixels}/{total_pixels}")
            
            # Display result
            self.display_image(mask, "Visual Detection Mask")
            
            if splash_ratio > 0.02:
                self.log("✅ SPLASH DETECTED!")
            else:
                self.log("❌ No splash detected")
                
        except Exception as e:
            self.log(f"❌ Visual test error: {e}")
    
    def test_audio(self):
        """Test audio detection"""
        self.log("Testing audio detection for 5 seconds...")
        
        def audio_test():
            try:
                import pyaudio
                import audioop
                
                CHUNK = 1024
                FORMAT = pyaudio.paInt16
                CHANNELS = 1
                RATE = 44100
                
                p = pyaudio.PyAudio()
                stream = p.open(format=FORMAT,
                              channels=CHANNELS,
                              rate=RATE,
                              input=True,
                              frames_per_buffer=CHUNK)
                
                max_volume = 0
                start_time = time.time()
                
                while time.time() - start_time < 5:
                    try:
                        data = stream.read(CHUNK, exception_on_overflow=False)
                        volume = audioop.rms(data, 2)
                        max_volume = max(max_volume, volume)
                        
                        if volume > 3000:
                            self.log(f"🔊 LOUD SOUND DETECTED! Volume: {volume}")
                        
                    except Exception as e:
                        self.log(f"Audio processing error: {e}")
                
                stream.stop_stream()
                stream.close()
                p.terminate()
                
                self.log(f"Audio test complete. Max volume: {max_volume}")
                
                if max_volume > 3000:
                    self.log("✅ Audio detection working - detected loud sounds")
                else:
                    self.log("⚠️ No loud sounds detected - try making noise or adjusting threshold")
                    
            except ImportError:
                self.log("❌ PyAudio not available for audio testing")
            except Exception as e:
                self.log(f"❌ Audio test error: {e}")
        
        # Run audio test in separate thread
        audio_thread = threading.Thread(target=audio_test)
        audio_thread.daemon = True
        audio_thread.start()
    
    def test_motion(self):
        """Test motion detection"""
        self.log("Testing motion detection...")
        self.log("Move something in the detection area...")
        
        def motion_test():
            try:
                # Capture initial frame
                previous_frame = self.capture_area()
                time.sleep(2)
                
                for i in range(10):
                    current_frame = self.capture_area()
                    
                    # Calculate frame difference
                    diff = cv2.absdiff(previous_frame, current_frame)
                    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                    
                    # Apply threshold
                    _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
                    
                    # Count motion pixels
                    motion_pixels = np.sum(thresh == 255)
                    total_pixels = thresh.shape[0] * thresh.shape[1]
                    motion_ratio = motion_pixels / total_pixels
                    
                    self.log(f"Frame {i+1}: Motion ratio = {motion_ratio:.4f}")
                    
                    if motion_ratio > 0.05:
                        self.log("🎯 MOTION DETECTED!")
                        self.display_image(thresh, "Motion Detection")
                    
                    previous_frame = current_frame.copy()
                    time.sleep(0.5)
                
                self.log("Motion test complete")
                
            except Exception as e:
                self.log(f"❌ Motion test error: {e}")
        
        # Run motion test in separate thread
        motion_thread = threading.Thread(target=motion_test)
        motion_thread.daemon = True
        motion_thread.start()
    
    def start_continuous_test(self):
        """Start continuous detection testing"""
        if self.is_testing:
            return
            
        self.is_testing = True
        self.log("Starting continuous detection test...")
        
        def continuous_test():
            previous_frame = None
            
            while self.is_testing:
                try:
                    # Visual detection
                    current_frame = self.capture_area()
                    
                    # Motion detection
                    if previous_frame is not None:
                        diff = cv2.absdiff(previous_frame, current_frame)
                        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                        _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
                        
                        motion_pixels = np.sum(thresh == 255)
                        total_pixels = thresh.shape[0] * thresh.shape[1]
                        motion_ratio = motion_pixels / total_pixels
                        
                        if motion_ratio > 0.05:
                            self.log(f"🎯 Motion detected: {motion_ratio:.4f}")
                    
                    # Color detection
                    hsv = cv2.cvtColor(current_frame, cv2.COLOR_BGR2HSV)
                    lower_splash = np.array([0, 0, 200])
                    upper_splash = np.array([180, 30, 255])
                    mask = cv2.inRange(hsv, lower_splash, upper_splash)
                    
                    white_pixels = np.sum(mask == 255)
                    total_pixels = mask.shape[0] * mask.shape[1]
                    splash_ratio = white_pixels / total_pixels
                    
                    if splash_ratio > 0.02:
                        self.log(f"💧 Splash detected: {splash_ratio:.4f}")
                    
                    previous_frame = current_frame.copy()
                    time.sleep(0.2)
                    
                except Exception as e:
                    self.log(f"❌ Continuous test error: {e}")
                    break
            
            self.log("Continuous test stopped")
        
        test_thread = threading.Thread(target=continuous_test)
        test_thread.daemon = True
        test_thread.start()
    
    def stop_test(self):
        """Stop continuous testing"""
        self.is_testing = False
        self.log("Stopping continuous test...")
    
    def capture_screenshot(self):
        """Capture and display current detection area"""
        try:
            screen = self.capture_area()
            self.display_image(screen, "Current Detection Area")
            self.log("Screenshot captured and displayed")
        except Exception as e:
            self.log(f"❌ Screenshot error: {e}")
    
    def display_image(self, image, title="Image"):
        """Display image in canvas"""
        try:
            # Convert to RGB for display
            if len(image.shape) == 3:
                display_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                display_img = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            
            # Resize for canvas
            height, width = display_img.shape[:2]
            canvas_width, canvas_height = 600, 300
            
            # Calculate scaling
            scale = min(canvas_width/width, canvas_height/height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            
            resized = cv2.resize(display_img, (new_width, new_height))
            
            # Convert to PhotoImage
            pil_image = Image.fromarray(resized)
            self.photo = ImageTk.PhotoImage(pil_image)
            
            # Display in canvas
            self.canvas.delete("all")
            self.canvas.create_image(canvas_width//2, canvas_height//2, image=self.photo)
            self.canvas.create_text(10, 10, text=title, anchor="nw", fill="white", font=("Arial", 12, "bold"))
            
        except Exception as e:
            self.log(f"❌ Display error: {e}")
    
    def run(self):
        """Run the tester"""
        self.root.mainloop()

def main():
    """Main entry point"""
    print("Fishbot Detection Tester")
    print("=======================")
    print("This utility helps test and verify detection methods")
    print()
    
    app = DetectionTester()
    app.run()

if __name__ == "__main__":
    main()