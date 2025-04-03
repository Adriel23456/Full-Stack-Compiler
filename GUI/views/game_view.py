"""
Game view
"""
import pygame
from GUI.view_base import ViewBase
from GUI.models.game_model import GameModel
from config import States, WHITE, BLACK, RED, GREEN

class GameView(ViewBase):
    """
    Game view (main game screen)
    """
    def __init__(self, view_controller):
        """
        Initializes the game view
        
        Args:
            view_controller: View Controller with FSM
        """
        super().__init__(view_controller)
        # Create game model
        self.model = GameModel()
        
    def setup(self):
        """
        Sets up the game view
        """
        # Button to return to menu
        self.menu_button = self.create_button(
            "Menu", 
            (10, 10),
            (100, 40),
            RED
        )
        
        # Player dimensions (example)
        self.player_size = (40, 40)
        
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
                
                # Check if menu button was clicked
                if self.menu_button['rect'].collidepoint(mouse_pos):
                    self.view_controller.change_state(States.MENU)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Go to menu when pressing Escape
                    self.view_controller.change_state(States.MENU)
                elif event.key == pygame.K_p:
                    # Pause/Resume game with P key
                    self.model.toggle_pause()
    
    def update(self, dt):
        """
        Updates view logic
        
        Args:
            dt: Time elapsed since last update (delta time)
        """
        # Handle keyboard input for movement
        keys = pygame.key.get_pressed()
        
        # Determine movement direction
        movement_x = 0
        movement_y = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            movement_x = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            movement_x = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            movement_y = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            movement_y = 1
            
        # Update model
        self.model.update(dt, movement_x, movement_y)
        
        # Add points (just for demonstration)
        if not self.model.paused:
            self.model.add_score(1)
    
    def render(self):
        """
        Renders the view on screen
        """
        # Clear the screen
        self.screen.fill(WHITE)
        
        # Draw menu button
        self.draw_button(self.menu_button)
        
        # Draw player (simple rectangle)
        player_rect = pygame.Rect(
            self.model.player_pos[0] - self.player_size[0] // 2,
            self.model.player_pos[1] - self.player_size[1] // 2,
            self.player_size[0],
            self.player_size[1]
        )
        pygame.draw.rect(self.screen, GREEN, player_rect)
        
        # Draw game information
        score_text = self.font.render(f"Score: {self.model.score}", True, BLACK)
        level_text = self.font.render(f"Level: {self.model.level}", True, BLACK)
        
        self.screen.blit(score_text, (10, 60))
        self.screen.blit(level_text, (10, 100))
        
        # If game is paused, show message
        if self.model.paused:
            pause_font = pygame.font.Font(None, 72)
            pause_text = pause_font.render("PAUSED", True, RED)
            pause_rect = pause_text.get_rect(center=self.screen_rect.center)
            self.screen.blit(pause_text, pause_rect)