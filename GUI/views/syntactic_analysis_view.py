"""
Syntactic Analysis View for the Full Stack Compiler
Displays the parse tree and provides access to symbol table
"""
import pygame
import os
from GUI.view_base import ViewBase
from GUI.components.button import Button
from GUI.design_base import design
from GUI.views.symbol_table_view import SymbolTableView
from config import States
from config import PARSE_TREE_CAMERA_WIDTH, PARSE_TREE_CAMERA_HEIGHT

class SyntacticAnalysisView(ViewBase):
    """
    View for displaying syntactic analysis results
    """
    def __init__(self, view_controller, editor_view=None, parse_tree_path=None, symbol_table_path=None):
        super().__init__(view_controller)
        self.editor_view = editor_view
        self.parse_tree_path = parse_tree_path
        self.symbol_table_path = symbol_table_path
        self.parse_tree_surface = None
        
        # Replace simple scroll_y with camera position
        self.camera_x = 0
        self.camera_y = 0
        self.max_camera_x = 0
        self.max_camera_y = 0
        
        self.symbol_table_view = None
        self.is_dragging = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0
    
    def setup(self):
        # Get screen dimensions
        screen_rect = self.screen.get_rect()
        screen_width = screen_rect.width
        screen_height = screen_rect.height
        
        # Calculate layout
        button_height = 40
        button_width = 150
        button_margin = 20
        bottom_margin = 15
        title_height = 50
        
        # Create back button (bottom left)
        self.back_button = Button(
            pygame.Rect(button_margin, screen_height - button_height - bottom_margin, 
                       button_width, button_height),
            "Back to Home"
        )
        
        # Create symbol table button (bottom center)
        symbol_button_x = (screen_width - button_width) // 2
        self.symbol_table_button = Button(
            pygame.Rect(symbol_button_x, screen_height - button_height - bottom_margin, 
                       button_width, button_height),
            "Symbol Table"
        )
        
        # Create next button (bottom right)
        self.next_button = Button(
            pygame.Rect(screen_width - button_width - button_margin, 
                       screen_height - button_height - bottom_margin,
                       button_width, button_height),
            "Next",
            fixed_width=button_width,
            fixed_height=button_height
        )
        
        # Full display area for parse tree scrollbar
        display_height = screen_height - title_height - button_height - bottom_margin - button_margin
        
        # Parse tree display area - full width
        self.parse_tree_rect = pygame.Rect(
            button_margin, 
            title_height,
            screen_width - 2 * button_margin,
            display_height
        )
        
        # Load parse tree image
        self.load_parse_tree()
    
    def load_parse_tree(self):
        if self.parse_tree_path and os.path.exists(self.parse_tree_path):
            try:
                self.parse_tree_surface = pygame.image.load(self.parse_tree_path)
                
                # Calculate maximum camera positions
                from config import PARSE_TREE_CAMERA_WIDTH, PARSE_TREE_CAMERA_HEIGHT
                self.max_camera_x = max(0, self.parse_tree_surface.get_width() - PARSE_TREE_CAMERA_WIDTH)
                self.max_camera_y = max(0, self.parse_tree_surface.get_height() - PARSE_TREE_CAMERA_HEIGHT)
                
                # No need for scrollbar with camera control
                self.scrollbar = None
            except Exception as e:
                print(f"Error loading parse tree image: {e}")
                self.parse_tree_surface = self.create_placeholder_image("Error loading parse tree image")
        else:
            self.parse_tree_surface = self.create_placeholder_image("Parse tree image not available")
    
    def create_placeholder_image(self, message):
        surface = pygame.Surface((400, 300))
        surface.fill((240, 240, 240))
        font = design.get_font("medium")
        text = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(200, 150))
        pygame.draw.rect(surface, (200, 200, 200), pygame.Rect(0, 0, 400, 300), 1)
        surface.blit(text, text_rect)
        return surface
    
    def handle_events(self, events):
        # Handle symbol table view first if active
        if self.symbol_table_view:
            if self.symbol_table_view.handle_events(events):
                return True
            return True
        
        mouse_buttons = pygame.mouse.get_pressed()
        if not mouse_buttons[0] and self.is_dragging:  # Left button not pressed
            self.is_dragging = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        for event in events:
            if event.type == pygame.QUIT:
                self.view_controller.quit()
                return True
            
            # Handle back button
            if self.back_button.handle_event(event):
                self.view_controller.change_state(States.EDITOR)
                return True
            
            # Handle symbol table button
            if self.symbol_table_button.handle_event(event):
                self.show_symbol_table_view()
                return True
            
            # Handle next button
            if self.next_button.handle_event(event):
                print("Next button pressed - semantic analysis not implemented yet")
                return True
            
            # Handle mouse dragging for camera control
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.parse_tree_rect.collidepoint(event.pos):
                    self.is_dragging = True
                    self.last_mouse_x = event.pos[0]
                    self.last_mouse_y = event.pos[1]
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    return True

            # Replace the mouse button up handling:
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Important: Reset dragging regardless of where the mouse is
                if self.is_dragging:
                    self.is_dragging = False
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    return True

            elif event.type == pygame.MOUSEMOTION:
                # Update cursor
                if not self.is_dragging:
                    if self.parse_tree_rect.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                
                # Handle camera dragging
                if self.is_dragging:
                    # Calculate delta movement
                    dx = self.last_mouse_x - event.pos[0]
                    dy = self.last_mouse_y - event.pos[1]
                    
                    # Update last position
                    self.last_mouse_x = event.pos[0]
                    self.last_mouse_y = event.pos[1]
                    
                    # Move camera (inverted direction: dragging moves viewport in opposite direction)
                    self.camera_x = max(0, min(self.max_camera_x, self.camera_x + dx))
                    self.camera_y = max(0, min(self.max_camera_y, self.camera_y + dy))
                    return True
        
        return False
    
    def update(self, dt):
        if self.symbol_table_view:
            self.symbol_table_view.update(dt)
    
    def render(self):
        # Fill background
        self.screen.fill(design.colors["background"])
        
        # Draw title
        title_font = design.get_font("large")
        title_text = title_font.render("Syntactic Analysis - Parse Tree", True, design.colors["text"])
        title_rect = title_text.get_rect(centerx=self.screen_rect.centerx, top=15)
        self.screen.blit(title_text, title_rect)
        
        # Draw parse tree area
        pygame.draw.rect(self.screen, (255, 255, 255), self.parse_tree_rect)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.parse_tree_rect, 1)
        
        if self.parse_tree_surface:
            # Calculate the viewport size while maintaining aspect ratio
            view_width = self.parse_tree_rect.width
            view_height = self.parse_tree_rect.height
            
            # Calculate the subsection of the image to display
            subsection = pygame.Rect(
                self.camera_x, 
                self.camera_y, 
                PARSE_TREE_CAMERA_WIDTH, 
                PARSE_TREE_CAMERA_HEIGHT
            )
            
            # Create a surface for the subsection
            subsection_surface = pygame.Surface((PARSE_TREE_CAMERA_WIDTH, PARSE_TREE_CAMERA_HEIGHT))
            subsection_surface.fill((255, 255, 255))
            
            # Blit only the visible part of the image
            subsection_surface.blit(self.parse_tree_surface, (0, 0), subsection)
            
            # Scale to fit the view rect while maintaining aspect ratio
            scale_factor = min(view_width / PARSE_TREE_CAMERA_WIDTH, view_height / PARSE_TREE_CAMERA_HEIGHT)
            scaled_width = int(PARSE_TREE_CAMERA_WIDTH * scale_factor)
            scaled_height = int(PARSE_TREE_CAMERA_HEIGHT * scale_factor)
            
            # Scale the subsection
            scaled_surface = pygame.transform.smoothscale(subsection_surface, (scaled_width, scaled_height))
            
            # Calculate position to center the scaled surface in the view rect
            pos_x = self.parse_tree_rect.left + (view_width - scaled_width) // 2
            pos_y = self.parse_tree_rect.top + (view_height - scaled_height) // 2
            
            # Blit the scaled surface
            self.screen.blit(scaled_surface, (pos_x, pos_y))
        
        # Draw buttons
        self.back_button.render(self.screen)
        self.symbol_table_button.render(self.screen)
        self.next_button.render(self.screen)
        
        # Render symbol table view if active
        if self.symbol_table_view:
            self.symbol_table_view.render()
    
    def show_symbol_table_view(self):
        self.symbol_table_view = SymbolTableView(self, self.symbol_table_path, 
                                                on_close=self.close_symbol_table_view)
    
    def close_symbol_table_view(self):
        self.symbol_table_view = None