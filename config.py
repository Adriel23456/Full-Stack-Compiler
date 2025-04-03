"""
System configuration file
Contains global constants and configurations
"""

# Window configuration
SCREEN_WIDTH = 950
SCREEN_HEIGHT = 750
WINDOW_TITLE = "Full Stack Compiler"
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Application states
class States:
    EDITOR = "EDITOR"  # Main editor state

# Font configuration
FONT_SIZE_SMALL = 24
FONT_SIZE_MEDIUM = 36
FONT_SIZE_LARGE = 48

# TextBox configuration
LINE_NUMBERS_WIDTH = 50  # width of line numbers area
LINE_HEIGHT_MULTIPLIER = 2  # multiplier for line height (doubles the height)
KEY_REPEAT_DELAY = 450  # ms before key starts repeating
KEY_REPEAT_INTERVAL = 25  # ms between repeats (over 60 times/second)
LINE_SEPARATOR_THICKNESS = 1  # thickness of line separators in pixels

# Path configuration
import os
# Project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Assets directory (if needed)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")