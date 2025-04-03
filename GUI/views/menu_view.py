"""
Main menu view
"""
import pygame
import sys
from GUI.view_base import ViewBase
from config import States, WHITE, BLACK, BLUE

class MenuView(ViewBase):
    """
    Main menu view of the application
    """
    def __init__(self, view_controller):
        """
        Initializes the menu view
        
        Args:
            view_controller: View Controller with FSM
        """
        super().__init__(view_controller)
        self.title_font = pygame.font.Font(None, 72)
        
    def setup(self):
        """
        Sets up the menu view
        """
        # Menu title
        self.title = self.title_font.render("Main Menu", True, BLACK)
        self.title_rect = self.title.get_rect(center=(self.screen_rect.centerx, 100))
        
        # Menu buttons
        button_width, button_height = 200, 50
        button_x = self.screen_rect.centerx - button_width // 2
        
        # Play Button
        self.play_button = self.create_button(
            "Play", 
            (button_x, 200),
            (button_width, button_height),
            BLUE
        )
        
        # Exit Button
        self.exit_button = self.create_button(
            "Exit", 
            (button_x, 300),
            (button_width, button_height),
            BLUE
        )
    
    def handle_events(self, events):
        """
        Handles pygame events
        
        Args:
            events: List of pygame events
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.view_controller.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Left click
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if any button was clicked
                if self.play_button['rect'].collidepoint(mouse_pos):
                    # Change to game state
                    self.view_controller.change_state(States.GAME)
                elif self.exit_button['rect'].collidepoint(mouse_pos):
                    # Exit application
                    self.view_controller.quit()
            
            # Can also add handling for specific keys
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.view_controller.quit()
    
    def update(self, dt):
        """
        Updates view logic
        
        Args:
            dt: Time elapsed since last update (delta time)
        """
        # For menu, we don't need much update logic
        pass
    
    def render(self):
        """
        Renders the view on screen
        """
        # Clear the screen
        self.screen.fill(WHITE)
        
        # Draw the title
        self.screen.blit(self.title, self.title_rect)
        
        # Draw buttons
        self.draw_button(self.play_button)
        self.draw_button(self.exit_button)