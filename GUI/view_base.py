"""
Base class for system views
Defines the common interface that all views must implement
"""
import pygame
from abc import ABC, abstractmethod

class ViewBase(ABC):
    """
    Abstract base class for all views
    """
    def __init__(self, view_controller):
        """
        Initializes the base view
        
        Args:
            view_controller: View Controller with FSM
        """
        self.view_controller = view_controller
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.running = True
        
        # UI elements common to all views
        self.font = pygame.font.Font(None, 36)
    
    @abstractmethod
    def setup(self):
        """
        Sets up the view before running it
        Must be implemented by derived classes
        """
        pass
    
    @abstractmethod
    def handle_events(self, events):
        """
        Handles pygame events
        
        Args:
            events: List of pygame events
        """
        pass
    
    @abstractmethod
    def update(self, dt):
        """
        Updates the view logic
        
        Args:
            dt: Time elapsed since last update (delta time)
        """
        pass
    
    @abstractmethod
    def render(self):
        """
        Renders the view on the screen
        """
        pass
    
    def run(self, dt):
        """
        Runs one cycle of the view
        
        Args:
            dt: Time elapsed since last update (delta time)
        """
        if self.running:
            self.update(dt)
            self.render()
    
    def create_button(self, text, position, size=(200, 50), color=(100, 100, 100), 
                     hover_color=(150, 150, 150), text_color=(255, 255, 255)):
        """
        Creates a button for the graphical interface
        
        Args:
            text: Button text
            position: Button position (x, y)
            size: Button size (width, height)
            color: Normal button color
            hover_color: Color when mouse is over the button
            text_color: Text color
            
        Returns:
            dict: A dictionary with button information
        """
        button_rect = pygame.Rect(position, size)
        button_text = self.font.render(text, True, text_color)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        
        return {
            'rect': button_rect,
            'text': button_text,
            'text_rect': button_text_rect,
            'color': color,
            'hover_color': hover_color,
            'action': None
        }
    
    def draw_button(self, button):
        """
        Draws a button on the screen
        
        Args:
            button: Button dictionary to draw
        """
        # Check if mouse is over the button
        mouse_pos = pygame.mouse.get_pos()
        if button['rect'].collidepoint(mouse_pos):
            color = button['hover_color']
        else:
            color = button['color']
            
        # Draw the button
        pygame.draw.rect(self.screen, color, button['rect'])
        pygame.draw.rect(self.screen, (0, 0, 0), button['rect'], 2)  # Border
        self.screen.blit(button['text'], button['text_rect'])