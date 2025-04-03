"""
System configuration file
Contains global constants and configurations
"""

# Window configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WINDOW_TITLE = "MVC System with FSM"
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
    MENU = "MENU"
    GAME = "GAME"
    # Add more states as needed

# Font configuration
FONT_SIZE_SMALL = 24
FONT_SIZE_MEDIUM = 36
FONT_SIZE_LARGE = 48

# Path configuration
import os
# Project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Assets directory (if needed)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")