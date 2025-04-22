"""
Syntactic Analysis View for the Full Stack Compiler
Displays the parse tree and symbol table
"""
import pygame
import os
from GUI.components.scrollbar import Scrollbar
from GUI.view_base import ViewBase
from GUI.components.button import Button
from GUI.design_base import design
from config import States

class SyntacticAnalysisView(ViewBase):
    """
    View for displaying syntactic analysis results
    """
    def __init__(self, view_controller, editor_view=None, parse_tree_path=None, symbol_table_path=None):
        """
        Initialize the syntactic analysis view
        
        Args:
            view_controller: View controller instance
            editor_view: Reference to the editor view for returning
            parse_tree_path: Path to the parse tree image
            symbol_table_path: Path to the symbol table image
        """
        super().__init__(view_controller)
        self.editor_view = editor_view
        self.parse_tree_path = parse_tree_path
        self.symbol_table_path = symbol_table_path
        
        # Initialize surfaces for the images
        self.parse_tree_surface = None
        self.symbol_table_surface = None
        
        # Scrolling state
        self.left_scroll_y = 0
        self.left_max_scroll_y = 0
        self.right_scroll_y = 0
        self.right_max_scroll_y = 0
        
        # Scrollbars
        self.left_scrollbar = None
        self.right_scrollbar = None
        
        # Mouse state for dragging
        self.is_dragging_left = False
        self.is_dragging_right = False
        self.last_mouse_y = 0
    
    def setup(self):
        """
        Set up the syntactic analysis view
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
        
        # Create back button (bottom left)
        self.back_button = Button(
            pygame.Rect(button_margin, screen_height - button_height - bottom_margin, 
                       button_width, button_height),
            "Back to Home"
        )
        
        # Create next button (bottom right)
        self.next_button = Button(
            pygame.Rect(screen_width - button_width - button_margin, 
                       screen_height - button_height - bottom_margin,
                       button_width, button_height),
            "Next"
        )
        
        # Calculate display areas for parse tree and symbol table
        # Full height excluding title and button areas
        display_height = screen_height - title_height - button_height - bottom_margin - button_margin
        
        # Left side for parse tree (60% of width)
        left_width = int(screen_width * 0.58)
        self.parse_tree_rect = pygame.Rect(
            button_margin, 
            title_height,
            left_width - button_margin * 2,
            display_height
        )
        
        # Right side for symbol table (40% of width)
        right_width = screen_width - left_width
        self.symbol_table_rect = pygame.Rect(
            left_width + button_margin, 
            title_height,
            right_width - button_margin * 2,
            display_height
        )
        
        # Create scrollbars
        scrollbar_width = 15
        self.left_scrollbar_rect = pygame.Rect(
            self.parse_tree_rect.right - scrollbar_width,
            self.parse_tree_rect.top,
            scrollbar_width,
            self.parse_tree_rect.height
        )
        
        self.right_scrollbar_rect = pygame.Rect(
            self.symbol_table_rect.right - scrollbar_width,
            self.symbol_table_rect.top,
            scrollbar_width,
            self.symbol_table_rect.height
        )
        
        # Load images
        self.load_images()
    
    def load_images(self):
        """
        Load the parse tree and symbol table images
        """
        # Load parse tree image
        if self.parse_tree_path and os.path.exists(self.parse_tree_path):
            try:
                self.parse_tree_surface = pygame.image.load(self.parse_tree_path)
                # Calculate max scroll
                self.left_max_scroll_y = max(0, self.parse_tree_surface.get_height() - self.parse_tree_rect.height)
                
                # Create scrollbar if needed
                if self.left_max_scroll_y > 0:
                    self.left_scrollbar = Scrollbar(
                        self.left_scrollbar_rect,
                        self.parse_tree_surface.get_height(),
                        self.parse_tree_rect.height
                    )
            except Exception as e:
                print(f"Error loading parse tree image: {e}")
                self.parse_tree_surface = self.create_placeholder_image("Error loading parse tree image")
        else:
            self.parse_tree_surface = self.create_placeholder_image("Parse tree image not available")
        
        # Load symbol table image
        if self.symbol_table_path and os.path.exists(self.symbol_table_path):
            try:
                self.symbol_table_surface = pygame.image.load(self.symbol_table_path)
                # Calculate max scroll
                self.right_max_scroll_y = max(0, self.symbol_table_surface.get_height() - self.symbol_table_rect.height)
                
                # Create scrollbar if needed
                if self.right_max_scroll_y > 0:
                    self.right_scrollbar = Scrollbar(
                        self.right_scrollbar_rect,
                        self.symbol_table_surface.get_height(),
                        self.symbol_table_rect.height
                    )
            except Exception as e:
                print(f"Error loading symbol table image: {e}")
                self.symbol_table_surface = self.create_placeholder_image("Error loading symbol table image")
        else:
            self.symbol_table_surface = self.create_placeholder_image("Symbol table image not available")
    
    def create_placeholder_image(self, message):
        """
        Create a placeholder image with a message
        
        Args:
            message: Message to display
            
        Returns:
            pygame.Surface: Placeholder image
        """
        # Create a surface for the placeholder
        surface = pygame.Surface((400, 300))
        surface.fill((240, 240, 240))
        
        # Create text
        font = design.get_font("medium")
        text = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(200, 150))
        
        # Draw border and text
        pygame.draw.rect(surface, (200, 200, 200), pygame.Rect(0, 0, 400, 300), 1)
        surface.blit(text, text_rect)
        
        return surface
    
    def handle_events(self, events):
        """
        Handle pygame events
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.view_controller.quit()
                return True
            
            # Handle back button
            if self.back_button.handle_event(event):
                # Change back to editor view
                self.view_controller.change_state(States.EDITOR)
                return True
            
            # Handle next button
            if self.next_button.handle_event(event):
                # This would be connected to semantic analysis view in the future
                print("Next button pressed - semantic analysis not implemented yet")
                return True
            
            # Handle scrollbar events
            if self.left_scrollbar and self.left_scrollbar.handle_event(event):
                self.left_scroll_y = int(self.left_scrollbar.get_scroll_offset())
                return True
            
            if self.right_scrollbar and self.right_scrollbar.handle_event(event):
                self.right_scroll_y = int(self.right_scrollbar.get_scroll_offset())
                return True
            
            # Handle mouse wheel events
            if event.type == pygame.MOUSEWHEEL:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check which area the mouse is over
                if self.parse_tree_rect.collidepoint(mouse_pos):
                    # Scroll parse tree
                    self.left_scroll_y = max(0, min(self.left_max_scroll_y, 
                                           self.left_scroll_y - event.y * 20))
                    if self.left_scrollbar:
                        self.left_scrollbar.set_scroll_offset(self.left_scroll_y)
                    return True
                
                elif self.symbol_table_rect.collidepoint(mouse_pos):
                    # Scroll symbol table
                    self.right_scroll_y = max(0, min(self.right_max_scroll_y, 
                                            self.right_scroll_y - event.y * 20))
                    if self.right_scrollbar:
                        self.right_scrollbar.set_scroll_offset(self.right_scroll_y)
                    return True
            
            # Handle mouse dragging for images
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                self.last_mouse_y = mouse_pos[1]
                
                if self.parse_tree_rect.collidepoint(mouse_pos):
                    self.is_dragging_left = True
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    return True
                
                elif self.symbol_table_rect.collidepoint(mouse_pos):
                    self.is_dragging_right = True
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    return True
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.is_dragging_left or self.is_dragging_right:
                    self.is_dragging_left = False
                    self.is_dragging_right = False
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    return True
            
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                
                # Change cursor if over image areas
                if not (self.is_dragging_left or self.is_dragging_right):
                    if self.parse_tree_rect.collidepoint(mouse_pos) or self.symbol_table_rect.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                
                # Handle dragging
                if self.is_dragging_left or self.is_dragging_right:
                    dy = self.last_mouse_y - mouse_pos[1]
                    self.last_mouse_y = mouse_pos[1]
                    
                    if self.is_dragging_left:
                        # Update parse tree scroll
                        self.left_scroll_y = max(0, min(self.left_max_scroll_y, 
                                               self.left_scroll_y + dy))
                        if self.left_scrollbar:
                            self.left_scrollbar.set_scroll_offset(self.left_scroll_y)
                    
                    if self.is_dragging_right:
                        # Update symbol table scroll
                        self.right_scroll_y = max(0, min(self.right_max_scroll_y, 
                                                self.right_scroll_y + dy))
                        if self.right_scrollbar:
                            self.right_scrollbar.set_scroll_offset(self.right_scroll_y)
                    
                    return True
        
        return False
    
    def update(self, dt):
        """
        Update the view
        """
        pass
    
    def render(self):
        """
        Render the view
        """
        # Fill the background
        self.screen.fill(design.colors["background"])
        
        # Draw title
        title_font = design.get_font("large")
        title_text = title_font.render("Syntactic Analysis", True, design.colors["text"])
        title_rect = title_text.get_rect(centerx=self.screen_rect.centerx, top=15)
        self.screen.blit(title_text, title_rect)
        
        # Draw parse tree section title
        section_font = design.get_font("medium")
        parse_title = section_font.render("Parse Tree", True, design.colors["text"])
        parse_title_rect = parse_title.get_rect(centerx=self.parse_tree_rect.centerx, top=self.parse_tree_rect.top - 30)
        self.screen.blit(parse_title, parse_title_rect)
        
        # Draw symbol table section title
        symbol_title = section_font.render("Symbol Table", True, design.colors["text"])
        symbol_title_rect = symbol_title.get_rect(centerx=self.symbol_table_rect.centerx, top=self.symbol_table_rect.top - 30)
        self.screen.blit(symbol_title, symbol_title_rect)
        
        # Draw parse tree area background
        pygame.draw.rect(self.screen, (255, 255, 255), self.parse_tree_rect)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.parse_tree_rect, 1)
        
        # Draw symbol table area background
        pygame.draw.rect(self.screen, (255, 255, 255), self.symbol_table_rect)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.symbol_table_rect, 1)
        
        # Render parse tree image
        if self.parse_tree_surface:
            # Create a subsurface to clip the content
            clip_rect = pygame.Rect(0, 0, self.parse_tree_rect.width, self.parse_tree_rect.height)
            parse_view = self.screen.subsurface(self.parse_tree_rect)
            parse_view.set_clip(clip_rect)
            
            # Calculate position based on scroll
            pos_x = (self.parse_tree_rect.width - self.parse_tree_surface.get_width()) // 2
            pos_x = max(pos_x, 0)  # Ensure non-negative
            pos_y = -self.left_scroll_y
            
            # Blit the image
            parse_view.blit(self.parse_tree_surface, (pos_x, pos_y))
            parse_view.set_clip(None)
        
        # Render symbol table image
        if self.symbol_table_surface:
            # Create a subsurface to clip the content
            clip_rect = pygame.Rect(0, 0, self.symbol_table_rect.width, self.symbol_table_rect.height)
            symbol_view = self.screen.subsurface(self.symbol_table_rect)
            symbol_view.set_clip(clip_rect)
            
            # Calculate position based on scroll
            pos_x = (self.symbol_table_rect.width - self.symbol_table_surface.get_width()) // 2
            pos_x = max(pos_x, 0)  # Ensure non-negative
            pos_y = -self.right_scroll_y
            
            # Blit the image
            symbol_view.blit(self.symbol_table_surface, (pos_x, pos_y))
            symbol_view.set_clip(None)
        
        # Draw scrollbars if needed
        if self.left_scrollbar:
            self.left_scrollbar.render(self.screen)
        
        if self.right_scrollbar:
            self.right_scrollbar.render(self.screen)
        
        # Draw buttons
        self.back_button.render(self.screen)
        self.next_button.render(self.screen)