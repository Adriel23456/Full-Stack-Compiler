"""
Basic model for the game (M component of MVC pattern)
Maintains game state and business logic
"""

class GameModel:
    """
    Model containing game data and logic
    """
    def __init__(self):
        """
        Initializes the game model
        """
        # Player score
        self.score = 0
        # Current level
        self.level = 1
        # Indicator if game is paused
        self.paused = False
        # Player position (example)
        self.player_pos = [400, 300]
        # Player speed
        self.player_speed = 200
        
    def update(self, dt, movement_x=0, movement_y=0):
        """
        Updates the model state
        
        Args:
            dt: Time elapsed since last update (delta time)
            movement_x: Player horizontal movement (-1, 0, 1)
            movement_y: Player vertical movement (-1, 0, 1)
        """
        if not self.paused:
            # Update player position
            self.player_pos[0] += movement_x * self.player_speed * dt
            self.player_pos[1] += movement_y * self.player_speed * dt
            
            # Keep player within bounds (example with 800x600 screen)
            self.player_pos[0] = max(20, min(self.player_pos[0], 780))
            self.player_pos[1] = max(20, min(self.player_pos[1], 580))
    
    def add_score(self, points):
        """
        Adds points to the current score
        
        Args:
            points: Points to add
        """
        self.score += points
        
        # Level up logic (example)
        if self.score >= self.level * 1000:
            self.level_up()
    
    def level_up(self):
        """
        Increases game level
        """
        self.level += 1
        # Here you could increase difficulty
        
    def toggle_pause(self):
        """
        Toggles game pause state
        """
        self.paused = not self.paused
        
    def reset(self):
        """
        Resets game state
        """
        self.score = 0
        self.level = 1
        self.paused = False
        self.player_pos = [400, 300]