"""
Main entry point of the program
Initializes pygame and the View Controller
"""
import pygame
import sys
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE, States
from GUI.view_controller import ViewController
from GUI.views.editor_view import EditorView

def main():
    """
    Main program function
    """
    # Initialize pygame
    pygame.init()
    
    # Initialize font module explicitly
    pygame.font.init()
    
    # Disable pygame's built-in key repeat - we'll handle it manually
    pygame.key.set_repeat(0)  # Disable key repeat
    
    # Center the window on the screen
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    
    # Create window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    
    # Initialize scrap module (clipboard)
    pygame.scrap.init()
    
    try:
        # Create View Controller
        controller = ViewController()
        
        # Register only the Editor state
        controller.add_state(States.EDITOR, EditorView)
        
        # Set initial state to Editor
        controller.set_initial_state(States.EDITOR)
        
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