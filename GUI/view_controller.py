"""
View Controller with Finite State Machine (FSM)
Handles transitions between different application views/states
"""
import pygame
from config import States

class ViewController:
    """
    View Controller with Finite State Machine implementation
    Controls transitions between application views
    """
    def __init__(self):
        """
        Initializes the View Controller
        """
        self.states = {}
        self.current_state = None
        self.next_state = None
        self.running = True
        
    def add_state(self, state_name, state_view_class):
        """
        Adds a state to the finite state machine
        
        Args:
            state_name: State name (use constants from config.States)
            state_view_class: View class associated with the state
        """
        self.states[state_name] = state_view_class
        
    def set_initial_state(self, state_name):
        """
        Sets the initial application state
        
        Args:
            state_name: Initial state name
        """
        if state_name in self.states:
            self.current_state = state_name
            # Instantiate the view associated with the current state
            self.current_view = self.states[state_name](self)
            # Set up the current view
            self.current_view.setup()
        else:
            raise ValueError(f"Unregistered state: {state_name}")
        
    def change_state(self, state_name):
        """
        Changes to the specified state in the next cycle
        
        Args:
            state_name: State name to change to
        """
        if state_name in self.states:
            self.next_state = state_name
        else:
            raise ValueError(f"Unregistered state: {state_name}")
    
    def handle_state_change(self):
        """
        Handles state change if necessary
        """
        if self.next_state is not None:
            # Change to the next state
            self.current_state = self.next_state
            # Instantiate the view associated with the new state
            self.current_view = self.states[self.next_state](self)
            # Set up the new view
            self.current_view.setup()
            # Reset the next_state variable
            self.next_state = None
    
    def quit(self):
        """
        Ends the application execution
        """
        self.running = False
    
    def run(self):
        """
        Runs the main application loop
        """
        # Initialize clock
        clock = pygame.time.Clock()
        # Main loop
        while self.running:
            # Calculate delta time (in seconds)
            dt = clock.tick(60) / 1000.0
            
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit()
            
            # If current view is configured, handle its events
            if hasattr(self, 'current_view'):
                self.current_view.handle_events(events)
            
            # Handle state changes if any
            self.handle_state_change()
            
            # Update and render current view
            if hasattr(self, 'current_view'):
                self.current_view.run(dt)
            
            # Update the screen
            pygame.display.flip()