"""
TextBox implementation with word wrapping based on Windows Notepad behavior
"""
import pygame
import time
from GUI.design_base import design
from config import (LINE_NUMBERS_WIDTH, LINE_HEIGHT_MULTIPLIER, 
                   KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL, 
                   LINE_SEPARATOR_THICKNESS)

class TextBox:
    """
    TextBox with Windows Notepad-like behavior and word wrapping
    """
    def __init__(self, rect):
        # Store the overall rectangle
        self.rect = pygame.Rect(rect)
        
        # Split into line numbers area and text area
        self.line_numbers_width = LINE_NUMBERS_WIDTH
        self.line_numbers_rect = pygame.Rect(rect.x, rect.y, self.line_numbers_width, rect.height)
        self.text_rect = pygame.Rect(rect.x + self.line_numbers_width, rect.y, 
                                    rect.width - self.line_numbers_width - 15, rect.height)
        self.scrollbar_rect = pygame.Rect(rect.right - 15, rect.y, 15, rect.height)
        
        # Text content as array of logical lines
        self.lines = [""]
        
        # Wrapped lines information
        self.wrapped_lines = []  # List of (logical_line_index, start_index, text)
        self.wrap_width = int(self.text_rect.width * 0.9)  # 90% of text area width for wrapping
        
        # Cursor state
        self.cursor_line = 0  # Current logical line index
        self.cursor_col = 0   # Current column index in logical line
        
        # Visual cursor position (in wrapped lines)
        self.visual_cursor_line = 0  # Index in wrapped_lines
        self.visual_cursor_col = 0   # Column in current wrapped line
        
        # Cursor blinking
        self.cursor_blink = True
        self.cursor_blink_time = 0
        self.cursor_blink_rate = 500  # ms
        
        # View state
        self.scroll_y = 0  # First visible wrapped line
        self.is_focused = False
        
        # Font and metrics
        self.font = design.get_font("medium")
        self.base_line_height = self.font.get_height()
        # Apply line height multiplier from config
        self.line_height = self.base_line_height * LINE_HEIGHT_MULTIPLIER
        self.visible_lines = self.text_rect.height // self.line_height
        
        # Key repeat tracking
        self.key_states = {}  # Tracks the state of each key for manual repeat
        self.repeat_delay = KEY_REPEAT_DELAY
        self.repeat_interval = KEY_REPEAT_INTERVAL
        
        # For monitoring performance
        self.repeat_count = {}  # Debug counter for measuring repeat rate
        self.last_frame_time = pygame.time.get_ticks()
        self.fps_avg = []
        
        # Mouse state
        self.scrollbar_dragging = False
        self.scrollbar_click_y = 0
        self.scrollbar_thumb_y = 0
        self.scrollbar_thumb_height = 30  # Will be calculated based on content
        
        # Line separator thickness
        self.line_thickness = LINE_SEPARATOR_THICKNESS
        
        # Scroll and cursor state
        self.allow_cursor_positioning = True
        self.last_scroll_time = 0
        self.scroll_cooldown = 100
        
        # Disable Pygame's key repeat system - we'll handle it manually
        pygame.key.set_repeat(0)  # Turn off built-in key repeat
        
        # Initialize wrapped lines
        self.update_wrapped_lines()
    
    def update_wrapped_lines(self):
        """Update the wrapped lines based on current content"""
        self.wrapped_lines = []
        
        for line_idx, line in enumerate(self.lines):
            if not line:
                # Empty line - no wrapping needed
                self.wrapped_lines.append((line_idx, 0, ""))
                continue
                
            # Process line for wrapping
            start_idx = 0
            remaining = line
            
            while remaining:
                # See if remaining text fits in wrap width
                if self.font.size(remaining)[0] <= self.wrap_width:
                    # It fits, add the whole thing
                    self.wrapped_lines.append((line_idx, start_idx, remaining))
                    break
                
                # Find a good wrap point
                wrap_idx = self.find_wrap_point(remaining)
                
                # Add the wrapped portion
                self.wrapped_lines.append((line_idx, start_idx, remaining[:wrap_idx]))
                
                # Update for next iteration
                remaining = remaining[wrap_idx:]
                start_idx += wrap_idx
        
        # Update cursor position in wrapped lines
        self.update_visual_cursor()
        
        # Ensure scroll_y stays within valid bounds after content changes
        max_scroll = max(0, len(self.wrapped_lines) - self.visible_lines)
        self.scroll_y = min(self.scroll_y, max_scroll)
        
        # Update scrollbar
        self.calculate_scrollbar()
    
    def find_wrap_point(self, text):
        """Find a good point to wrap the text"""
        # Try to find the last character that fits
        for i in range(1, len(text) + 1):
            if self.font.size(text[:i])[0] > self.wrap_width:
                # This character doesn't fit
                if i > 1:
                    # Go back one character
                    i -= 1
                    
                    # Try to find a word boundary
                    last_space = text[:i].rfind(' ')
                    if last_space > 0 and last_space > i // 2:
                        # Use word boundary if it's not too far back
                        return last_space + 1
                
                return i
        
        # Everything fits
        return len(text)
    
    def update_visual_cursor(self):
        """Update visual cursor position based on logical cursor"""
        # Find the wrapped line containing the cursor
        cursor_pos = 0
        for i, (line_idx, start_idx, text) in enumerate(self.wrapped_lines):
            if line_idx == self.cursor_line:
                if start_idx <= self.cursor_col and (start_idx + len(text) >= self.cursor_col or start_idx + len(text) == len(self.lines[line_idx])):
                    # Found the wrapped line containing the cursor
                    self.visual_cursor_line = i
                    self.visual_cursor_col = self.cursor_col - start_idx
                    return
                
    def calculate_scrollbar(self):
        """Calculate scrollbar dimensions"""
        if len(self.wrapped_lines) <= self.visible_lines:
            # All lines fit in view, no need for scrollbar
            self.scrollbar_thumb_height = self.scrollbar_rect.height
            self.scrollbar_thumb_y = 0
        else:
            # Calculate thumb size as proportion of visible to total content
            self.scrollbar_thumb_height = max(30, int(self.scrollbar_rect.height * 
                                                   (self.visible_lines / len(self.wrapped_lines))))
            
            # Calculate thumb position
            max_scroll_range = len(self.wrapped_lines) - self.visible_lines
            if max_scroll_range > 0:
                scroll_ratio = self.scroll_y / max_scroll_range
            else:
                scroll_ratio = 0
                
            max_thumb_travel = self.scrollbar_rect.height - self.scrollbar_thumb_height
            self.scrollbar_thumb_y = int(scroll_ratio * max_thumb_travel)
    
    def set_text(self, text):
        """Set the text content of the editor"""
        self.lines = text.split('\n')
        if not self.lines:
            self.lines = [""]
        
        # Reset cursor and scroll
        self.cursor_line = 0
        self.cursor_col = 0
        self.scroll_y = 0
        
        # Update wrapped lines
        self.update_wrapped_lines()
    
    def get_text(self):
        """Get the text content as a string"""
        return '\n'.join(self.lines)
    
    def process_key_repeat(self, key, unicode=""):
        """Process a key repeat action"""
        # Create a simulated key event
        event = pygame.event.Event(pygame.KEYDOWN, {
            'key': key,
            'unicode': unicode
        })
        
        # Handle it
        self.handle_keydown(event)
        
        # Count for debugging purposes
        if key not in self.repeat_count:
            self.repeat_count[key] = 0
        self.repeat_count[key] += 1
    
    def handle_keydown(self, event):
        """Handle key down events"""
        # Register this key as pressed
        if hasattr(event, 'key'):
            if event.key not in self.key_states:
                self.key_states[event.key] = {
                    'time': pygame.time.get_ticks(),
                    'unicode': event.unicode,
                    'repeat_count': 0
                }
            else:
                # Update for a repeated key
                self.key_states[event.key]['repeat_count'] += 1
        
        # Check for special keys
        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            # Split line at cursor
            current_line = self.lines[self.cursor_line]
            self.lines[self.cursor_line] = current_line[:self.cursor_col]
            self.lines.insert(self.cursor_line + 1, current_line[self.cursor_col:])
            
            # Move cursor to beginning of new line
            self.cursor_line += 1
            self.cursor_col = 0
            
            # Update wrapped lines
            self.update_wrapped_lines()
            
            # Make sure cursor is visible
            self.ensure_cursor_visible()
            
            return True
            
        elif event.key == pygame.K_BACKSPACE:
            if self.cursor_col > 0:
                # Delete character before cursor
                current_line = self.lines[self.cursor_line]
                self.lines[self.cursor_line] = current_line[:self.cursor_col-1] + current_line[self.cursor_col:]
                self.cursor_col -= 1
            elif self.cursor_line > 0:
                # At beginning of line, join with previous line
                prev_line = self.lines[self.cursor_line - 1]
                current_line = self.lines[self.cursor_line]
                self.cursor_col = len(prev_line)
                self.lines[self.cursor_line - 1] = prev_line + current_line
                self.lines.pop(self.cursor_line)
                self.cursor_line -= 1
            
            # Update wrapped lines
            self.update_wrapped_lines()
            
            # Make sure cursor is visible
            self.ensure_cursor_visible()
            
            return True
            
        elif event.key == pygame.K_DELETE:
            current_line = self.lines[self.cursor_line]
            if self.cursor_col < len(current_line):
                # Delete character at cursor
                self.lines[self.cursor_line] = current_line[:self.cursor_col] + current_line[self.cursor_col+1:]
            elif self.cursor_line < len(self.lines) - 1:
                # At end of line, join with next line
                next_line = self.lines[self.cursor_line + 1]
                self.lines[self.cursor_line] = current_line + next_line
                self.lines.pop(self.cursor_line + 1)
            
            # Update wrapped lines
            self.update_wrapped_lines()
            
            return True
            
        elif event.key == pygame.K_LEFT:
            if self.cursor_col > 0:
                self.cursor_col -= 1
            elif self.cursor_line > 0:
                self.cursor_line -= 1
                self.cursor_col = len(self.lines[self.cursor_line])
            
            # Update visual cursor
            self.update_visual_cursor()
            
            # Make sure cursor is visible
            self.ensure_cursor_visible()
            
            return True
            
        elif event.key == pygame.K_RIGHT:
            current_line = self.lines[self.cursor_line]
            if self.cursor_col < len(current_line):
                self.cursor_col += 1
            elif self.cursor_line < len(self.lines) - 1:
                self.cursor_line += 1
                self.cursor_col = 0
            
            # Update visual cursor
            self.update_visual_cursor()
            
            # Make sure cursor is visible
            self.ensure_cursor_visible()
            
            return True
            
        elif event.key == pygame.K_UP:
            # Need to handle wrapping - move to previous wrapped line
            if self.visual_cursor_line > 0:
                prev_wrapped = self.wrapped_lines[self.visual_cursor_line - 1]
                prev_line_idx, prev_start_idx, prev_text = prev_wrapped
                
                # Set logical cursor position
                self.cursor_line = prev_line_idx
                self.cursor_col = min(prev_start_idx + self.visual_cursor_col, prev_start_idx + len(prev_text))
                
                # Update visual cursor
                self.update_visual_cursor()
                
                # Make sure cursor is visible
                self.ensure_cursor_visible()
            
            return True
            
        elif event.key == pygame.K_DOWN:
            # Need to handle wrapping - move to next wrapped line
            if self.visual_cursor_line < len(self.wrapped_lines) - 1:
                next_wrapped = self.wrapped_lines[self.visual_cursor_line + 1]
                next_line_idx, next_start_idx, next_text = next_wrapped
                
                # Set logical cursor position
                self.cursor_line = next_line_idx
                self.cursor_col = min(next_start_idx + self.visual_cursor_col, next_start_idx + len(next_text))
                
                # Update visual cursor
                self.update_visual_cursor()
                
                # Make sure cursor is visible
                self.ensure_cursor_visible()
            
            return True
            
        elif event.key == pygame.K_HOME:
            # Find the start of the current wrapped line
            wrapped = self.wrapped_lines[self.visual_cursor_line]
            line_idx, start_idx, text = wrapped
            
            # Move to start of wrapped line
            self.cursor_col = start_idx
            
            # Update visual cursor
            self.update_visual_cursor()
            
            return True
            
        elif event.key == pygame.K_END:
            # Find the end of the current wrapped line
            wrapped = self.wrapped_lines[self.visual_cursor_line]
            line_idx, start_idx, text = wrapped
            
            # Move to end of wrapped line
            self.cursor_col = start_idx + len(text)
            
            # Update visual cursor
            self.update_visual_cursor()
            
            return True
            
        elif event.key == pygame.K_PAGEUP:
            # Move cursor up by visible_lines
            target_visual_line = max(0, self.visual_cursor_line - self.visible_lines)
            
            if target_visual_line != self.visual_cursor_line:
                # Move to the target line
                wrapped = self.wrapped_lines[target_visual_line]
                line_idx, start_idx, text = wrapped
                
                # Try to maintain horizontal position
                self.cursor_line = line_idx
                self.cursor_col = min(start_idx + self.visual_cursor_col, start_idx + len(text))
                
                # Update visual cursor
                self.update_visual_cursor()
                
                # Also scroll the view
                self.scroll_y = max(0, self.scroll_y - self.visible_lines)
                
                # Update scrollbar
                self.calculate_scrollbar()
            
            return True
            
        elif event.key == pygame.K_PAGEDOWN:
            # Move cursor down by visible_lines
            target_visual_line = min(len(self.wrapped_lines) - 1, self.visual_cursor_line + self.visible_lines)
            
            if target_visual_line != self.visual_cursor_line:
                # Move to the target line
                wrapped = self.wrapped_lines[target_visual_line]
                line_idx, start_idx, text = wrapped
                
                # Try to maintain horizontal position
                self.cursor_line = line_idx
                self.cursor_col = min(start_idx + self.visual_cursor_col, start_idx + len(text))
                
                # Update visual cursor
                self.update_visual_cursor()
                
                # Also scroll the view
                self.scroll_y = min(max(0, len(self.wrapped_lines) - self.visible_lines), 
                                   self.scroll_y + self.visible_lines)
                
                # Update scrollbar
                self.calculate_scrollbar()
            
            return True
        
        # Handle normal key input
        elif event.unicode and event.unicode.isprintable():
            # Insert character at cursor
            current_line = self.lines[self.cursor_line]
            self.lines[self.cursor_line] = current_line[:self.cursor_col] + event.unicode + current_line[self.cursor_col:]
            self.cursor_col += 1
            
            # Update wrapped lines
            self.update_wrapped_lines()
            
            # Make sure cursor is visible
            self.ensure_cursor_visible()
            
            return True
        
        return False
    
    def is_cursor_visible(self):
        """Check if cursor is currently visible in the viewport"""
        return (self.visual_cursor_line >= self.scroll_y and 
                self.visual_cursor_line < self.scroll_y + self.visible_lines)
    
    def ensure_cursor_visible(self):
        """Make sure cursor is visible in the viewport"""
        # If cursor is above viewport, scroll up
        if self.visual_cursor_line < self.scroll_y:
            self.scroll_y = self.visual_cursor_line
        
        # If cursor is below viewport, scroll down
        elif self.visual_cursor_line >= self.scroll_y + self.visible_lines:
            self.scroll_y = self.visual_cursor_line - self.visible_lines + 1
        
        # Update scrollbar
        self.calculate_scrollbar()
    
    def handle_event(self, event):
        """Handle pygame events"""
        # First check for typing or cursor movement
        if event.type == pygame.KEYDOWN:
            self.allow_cursor_positioning = True
            if self.is_focused:
                # Reset cursor blink
                self.cursor_blink = True
                self.cursor_blink_time = pygame.time.get_ticks()
                
                # If typing and cursor not visible, make it visible
                if not self.is_cursor_visible():
                    self.ensure_cursor_visible()
                
                # Handle the key
                if self.handle_keydown(event):
                    return True
        
        # Handle key release to stop repeating
        elif event.type == pygame.KEYUP:
            if event.key in self.key_states:
                del self.key_states[event.key]
                if event.key in self.repeat_count:
                    # Debug info - print repeat count for this key
                    # print(f"Key {event.key} repeated {self.repeat_count[event.key]} times")
                    del self.repeat_count[event.key]
        
        # Handle mouse wheel for scrolling
        elif event.type == pygame.MOUSEWHEEL:
            # Scroll up or down
            self.scroll_y = max(0, min(len(self.wrapped_lines) - self.visible_lines, 
                                    self.scroll_y - event.y * 3))
            # Update scrollbar
            self.calculate_scrollbar()
            # Disable cursor positioning until explicit reset
            self.allow_cursor_positioning = False
            return True
        
        # Handle mouse motion
        elif event.type == pygame.MOUSEMOTION:                
            # Handle scrollbar dragging
            if self.scrollbar_dragging:
                # Calculate new thumb position
                new_thumb_y = event.pos[1] - self.scrollbar_click_y
                
                # Constrain to scrollbar
                new_thumb_y = max(0, min(self.scrollbar_rect.height - self.scrollbar_thumb_height, new_thumb_y))
                
                # Calculate new scroll position
                ratio = new_thumb_y / (self.scrollbar_rect.height - self.scrollbar_thumb_height)
                max_scroll = max(0, len(self.wrapped_lines) - self.visible_lines)
                self.scroll_y = int(ratio * max_scroll)
                
                # Update scrollbar
                self.calculate_scrollbar()
                
                # Disable cursor positioning when using scrollbar
                self.allow_cursor_positioning = False
                
                return True
        
        # Handle mouse clicks on the text area
        elif event.type == pygame.MOUSEBUTTONDOWN:            
            # Check if clicking in text area
            if self.text_rect.collidepoint(event.pos):
                self.is_focused = True
                # Update cursor only if positioning is allowed
                if self.allow_cursor_positioning:
                    # Calculate the wrapped line clicked
                    rel_y = event.pos[1] - self.text_rect.top
                    wrapped_line_idx = self.scroll_y + rel_y // self.line_height
                    wrapped_line_idx = min(wrapped_line_idx, len(self.wrapped_lines) - 1)
                    
                    # Get the wrapped line info
                    if wrapped_line_idx >= 0 and wrapped_line_idx < len(self.wrapped_lines):
                        line_idx, start_idx, text = self.wrapped_lines[wrapped_line_idx]
                        
                        # Calculate the closest character position
                        rel_x = event.pos[0] - self.text_rect.left
                        
                        # Find the closest character position by checking each character width
                        visual_col = 0
                        x_pos = 0
                        for i, char in enumerate(text):
                            char_width = self.font.size(char)[0]
                            if x_pos + (char_width / 2) > rel_x:
                                break
                            x_pos += char_width
                            visual_col = i + 1
                        
                        # Set cursor position
                        self.cursor_line = line_idx
                        self.cursor_col = start_idx + visual_col
                        
                        # Update visual cursor
                        self.update_visual_cursor()
                        
                        # Reset cursor blink
                        self.cursor_blink = True
                        self.wheel_scrolling_active = False
                        self.cursor_blink_time = pygame.time.get_ticks()
                else:
                    # First click after scrolling just enables positioning for next click
                    self.allow_cursor_positioning = True
                
                return True
            
            # Check if clicking on scrollbar
            elif self.scrollbar_rect.collidepoint(event.pos):
                # Check if clicking on thumb
                thumb_rect = pygame.Rect(
                    self.scrollbar_rect.x,
                    self.scrollbar_rect.y + self.scrollbar_thumb_y,
                    self.scrollbar_rect.width,
                    self.scrollbar_thumb_height
                )
                
                if thumb_rect.collidepoint(event.pos):
                    # Start dragging
                    self.scrollbar_dragging = True
                    self.scrollbar_click_y = event.pos[1] - self.scrollbar_thumb_y
                else:
                    # Click in scrollbar but not on thumb - jump to position
                    rel_y = event.pos[1] - self.scrollbar_rect.top
                    
                    # Calculate ratio of click to scrollbar height
                    ratio = rel_y / self.scrollbar_rect.height
                    
                    # Set scroll position
                    max_scroll = max(0, len(self.wrapped_lines) - self.visible_lines)
                    self.scroll_y = max(0, min(max_scroll, int(ratio * len(self.wrapped_lines))))
                    
                    # Update scrollbar
                    self.calculate_scrollbar()
                self.allow_cursor_positioning = False
                return True
            else:
                # Clicking outside text area and scrollbar
                self.is_focused = False
        
        # Handle mouse up to stop dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            self.scrollbar_dragging = False
            
        return False
    
    def update(self):
        """Update the textbox state"""
        current_time = pygame.time.get_ticks()
        
        # Calculate FPS for debugging
        frame_time = current_time - self.last_frame_time
        self.last_frame_time = current_time
        fps = 1000 / frame_time if frame_time > 0 else 0
        self.fps_avg.append(fps)
        if len(self.fps_avg) > 60:
            self.fps_avg.pop(0)
        
        # Update cursor blink
        if current_time - self.cursor_blink_time > self.cursor_blink_rate:
            self.cursor_blink = not self.cursor_blink
            self.cursor_blink_time = current_time
        
        # Handle key repeats with direct polling
        keys = pygame.key.get_pressed()
        for key, state in list(self.key_states.items()):
            # Check if key is still pressed
            if key < len(keys) and keys[key]:
                # Calculate time since first press
                elapsed = current_time - state['time']
                
                # Check if we should repeat
                if elapsed >= self.repeat_delay:
                    # Calculate how many repeats should have happened by now
                    target_repeats = int((elapsed - self.repeat_delay) / self.repeat_interval) + 1
                    
                    # If we need more repeats, do them now
                    while state['repeat_count'] < target_repeats:
                        self.process_key_repeat(key, state.get('unicode', ''))
                        state['repeat_count'] += 1
            else:
                # Key no longer pressed
                del self.key_states[key]
    
    def render(self, surface):
        """Render the textbox"""
        # Draw background
        pygame.draw.rect(surface, design.colors["textbox_bg"], self.rect)
        
        # Draw line numbers background
        pygame.draw.rect(surface, design.colors["toolbar"], self.line_numbers_rect)
        
        # Draw text area border
        pygame.draw.rect(surface, design.colors["textbox_border"], self.rect, 1)
        
        # Determine line colors based on theme
        is_light_theme = design.colors["background"][0] > 128
        line_color = (180, 180, 180) if is_light_theme else (80, 80, 80)
        
        # Draw visible wrapped lines
        for i in range(min(self.visible_lines, len(self.wrapped_lines) - self.scroll_y)):
            display_idx = self.scroll_y + i
            y = self.text_rect.top + i * self.line_height
            
            # Draw line separator at top of this line
            pygame.draw.line(surface, line_color, 
                           (self.line_numbers_rect.left, y), 
                           (self.text_rect.right, y), self.line_thickness)
            
            # Get wrapped line info
            line_idx, start_idx, text = self.wrapped_lines[display_idx]
            
            # Draw line number (only for start of logical lines)
            if start_idx == 0:  # This is the first wrapped segment of a logical line
                line_num_text = f"Line {line_idx + 1}"
                line_num_surf = design.get_font("small").render(line_num_text, True, design.colors["textbox_text"])
                line_num_y = y + (self.line_height - line_num_surf.get_height()) // 2  # Center vertically
                surface.blit(line_num_surf, (self.line_numbers_rect.left + 5, line_num_y))
            
            # Draw text - center vertically in the larger line height
            text_surf = self.font.render(text, True, design.colors["textbox_text"])
            text_y = y + (self.line_height - self.base_line_height) // 2  # Center text vertically
            surface.blit(text_surf, (self.text_rect.left + 5, text_y))
            
            # Draw cursor if on this line and cursor is visible and textbox is focused
            if self.is_focused and display_idx == self.visual_cursor_line and self.cursor_blink:
                # Calculate cursor position
                cursor_text = text[:self.visual_cursor_col]
                cursor_width = self.font.size(cursor_text)[0]
                cursor_x = self.text_rect.left + 5 + cursor_width
                cursor_y = text_y
                
                # Draw cursor - height based on base line height, not scaled
                pygame.draw.line(surface, design.colors["textbox_cursor"],
                               (cursor_x, cursor_y),
                               (cursor_x, cursor_y + self.base_line_height), 2)
        
        # Draw bottom line separator for last visible line
        if self.visible_lines > 0 and self.scroll_y + self.visible_lines <= len(self.wrapped_lines):
            y = self.text_rect.top + self.visible_lines * self.line_height
            pygame.draw.line(surface, line_color, 
                           (self.line_numbers_rect.left, y), 
                           (self.text_rect.right, y), self.line_thickness)
        
        # Draw scrollbar if needed
        if len(self.wrapped_lines) > self.visible_lines:
            # Draw scrollbar background
            pygame.draw.rect(surface, design.colors["button"], self.scrollbar_rect)
            
            # Draw scrollbar thumb
            thumb_rect = pygame.Rect(
                self.scrollbar_rect.x,
                self.scrollbar_rect.y + self.scrollbar_thumb_y,
                self.scrollbar_rect.width,
                self.scrollbar_thumb_height
            )
            pygame.draw.rect(surface, design.colors["button_hover"], thumb_rect, 0, 3)
            pygame.draw.rect(surface, design.colors["textbox_border"], thumb_rect, 1, 3)