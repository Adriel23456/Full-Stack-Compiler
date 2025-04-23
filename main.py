"""
Main entry point of the program
Initializes pygame and the View Controller
"""
import pygame
import sys
import os
from config import WINDOW_TITLE, States
from GUI.view_controller import ViewController
from GUI.views.editor_view import EditorView
from GUI.views.lexical_analysis_view import LexicalAnalysisView
from GUI.views.syntactic_analysis_view import SyntacticAnalysisView
from GUI.design_base import design

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
    
    # Get configured window size
    window_size = design.get_window_size()
    
    # Create window with the configured size
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption(WINDOW_TITLE)
    
    # Initialize scrap module (clipboard)
    pygame.scrap.init()
    
    try:
        # Create View Controller
        controller = ViewController()
        
        # Register the posible states
        controller.add_state(States.EDITOR, EditorView)
        controller.add_state(States.LEXICAL_ANALYSIS, LexicalAnalysisView)
        controller.add_state(States.SYNTACTIC_ANALYSIS, SyntacticAnalysisView)
        
        # Set initial state to Editor
        controller.set_initial_state(States.EDITOR)
        
        # Run main loop con protección adicional
        safe_run(controller)

    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        # Finalize pygame
        pygame.quit()
        sys.exit()

def safe_run(controller):
    """
    Versión protegida del bucle principal que atrapa errores
    """
    # Initialize clock
    clock = pygame.time.Clock()
    
    # Main loop
    while controller.running:
        try:
            # Calculate delta time (in seconds)
            dt = clock.tick(60) / 1000.0
            
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    controller.quit()
            
            # If current view is configured, handle its events
            if hasattr(controller, 'current_view'):
                try:
                    controller.current_view.handle_events(events)
                except Exception as e:
                    print(f"Error en handle_events: {e}")
                    # Intenta continuar con la ejecución
            
            # Handle state changes if any
            try:
                controller.handle_state_change()
            except Exception as e:
                print(f"Error en handle_state_change: {e}")
                # Intenta continuar con la ejecución
            
            # Update and render current view
            if hasattr(controller, 'current_view'):
                try:
                    # Separamos update y render para identificar mejor dónde está el error
                    # Update
                    try:
                        controller.current_view.update(dt)
                    except Exception as e:
                        print(f"Error en update: {e}")
                    
                    # Render
                    try:
                        controller.current_view.render()
                    except Exception as e:
                        print(f"Error en render: {e}")
                except Exception as e:
                    print(f"Error general en ejecución del view: {e}")
            
            # Update the screen
            try:
                pygame.display.flip()
            except Exception as e:
                print(f"Error en pygame.display.flip(): {e}")
        
        except Exception as e:
            print(f"Error crítico en el bucle principal: {e}")
            # En lugar de permitir que la aplicación se cierre, intentamos continuar
            # esperando un poco para no consumir demasiada CPU en caso de error persistente
            pygame.time.wait(100)

if __name__ == "__main__":
    main()