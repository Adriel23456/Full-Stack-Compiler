import pygame
from GUI.design_base import design

class PopupDialog:
    """Styled popup dialog for showing messages based on app design"""
    def __init__(self, screen, message, timeout=2000):
        self.screen = screen
        self.message = message
        self.start_time = pygame.time.get_ticks()
        self.timeout = timeout
        self.active = True
        
        # Calculate size and position
        screen_rect = screen.get_rect()
        font = design.get_font("medium")
        
        # Use design system colors for text
        self.text_surf = font.render(message, True, design.colors["textbox_text"])
        
        padding = 20
        self.width = self.text_surf.get_width() + padding * 2
        self.height = self.text_surf.get_height() + padding * 2
        
        # Position popup at top third of screen
        self.rect = pygame.Rect(
            (screen_rect.width - self.width) // 2,
            (screen_rect.height - self.height) // 3,
            self.width, 
            self.height
        )
        
    def update(self):
        """Update popup state"""
        if pygame.time.get_ticks() - self.start_time > self.timeout:
            self.active = False
        
    def render(self):
        """Render the popup using the design system colors"""
        if not self.active:
            return
            
        # Draw popup with rounded corners
        # Use design system colors for background and border
        pygame.draw.rect(self.screen, design.colors["textbox_bg"], self.rect, 0, 10)
        pygame.draw.rect(self.screen, design.colors["primary"], self.rect, 2, 10)
        
        # Draw text centered in popup
        text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.screen.blit(self.text_surf, text_rect)