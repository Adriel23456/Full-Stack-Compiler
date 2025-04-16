"""
Base design system for the application
Defines themes, colors, fonts and other UI elements
"""
import pygame
import json
import os
from config import (BASE_DIR, DEFAULT_FONT_SIZE_SMALL, DEFAULT_FONT_SIZE_MEDIUM, 
                       DEFAULT_FONT_SIZE_LARGE)

class DesignSystem:
    """
    Design system for managing UI appearance across the application
    """
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """
        Singleton pattern implementation
        """
        if cls._instance is None:
            cls._instance = super(DesignSystem, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """
        Initialize the design system
        """
        # Only initialize once
        if DesignSystem._initialized:
            return
        
        self.settings_file = os.path.join(BASE_DIR, "design_settings.json")
        self.settings = self._load_settings()
        
        # Initialize colors
        self._initialize_colors()
        
        # UI element properties
        self._initialize_ui_properties()
        
        # Fonts will be initialized on demand
        self.font_small = None
        self.font_medium = None
        self.font_large = None
        
        # Actualizar a valores predeterminados si han cambiado
        self.update_to_current_defaults()
        
        DesignSystem._initialized = True
    
    def _load_settings(self):
        """
        Load settings from JSON file or create with defaults if not exists
        """
        # Default settings
        defaults = {
            "theme": "light",  # light or dark
            "font_size_small": DEFAULT_FONT_SIZE_SMALL,
            "font_size_medium": DEFAULT_FONT_SIZE_MEDIUM,
            "font_size_large": DEFAULT_FONT_SIZE_LARGE,
            "button_radius": 5,
            "text_padding": 10,
            "toolbar_height": 40,
            "status_bar_height": 30
        }
        
        # Create settings file if it doesn't exist
        if not os.path.exists(self.settings_file):
            with open(self.settings_file, 'w') as f:
                json.dump(defaults, f, indent=4)
            return defaults
        
        # Load settings from file
        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                # Ensure all default keys exist
                for key, value in defaults.items():
                    if key not in settings:
                        settings[key] = value
                return settings
        except Exception as e:
            print(f"Error loading settings: {e}")
            return defaults
    
    def update_to_current_defaults(self):
        """
        Update settings to current defaults if any values change in config.py
        """
        # Check if current settings match defaults
        current_size = self.settings.get("font_size_option", "small")
        
        # Si el usuario tiene seleccionado "small", actualizar a los valores default actuales
        if current_size == "small":
            if (self.settings.get("font_size_small") != DEFAULT_FONT_SIZE_SMALL or
                self.settings.get("font_size_medium") != DEFAULT_FONT_SIZE_MEDIUM or
                self.settings.get("font_size_large") != DEFAULT_FONT_SIZE_LARGE):
                
                # Actualizar a los valores actuales
                self.settings["font_size_small"] = DEFAULT_FONT_SIZE_SMALL
                self.settings["font_size_medium"] = DEFAULT_FONT_SIZE_MEDIUM
                self.settings["font_size_large"] = DEFAULT_FONT_SIZE_LARGE
                self.save_settings()
                
                # Reinicializar fuentes
                self.font_small = None
                self.font_medium = None
                self.font_large = None
    
    def save_settings(self):
        """
        Save current settings to JSON file
        """
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def _initialize_fonts(self):
        """
        Initialize fonts based on current settings
        """
        from config import FONTS_DIR, MAIN_FONT
        font_path = os.path.join(FONTS_DIR, MAIN_FONT)
        
        # Verificar si el archivo de fuente existe
        if os.path.exists(font_path):
            # Crear fuentes con la tipografía personalizada
            self.font_small = pygame.font.Font(font_path, self.settings["font_size_small"])
            self.font_medium = pygame.font.Font(font_path, self.settings["font_size_medium"])
            self.font_large = pygame.font.Font(font_path, self.settings["font_size_large"])
        else:
            # Fallback a la fuente predeterminada si no encuentra el archivo
            print(f"No se encontró la fuente personalizada. Usando fuente predeterminada.")
            self.font_small = pygame.font.Font(None, self.settings["font_size_small"])
            self.font_medium = pygame.font.Font(None, self.settings["font_size_medium"])
            self.font_large = pygame.font.Font(None, self.settings["font_size_large"])
    
    def _initialize_colors(self):
        """
        Initialize color schemes based on current theme
        """
        # Color schemes
        themes = {
            "light": {
                "background": (245, 245, 245),
                "text": (30, 30, 30),
                "primary": (30, 144, 255),  # Dodger blue
                "secondary": (70, 130, 180),  # Steel blue
                "accent": (255, 69, 0),  # Orange red
                "button": (240, 240, 240),
                "button_hover": (220, 220, 220),
                "button_text": (30, 30, 30),
                "toolbar": (220, 220, 220),
                "textbox_bg": (255, 255, 255),
                "textbox_border": (200, 200, 200),
                "textbox_text": (30, 30, 30),
                "textbox_cursor": (30, 30, 30),
                "textbox_selection": (173, 216, 230)  # Light blue
            },
            "dark": {
                "background": (40, 40, 40),
                "text": (220, 220, 220),
                "primary": (30, 144, 255),  # Dodger blue
                "secondary": (70, 130, 180),  # Steel blue
                "accent": (255, 165, 0),  # Orange
                "button": (60, 60, 60),
                "button_hover": (80, 80, 80),
                "button_text": (220, 220, 220),
                "toolbar": (50, 50, 50),
                "textbox_bg": (50, 50, 50),
                "textbox_border": (100, 100, 100),
                "textbox_text": (220, 220, 220),
                "textbox_cursor": (220, 220, 220),
                "textbox_selection": (70, 130, 180)  # Steel blue
            }
        }
        
        # Set current theme colors
        theme = self.settings.get("theme", "light")
        if theme not in themes:
            theme = "light"
        
        self.colors = themes[theme]
    
    def _initialize_ui_properties(self):
        """
        Initialize UI element properties
        """
        self.button_radius = self.settings["button_radius"]
        self.text_padding = self.settings["text_padding"]
        self.toolbar_height = self.settings["toolbar_height"]
        self.status_bar_height = self.settings["status_bar_height"]
    
    def toggle_theme(self):
        """
        Toggle between light and dark themes
        """
        current_theme = self.settings.get("theme", "light")
        self.settings["theme"] = "dark" if current_theme == "light" else "light"
        self._initialize_colors()
        self.save_settings()
    
    def set_font_size(self, size_category, new_size):
        """
        Set font size for a specific category
        
        Args:
            size_category: Category to change (small, medium, large)
            new_size: New font size
        """
        if size_category in ["small", "medium", "large"]:
            key = f"font_size_{size_category}"
            self.settings[key] = new_size
            
            # Reset fonts so they'll be recreated with new sizes
            self.font_small = None
            self.font_medium = None
            self.font_large = None
            
            self.save_settings()
    
    def get_font(self, size_type="medium"):
        """
        Get a font of the specified size type
        
        Args:
            size_type: Font size type (small, medium, large)
            
        Returns:
            pygame.font.Font: Font object
        """
        # Make sure fonts are initialized
        self._initialize_fonts()
        
        if size_type == "small":
            return self.font_small
        elif size_type == "large":
            return self.font_large
        else:  # Default to medium
            return self.font_medium
    
    def create_rounded_rect(self, surface, rect, color, radius=0):
        """
        Draw a rounded rectangle on a surface
        
        Args:
            surface: Surface to draw on
            rect: Rectangle to draw
            color: Color of the rectangle
            radius: Corner radius
        """
        rect = pygame.Rect(rect)
        color = pygame.Color(*color)
        
        # Special case for radius = 0
        if radius == 0:
            pygame.draw.rect(surface, color, rect)
            return
        
        # Constraint radius to be at most half of width or height
        radius = min(radius, rect.width // 2, rect.height // 2)
        
        # Draw the rounded rectangle
        # Top left corner
        pygame.draw.circle(surface, color, (rect.left + radius, rect.top + radius), radius)
        # Top right corner
        pygame.draw.circle(surface, color, (rect.right - radius, rect.top + radius), radius)
        # Bottom left corner
        pygame.draw.circle(surface, color, (rect.left + radius, rect.bottom - radius), radius)
        # Bottom right corner
        pygame.draw.circle(surface, color, (rect.right - radius, rect.bottom - radius), radius)
        
        # Fill in the middle parts
        pygame.draw.rect(surface, color, (rect.left + radius, rect.top, rect.width - 2 * radius, rect.height))
        pygame.draw.rect(surface, color, (rect.left, rect.top + radius, rect.width, rect.height - 2 * radius))
    
    def draw_button(self, surface, rect, text, is_hover=False, is_active=False):
        """
        Draw a styled button on a surface
        
        Args:
            surface: Surface to draw on
            rect: Rectangle of the button
            text: Text to display on the button
            is_hover: Whether the mouse is hovering over the button
            is_active: Whether the button is in active state
        """
        # Choose the appropriate color
        if is_active:
            color = self.colors["primary"]
            text_color = self.colors["button_text"]
        elif is_hover:
            color = self.colors["button_hover"]
            text_color = self.colors["button_text"]
        else:
            color = self.colors["button"]
            text_color = self.colors["button_text"]
        
        # Draw the button background
        self.create_rounded_rect(surface, rect, color, self.button_radius)
        
        # Draw the button border
        pygame.draw.rect(surface, self.colors["textbox_border"], rect, 1, self.button_radius)
        
        # Make sure fonts are initialized
        self._initialize_fonts()
        
        # Draw the text
        text_surf = self.font_medium.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)
        
        return rect
    
    def draw_toolbar_button(self, surface, rect, text, is_hover=False, is_active=False):
        """
        Draw a styled toolbar button
        """
        # Similar to regular button but with slightly different styling
        return self.draw_button(surface, rect, text, is_hover, is_active)
    
    def draw_textbox(self, surface, rect, text="", cursor_pos=None, selection=None):
        """
        Draw a styled textbox on a surface
        
        Args:
            surface: Surface to draw on
            rect: Rectangle of the textbox
            text: Text to display
            cursor_pos: Position of the cursor in the text (optional)
            selection: (start, end) tuple for text selection (optional)
        """
        # Draw textbox background
        pygame.draw.rect(surface, self.colors["textbox_bg"], rect, 0, self.button_radius)
        
        # Draw textbox border
        pygame.draw.rect(surface, self.colors["textbox_border"], rect, 1, self.button_radius)
        
        return rect
    
    def get_window_size(self):
        """
        Get the configured window size
        
        Returns:
            tuple: (width, height)
        """
        window_size = self.settings.get("window_size", "small")
        
        if window_size == "large":
            return (1920, 1080)
        elif window_size == "medium":
            return (1500, 900)
        elif window_size == "fullscreen":
            return (0, 0, pygame.FULLSCREEN)  # Special format for fullscreen mode
        else:  # Default to small
            return (950, 750)

    def set_window_size(self, size_name):
        """
        Set the window size configuration
        
        Args:
            size_name: Size name ("small" or "large")
        """
        if size_name in ["small", "large"]:
            self.settings["window_size"] = size_name
            self.save_settings()

# Create a singleton instance but don't initialize fonts yet
design = DesignSystem()