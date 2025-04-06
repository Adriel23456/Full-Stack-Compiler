"""
Configuration view for application settings
"""
import pygame
from GUI.design_base import design
from GUI.components.button import Button

class ConfigView:
    """
    Modal configuration view that overlays on top of the main application
    """
    def __init__(self, parent_view, on_close=None, on_apply=None):
        """
        Initialize the configuration view
        
        Args:
            parent_view: Parent view that opened this config view
            on_close: Callback function when config is closed without applying
            on_apply: Callback function when config is applied
        """
        self.parent_view = parent_view
        self.screen = pygame.display.get_surface()
        self.on_close = on_close
        self.on_apply = on_apply
        
        # Calculate dimensions - make it centered and smaller than the main window
        screen_rect = self.screen.get_rect()
        self.width = min(850, screen_rect.width - 40)
        self.height = min(650, screen_rect.height - 40)
        
        self.rect = pygame.Rect(
            (screen_rect.width - self.width) // 2,
            (screen_rect.height - self.height) // 2,
            self.width,
            self.height
        )
        
        # Configuration options
        self.selected_theme = design.settings.get("theme", "light")
        # Guardar la opción de tamaño seleccionada
        self.selected_font_size = design.settings.get("font_size_option", "small")
        
        # Match current font size
        if design.settings.get("font_size_small", 16) == 16:
            self.selected_font_size = "small"
        elif design.settings.get("font_size_small", 16) == 24:
            self.selected_font_size = "large"
            
        # Window size - start with current setting
        current_width = pygame.display.get_surface().get_width()
        current_height = pygame.display.get_surface().get_height()
        
        # Check for fullscreen mode
        self.is_fullscreen = pygame.display.get_surface().get_flags() & pygame.FULLSCREEN
        
        # Determine selected window size based on dimensions
        if abs(current_width - 1920) < 50 and abs(current_height - 1080) < 50 and not self.is_fullscreen:
            self.selected_window_size = "large"
        elif abs(current_width - 1500) < 50 and abs(current_height - 900) < 50:
            self.selected_window_size = "medium"
        else:
            self.selected_window_size = "small"
        
        # Create UI elements
        self.setup_ui()
    

    def setup_ui(self):
        """Set up UI elements"""
        # Header
        self.title_font = design.get_font("large")
        self.regular_font = design.get_font("medium")
        
        # Button dimensions
        BUTTON_WIDTH = 150  # Ancho constante para Apply & Cancel
        button_height = 40
        button_margin = 30  # Margen desde los bordes del componente
        button_gap = 10     # Espacio entre botones en la misma fila
        section_spacing = 60  # Espacio entre secciones
        
        # Calculate positions for buttons at the bottom
        bottom_y = self.rect.bottom - button_height - button_margin
        
        # Create buttons
        self.cancel_button = Button(
            pygame.Rect(
                self.rect.left + button_margin,
                bottom_y,
                BUTTON_WIDTH,
                button_height
            ),
            "Cancel",
            fixed_width=BUTTON_WIDTH,
        )
        
        self.apply_button = Button(
            pygame.Rect(
                self.rect.right - button_margin - BUTTON_WIDTH,
                bottom_y,
                BUTTON_WIDTH,
                button_height
            ),
            "Apply",
            fixed_width=BUTTON_WIDTH,
        )
        
        # Option buttons - theme selection
        theme_section_y = self.rect.top + 100
        option_height = 40  # Increased height
        theme_button_width = (self.width - 2 * button_margin - button_gap) // 2
        
        self.theme_light_button = Button(
            pygame.Rect(
                self.rect.left + button_margin,
                theme_section_y,
                theme_button_width,
                option_height
            ),
            "Light Theme"
        )
        
        self.theme_dark_button = Button(
            pygame.Rect(
                self.theme_light_button.rect.right + button_gap,
                theme_section_y,
                theme_button_width,
                option_height
            ),
            "Dark Theme"
        )
        
        # Font size selection - calculate positions based on previous section
        font_section_y = theme_section_y + option_height + section_spacing
        font_option_width = (self.width - 2 * button_margin - 2 * button_gap) // 3
        
        self.font_small_button = Button(
            pygame.Rect(
                self.rect.left + button_margin,
                font_section_y,
                font_option_width,
                option_height
            ),
            "Small"
        )
        
        self.font_medium_button = Button(
            pygame.Rect(
                self.font_small_button.rect.right + button_gap,
                font_section_y,
                font_option_width,
                option_height
            ),
            "Medium"
        )
        
        self.font_large_button = Button(
            pygame.Rect(
                self.font_medium_button.rect.right + button_gap,
                font_section_y,
                font_option_width,
                option_height
            ),
            "Large"
        )
        
        # Window size selection
        window_section_y = font_section_y + option_height + section_spacing
        
        # Three window size options with equal width and improved spacing
        window_option_width = (self.width - 2 * button_margin - 3 * button_gap) // 4
        
        self.size_small_button = Button(
            pygame.Rect(
                self.rect.left + button_margin,
                window_section_y,
                window_option_width,
                option_height
            ),
            "950 x 750"
        )
        
        self.size_medium_button = Button(
            pygame.Rect(
                self.size_small_button.rect.right + button_gap,
                window_section_y,
                window_option_width,
                option_height
            ),
            "1500 x 900"
        )
        
        self.size_large_button = Button(
            pygame.Rect(
                self.size_medium_button.rect.right + button_gap,
                window_section_y,
                window_option_width,
                option_height
            ),
            "1920 x 1080"
        )
        
        self.fullscreen_button = Button(
            pygame.Rect(
                self.size_large_button.rect.right + button_gap,
                window_section_y,
                window_option_width,
                option_height
            ),
            "Fullscreen"
        )
    
    def handle_events(self, events):
        """
        Handle pygame events
        
        Args:
            events: List of pygame events
        """
        # Reset cursor to arrow when config view is active
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        for event in events:
            # Cancel button
            if self.cancel_button.handle_event(event):
                if self.on_close:
                    self.on_close()
                return True
            
            # Apply button
            if self.apply_button.handle_event(event):
                self.apply_changes()
                if self.on_apply:
                    self.on_apply()
                return True
            
            # Theme selection
            if self.theme_light_button.handle_event(event):
                self.selected_theme = "light"
                return True
            
            if self.theme_dark_button.handle_event(event):
                self.selected_theme = "dark"
                return True
            
            # Font size selection
            if self.font_small_button.handle_event(event):
                self.selected_font_size = "small"
                return True
            
            if self.font_medium_button.handle_event(event):
                self.selected_font_size = "medium"
                return True
            
            if self.font_large_button.handle_event(event):
                self.selected_font_size = "large"
                return True
            
            # Window size selection
            if self.size_small_button.handle_event(event):
                self.selected_window_size = "small"
                self.is_fullscreen = False
                return True
            
            if self.size_medium_button.handle_event(event):
                self.selected_window_size = "medium"
                self.is_fullscreen = False
                return True
            
            if self.size_large_button.handle_event(event):
                self.selected_window_size = "large"
                self.is_fullscreen = False
                return True
            
            # Fullscreen toggle
            if self.fullscreen_button.handle_event(event):
                self.is_fullscreen = True
                return True
            
            # ESC key to exit fullscreen mode
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.is_fullscreen:
                    self.is_fullscreen = False
                    self.selected_window_size = "large"  # Default to large windowed mode
                    return True
        
        return False
    
    def apply_changes(self):
        """Apply the selected configuration"""
        # Import font size settings from config
        from config import (FONT_SIZE_SMALL_OPTION, FONT_SIZE_MEDIUM_OPTION, 
                       FONT_SIZE_LARGE_OPTION)
    
        # Apply theme if changed
        if self.selected_theme != design.settings.get("theme", "light"):
            design.settings["theme"] = self.selected_theme
            design._initialize_colors()
            
        # Apply font size con valores de config.py
        if self.selected_font_size == "small":
            design.set_font_size("small", FONT_SIZE_SMALL_OPTION["small"])
            design.set_font_size("medium", FONT_SIZE_SMALL_OPTION["medium"])
            design.set_font_size("large", FONT_SIZE_SMALL_OPTION["large"])
        elif self.selected_font_size == "medium":
            design.set_font_size("small", FONT_SIZE_MEDIUM_OPTION["small"])
            design.set_font_size("medium", FONT_SIZE_MEDIUM_OPTION["medium"])
            design.set_font_size("large", FONT_SIZE_MEDIUM_OPTION["large"])
        elif self.selected_font_size == "large":
            design.set_font_size("small", FONT_SIZE_LARGE_OPTION["small"])
            design.set_font_size("medium", FONT_SIZE_LARGE_OPTION["medium"])
            design.set_font_size("large", FONT_SIZE_LARGE_OPTION["large"])
        
        # Save window size setting
        if self.is_fullscreen:
            design.settings["window_size"] = "fullscreen"
        else:
            design.settings["window_size"] = self.selected_window_size
        
        # Guardar la opción de tamaño seleccionada
        design.settings["font_size_option"] = self.selected_font_size
        
        # Save all settings
        design.save_settings()
    
    def update(self, dt):
        """
        Update view logic
        
        Args:
            dt: Time elapsed since last update
        """
        pass

    def render(self):
        """Render the configuration view"""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Draw config window background
        pygame.draw.rect(self.screen, design.colors["background"], self.rect, 0, 10)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.rect, 2, 10)
        
        # Draw title
        title_text = self.title_font.render("Configuration", True, design.colors["text"])
        title_rect = title_text.get_rect(centerx=self.rect.centerx, top=self.rect.top + 30)
        self.screen.blit(title_text, title_rect)
        
        # Draw section headers - improved positioning
        theme_text = self.regular_font.render("Theme:", True, design.colors["text"])
        self.screen.blit(theme_text, (self.rect.left + 30, self.theme_light_button.rect.top - 30))
        
        font_text = self.regular_font.render("Text Size:", True, design.colors["text"])
        self.screen.blit(font_text, (self.rect.left + 30, self.font_small_button.rect.top - 30))
        
        size_text = self.regular_font.render("Window Size:", True, design.colors["text"])
        self.screen.blit(size_text, (self.rect.left + 30, self.size_small_button.rect.top - 30))
        
        # Draw buttons
        self.cancel_button.render(self.screen)
        self.apply_button.render(self.screen)
        
        # Draw theme buttons with active highlight
        self.theme_light_button.is_active = (self.selected_theme == "light")
        self.theme_dark_button.is_active = (self.selected_theme == "dark")
        self.theme_light_button.render(self.screen)
        self.theme_dark_button.render(self.screen)
        
        # Draw font size buttons with active highlight
        self.font_small_button.is_active = (self.selected_font_size == "small")
        self.font_medium_button.is_active = (self.selected_font_size == "medium")
        self.font_large_button.is_active = (self.selected_font_size == "large")
        self.font_small_button.render(self.screen)
        self.font_medium_button.render(self.screen)
        self.font_large_button.render(self.screen)
        
        # Draw window size buttons with active highlight
        self.size_small_button.is_active = (self.selected_window_size == "small" and not self.is_fullscreen)
        self.size_medium_button.is_active = (self.selected_window_size == "medium" and not self.is_fullscreen)
        self.size_large_button.is_active = (self.selected_window_size == "large" and not self.is_fullscreen)
        self.size_small_button.render(self.screen)
        self.size_medium_button.render(self.screen)
        self.size_large_button.render(self.screen)
        
        # Draw fullscreen button with active highlight
        self.fullscreen_button.is_active = self.is_fullscreen
        self.fullscreen_button.render(self.screen)