# WoW Fishing Bot - Educational Implementation

## ⚠️ Educational Purpose Disclaimer

**This fishing bot is created for educational purposes only to demonstrate:**
- Computer vision techniques using OpenCV
- Audio processing and sound detection
- GUI development with Tkinter
- Automation concepts and machine learning
- Game interaction programming

**Important Notes:**
- This project is intended for learning programming concepts
- Use only on private servers or for educational testing
- Always respect game terms of service
- The author is not responsible for any consequences of misuse

## Features

### 🎣 Core Functionality
- **Automated Fishing**: Casts fishing line and detects fish bites
- **Multi-Detection**: Uses both visual and audio detection methods
- **Smart Timing**: Human-like reaction delays and randomization
- **Auto-Looting**: Automatically loots caught fish
- **Statistics Tracking**: Monitors catch rates and efficiency

### 🔍 Detection Methods
- **Visual Detection**: 
  - Motion detection using frame differencing
  - Color-based splash detection
  - Template matching for bobber recognition
- **Audio Detection**: 
  - Real-time sound monitoring
  - Volume spike detection for splash sounds
- **Configurable Areas**: Custom detection zones

### 🖥️ User Interface
- **GUI Mode**: User-friendly graphical interface
- **CLI Mode**: Command-line operation
- **Setup Utility**: Easy configuration and calibration
- **Real-time Statistics**: Live performance monitoring
- **Hotkey Controls**: F9/F10/F11 for quick control

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows/Linux/macOS
- Microphone (for audio detection)
- World of Warcraft client

### Install Dependencies

```bash
# Clone or download the project
cd wow_fishbot

# Install required packages
pip install -r requirements.txt
```

### Linux Additional Requirements
```bash
# For audio support on Linux
sudo apt-get install portaudio19-dev python3-pyaudio

# For GUI support
sudo apt-get install python3-tk

# For screen capture
sudo apt-get install scrot
```

### macOS Additional Requirements
```bash
# Install portaudio for audio support
brew install portaudio

# Install additional dependencies
pip install pyobjc-framework-Quartz
```

## Quick Start

### 1. Setup and Configuration

Run the setup utility to configure detection areas:

```bash
python setup_detector.py
```

**Setup Steps:**
1. Position your WoW window
2. Cast your fishing line to see the bobber
3. Adjust the detection area to cover the water
4. Take screenshots to verify the area
5. Save bobber templates for better detection
6. Save your configuration

### 2. Running the Bot

**GUI Mode (Recommended):**
```bash
python main.py
# or
python main.py --gui
```

**Command Line Mode:**
```bash
python main.py --cli
```

### 3. In-Game Setup

1. **Position Character**: Stand near water with fishing rod equipped
2. **Keybind Setup**: 
   - Fishing: Assign to key "1" (configurable)
   - Loot: Use "Shift+Right Click" (configurable)
3. **Audio**: Ensure game sounds are enabled
4. **Graphics**: Set to a stable framerate for consistent detection

## Configuration

### Default Settings
```json
{
    "fishing_key": "1",
    "loot_key": "shift+right",
    "bobber_detection_area": [400, 200, 800, 600],
    "splash_threshold": 0.7,
    "reaction_delay_min": 0.1,
    "reaction_delay_max": 0.3,
    "cast_delay": 2.0,
    "timeout_duration": 30.0,
    "enable_sound_detection": true,
    "enable_visual_detection": true,
    "auto_loot": true
}
```

### Key Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| `fishing_key` | Key to cast fishing line | "1" |
| `loot_key` | Key combination to loot | "shift+right" |
| `bobber_detection_area` | Screen area to monitor [x, y, w, h] | [400, 200, 800, 600] |
| `reaction_delay_min/max` | Human-like reaction time (seconds) | 0.1 - 0.3 |
| `timeout_duration` | Max time to wait for bite (seconds) | 30.0 |

## Controls

### Hotkeys (Global)
- **F9**: Start/Stop Bot
- **F10**: Pause/Resume
- **F11**: Emergency Stop

### GUI Controls
- **Start/Stop**: Toggle bot operation
- **Pause/Resume**: Temporarily pause without losing state
- **Configuration**: Adjust settings without restart
- **Statistics**: Real-time performance monitoring

## Detection Tuning

### Visual Detection
- **Motion Sensitivity**: Adjust threshold for bobber movement
- **Color Detection**: Tune splash color ranges
- **Template Matching**: Create custom bobber templates

### Audio Detection
- **Volume Threshold**: Adjust for splash sound sensitivity
- **Background Noise**: Account for ambient game sounds
- **Sample Rate**: Configure audio processing parameters

## Troubleshooting

### Common Issues

**Bot not detecting bites:**
- Check detection area covers bobber location
- Verify audio levels and microphone access
- Adjust sensitivity thresholds
- Ensure stable game framerate

**False positives:**
- Increase reaction delays
- Narrow detection area
- Adjust color/motion thresholds
- Use template matching

**Performance issues:**
- Reduce detection area size
- Disable unused detection methods
- Lower screen resolution
- Close unnecessary applications

### Debug Mode

Enable detailed logging:
```python
# In main.py, change logging level
logging.basicConfig(level=logging.DEBUG)
```

## File Structure

```
wow_fishbot/
├── main.py              # Main bot application
├── setup_detector.py    # Configuration utility
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── templates/          # Bobber templates (created)
├── logs/              # Log files (created)
└── fishbot_config.json # Configuration (created)
```

## Technical Implementation

### Computer Vision
- **OpenCV**: Image processing and template matching
- **NumPy**: Array operations and mathematical computations
- **PIL**: Screenshot capture and image manipulation

### Audio Processing
- **PyAudio**: Real-time audio stream processing
- **audioop**: Audio signal analysis
- **Threading**: Non-blocking audio monitoring

### Automation
- **PyAutoGUI**: Mouse and keyboard simulation
- **Keyboard**: Global hotkey management
- **Threading**: Concurrent operation handling

## Educational Value

This project demonstrates several important programming concepts:

1. **Computer Vision**: Image processing, template matching, color detection
2. **Signal Processing**: Audio analysis, noise filtering, pattern recognition
3. **GUI Development**: Event-driven programming, real-time updates
4. **Automation**: Input simulation, state machines, timing
5. **Threading**: Concurrent programming, synchronization
6. **Configuration Management**: JSON handling, user preferences
7. **Error Handling**: Robust exception management
8. **Logging**: Debugging and monitoring techniques

## Contributing

This is an educational project. Contributions that enhance the learning value are welcome:

- Improved detection algorithms
- Additional configuration options
- Better error handling
- Documentation improvements
- Cross-platform compatibility

## License

This project is released under the MIT License for educational use only.

## Disclaimer

**This software is provided "as is" for educational purposes only. The author makes no warranties and accepts no liability for any consequences of its use. Users are responsible for ensuring compliance with all applicable terms of service and local laws.**

---

*Happy Learning! 🎓*