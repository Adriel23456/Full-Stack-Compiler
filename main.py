"""
Main entry point of the program
Initializes pygame and the View Controller
"""
import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE, States
from GUI.view_controller import ViewController
from GUI.views.menu_view import MenuView
from GUI.views.game_view import GameView

def main():
    """
    Main program function
    """
    # Initialize pygame
    pygame.init()
    
    # Create window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    
    try:
        # Create View Controller
        controller = ViewController()
        
        # Register states
        controller.add_state(States.MENU, MenuView)
        controller.add_state(States.GAME, GameView)
        
        # Set initial state
        controller.set_initial_state(States.MENU)
        
        # Run main loop
        controller.run()
    
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        # Finalize pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()