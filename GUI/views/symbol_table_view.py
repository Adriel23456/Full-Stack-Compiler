"""
Symbol Table View - A fullscreen modal for displaying the symbol table
"""
import pygame
import os
from GUI.design_base import design
from GUI.components.button import Button

class SymbolTableView:
    def __init__(self, parent_view, symbol_table_path, on_close=None):
        self.parent_view = parent_view
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.symbol_table_path = symbol_table_path
        self.on_close = on_close
        
        # Setup layout based on screen size
        self.setup_layout()
        
        # Load image
        self.symbol_table_surface = None
        self.original_width = 0
        self.original_height = 0
        self.load_symbol_table_image()
        
        # Camera and scale state
        self.camera_x = 0
        self.camera_y = 0
        self.scale_factor = 1.0
        
        # Calculate initial scale and camera limits
        if self.symbol_table_surface:
            self.calculate_initial_scale()
            self.update_camera_limits()
        
        # Dragging state
        self.is_dragging = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        
        # Store last screen size to detect resize
        self.last_screen_size = (self.screen_rect.width, self.screen_rect.height)
    
    def setup_layout(self):
        """Setup layout based on current screen size"""
        # Get current screen dimensions
        screen_width = self.screen_rect.width
        screen_height = self.screen_rect.height
        
        # Modal takes full screen with margins
        margin = 50  # Outer margin from screen edges
        self.rect = pygame.Rect(margin, margin, 
                               screen_width - 2*margin, 
                               screen_height - 2*margin)
        
        # Content area with inner margin
        inner_margin = 30
        self.content_rect = pygame.Rect(
            self.rect.x + inner_margin, 
            self.rect.y + inner_margin,
            self.rect.width - 2*inner_margin, 
            self.rect.height - 2*inner_margin
        )
        
        # Button dimensions
        button_height = 40
        button_width = 150
        button_margin = 20
        title_height = 50
        
        # Image display area (excluding title and button areas)
        self.image_rect = pygame.Rect(
            self.content_rect.x, 
            self.content_rect.y + title_height,
            self.content_rect.width, 
            self.content_rect.height - title_height - button_height - button_margin * 2
        )
        
        # Create return button centered at bottom
        self.return_button = Button(
            pygame.Rect(
                self.rect.centerx - button_width // 2, 
                self.rect.bottom - button_height - button_margin,
                button_width, 
                button_height
            ), 
            "Return"
        )
        
        # Create zoom info text position
        self.zoom_info_pos = (self.content_rect.right - 200, self.content_rect.top + 10)
    
    def load_symbol_table_image(self):
        """Load the symbol table image"""
        if os.path.exists(self.symbol_table_path):
            try:
                self.symbol_table_surface = pygame.image.load(self.symbol_table_path)
                self.original_width = self.symbol_table_surface.get_width()
                self.original_height = self.symbol_table_surface.get_height()
                
                # Set initial camera to center of image
                self.camera_x = self.original_width / 2
                self.camera_y = self.original_height / 2
            except Exception as e:
                print(f"Error loading symbol table image: {e}")
                self.symbol_table_surface = None
    
    def calculate_initial_scale(self):
        """Calculate initial scale to fit the image in the view"""
        if not self.symbol_table_surface or not hasattr(self, 'image_rect'):
            return
        
        # Calculate scale to fit the image in the display area
        width_ratio = self.image_rect.width / self.original_width
        height_ratio = self.image_rect.height / self.original_height
        
        # Use the smaller ratio to ensure the entire image fits
        self.scale_factor = min(width_ratio, height_ratio) * 0.9  # 90% to leave margin
        
        # Ensure minimum scale
        self.scale_factor = max(0.1, self.scale_factor)
    
    def update_camera_limits(self):
        """Update camera movement limits based on current scale"""
        if not self.symbol_table_surface:
            return
        
        # Calculate half of the view size in image coordinates
        view_width_half = self.image_rect.width / (2 * self.scale_factor)
        view_height_half = self.image_rect.height / (2 * self.scale_factor)
        
        # Set camera limits (camera position is center of view)
        self.min_camera_x = view_width_half
        self.min_camera_y = view_height_half
        self.max_camera_x = self.original_width - view_width_half
        self.max_camera_y = self.original_height - view_height_half
        
        # Handle case where image is smaller than view
        if self.min_camera_x > self.max_camera_x:
            avg = (self.min_camera_x + self.max_camera_x) / 2
            self.min_camera_x = self.max_camera_x = avg
            
        if self.min_camera_y > self.max_camera_y:
            avg = (self.min_camera_y + self.max_camera_y) / 2
            self.min_camera_y = self.max_camera_y = avg
        
        # Clamp current camera position
        self.camera_x = max(self.min_camera_x, min(self.max_camera_x, self.camera_x))
        self.camera_y = max(self.min_camera_y, min(self.max_camera_y, self.camera_y))
    
    def handle_events(self, events):
        # Check for mouse button release outside of event loop
        mouse_buttons = pygame.mouse.get_pressed()
        if self.is_dragging and not mouse_buttons[0]:
            self.is_dragging = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        for event in events:
            # Handle return button
            if self.return_button.handle_event(event):
                if self.on_close:
                    self.on_close()
                return True
            
            # Handle escape key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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
            
            elif event.type == pygame.MOUSEMOTION:
                if self.is_dragging:
                    # Calculate movement delta
                    dx = self.last_mouse_x - event.pos[0]
                    dy = self.last_mouse_y - event.pos[1]
                    
                    # Update last position
                    self.last_mouse_x = event.pos[0]
                    self.last_mouse_y = event.pos[1]
                    
                    # Convert screen delta to image delta
                    scaled_dx = dx / self.scale_factor
                    scaled_dy = dy / self.scale_factor
                    
                    # Update camera position
                    self.camera_x = max(self.min_camera_x, min(self.max_camera_x, self.camera_x + scaled_dx))
                    self.camera_y = max(self.min_camera_y, min(self.max_camera_y, self.camera_y + scaled_dy))
                else:
                    # Update cursor based on hover
                    if self.image_rect.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
            # Handle mouse wheel for zoom
            elif event.type == pygame.MOUSEWHEEL:
                if self.image_rect.collidepoint(pygame.mouse.get_pos()):
                    # Store old scale
                    old_scale = self.scale_factor
                    
                    # Calculate new scale
                    zoom_factor = 1.1
                    if event.y > 0:  # Scroll up = zoom in
                        self.scale_factor *= zoom_factor
                    else:  # Scroll down = zoom out
                        self.scale_factor /= zoom_factor
                    
                    # Limit zoom range
                    min_scale = 0.1
                    max_scale = 3.0
                    self.scale_factor = max(min_scale, min(max_scale, self.scale_factor))
                    
                    # Update camera limits with new scale
                    self.update_camera_limits()
            
            # Handle window resize
            elif event.type == pygame.VIDEORESIZE:
                self.screen_rect = self.screen.get_rect()
                self.setup_layout()
                self.calculate_initial_scale()
                self.update_camera_limits()
        
        return True
    
    def update(self, dt):
        # Check if window was resized
        current_size = (self.screen.get_width(), self.screen.get_height())
        if current_size != self.last_screen_size:
            self.last_screen_size = current_size
            self.screen_rect = self.screen.get_rect()
            self.setup_layout()
            self.update_camera_limits()
    
    def render(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Darker overlay for better contrast
        self.screen.blit(overlay, (0, 0))
        
        # Draw modal window background
        pygame.draw.rect(self.screen, design.colors["background"], self.rect, 0, 10)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.rect, 3, 10)
        
        # Draw title
        title_font = design.get_font("large")
        title_text = title_font.render("Symbol Table", True, design.colors["text"])
        title_rect = title_text.get_rect(centerx=self.rect.centerx, top=self.content_rect.y + 10)
        self.screen.blit(title_text, title_rect)
        
        # Draw zoom info
        zoom_font = design.get_font("small")
        zoom_text = f"Zoom: {self.scale_factor:.1f}x"
        zoom_surface = zoom_font.render(zoom_text, True, design.colors["text"])
        self.screen.blit(zoom_surface, self.zoom_info_pos)
        
        # Draw image area background
        pygame.draw.rect(self.screen, (255, 255, 255), self.image_rect)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.image_rect, 2)
        
        # Draw the symbol table image
        if self.symbol_table_surface:
            try:
                # Create clipped view
                image_view = self.screen.subsurface(self.image_rect)
                
                # Calculate scaled dimensions
                scaled_width = int(self.original_width * self.scale_factor)
                scaled_height = int(self.original_height * self.scale_factor)
                
                # Scale the image
                scaled_surface = pygame.transform.smoothscale(
                    self.symbol_table_surface, 
                    (scaled_width, scaled_height)
                )
                
                # Calculate position to center the view on camera position
                view_x = (self.image_rect.width / 2) - (self.camera_x * self.scale_factor)
                view_y = (self.image_rect.height / 2) - (self.camera_y * self.scale_factor)
                
                # Blit the scaled image
                image_view.blit(scaled_surface, (view_x, view_y))
                
            except Exception as e:
                print(f"Error rendering symbol table: {e}")
                # Draw error message
                error_font = design.get_font("medium")
                error_text = error_font.render("Error displaying symbol table", True, (255, 0, 0))
                error_rect = error_text.get_rect(center=self.image_rect.center)
                self.screen.blit(error_text, error_rect)
        else:
            # Draw placeholder message
            placeholder_font = design.get_font("medium")
            placeholder_text = placeholder_font.render("Symbol table not available", True, design.colors["text"])
            placeholder_rect = placeholder_text.get_rect(center=self.image_rect.center)
            self.screen.blit(placeholder_text, placeholder_rect)
        
        # Draw navigation hints
        hint_font = design.get_font("small")
        hint_text = "Drag to pan • Scroll to zoom • ESC to close"
        hint_surface = hint_font.render(hint_text, True, design.colors["text"])
        hint_rect = hint_surface.get_rect(
            centerx=self.rect.centerx, 
            bottom=self.return_button.rect.top - 10
        )
        self.screen.blit(hint_surface, hint_rect)
        
        # Draw return button
        self.return_button.render(self.screen)