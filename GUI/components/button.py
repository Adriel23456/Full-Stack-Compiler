"""
Button components for UI
"""
import pygame
from GUI.design_base import design

class Button:
    """
    Button component for UI
    """
    def __init__(self, rect, text, fixed_width=None, fixed_height=None):
        """
        Initialize the Button
        
        Args:
            rect: Rectangle for the Button
            text: Text for the Button
        """
        self.rect = pygame.Rect(rect)
        self.text = text
        self.is_hover = False
        self.is_active = False
        self.is_clicked = False  # Track if button is currently clicked
        self.fixed_width = fixed_width
        self.fixed_height = fixed_height
        
        # Adjust size based on text if no fixed dimensions
        self.adjust_size()
    
    def adjust_size(self):
        """Adjust button size based on text content"""
        # Use the medium font for all buttons
        font = design.get_font("medium")
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_width, text_height = text_surface.get_size()
        
        # Preserve original position
        original_x, original_y = self.rect.x, self.rect.y
        
        # Calculate new width and height with padding
        padding_x = 20
        padding_y = 10
        
        # Use fixed dimensions if provided, otherwise calculate from text
        width = self.fixed_width if self.fixed_width else text_width + (padding_x * 2)
        height = self.fixed_height if self.fixed_height else text_height + (padding_y * 2)
        
        # Create new rect with adjusted size but same position
        self.rect = pygame.Rect(original_x, original_y, width, height)
        
    def handle_event(self, event):
        """
        Handle events for the Button
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hover = self.rect.collidepoint(event.pos)
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and not self.is_clicked:
                self.is_active = True
                self.is_clicked = True
                return True  # Trigger action on press, not on release
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            was_active = self.is_active
            self.is_active = False
            
            # Reset click state when mouse button is released
            if self.is_clicked:
                self.is_clicked = False
            
            return False
        
        return False
    
    def render(self, surface):
        """
        Render the Button
        
        Args:
            surface: Surface to render on
        """
        design.draw_button(surface, self.rect, self.text, self.is_hover, self.is_active)

class ToolbarButton(Button):
    """
    Button specifically for the toolbar
    """
    def __init__(self, rect, text, fixed_width=None, fixed_height=None):
        super().__init__(rect, text, fixed_width, fixed_height)
    
    def render(self, surface):
        """
        Render the toolbar button
        
        Args:
            surface: Surface to render on
        """
        # Get the original rect
        orig_rect = self.rect.copy()
        
        # Draw the button
        design.draw_toolbar_button(surface, self.rect, self.text, self.is_hover, self.is_active)