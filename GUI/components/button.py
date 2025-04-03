"""
Button components for UI
"""
import pygame
from GUI.design_base import design

class Button:
    """
    Button component for UI
    """
    def __init__(self, rect, text):
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
                return False  # Don't trigger action on press, only on release
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            was_active = self.is_active
            self.is_active = False
            
            # Only register a click if button was active and mouse is still over it
            if self.rect.collidepoint(event.pos) and was_active and self.is_clicked:
                self.is_clicked = False
                return True  # Trigger action
            
            self.is_clicked = False
        
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
    def render(self, surface):
        """
        Render the toolbar button
        
        Args:
            surface: Surface to render on
        """
        design.draw_toolbar_button(surface, self.rect, self.text, self.is_hover, self.is_active)