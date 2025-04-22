"""
Syntactic Analysis View for the Full Stack Compiler
Displays the parse tree and provides access to symbol table
"""
import pygame
import os
from GUI.view_base import ViewBase
from GUI.components.button import Button
from GUI.design_base import design
from GUI.components.scrollbar import Scrollbar
from GUI.views.symbol_table_view import SymbolTableView
from config import States

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
        self.scroll_y = 0
        self.max_scroll_y = 0
        self.scrollbar = None
        self.symbol_table_view = None
        self.is_dragging = False
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
        
        # Full display area for parse tree
        display_height = screen_height - title_height - button_height - bottom_margin - button_margin
        
        # Parse tree display area - full width
        self.parse_tree_rect = pygame.Rect(
            button_margin, 
            title_height,
            screen_width - 2 * button_margin,
            display_height
        )
        
        # Create scrollbar
        scrollbar_width = 15
        self.scrollbar_rect = pygame.Rect(
            self.parse_tree_rect.right - scrollbar_width,
            self.parse_tree_rect.top,
            scrollbar_width,
            self.parse_tree_rect.height
        )
        
        # Load parse tree image
        self.load_parse_tree()
    
    def load_parse_tree(self):
        if self.parse_tree_path and os.path.exists(self.parse_tree_path):
            try:
                self.parse_tree_surface = pygame.image.load(self.parse_tree_path)
                self.max_scroll_y = max(0, self.parse_tree_surface.get_height() - self.parse_tree_rect.height)
                
                if self.max_scroll_y > 0:
                    self.scrollbar = Scrollbar(
                        self.scrollbar_rect,
                        self.parse_tree_surface.get_height(),
                        self.parse_tree_rect.height
                    )
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
            
            # Handle scrolling
            if self.scrollbar and self.scrollbar.handle_event(event):
                self.scroll_y = int(self.scrollbar.get_scroll_offset())
                return True
            
            # Mouse wheel scrolling
            if event.type == pygame.MOUSEWHEEL:
                if self.parse_tree_rect.collidepoint(pygame.mouse.get_pos()):
                    self.scroll_y = max(0, min(self.max_scroll_y, 
                                       self.scroll_y - event.y * 20))
                    if self.scrollbar:
                        self.scrollbar.set_scroll_offset(self.scroll_y)
                    return True
            
            # Handle mouse dragging
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.parse_tree_rect.collidepoint(event.pos):
                    self.is_dragging = True
                    self.last_mouse_y = event.pos[1]
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    return True
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
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
                
                # Handle dragging
                if self.is_dragging:
                    dy = self.last_mouse_y - event.pos[1]
                    self.last_mouse_y = event.pos[1]
                    
                    self.scroll_y = max(0, min(self.max_scroll_y, self.scroll_y + dy))
                    if self.scrollbar:
                        self.scrollbar.set_scroll_offset(self.scroll_y)
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
        
        # Render parse tree image
        if self.parse_tree_surface:
            clip_rect = pygame.Rect(0, 0, self.parse_tree_rect.width, self.parse_tree_rect.height)
            parse_view = self.screen.subsurface(self.parse_tree_rect)
            parse_view.set_clip(clip_rect)
            
            pos_x = (self.parse_tree_rect.width - self.parse_tree_surface.get_width()) // 2
            pos_x = max(pos_x, 0)
            pos_y = -self.scroll_y
            
            parse_view.blit(self.parse_tree_surface, (pos_x, pos_y))
            parse_view.set_clip(None)
        
        # Draw scrollbar
        if self.scrollbar:
            self.scrollbar.render(self.screen)
        
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