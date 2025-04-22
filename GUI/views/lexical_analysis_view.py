"""
Updated Lexical Analysis View with proper HorizontalScrollbar
"""
import pygame
import os
from GUI.view_base import ViewBase
from GUI.components.button import Button
from GUI.design_base import design
from GUI.components.horizontal_scrollbar import HorizontalScrollbar
from CompilerLogic.syntacticAnalyzer import SyntacticAnalyzer
from config import States

class LexicalAnalysisView(ViewBase):
    """
    View for displaying lexical analysis results
    """
    def __init__(self, view_controller, editor_view=None, token_graph_path=None):
        """
        Initialize the lexical analysis view
        
        Args:
            view_controller: View controller instance
            editor_view: Reference to the editor view for returning
            token_graph_path: Path to the token graph image
        """
        super().__init__(view_controller)
        self.editor_view = editor_view
        self.token_graph_path = token_graph_path
        self.token_graph_surface = None
        self.horizontal_scroll = 0
        self.max_horizontal_scroll = 0
        self.scrollbar = None
        self.is_dragging = False
        self.last_mouse_x = 0
    
    def setup(self):
        """
        Set up the lexical analysis view
        """
        # Get screen dimensions
        screen_rect = self.screen.get_rect()
        screen_width = screen_rect.width
        screen_height = screen_rect.height
        
        # Calculate layout
        button_height = 40
        button_width = 150
        button_margin = 20
        bottom_margin = 15
        title_height = 50  # Space for title
        extra_bottom_space = 100  # Additional space between image and buttons
        
        # Create back button (bottom left)
        self.back_button = Button(
            pygame.Rect(button_margin, screen_height - button_height - bottom_margin, 
                       button_width, button_height),
            "Back to Editor"
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
        
        # Create image display area with proper spacing
        image_margin_top = title_height
        # Reduce image area height to add space at the bottom
        image_area_height = screen_height - button_height - bottom_margin - image_margin_top - extra_bottom_space
        self.image_rect = pygame.Rect(
            button_margin, 
            image_margin_top,
            screen_width - 2 * button_margin,
            image_area_height
        )
        
        # Create horizontal scrollbar
        scrollbar_height = 15
        self.scrollbar_rect = pygame.Rect(
            self.image_rect.left,
            self.image_rect.bottom + 5,
            self.image_rect.width,
            scrollbar_height
        )
        
        # Load token graph image
        self.load_token_graph()
        
        # Initialize scrollbar if image is wider than display area
        if self.token_graph_surface and self.token_graph_surface.get_width() > self.image_rect.width:
            # Use HorizontalScrollbar instead of Scrollbar
            self.scrollbar = HorizontalScrollbar(
                self.scrollbar_rect,
                self.token_graph_surface.get_width(),
                self.image_rect.width
            )
            self.max_horizontal_scroll = max(0, self.token_graph_surface.get_width() - self.image_rect.width)
        else:
            self.scrollbar = None
            self.max_horizontal_scroll = 0
    
    def load_token_graph(self):
        """
        Load the token graph image from file with better scaling
        """
        if not self.token_graph_path or not os.path.exists(self.token_graph_path):
            # Create a placeholder image if no token graph is available
            self.token_graph_surface = self.create_placeholder_image("No token graph available")
            return
        
        try:
            # Load the image
            original_surface = pygame.image.load(self.token_graph_path)
            
            # Get available display area
            available_height = self.image_rect.height * 0.9  # Leave 10% margin
            available_width = self.image_rect.width * 0.9  # For initial display
            
            # Calculate aspect ratio of original image
            original_aspect = original_surface.get_width() / original_surface.get_height()
            
            # Determine target height based on available space, limited by available height
            target_height = min(available_height, original_surface.get_height())
            
            # Calculate width based on aspect ratio
            calculated_width = target_height * original_aspect
            
            # Ensure width is reasonable for scrolling (not too small)
            # We want the image to be larger than the viewport to enable scrolling
            minimum_width = max(original_surface.get_width() * 0.5, self.image_rect.width * 1.5)
            target_width = max(calculated_width, minimum_width)
            
            # Scale the image
            self.token_graph_surface = pygame.transform.smoothscale(
                original_surface, (int(target_width), int(target_height)))
                
        except Exception as e:
            print(f"Error loading token graph: {e}")
            self.token_graph_surface = self.create_placeholder_image(f"Error loading token graph: {e}")
    
    def create_placeholder_image(self, message):
        """
        Create a placeholder image with an error message
        
        Args:
            message: Message to display in the placeholder
            
        Returns:
            pygame.Surface: Placeholder image surface
        """
        # Create a surface for the placeholder
        surface = pygame.Surface((800, 200))
        surface.fill((240, 240, 240))
        
        # Create text
        font = design.get_font("medium")
        text = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(400, 100))
        
        # Draw border and text
        pygame.draw.rect(surface, (200, 200, 200), pygame.Rect(0, 0, 800, 200), 1)
        surface.blit(text, text_rect)
        
        return surface
    
    def update(self, dt):
        """
        Update the view
        
        Args:
            dt: Time elapsed since last update (delta time)
        """
        pass
    
    def set_token_graph(self, token_graph_path):
        """
        Set the token graph path and reload the image
        
        Args:
            token_graph_path: Path to the token graph image
        """
        self.token_graph_path = token_graph_path
        self.load_token_graph()
        
        # Reset scroll position
        self.horizontal_scroll = 0
        
        # Update scrollbar
        if self.token_graph_surface and self.image_rect:
            if self.token_graph_surface.get_width() > self.image_rect.width:
                # Use HorizontalScrollbar instead of Scrollbar
                self.scrollbar = HorizontalScrollbar(
                    self.scrollbar_rect,
                    self.token_graph_surface.get_width(),
                    self.image_rect.width
                )
                self.max_horizontal_scroll = max(0, self.token_graph_surface.get_width() - self.image_rect.width)
            else:
                self.scrollbar = None
                self.max_horizontal_scroll = 0
    
    def handle_events(self, events):
        """
        Handle pygame events
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.view_controller.quit()
                return True
            
            # Handle back button - preserve editor state
            if self.back_button.handle_event(event):
                # The editor view reference should be properly set during initialization
                if self.editor_view:
                    # Clear any error highlights in the editor
                    if hasattr(self.editor_view, 'text_editor') and hasattr(self.editor_view.text_editor, 'clear_error_highlights'):
                        self.editor_view.text_editor.clear_error_highlights()
                    
                    # Ensure the editor instance is stored in the view controller
                    # This is critical to ensure we don't lose state
                    self.view_controller.editor_view_instance = self.editor_view
                    
                    # Print debug information
                    print(f"Returning to editor with file: {self.editor_view.current_file_path}")
                    print(f"Editor file status: {self.editor_view.file_status}")
                else:
                    print("Warning: No editor view reference found!")
                
                # Change back to editor state
                self.view_controller.change_state(States.EDITOR)
                return True
            
            # Handle next button
            if self.next_button.handle_event(event):
                # Run syntactic analysis
                analyzer = SyntacticAnalyzer()
                
                # Get the current code from the editor
                if self.editor_view and hasattr(self.editor_view, 'text_editor'):
                    code_text = self.editor_view.text_editor.get_text()
                    
                    # Run analysis
                    success, errors, parse_tree_path, symbol_table_path = analyzer.analyze(code_text)
                    
                    if success:
                        # Move to syntactic analysis view
                        self.view_controller.parse_tree_path = parse_tree_path
                        self.view_controller.symbol_table_path = symbol_table_path
                        self.view_controller.change_state(States.SYNTACTIC_ANALYSIS)
                    else:
                        # Show errors in editor view
                        if self.editor_view and hasattr(self.editor_view, 'text_editor'):
                            self.editor_view.text_editor.clear_error_highlights()
                            self.editor_view.text_editor.highlight_errors(errors)
                            
                        # Return to editor view to show errors
                        self.view_controller.change_state(States.EDITOR)
                else:
                    print("Cannot access editor content")
                
                return True
            
            # Handle scrollbar events with the horizontal scrollbar
            if self.scrollbar and self.scrollbar.handle_event(event):
                self.horizontal_scroll = int(self.scrollbar.get_scroll_offset())
                return True
            
            # Handle direct image dragging with mouse
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.image_rect.collidepoint(event.pos):
                    self.is_dragging = True
                    self.last_mouse_x = event.pos[0]
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
                    return True
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.is_dragging:
                    self.is_dragging = False
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    return True
            
            elif event.type == pygame.MOUSEMOTION and self.is_dragging:
                dx = self.last_mouse_x - event.pos[0]
                self.last_mouse_x = event.pos[0]
                
                # Update horizontal scroll
                new_scroll = min(self.max_horizontal_scroll, 
                            max(0, self.horizontal_scroll + dx))
                self.horizontal_scroll = new_scroll
                
                # Update scrollbar if it exists
                if self.scrollbar:
                    self.scrollbar.set_scroll_offset(self.horizontal_scroll)
                
                return True
            
            # Handle mousewheel for horizontal scrolling
            elif event.type == pygame.MOUSEWHEEL:
                if self.image_rect.collidepoint(pygame.mouse.get_pos()):
                    # Use horizontal value if available, otherwise vertical
                    scroll_amount = event.x if hasattr(event, 'x') and event.x != 0 else event.y
                    # For smoother scrolling, scale the amount
                    dx = scroll_amount * -30  # Negative because scrolling down should move content right
                    
                    new_scroll = min(self.max_horizontal_scroll,
                                max(0, self.horizontal_scroll - dx))
                    self.horizontal_scroll = new_scroll
                    
                    # Update scrollbar if it exists
                    if self.scrollbar:
                        self.scrollbar.set_scroll_offset(self.horizontal_scroll)
                    
                    return True
            
            # Reset cursor when not over the image area
            if event.type == pygame.MOUSEMOTION and not self.is_dragging:
                if self.image_rect.collidepoint(event.pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        return False

    def render(self):
        """
        Render the view on screen
        """
        # Fill the background
        self.screen.fill(design.colors["background"])
        
        # Draw title with more vertical space
        title_font = design.get_font("large")
        title_text = title_font.render("Lexical Analysis", True, design.colors["text"])
        title_rect = title_text.get_rect(centerx=self.screen_rect.centerx, top=15)
        self.screen.blit(title_text, title_rect)
        
        # Draw image display area background
        pygame.draw.rect(self.screen, (255, 255, 255), self.image_rect)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.image_rect, 1)
        
        # Draw the token graph
        if self.token_graph_surface:
            try:
                # Create a subsurface of the screen for the image area to clip the content
                image_view = self.screen.subsurface(self.image_rect)
                
                # Calculate vertical centering
                y_offset = max(0, (self.image_rect.height - self.token_graph_surface.get_height()) // 2)
                
                # Calculate horizontal offset based on scroll position
                x_offset = -self.horizontal_scroll
                
                # Ensure we don't scroll past the image width
                if self.horizontal_scroll + self.image_rect.width > self.token_graph_surface.get_width():
                    x_offset = -(self.token_graph_surface.get_width() - self.image_rect.width)
                    if x_offset > 0:
                        x_offset = 0
                
                # Blit the image with proper positioning
                image_view.blit(
                    self.token_graph_surface,
                    (x_offset, y_offset)
                )
            except Exception as e:
                print(f"Error rendering token graph: {e}")
        
        # Draw scrollbar if needed
        if self.scrollbar:
            self.scrollbar.render(self.screen)
        
        # Draw buttons
        self.back_button.render(self.screen)
        self.next_button.render(self.screen)