"""
Scrollbar component for scrollable content
"""
import pygame
from GUI.design_base import design

class Scrollbar:
    """
    Scrollbar component for scrollable content
    """
    def __init__(self, rect, content_height, viewport_height):
        """
        Initialize the scrollbar
        
        Args:
            rect: Rectangle for the scrollbar
            content_height: Total height of the content
            viewport_height: Height of the visible viewport
        """
        self.rect = pygame.Rect(rect)
        self.content_height = max(content_height, viewport_height)
        self.viewport_height = viewport_height
        self.scroll_pos = 0  # Position from 0 to 1
        self.is_dragging = False
        self.drag_offset = 0
        
        # Calculate thumb dimensions
        self.update_thumb()
    
    def update_content_height(self, content_height):
        """
        Update the content height and recalculate thumb dimensions
        
        Args:
            content_height: New content height
        """
        # Always set content height to at least viewport height to avoid division by zero
        self.content_height = max(content_height, self.viewport_height)
        self.update_thumb()
    
    def update_thumb(self):
        """
        Update the thumb dimensions based on content vs viewport
        """
        visible_ratio = min(1.0, self.viewport_height / self.content_height)
        
        # Thumb height is the visible_ratio of the scrollbar height
        self.thumb_height = max(20, int(self.rect.height * visible_ratio))
        
        # Calculate thumb position
        thumb_range = max(1, self.rect.height - self.thumb_height)
        self.thumb_pos = int(self.scroll_pos * thumb_range)
        
        # Create thumb rectangle
        self.thumb_rect = pygame.Rect(
            self.rect.x,
            self.rect.y + self.thumb_pos,
            self.rect.width,
            self.thumb_height
        )
    
    def handle_event(self, event):
        """
        Handle events for the scrollbar
        
        Args:
            event: Pygame event
        """
        if self.content_height <= self.viewport_height:
            # No need for scrollbar if content fits in viewport
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.thumb_rect.collidepoint(event.pos):
                self.is_dragging = True
                self.drag_offset = event.pos[1] - self.thumb_rect.y
                return True
            elif self.rect.collidepoint(event.pos):
                # Click on scrollbar but not on thumb - jump to that position
                self.scroll_pos = min(1.0, max(0.0, 
                    (event.pos[1] - self.rect.y - self.thumb_height / 2) / 
                    max(1, self.rect.height - self.thumb_height)))
                self.update_thumb()
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging = False
        
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            # Calculate new scroll position based on mouse movement
            scroll_y = event.pos[1] - self.drag_offset - self.rect.y
            self.scroll_pos = min(1.0, max(0.0, 
                scroll_y / max(1, self.rect.height - self.thumb_height)))
            self.update_thumb()
            return True
        
        elif event.type == pygame.MOUSEWHEEL:
            # Increase scroll amount for more responsiveness
            scroll_amount = event.y * -0.25  # Increased for faster scrolling
            self.scroll_pos = min(1.0, max(0.0, self.scroll_pos + scroll_amount))
            self.update_thumb()
            return True
        
        return False
    
    def get_scroll_offset(self):
        """
        Get the scroll offset in pixels
        
        Returns:
            int: Scroll offset in pixels
        """
        try:
            # Calculate the actual scroll offset based on content height and viewport height
            max_offset = max(0, self.content_height - self.viewport_height)
            return int(self.scroll_pos * max_offset)
        except Exception as e:
            print(f"Error en get_scroll_offset: {e}")
            return 0
    
    def set_scroll_offset(self, offset_pixels):
        """
        Set the scroll position based on pixel offset
        
        Args:
            offset_pixels: Offset in pixels
        """
        try:
            max_offset = max(1, self.content_height - self.viewport_height)
            if max_offset > 0:
                self.scroll_pos = min(1.0, max(0.0, offset_pixels / max_offset))
            else:
                self.scroll_pos = 0
            
            self.update_thumb()
        except Exception as e:
            print(f"Error en set_scroll_offset: {e}")
            self.scroll_pos = 0
            self.update_thumb()
        
        self.update_thumb()
    
    def render(self, surface):
        """
        Render the scrollbar
        
        Args:
            surface: Surface to render on
        """
        if self.content_height <= self.viewport_height:
            # Don't render if content fits in viewport
            return
        
        # Draw scrollbar background
        pygame.draw.rect(surface, design.colors["button"], self.rect)
        
        # Draw thumb
        pygame.draw.rect(surface, design.colors["button_hover"], self.thumb_rect, 0, 3)
        pygame.draw.rect(surface, design.colors["textbox_border"], self.thumb_rect, 1, 3)