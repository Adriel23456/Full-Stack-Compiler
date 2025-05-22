"""
Semantic Analysis View for the Full Stack Compiler
Displays the semantic analysis graph and enhanced symbol table
"""
import pygame
import os
from GUI.components.pop_up_dialog import PopupDialog
from GUI.view_base import ViewBase
from GUI.components.button import Button
from GUI.design_base import design
from GUI.views.symbol_table_view import SymbolTableView
from config import CompilerData, States
from CompilerLogic.intermediateCodeGenerator import IntermediateCodeGenerator

class SemanticAnalysisView(ViewBase):
    """
    View for displaying semantic analysis results
    """
    def __init__(self, view_controller, editor_view=None, semantic_analysis_path=None, enhanced_symbol_table_path=None):
        super().__init__(view_controller)
        self.editor_view = editor_view
        self.semantic_analysis_path = semantic_analysis_path
        self.enhanced_symbol_table_path = enhanced_symbol_table_path
        self.semantic_analysis_surface = None
        
        # Camera position for navigation (center of view in image coordinates)
        self.camera_x = 0
        self.camera_y = 0
        
        # Min and max camera positions
        self.min_camera_x = 0
        self.min_camera_y = 0
        self.max_camera_x = 0
        self.max_camera_y = 0
        
        # For scaling
        self.scale_factor = 1.0
        self.original_width = 0
        self.original_height = 0
        
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
        
        # Full display area for semantic analysis graph
        display_height = screen_height - title_height - button_height - bottom_margin - button_margin
        
        # Semantic analysis display area - full width
        self.semantic_analysis_rect = pygame.Rect(
            button_margin, 
            title_height,
            screen_width - 2 * button_margin,
            display_height
        )
        
        # Load semantic analysis image
        self.load_semantic_analysis()
    
    def load_semantic_analysis(self):
        if self.semantic_analysis_path and os.path.exists(self.semantic_analysis_path):
            try:
                self.semantic_analysis_surface = pygame.image.load(self.semantic_analysis_path)
                
                # Store original dimensions
                self.original_width = self.semantic_analysis_surface.get_width()
                self.original_height = self.semantic_analysis_surface.get_height()
                
                # Calculate initial scale factor to fit the view rect
                self.calculate_scale_factor()
                
                # Set initial camera position to center of image
                self.camera_x = self.original_width / 2
                self.camera_y = self.original_height / 2
                
                # Update camera limits
                self.update_camera_limits()
                
            except Exception as e:
                print(f"Error loading semantic analysis image: {e}")
                self.semantic_analysis_surface = self.create_placeholder_image("Error loading semantic analysis image")
        else:
            self.semantic_analysis_surface = self.create_placeholder_image("Semantic analysis image not available")
    
    def calculate_scale_factor(self):
        """Calculate scale factor to fit the semantic analysis graph in the view rect"""
        if not self.semantic_analysis_surface or not hasattr(self, 'semantic_analysis_rect'):
            return
            
        # Calculate scale factor to fit the view rect while maintaining aspect ratio
        width_ratio = self.semantic_analysis_rect.width / self.original_width
        height_ratio = self.semantic_analysis_rect.height / self.original_height
        
        # Use the smallest ratio to ensure the image fits completely
        self.scale_factor = min(width_ratio, height_ratio) * 0.9  # 90% to leave some margin
    
    def update_camera_limits(self):
        """Update camera limits based on current scale factor"""
        if not self.semantic_analysis_surface:
            return
        
        # Calculate half of the view size in image coordinates
        view_width_half = self.semantic_analysis_rect.width / (2 * self.scale_factor)
        view_height_half = self.semantic_analysis_rect.height / (2 * self.scale_factor)
        
        # Set camera limits to allow the full image to be viewed
        # The camera position represents the center of the view in image coordinates
        self.min_camera_x = view_width_half
        self.min_camera_y = view_height_half
        self.max_camera_x = self.original_width - view_width_half
        self.max_camera_y = self.original_height - view_height_half
        
        # Ensure min doesn't exceed max (can happen with small images or high zoom)
        if self.min_camera_x > self.max_camera_x:
            avg = (self.min_camera_x + self.max_camera_x) / 2
            self.min_camera_x = self.max_camera_x = avg
            
        if self.min_camera_y > self.max_camera_y:
            avg = (self.min_camera_y + self.max_camera_y) / 2
            self.min_camera_y = self.max_camera_y = avg
    
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
        
        # Check if we're already dragging before processing events
        mouse_buttons = pygame.mouse.get_pressed()
        if self.is_dragging and not mouse_buttons[0]:  # Left button was released outside an event
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
            
            # Handle next button – genera LLVM IR
            if self.next_button.handle_event(event):

                # 1) Ejecutar generador de IR
                ir_text = IntermediateCodeGenerator.emit_ir()

                # 2) Hubo errores semánticos  → destacar en el editor
                if ir_text is None:
                    if self.editor_view and hasattr(self.editor_view, 'text_editor'):
                        self.editor_view.text_editor.clear_error_highlights()

                        # Usa los errores recolectados por el semantic analyzer
                        errs = CompilerData.semantic_errors
                        if errs and hasattr(self.editor_view.text_editor, 'highlight_errors'):
                            self.editor_view.text_editor.highlight_errors(errs)

                    # Popup informativo
                    if self.editor_view:
                        self.editor_view.popup = PopupDialog(
                            self.editor_view.screen,
                            "IR generation failed - fix semantic errors",
                            10000
                        )
                    
                    self.view_controller.change_state(States.EDITOR)
                    return True

                # 3) IR generado con éxito  → siguiente vista
                else:
                    self.view_controller.change_state(States.IR_VIEW)
                    return True
            
            # Handle mouse dragging for camera control
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.semantic_analysis_rect.collidepoint(event.pos):
                    self.is_dragging = True
                    self.last_mouse_x = event.pos[0]
                    self.last_mouse_y = event.pos[1]
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    return True
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.is_dragging:
                    self.is_dragging = False
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    return True
            
            # Handle zooming with mousewheel
            elif event.type == pygame.MOUSEWHEEL:
                if self.semantic_analysis_rect.collidepoint(pygame.mouse.get_pos()):
                    # Save old scale for calculating camera adjustment
                    old_scale = self.scale_factor
                    
                    # Zoom in/out
                    zoom_factor = 1.1
                    if event.y > 0:  # Scroll up = zoom in
                        self.scale_factor *= zoom_factor
                    else:  # Scroll down = zoom out
                        self.scale_factor /= zoom_factor
                    
                    # Limit zoom
                    min_scale = 0.1
                    max_scale = 2.0
                    self.scale_factor = max(min_scale, min(max_scale, self.scale_factor))
                    
                    # Update camera limits first
                    self.update_camera_limits()
                    
                    # Ensure camera stays within bounds
                    self.camera_x = max(self.min_camera_x, min(self.max_camera_x, self.camera_x))
                    self.camera_y = max(self.min_camera_y, min(self.max_camera_y, self.camera_y))
                    
                    return True
            
            elif event.type == pygame.MOUSEMOTION:
                # Handle camera dragging
                if self.is_dragging:
                    # Calculate delta movement
                    dx = self.last_mouse_x - event.pos[0]
                    dy = self.last_mouse_y - event.pos[1]
                    
                    # Update last position
                    self.last_mouse_x = event.pos[0]
                    self.last_mouse_y = event.pos[1]
                    
                    # Convert screen distance to image distance based on scale
                    scaled_dx = dx / self.scale_factor
                    scaled_dy = dy / self.scale_factor
                    
                    # Move camera (dragging moves viewport in opposite direction)
                    self.camera_x = max(self.min_camera_x, min(self.max_camera_x, self.camera_x + scaled_dx))
                    self.camera_y = max(self.min_camera_y, min(self.max_camera_y, self.camera_y + scaled_dy))
                    
                    return True
                else:
                    # Update cursor based on hover
                    if self.semantic_analysis_rect.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
            # Handle window resize events
            elif event.type == pygame.VIDEORESIZE:
                # Recalculate layout
                self.setup()
                return True
        
        return False
    
    def update(self, dt):
        if self.symbol_table_view:
            self.symbol_table_view.update(dt)
            
        # Check if window size has changed and recalculate
        current_rect = self.screen.get_rect()
        if (hasattr(self, 'last_screen_size') and 
                (current_rect.width != self.last_screen_size[0] or 
                 current_rect.height != self.last_screen_size[1])):
            self.setup()
        
        # Store current screen size
        self.last_screen_size = (current_rect.width, current_rect.height)
    
    def render(self):
        # Fill background
        self.screen.fill(design.colors["background"])
        
        # Draw title
        title_font = design.get_font("large")
        title_text = title_font.render("Semantic Analysis", True, design.colors["text"])
        title_rect = title_text.get_rect(centerx=self.screen_rect.centerx, top=15)
        self.screen.blit(title_text, title_rect)
        
        # Draw semantic analysis area
        pygame.draw.rect(self.screen, (255, 255, 255), self.semantic_analysis_rect)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.semantic_analysis_rect, 1)
        
        if self.semantic_analysis_surface:
            try:
                # Create a subsurface of the screen for the image area to clip the content
                image_view = self.screen.subsurface(self.semantic_analysis_rect)
                
                # Calculate scaled dimensions
                scaled_width = int(self.original_width * self.scale_factor)
                scaled_height = int(self.original_height * self.scale_factor)
                
                # Create a scaled surface with current scale factor
                # Using smoothscale for better quality
                scaled_surface = pygame.transform.smoothscale(
                    self.semantic_analysis_surface, (scaled_width, scaled_height)
                )
                
                # Calculate position to center the view
                view_x = (self.semantic_analysis_rect.width / 2) - (self.camera_x * self.scale_factor)
                view_y = (self.semantic_analysis_rect.height / 2) - (self.camera_y * self.scale_factor)
                
                # Blit the image with calculated position
                image_view.blit(scaled_surface, (view_x, view_y))
                
            except Exception as e:
                print(f"Error rendering semantic analysis: {e}")
        
        # Draw buttons
        self.back_button.render(self.screen)
        self.symbol_table_button.render(self.screen)
        self.next_button.render(self.screen)
        
        # Render symbol table view if active
        if self.symbol_table_view:
            self.symbol_table_view.render()
    
    def show_symbol_table_view(self):
        self.symbol_table_view = SymbolTableView(self, self.enhanced_symbol_table_path, 
                                                on_close=self.close_symbol_table_view)
    
    def close_symbol_table_view(self):
        self.symbol_table_view = None