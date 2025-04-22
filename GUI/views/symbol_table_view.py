"""
Symbol Table View - A modal popup for displaying the symbol table
"""
import pygame
import os
from GUI.design_base import design
from GUI.components.button import Button

class SymbolTableView:
    """
    Modal symbol table view that overlays on top of the application
    """
    def __init__(self, parent_view, symbol_table_path, on_close=None):
        self.parent_view = parent_view
        self.screen = pygame.display.get_surface()
        self.symbol_table_path = symbol_table_path
        self.on_close = on_close
        
        # Calculate dimensions
        screen_rect = self.screen.get_rect()
        self.width = min(850, screen_rect.width - 40)
        self.height = min(650, screen_rect.height - 40)
        
        self.rect = pygame.Rect(
            (screen_rect.width - self.width) // 2,
            (screen_rect.height - self.height) // 2,
            self.width,
            self.height
        )
        
        # Content area (with margin)
        margin = 30
        self.content_rect = pygame.Rect(
            self.rect.x + margin,
            self.rect.y + margin,
            self.width - (margin * 2),
            self.height - (margin * 2)
        )
        
        # Image area
        button_height = 40
        button_margin = 20
        self.image_rect = pygame.Rect(
            self.content_rect.x,
            self.content_rect.y,
            self.content_rect.width,
            self.content_rect.height - button_height - button_margin
        )
        
        # Load symbol table image
        self.load_symbol_table()
        
        # Scrolling
        self.scroll_y = 0
        self.max_scroll_y = 0
        self.scroll_speed = 20
        
        # Scrollbar state
        self.scrollbar_dragging = False
        self.scrollbar_rect = None
        self.thumb_rect = None
        self.drag_offset_y = 0
        
        # Setup UI
        self.setup_ui()
        self.calculate_max_scroll()
    
    def load_symbol_table(self):
        try:
            if self.symbol_table_path and os.path.exists(self.symbol_table_path):
                self.symbol_table_surface = pygame.image.load(self.symbol_table_path)
            else:
                self.symbol_table_surface = self.create_placeholder_image("Symbol table image not available")
        except Exception as e:
            print(f"Error loading symbol table image: {e}")
            self.symbol_table_surface = self.create_placeholder_image(f"Error loading symbol table: {e}")
    
    def create_placeholder_image(self, message):
        surface = pygame.Surface((400, 200))
        surface.fill((240, 240, 240))
        font = design.get_font("medium")
        text = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(200, 100))
        pygame.draw.rect(surface, (200, 200, 200), pygame.Rect(0, 0, 400, 200), 1)
        surface.blit(text, text_rect)
        return surface
    
    def setup_ui(self):
        # Return button
        button_width = 150
        button_height = 40
        button_margin = 20
        
        self.return_button = Button(
            pygame.Rect(
                self.rect.centerx - button_width // 2,
                self.rect.bottom - button_height - button_margin,
                button_width,
                button_height
            ),
            "Return"
        )
    
    def calculate_max_scroll(self):
        if self.symbol_table_surface:
            image_height = self.symbol_table_surface.get_height()
            self.max_scroll_y = max(0, image_height - self.image_rect.height)
        else:
            self.max_scroll_y = 0
    
    def handle_events(self, events):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        for event in events:
            # Return button
            if self.return_button.handle_event(event):
                if self.on_close:
                    self.on_close()
                return True
            
            # Mouse wheel scrolling
            if event.type == pygame.MOUSEWHEEL:
                self.scroll_y = max(0, min(self.max_scroll_y, self.scroll_y - event.y * self.scroll_speed))
                return True
            
            # Scrollbar interaction
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.thumb_rect and self.thumb_rect.collidepoint(event.pos):
                    self.scrollbar_dragging = True
                    self.drag_offset_y = event.pos[1] - self.thumb_rect.y
                    return True
                elif self.scrollbar_rect and self.scrollbar_rect.collidepoint(event.pos):
                    relative_y = event.pos[1] - self.scrollbar_rect.y
                    ratio = relative_y / self.scrollbar_rect.height
                    self.scroll_y = min(self.max_scroll_y, max(0, int(ratio * self.max_scroll_y)))
                    return True
            
            # End dragging
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.scrollbar_dragging = False
                return False
            
            # Handle dragging
            if event.type == pygame.MOUSEMOTION and self.scrollbar_dragging:
                new_y = event.pos[1] - self.drag_offset_y
                scroll_range = self.scrollbar_rect.height - self.thumb_rect.height
                if scroll_range > 0:
                    ratio = max(0, min(1, (new_y - self.scrollbar_rect.y) / scroll_range))
                    self.scroll_y = int(ratio * self.max_scroll_y)
                return True
                    
            # ESC key to close
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.on_close:
                    self.on_close()
                return True
        
        return False
    
    def update(self, dt):
        pass

    def render(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Window background
        pygame.draw.rect(self.screen, design.colors["background"], self.rect, 0, 10)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.rect, 2, 10)
        
        # Title
        title_font = design.get_font("large")
        title_text = title_font.render("Symbol Table", True, design.colors["text"])
        title_rect = title_text.get_rect(centerx=self.rect.centerx, top=self.rect.top + 30)
        self.screen.blit(title_text, title_rect)
        
        # Image area
        pygame.draw.rect(self.screen, (255, 255, 255), self.image_rect)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.image_rect, 1)
        
        # Render image with scrolling
        if self.symbol_table_surface:
            image_view = self.screen.subsurface(self.image_rect)
            image_view.set_clip(pygame.Rect(0, 0, self.image_rect.width, self.image_rect.height))
            
            pos_x = max(0, (self.image_rect.width - self.symbol_table_surface.get_width()) // 2)
            pos_y = -self.scroll_y
            
            image_view.blit(self.symbol_table_surface, (pos_x, pos_y))
            image_view.set_clip(None)
        
        # Draw scrollbar if needed
        if self.max_scroll_y > 0:
            self.render_scrollbar()
        
        # Draw return button
        self.return_button.render(self.screen)
    
    def render_scrollbar(self):
        scrollbar_width = 10
        self.scrollbar_rect = pygame.Rect(
            self.image_rect.right - scrollbar_width,
            self.image_rect.top,
            scrollbar_width,
            self.image_rect.height
        )
        
        pygame.draw.rect(self.screen, design.colors["button"], self.scrollbar_rect)
        
        visible_ratio = min(1.0, self.image_rect.height / (self.image_rect.height + self.max_scroll_y))
        thumb_height = max(20, int(self.scrollbar_rect.height * visible_ratio))
        
        scroll_ratio = self.scroll_y / self.max_scroll_y if self.max_scroll_y > 0 else 0
        thumb_y = self.scrollbar_rect.top + int(scroll_ratio * (self.scrollbar_rect.height - thumb_height))
        
        self.thumb_rect = pygame.Rect(
            self.scrollbar_rect.x,
            thumb_y,
            self.scrollbar_rect.width,
            thumb_height
        )
        
        pygame.draw.rect(self.screen, design.colors["button_hover"], self.thumb_rect, 0, 3)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.thumb_rect, 1, 3)