# Getting Started with WoW Fishbot

## ⚠️ Important Notice
**This fishbot is for educational purposes ONLY. Use responsibly and respect game terms of service.**

## Quick Start (3 Steps)

### 1. Install Dependencies

**Windows:**
```bash
# Run the installation script
install.bat
```

**Linux:**
```bash
# Run the installation script
./install.sh
```

**Manual Installation:**
```bash
pip install -r requirements.txt
```

### 2. Configure the Bot

**Easy Way:**
```bash
python run.py
```
Then click "Setup & Configuration"

**Manual Way:**
```bash
python setup_detector.py
```

### 3. Run the Bot

**GUI Mode (Recommended):**
```bash
python main.py
```

**CLI Mode:**
```bash
python main.py --cli
```

## File Overview

| File | Purpose |
|------|---------|
| `main.py` | Main fishbot application |
| `setup_detector.py` | Configuration utility |
| `test_detection.py` | Detection testing tool |
| `run.py` | Launcher with menu |
| `requirements.txt` | Python dependencies |
| `README.md` | Complete documentation |

## Hotkeys

- **F9**: Start/Stop Bot
- **F10**: Pause/Resume
- **F11**: Emergency Stop

## Troubleshooting

**Bot not working?**
1. Run `python test_detection.py` to verify detection
2. Adjust detection area in setup utility
3. Check audio levels and microphone permissions
4. Ensure stable game framerate

**Missing dependencies?**
```bash
# Install missing packages
pip install opencv-python pyautogui keyboard numpy pillow pyaudio
```

## Support

For issues or questions about the educational aspects of this project, please refer to the main README.md file for detailed documentation.

---
*Remember: Educational use only! 🎓*