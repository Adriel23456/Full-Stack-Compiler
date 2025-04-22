"""
Symbol Table View - A modal popup for displaying the symbol table
"""
import pygame
import os
from GUI.design_base import design
from GUI.components.button import Button
from config import SYMBOL_TABLE_CAMERA_WIDTH, SYMBOL_TABLE_CAMERA_HEIGHT

class SymbolTableView:
    def __init__(self, parent_view, symbol_table_path, on_close=None):
        self.parent_view = parent_view
        self.screen = pygame.display.get_surface()
        self.symbol_table_path = symbol_table_path
        self.on_close = on_close
        self.rect = pygame.Rect((self.screen.get_width() - 850) // 2, 
                               (self.screen.get_height() - 650) // 2, 850, 650)
        
        # Content area with margin
        margin = 30
        self.content_rect = pygame.Rect(self.rect.x + margin, self.rect.y + margin,
                                      self.rect.width - 2*margin, self.rect.height - 2*margin)
        
        # Image area
        button_height = 40
        button_margin = 20
        self.image_rect = pygame.Rect(self.content_rect.x, self.content_rect.y,
                                    self.content_rect.width, 
                                    self.content_rect.height - button_height - button_margin)
        
        # Create return button
        self.return_button = Button(
            pygame.Rect(self.rect.centerx - 75, self.rect.bottom - button_height - button_margin,
                      150, button_height), "Return")
        
        # Load image
        self.symbol_table_surface = None
        if os.path.exists(self.symbol_table_path):
            self.symbol_table_surface = pygame.image.load(self.symbol_table_path)
        
        # Camera state - these variables must persist between frames
        self.camera_x = 0
        self.camera_y = 0
        self.max_camera_x = 0
        self.max_camera_y = 0
        
        if self.symbol_table_surface:
            self.max_camera_x = max(0, self.symbol_table_surface.get_width() - SYMBOL_TABLE_CAMERA_WIDTH)
            self.max_camera_y = max(0, self.symbol_table_surface.get_height() - SYMBOL_TABLE_CAMERA_HEIGHT)
        
        # Dragging state
        self.is_dragging = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0
    
    def handle_events(self, events):
        for event in events:
            if self.return_button.handle_event(event):
                if self.on_close:
                    self.on_close()
                return True
            
            # Handle mouse events for camera control
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.image_rect.collidepoint(event.pos):
                    self.is_dragging = True
                    self.last_mouse_x = event.pos[0]
                    self.last_mouse_y = event.pos[1]
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.is_dragging:
                    self.is_dragging = False
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
            elif event.type == pygame.MOUSEMOTION and self.is_dragging:
                # Calculate how far the mouse moved
                dx = self.last_mouse_x - event.pos[0]
                dy = self.last_mouse_y - event.pos[1]
                
                # Save the new mouse position
                self.last_mouse_x = event.pos[0]
                self.last_mouse_y = event.pos[1]
                
                # Update the camera position
                new_x = self.camera_x + dx
                new_y = self.camera_y + dy
                
                # Clamp within bounds
                self.camera_x = max(0, min(self.max_camera_x, new_x))
                self.camera_y = max(0, min(self.max_camera_y, new_y))
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.on_close:
                    self.on_close()
                return True
        
        return True
    
    def update(self, dt):
        pass
    
    def render(self):
        # Draw the background overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Draw the modal window
        pygame.draw.rect(self.screen, design.colors["background"], self.rect, 0, 10)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.rect, 2, 10)
        
        # Draw image area
        pygame.draw.rect(self.screen, (255, 255, 255), self.image_rect)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.image_rect, 1)
        
        # Draw the image with camera offset
        if self.symbol_table_surface:
            # Create subsection surface - this is the visible part determined by camera position
            width = min(SYMBOL_TABLE_CAMERA_WIDTH, self.symbol_table_surface.get_width())
            height = min(SYMBOL_TABLE_CAMERA_HEIGHT, self.symbol_table_surface.get_height())
            subsection = pygame.Surface((width, height))
            
            # Blit the appropriate portion of the image to the subsection
            subsection.blit(
                self.symbol_table_surface,
                (0, 0),
                (self.camera_x, self.camera_y, width, height)
            )
            
            # Scale and center in the image rect
            scale = min(
                self.image_rect.width / width,
                self.image_rect.height / height
            )
            
            scaled_width = int(width * scale)
            scaled_height = int(height * scale)
            
            scaled_subsection = pygame.transform.smoothscale(subsection, (scaled_width, scaled_height))
            
            # Center in image area
            x = self.image_rect.left + (self.image_rect.width - scaled_width) // 2
            y = self.image_rect.top + (self.image_rect.height - scaled_height) // 2
            
            self.screen.blit(scaled_subsection, (x, y))
        
        # Draw return button
        self.return_button.render(self.screen)