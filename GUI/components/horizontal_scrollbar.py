"""
Horizontal Scrollbar component for scrollable content
"""
import pygame
from GUI.design_base import design

class HorizontalScrollbar:
    """
    Horizontal Scrollbar component for scrollable content
    """
    def __init__(self, rect, content_width, viewport_width):
        """
        Initialize the horizontal scrollbar
        
        Args:
            rect: Rectangle for the scrollbar
            content_width: Total width of the content
            viewport_width: Width of the visible viewport
        """
        self.rect = pygame.Rect(rect)
        self.content_width = max(content_width, viewport_width)
        self.viewport_width = viewport_width
        self.scroll_pos = 0  # Position from 0 to 1
        self.is_dragging = False
        self.drag_offset = 0
        
        # Calculate thumb dimensions
        self.update_thumb()
    
    def update_content_width(self, content_width):
        """
        Update the content width and recalculate thumb dimensions
        
        Args:
            content_width: New content width
        """
        # Always set content width to at least viewport width to avoid division by zero
        self.content_width = max(content_width, self.viewport_width)
        self.update_thumb()
    
    def update_thumb(self):
        """
        Update the thumb dimensions based on content vs viewport
        """
        visible_ratio = min(1.0, self.viewport_width / self.content_width)
        
        # Thumb width is the visible_ratio of the scrollbar width
        self.thumb_width = max(20, int(self.rect.width * visible_ratio))
        
        # Calculate thumb position
        thumb_range = max(1, self.rect.width - self.thumb_width)
        self.thumb_pos = int(self.scroll_pos * thumb_range)
        
        # Create thumb rectangle
        self.thumb_rect = pygame.Rect(
            self.rect.x + self.thumb_pos,
            self.rect.y,
            self.thumb_width,
            self.rect.height
        )
    
    def handle_event(self, event):
        """
        Handle events for the scrollbar
        
        Args:
            event: Pygame event
        """
        if self.content_width <= self.viewport_width:
            # No need for scrollbar if content fits in viewport
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.thumb_rect.collidepoint(event.pos):
                self.is_dragging = True
                self.drag_offset = event.pos[0] - self.thumb_rect.x
                return True
            elif self.rect.collidepoint(event.pos):
                # Click on scrollbar but not on thumb - jump to that position
                self.scroll_pos = min(1.0, max(0.0, 
                    (event.pos[0] - self.rect.x - self.thumb_width / 2) / 
                    max(1, self.rect.width - self.thumb_width)))
                self.update_thumb()
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging = False
        
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            # Calculate new scroll position based on mouse movement
            scroll_x = event.pos[0] - self.drag_offset - self.rect.x
            self.scroll_pos = min(1.0, max(0.0, 
                scroll_x / max(1, self.rect.width - self.thumb_width)))
            self.update_thumb()
            return True
        
        elif event.type == pygame.MOUSEWHEEL:
            # For horizontal scrolling, we should use horizontal wheel values if available
            # Otherwise use vertical values (most common)
            scroll_amount = event.x if hasattr(event, 'x') and event.x != 0 else event.y
            # Increase scroll amount for more responsiveness
            scroll_amount = scroll_amount * -0.25  # Increased for faster scrolling
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
            # Calculate the actual scroll offset based on content width and viewport width
            max_offset = max(0, self.content_width - self.viewport_width)
            return int(self.scroll_pos * max_offset)
        except Exception as e:
            print(f"Error in get_scroll_offset: {e}")
            return 0
    
    def set_scroll_offset(self, offset_pixels):
        """
        Set the scroll position based on pixel offset
        
        Args:
            offset_pixels: Offset in pixels
        """
        try:
            max_offset = max(1, self.content_width - self.viewport_width)
            if max_offset > 0:
                self.scroll_pos = min(1.0, max(0.0, offset_pixels / max_offset))
            else:
                self.scroll_pos = 0
            
            self.update_thumb()
        except Exception as e:
            print(f"Error in set_scroll_offset: {e}")
            self.scroll_pos = 0
            self.update_thumb()
    
    def render(self, surface):
        """
        Render the scrollbar
        
        Args:
            surface: Surface to render on
        """
        if self.content_width <= self.viewport_width:
            # Don't render if content fits in viewport
            return
        
        # Draw scrollbar background
        pygame.draw.rect(surface, design.colors["button"], self.rect)
        
        # Draw thumb
        pygame.draw.rect(surface, design.colors["button_hover"], self.thumb_rect, 0, 3)
        pygame.draw.rect(surface, design.colors["textbox_border"], self.thumb_rect, 1, 3)