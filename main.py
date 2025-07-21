#!/usr/bin/env python3
"""
World of Warcraft Fishbot - Educational Implementation
This bot demonstrates automation concepts for educational purposes.
"""

import cv2
import numpy as np
import pyautogui
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from PIL import Image, ImageTk
import os
import json
from dataclasses import dataclass, asdict
from typing import Optional, Tuple, List
import keyboard

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fishbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class FishbotConfig:
    """Configuration settings for the fishbot"""
    fishing_key: str = "1"
    loot_key: str = "shift+right"
    bobber_detection_area: Tuple[int, int, int, int] = (400, 200, 800, 600)
    splash_threshold: float = 0.7
    reaction_delay_min: float = 0.1
    reaction_delay_max: float = 0.3
    cast_delay: float = 2.0
    timeout_duration: float = 30.0
    enable_sound_detection: bool = True
    enable_visual_detection: bool = True
    auto_loot: bool = True

class SoundDetector:
    """Detects fishing sounds using audio analysis"""
    
    def __init__(self):
        self.is_listening = False
        self.sound_detected = False
        
    def start_listening(self):
        """Start listening for fishing sounds"""
        try:
            import pyaudio
            import audioop
            self.is_listening = True
            self.sound_detected = False
            
            # Audio parameters
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
            
            logger.info("Sound detection started")
            
            while self.is_listening:
                try:
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    volume = audioop.rms(data, 2)
                    
                    # Detect sudden volume spikes (splash sound)
                    if volume > 3000:  # Adjust threshold as needed
                        self.sound_detected = True
                        logger.info(f"Sound detected: volume {volume}")
                        break
                        
                except Exception as e:
                    logger.error(f"Audio processing error: {e}")
                    
            stream.stop_stream()
            stream.close()
            p.terminate()
            
        except ImportError:
            logger.warning("PyAudio not available, sound detection disabled")
        except Exception as e:
            logger.error(f"Sound detection error: {e}")
    
    def stop_listening(self):
        """Stop listening for sounds"""
        self.is_listening = False

class VisualDetector:
    """Detects bobber and splash using computer vision"""
    
    def __init__(self, config: FishbotConfig):
        self.config = config
        self.bobber_template = None
        self.splash_template = None
        self.load_templates()
    
    def load_templates(self):
        """Load bobber and splash templates if available"""
        try:
            if os.path.exists('templates/bobber.png'):
                self.bobber_template = cv2.imread('templates/bobber.png', 0)
            if os.path.exists('templates/splash.png'):
                self.splash_template = cv2.imread('templates/splash.png', 0)
        except Exception as e:
            logger.error(f"Error loading templates: {e}")
    
    def capture_screen_area(self, area: Tuple[int, int, int, int]) -> np.ndarray:
        """Capture a specific area of the screen"""
        x, y, w, h = area
        screenshot = pyautogui.screenshot(region=(x, y, w, h))
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    def detect_bobber(self) -> Optional[Tuple[int, int]]:
        """Detect bobber position using template matching"""
        if self.bobber_template is None:
            return None
            
        screen = self.capture_screen_area(self.config.bobber_detection_area)
        gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        
        result = cv2.matchTemplate(gray_screen, self.bobber_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val > 0.8:  # High confidence threshold
            return max_loc
        return None
    
    def detect_splash(self) -> bool:
        """Detect splash effect around bobber area"""
        screen = self.capture_screen_area(self.config.bobber_detection_area)
        
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
        
        # Define white/light blue color range for splash
        lower_splash = np.array([0, 0, 200])
        upper_splash = np.array([180, 30, 255])
        
        mask = cv2.inRange(hsv, lower_splash, upper_splash)
        
        # Count white pixels (splash indicators)
        white_pixels = np.sum(mask == 255)
        total_pixels = mask.shape[0] * mask.shape[1]
        
        splash_ratio = white_pixels / total_pixels
        
        logger.debug(f"Splash ratio: {splash_ratio}")
        return splash_ratio > 0.02  # Adjust threshold as needed
    
    def detect_motion(self, previous_frame: np.ndarray, current_frame: np.ndarray) -> bool:
        """Detect motion in the bobber area"""
        if previous_frame is None:
            return False
            
        # Calculate frame difference
        diff = cv2.absdiff(previous_frame, current_frame)
        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold
        _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
        
        # Count motion pixels
        motion_pixels = np.sum(thresh == 255)
        total_pixels = thresh.shape[0] * thresh.shape[1]
        
        motion_ratio = motion_pixels / total_pixels
        return motion_ratio > 0.05  # Adjust threshold as needed

class FishBot:
    """Main fishing bot class"""
    
    def __init__(self):
        self.config = FishbotConfig()
        self.is_running = False
        self.is_paused = False
        self.visual_detector = VisualDetector(self.config)
        self.sound_detector = SoundDetector()
        self.stats = {
            'casts': 0,
            'catches': 0,
            'start_time': None,
            'runtime': 0
        }
        self.previous_frame = None
        
        # Setup hotkeys
        keyboard.add_hotkey('f9', self.toggle_bot)
        keyboard.add_hotkey('f10', self.pause_resume)
        keyboard.add_hotkey('f11', self.stop_bot)
    
    def load_config(self, filename: str = 'fishbot_config.json'):
        """Load configuration from file"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    config_dict = json.load(f)
                    self.config = FishbotConfig(**config_dict)
                logger.info("Configuration loaded successfully")
        except Exception as e:
            logger.error(f"Error loading config: {e}")
    
    def save_config(self, filename: str = 'fishbot_config.json'):
        """Save configuration to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(asdict(self.config), f, indent=4)
            logger.info("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def cast_line(self):
        """Cast the fishing line"""
        logger.info("Casting fishing line")
        pyautogui.press(self.config.fishing_key)
        self.stats['casts'] += 1
        time.sleep(self.config.cast_delay)
    
    def loot_fish(self):
        """Loot the caught fish"""
        if self.config.auto_loot:
            logger.info("Looting fish")
            pyautogui.hotkey(*self.config.loot_key.split('+'))
            self.stats['catches'] += 1
            time.sleep(0.5)
    
    def wait_for_bite(self) -> bool:
        """Wait for fish to bite using multiple detection methods"""
        start_time = time.time()
        
        # Start sound detection in separate thread if enabled
        if self.config.enable_sound_detection:
            sound_thread = threading.Thread(target=self.sound_detector.start_listening)
            sound_thread.daemon = True
            sound_thread.start()
        
        while time.time() - start_time < self.config.timeout_duration:
            if not self.is_running or self.is_paused:
                return False
            
            # Visual detection
            if self.config.enable_visual_detection:
                current_frame = self.visual_detector.capture_screen_area(
                    self.config.bobber_detection_area
                )
                
                # Check for splash
                if self.visual_detector.detect_splash():
                    logger.info("Splash detected!")
                    self.sound_detector.stop_listening()
                    return True
                
                # Check for motion
                if (self.previous_frame is not None and 
                    self.visual_detector.detect_motion(self.previous_frame, current_frame)):
                    logger.info("Motion detected!")
                    self.sound_detector.stop_listening()
                    return True
                
                self.previous_frame = current_frame.copy()
            
            # Sound detection
            if self.config.enable_sound_detection and self.sound_detector.sound_detected:
                logger.info("Sound detected!")
                return True
            
            time.sleep(0.1)  # Small delay to prevent excessive CPU usage
        
        logger.info("Fishing timeout reached")
        self.sound_detector.stop_listening()
        return False
    
    def fishing_cycle(self):
        """Complete fishing cycle"""
        self.cast_line()
        
        if self.wait_for_bite():
            # Add reaction delay to simulate human response
            reaction_delay = np.random.uniform(
                self.config.reaction_delay_min,
                self.config.reaction_delay_max
            )
            time.sleep(reaction_delay)
            
            self.loot_fish()
            time.sleep(1)  # Wait before next cast
        else:
            time.sleep(0.5)  # Short delay before recasting
    
    def start_bot(self):
        """Start the fishing bot"""
        if self.is_running:
            return
            
        logger.info("Starting fishing bot")
        self.is_running = True
        self.is_paused = False
        self.stats['start_time'] = time.time()
        
        try:
            while self.is_running:
                if not self.is_paused:
                    self.fishing_cycle()
                else:
                    time.sleep(0.5)
                    
        except KeyboardInterrupt:
            logger.info("Bot interrupted by user")
        except Exception as e:
            logger.error(f"Bot error: {e}")
        finally:
            self.stop_bot()
    
    def stop_bot(self):
        """Stop the fishing bot"""
        logger.info("Stopping fishing bot")
        self.is_running = False
        self.is_paused = False
        self.sound_detector.stop_listening()
        
        if self.stats['start_time']:
            self.stats['runtime'] = time.time() - self.stats['start_time']
        
        self.print_stats()
    
    def toggle_bot(self):
        """Toggle bot on/off"""
        if self.is_running:
            self.stop_bot()
        else:
            bot_thread = threading.Thread(target=self.start_bot)
            bot_thread.daemon = True
            bot_thread.start()
    
    def pause_resume(self):
        """Pause or resume the bot"""
        if self.is_running:
            self.is_paused = not self.is_paused
            status = "paused" if self.is_paused else "resumed"
            logger.info(f"Bot {status}")
    
    def print_stats(self):
        """Print fishing statistics"""
        runtime_minutes = self.stats['runtime'] / 60
        catch_rate = (self.stats['catches'] / self.stats['casts'] * 100) if self.stats['casts'] > 0 else 0
        
        logger.info("=== Fishing Statistics ===")
        logger.info(f"Runtime: {runtime_minutes:.1f} minutes")
        logger.info(f"Total casts: {self.stats['casts']}")
        logger.info(f"Total catches: {self.stats['catches']}")
        logger.info(f"Catch rate: {catch_rate:.1f}%")
        logger.info(f"Catches per hour: {(self.stats['catches'] / runtime_minutes * 60):.1f}")

class FishBotGUI:
    """GUI interface for the fishing bot"""
    
    def __init__(self):
        self.bot = FishBot()
        self.root = tk.Tk()
        self.root.title("WoW Fishing Bot - Educational")
        self.root.geometry("600x500")
        self.setup_gui()
        
        # Update stats every second
        self.update_stats()
    
    def setup_gui(self):
        """Setup the GUI elements"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="WoW Fishing Bot", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Control buttons
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.start_button = ttk.Button(control_frame, text="Start Bot (F9)", command=self.toggle_bot)
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        self.pause_button = ttk.Button(control_frame, text="Pause/Resume (F10)", command=self.pause_resume)
        self.pause_button.grid(row=0, column=1, padx=(0, 10))
        
        self.stop_button = ttk.Button(control_frame, text="Stop (F11)", command=self.stop_bot)
        self.stop_button.grid(row=0, column=2)
        
        # Configuration frame
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Fishing key
        ttk.Label(config_frame, text="Fishing Key:").grid(row=0, column=0, sticky=tk.W)
        self.fishing_key_var = tk.StringVar(value=self.bot.config.fishing_key)
        ttk.Entry(config_frame, textvariable=self.fishing_key_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Loot key
        ttk.Label(config_frame, text="Loot Key:").grid(row=1, column=0, sticky=tk.W)
        self.loot_key_var = tk.StringVar(value=self.bot.config.loot_key)
        ttk.Entry(config_frame, textvariable=self.loot_key_var, width=15).grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # Detection options
        self.visual_detection_var = tk.BooleanVar(value=self.bot.config.enable_visual_detection)
        ttk.Checkbutton(config_frame, text="Visual Detection", variable=self.visual_detection_var).grid(row=2, column=0, sticky=tk.W)
        
        self.sound_detection_var = tk.BooleanVar(value=self.bot.config.enable_sound_detection)
        ttk.Checkbutton(config_frame, text="Sound Detection", variable=self.sound_detection_var).grid(row=2, column=1, sticky=tk.W)
        
        self.auto_loot_var = tk.BooleanVar(value=self.bot.config.auto_loot)
        ttk.Checkbutton(config_frame, text="Auto Loot", variable=self.auto_loot_var).grid(row=3, column=0, sticky=tk.W)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="10")
        stats_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.stats_text = tk.Text(stats_frame, height=8, width=60)
        self.stats_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Scrollbar for stats
        stats_scrollbar = ttk.Scrollbar(stats_frame, orient="vertical", command=self.stats_text.yview)
        stats_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.stats_text.configure(yscrollcommand=stats_scrollbar.set)
        
        # Save/Load config buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(button_frame, text="Save Config", command=self.save_config).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Load Config", command=self.load_config).grid(row=0, column=1)
    
    def update_config(self):
        """Update bot configuration from GUI"""
        self.bot.config.fishing_key = self.fishing_key_var.get()
        self.bot.config.loot_key = self.loot_key_var.get()
        self.bot.config.enable_visual_detection = self.visual_detection_var.get()
        self.bot.config.enable_sound_detection = self.sound_detection_var.get()
        self.bot.config.auto_loot = self.auto_loot_var.get()
    
    def toggle_bot(self):
        """Toggle bot on/off"""
        self.update_config()
        self.bot.toggle_bot()
        
        if self.bot.is_running:
            self.start_button.config(text="Stop Bot (F9)")
        else:
            self.start_button.config(text="Start Bot (F9)")
    
    def pause_resume(self):
        """Pause or resume the bot"""
        self.bot.pause_resume()
    
    def stop_bot(self):
        """Stop the bot"""
        self.bot.stop_bot()
        self.start_button.config(text="Start Bot (F9)")
    
    def save_config(self):
        """Save configuration"""
        self.update_config()
        self.bot.save_config()
        messagebox.showinfo("Config", "Configuration saved successfully!")
    
    def load_config(self):
        """Load configuration"""
        self.bot.load_config()
        self.fishing_key_var.set(self.bot.config.fishing_key)
        self.loot_key_var.set(self.bot.config.loot_key)
        self.visual_detection_var.set(self.bot.config.enable_visual_detection)
        self.sound_detection_var.set(self.bot.config.enable_sound_detection)
        self.auto_loot_var.set(self.bot.config.auto_loot)
        messagebox.showinfo("Config", "Configuration loaded successfully!")
    
    def update_stats(self):
        """Update statistics display"""
        runtime = 0
        if self.bot.stats['start_time'] and self.bot.is_running:
            runtime = time.time() - self.bot.stats['start_time']
        elif self.bot.stats['runtime']:
            runtime = self.bot.stats['runtime']
        
        runtime_minutes = runtime / 60
        catch_rate = (self.bot.stats['catches'] / self.bot.stats['casts'] * 100) if self.bot.stats['casts'] > 0 else 0
        catches_per_hour = (self.bot.stats['catches'] / runtime_minutes * 60) if runtime_minutes > 0 else 0
        
        status = "Running" if self.bot.is_running else "Stopped"
        if self.bot.is_paused:
            status = "Paused"
        
        stats_text = f"""Status: {status}
Runtime: {runtime_minutes:.1f} minutes
Total Casts: {self.bot.stats['casts']}
Total Catches: {self.bot.stats['catches']}
Catch Rate: {catch_rate:.1f}%
Catches/Hour: {catches_per_hour:.1f}

Hotkeys:
F9 - Start/Stop Bot
F10 - Pause/Resume
F11 - Stop Bot

Detection Area: {self.bot.config.bobber_detection_area}
Visual Detection: {'Enabled' if self.bot.config.enable_visual_detection else 'Disabled'}
Sound Detection: {'Enabled' if self.bot.config.enable_sound_detection else 'Disabled'}
Auto Loot: {'Enabled' if self.bot.config.auto_loot else 'Disabled'}
"""
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        
        # Schedule next update
        self.root.after(1000, self.update_stats)
    
    def run(self):
        """Run the GUI"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.bot.stop_bot()

def main():
    """Main entry point"""
    print("WoW Fishing Bot - Educational Implementation")
    print("==========================================")
    print("This bot is for educational purposes only.")
    print("Use responsibly and in accordance with game terms of service.")
    print()
    print("Controls:")
    print("F9 - Start/Stop Bot")
    print("F10 - Pause/Resume")
    print("F11 - Stop Bot")
    print()
    
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Choose interface
    import sys
    if '--gui' in sys.argv or len(sys.argv) == 1:
        # GUI mode
        app = FishBotGUI()
        app.run()
    else:
        # CLI mode
        bot = FishBot()
        bot.load_config()
        
        try:
            print("Starting bot in CLI mode...")
            print("Press Ctrl+C to stop")
            bot.start_bot()
        except KeyboardInterrupt:
            print("\nBot stopped by user")
        finally:
            bot.stop_bot()

if __name__ == "__main__":
    main()