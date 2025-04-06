import pygame
from GUI.design_base import design
from GUI.components.button import Button
from config import GRAMMAR

class GrammarView:
    """
    Modal grammar view that overlays on top of the main application
    """
    def __init__(self, parent_view, on_close=None):
        """
        Initialize the grammar view
        
        Args:
            parent_view: Parent view that opened this grammar view
            on_close: Callback function when grammar is closed
        """
        self.parent_view = parent_view
        self.screen = pygame.display.get_surface()
        self.on_close = on_close
        
        # Calculate dimensions - make it centered and smaller than the main window
        screen_rect = self.screen.get_rect()
        self.width = min(850, screen_rect.width - 40)
        self.height = min(650, screen_rect.height - 40)
        
        self.rect = pygame.Rect(
            (screen_rect.width - self.width) // 2,
            (screen_rect.height - self.height) // 2,
            self.width,
            self.height
        )
        
        # Calculate content area (with margin)
        margin = 30
        self.content_rect = pygame.Rect(
            self.rect.x + margin,
            self.rect.y + margin,
            self.width - (margin * 2),
            self.height - (margin * 2)
        )
        
        # Calculate text area (leaving space for button at bottom)
        button_height = 40
        button_margin = 20
        self.text_rect = pygame.Rect(
            self.content_rect.x,
            self.content_rect.y,
            self.content_rect.width,
            self.content_rect.height - button_height - button_margin
        )
        
        # Text content - from config.py
        self.text_content = GRAMMAR
        
        # Scrolling variables
        self.scroll_y = 0
        self.max_scroll_y = 0
        self.scroll_speed = 20
        
        # Scrollbar dragging state
        self.scrollbar_dragging = False
        self.scrollbar_rect = None
        self.thumb_rect = None
        self.drag_offset_y = 0
        
        # Create UI elements
        self.setup_ui()
        
        # Calculate maximum scroll value based on text height
        self.calculate_max_scroll()
    
    def setup_ui(self):
        """Set up UI elements"""
        # Return button at the center bottom of the window
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
        """Calculate the maximum scroll value based on text height"""
        # This will be dynamically calculated during rendering based on actual wrapped text
        # Just set an initial value here
        self.max_scroll_y = 1000  # Will be refined during rendering
    
    def handle_events(self, events):
        """
        Handle pygame events
        
        Args:
            events: List of pygame events
        """
        # Reset cursor to arrow when grammar view is active
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        for event in events:
            # Return button
            if self.return_button.handle_event(event):
                if self.on_close:
                    self.on_close()
                return True
            
            # Mouse wheel for scrolling
            if event.type == pygame.MOUSEWHEEL:
                # Scroll up or down
                self.scroll_y = max(0, min(self.max_scroll_y, self.scroll_y - event.y * self.scroll_speed))
                return True
            
            # Mouse button down - check for scrollbar interaction
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if clicking on the scrollbar thumb
                if self.thumb_rect and self.thumb_rect.collidepoint(event.pos):
                    self.scrollbar_dragging = True
                    self.drag_offset_y = event.pos[1] - self.thumb_rect.y
                    return True
                
                # Check if clicking on the scrollbar track
                elif self.scrollbar_rect and self.scrollbar_rect.collidepoint(event.pos):
                    # Click on track - move the scroll position proportionally
                    relative_y = event.pos[1] - self.scrollbar_rect.y
                    ratio = relative_y / self.scrollbar_rect.height
                    
                    # Set scroll position
                    self.scroll_y = min(self.max_scroll_y, max(0, int(ratio * (self.text_rect.height + self.max_scroll_y) - self.text_rect.height/2)))
                    return True
            
            # Mouse button up - stop dragging
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.scrollbar_dragging = False
                return False
            
            # Mouse motion - handle dragging
            if event.type == pygame.MOUSEMOTION and self.scrollbar_dragging:
                # Calculate new thumb position
                new_y = event.pos[1] - self.drag_offset_y
                
                # Calculate scroll position from thumb position
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
        """
        Update view logic
        
        Args:
            dt: Time elapsed since last update
        """
        pass

    def render(self):
        """Render the grammar view"""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Draw grammar window background
        pygame.draw.rect(self.screen, design.colors["background"], self.rect, 0, 10)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.rect, 2, 10)
        
        # Draw title
        title_font = design.get_font("large")
        title_text = title_font.render("Grammar", True, design.colors["text"])
        title_rect = title_text.get_rect(centerx=self.rect.centerx, top=self.rect.top + 30)
        self.screen.blit(title_text, title_rect)
        
        # Create a clipping rect for the text area to enable scrolling
        text_surface = pygame.Surface((self.text_rect.width, self.text_rect.height))
        text_surface.fill(design.colors["background"])
        
        # Render text with appropriate font
        font = design.get_font("medium")
        line_height = font.get_linesize()
        
        # Split text into paragraphs (split by double newlines)
        paragraphs = self.text_content.strip().split('\n\n')
        
        # Render each paragraph with word wrapping
        y_offset = -self.scroll_y
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                # Empty paragraph, just add some space
                y_offset += line_height
                continue
                
            # Process the paragraph line by line
            lines = paragraph.split('\n')
            for line in lines:
                if not line.strip():
                    # Empty line within paragraph
                    y_offset += line_height
                    continue
                    
                words = line.split(' ')
                current_line = []
                
                for word in words:
                    # Check if adding this word would exceed the text width
                    test_line = ' '.join(current_line + [word])
                    test_width = font.size(test_line)[0]
                    
                    if test_width < self.text_rect.width - 20:  # Leave a small margin
                        # Word fits, add it to the line
                        current_line.append(word)
                    else:
                        # Word doesn't fit, render the current line and start a new one
                        if current_line:
                            # Skip lines that are completely above or below the visible area
                            if y_offset + line_height >= 0 and y_offset < self.text_rect.height:
                                # Render and blit the line
                                line_text = ' '.join(current_line)
                                line_surface = font.render(line_text, True, design.colors["text"])
                                text_surface.blit(line_surface, (0, y_offset))
                                
                            y_offset += line_height
                            current_line = [word]
                        else:
                            # If line is empty, force add the word and move on
                            # (this handles very long words)
                            if y_offset + line_height >= 0 and y_offset < self.text_rect.height:
                                line_surface = font.render(word, True, design.colors["text"])
                                text_surface.blit(line_surface, (0, y_offset))
                                
                            y_offset += line_height
                            current_line = []
                
                # Render any remaining words in the last line
                if current_line:
                    if y_offset + line_height >= 0 and y_offset < self.text_rect.height:
                        line_text = ' '.join(current_line)
                        line_surface = font.render(line_text, True, design.colors["text"])
                        text_surface.blit(line_surface, (0, y_offset))
                        
                    y_offset += line_height
            
            # Add extra space after each paragraph
            y_offset += line_height // 2
        
        # Update the max scroll based on final content height
        self.max_scroll_y = max(0, y_offset + self.scroll_y - self.text_rect.height)
        
        # Draw the text surface onto the screen
        self.screen.blit(text_surface, self.text_rect)
        
        # Draw a border around the text area
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.text_rect, 1)
        
        # Draw scrollbar if needed
        if self.max_scroll_y > 0:
            self.render_scrollbar()
        
        # Draw return button
        self.return_button.render(self.screen)
    
    def render_scrollbar(self):
        """Render the scrollbar with click functionality"""
        scrollbar_width = 10
        self.scrollbar_rect = pygame.Rect(
            self.text_rect.right - scrollbar_width,
            self.text_rect.top,
            scrollbar_width,
            self.text_rect.height
        )
        
        # Draw scrollbar background
        pygame.draw.rect(self.screen, design.colors["button"], self.scrollbar_rect)
        
        # Calculate and draw scrollbar thumb
        visible_ratio = min(1.0, self.text_rect.height / (self.text_rect.height + self.max_scroll_y))
        thumb_height = max(20, int(self.scrollbar_rect.height * visible_ratio))
        
        # Calculate thumb position
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