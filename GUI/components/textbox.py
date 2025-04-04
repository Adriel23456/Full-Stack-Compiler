"""
TextBox implementation with word wrapping based on Windows Notepad behavior
"""
import pygame
import time
from GUI.design_base import design
from config import (LINE_NUMBERS_WIDTH, LINE_HEIGHT_MULTIPLIER, 
                   KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL, 
                   LINE_SEPARATOR_THICKNESS)
from .text_selection import TextSelection
from .key_handler import KeyHandler

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
        
        # Line separator thickness
        self.line_thickness = LINE_SEPARATOR_THICKNESS
        
        # Text content storage variable
        self.text_content = ""
        
        # Initialize components
        self.selection = TextSelection(self)
        self.key_handler = KeyHandler(self)
        
        # Mouse state
        self.scrollbar_dragging = False
        self.scrollbar_click_y = 0
        self.scrollbar_thumb_y = 0
        self.scrollbar_thumb_height = 30  # Will be calculated based on content
        
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
        
        # Update text content variable with all text including line breaks
        self.update_text_content()
        
        # Update selection visual ranges if selection is active
        if self.selection.is_active():
            self.selection.update_visuals()
    
    def update_text_content(self):
        """Update the text_content variable with all current text including newlines"""
        self.text_content = '\n'.join(self.lines)
    
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
        return self.text_content
    
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
    
    def get_position_at_mouse(self, mouse_pos):
        """Get logical cursor position at mouse position"""
        # Calculate the wrapped line clicked
        rel_y = mouse_pos[1] - self.text_rect.top
        wrapped_line_idx = self.scroll_y + rel_y // self.line_height
        wrapped_line_idx = min(max(0, wrapped_line_idx), len(self.wrapped_lines) - 1)
        
        # Get the wrapped line info
        line_idx, start_idx, text = self.wrapped_lines[wrapped_line_idx]
        
        # Calculate the closest character position
        rel_x = mouse_pos[0] - self.text_rect.left - 5  # Adjust for padding
        
        # Find the closest character position by checking each character width
        visual_col = 0
        x_pos = 0
        accumulated_width = 0
        
        for i, char in enumerate(text):
            char_width = self.font.size(char)[0]
            accumulated_width += char_width
            
            # Calculate total text width to determine position percentage
            total_width = self.font.size(text)[0]
            position_percentage = accumulated_width / total_width if total_width > 0 else 0
            
            # Find appropriate correction factor based on position
            factor_ranges = [
                (0.1, 0.00535),  # 0-10%: 0.535% adjustment
                (0.2, 0.00755),  # 10-20%: 0.755% adjustment
                (0.3, 0.0122),   # 20-30%: 1.22% adjustment
                (0.4, 0.0135),   # 30-40%: 1.35% adjustment
                (0.5, 0.0155),   # 40-50%: 1.45% adjustment
                (0.6, 0.0159),   # 50-60%: 1.55% adjustment
                (0.7, 0.0160),   # 60-70%: 1.62% adjustment
                (0.8, 0.0161),   # 70-80%: 1.69% adjustment
                (0.9, 0.0162),   # 80-90%: 1.76% adjustment
                (1.0, 0.0165)    # 90-100%: 1.82% adjustment
            ]
            
            # Find appropriate factor
            factor = factor_ranges[-1][1]  # Default (last range)
            for threshold, factor_value in factor_ranges:
                if position_percentage < threshold:
                    factor = factor_value
                    break
            
            offset_correction = int(-(accumulated_width * factor))
            adjusted_x_pos = x_pos - offset_correction
            
            if adjusted_x_pos + (char_width / 2) > rel_x:
                break
            
            x_pos += char_width
            visual_col = i + 1
        
        return line_idx, start_idx + visual_col
    
    def handle_event(self, event):
        """Handle pygame events"""
        # First check for typing or cursor movement
        if event.type == pygame.KEYDOWN:
            return self.key_handler.handle_keydown_event(event)
        
        # Handle key release to stop repeating
        elif event.type == pygame.KEYUP:
            return self.key_handler.handle_keyup_event(event)
        
        # Handle mouse wheel for scrolling
        elif event.type == pygame.MOUSEWHEEL:
            # Scroll up or down
            self.scroll_y = max(0, min(len(self.wrapped_lines) - self.visible_lines, 
                                    self.scroll_y - event.y * 3))
            # Update scrollbar
            self.calculate_scrollbar()
            return True
        
        # Handle mouse motion
        elif event.type == pygame.MOUSEMOTION:
            return self.handle_mouse_motion(event)
        
        # Handle mouse clicks on the text area
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return self.handle_mouse_down(event)
        
        # Handle mouse up
        elif event.type == pygame.MOUSEBUTTONUP:
            return self.handle_mouse_up(event)
            
        return False
    
    def handle_mouse_motion(self, event):
        """Handle mouse motion events"""
        # Update mouse cursor style when over textbox
        if self.text_rect.collidepoint(event.pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        # Verificar si el botón del mouse está presionado
        mouse_buttons = pygame.mouse.get_pressed()
        left_button_pressed = mouse_buttons[0]  # El índice 0 corresponde al botón izquierdo
            
        # Handle selection mode movement - solo si el botón del mouse está presionado
        if left_button_pressed and self.selection.is_selection_mode() and self.text_rect.collidepoint(event.pos):
            # Get logical position at mouse
            end_line, end_col = self.get_position_at_mouse(event.pos)
            
            # Update selection end
            self.selection.update_selection_end(end_line, end_col)
            
            # Update cursor position to match selection end
            self.cursor_line = end_line
            self.cursor_col = end_col
            self.update_visual_cursor()
            
            # Make sure cursor is visible
            self.ensure_cursor_visible()
            
            return True
            
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
            
            return True
            
        return False
    
    def handle_mouse_down(self, event):
        """Handle mouse button down events"""
        # Check if clicking in text area
        if self.text_rect.collidepoint(event.pos):
            # Set focus
            self.is_focused = True
            
            # Get logical position at mouse
            line_idx, col_idx = self.get_position_at_mouse(event.pos)
            
            # Set cursor position
            self.cursor_line = line_idx
            self.cursor_col = col_idx
            
            # Store as potential selection start
            self.selection.set_selection_start(line_idx, col_idx)
            
            # Clear current selection
            self.selection.clear()
            
            # Update visual cursor
            self.update_visual_cursor()
            
            # Reset cursor blink
            self.cursor_blink = True
            self.cursor_blink_time = pygame.time.get_ticks()
            
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
            return True
        else:
            # Clicking outside text area and scrollbar
            self.is_focused = False
        
        return False
    
    def handle_mouse_up(self, event):
        """Handle mouse button up events"""
        self.scrollbar_dragging = False
        
        # Si estábamos en modo selección y soltamos el botón
        if self.selection.is_selection_mode():
            # Terminar el modo de selección pero MANTENER la selección activa
            self.selection.end_selection_mode()
            
            # Solo actualizar la posición final de la selección si el mouse está sobre el texto
            if self.text_rect.collidepoint(event.pos):
                end_line, end_col = self.get_position_at_mouse(event.pos)
                self.selection.update_selection_end(end_line, end_col)
                
                # Actualizar posición del cursor para que coincida con el final de la selección
                self.cursor_line = end_line
                self.cursor_col = end_col
                self.update_visual_cursor()
                
                self.selection.active = True
            
            # Resetear el seguimiento de selección para prevenir re-entrar en modo selección
            self.selection.reset_selection_start()
            
            return True
            
        # Check if this was a click and hold long enough for selection
        elif self.text_rect.collidepoint(event.pos) and self.selection.has_selection_start():
            current_time = pygame.time.get_ticks()
            # If mouse was held down for 100ms or more, complete selection
            if current_time - self.selection.get_selection_start_time() >= 350:
                # Get position at mouse up
                end_line, end_col = self.get_position_at_mouse(event.pos)
                
                # Create selection
                self.selection.create_selection(end_line, end_col)
                
                # Update cursor position to match selection end
                self.cursor_line = end_line
                self.cursor_col = end_col
                self.update_visual_cursor()
                
                # Make sure cursor is visible
                self.ensure_cursor_visible()
                
                return True
        
        # Reset selection tracking
        self.selection.reset_selection_start()
        
        return False
    
    def update(self):
        """Update the textbox state"""
        current_time = pygame.time.get_ticks()
        
        # Update cursor blink
        if current_time - self.cursor_blink_time > self.cursor_blink_rate:
            self.cursor_blink = not self.cursor_blink
            self.cursor_blink_time = current_time
        
        # Check for selection mode activation
        self.selection.check_for_selection_mode(current_time)
        
        # Update key handler
        self.key_handler.update(current_time)
    
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
        grid_color = (220, 220, 220) if is_light_theme else (50, 50, 50)
        
        # Draw vertical grid lines at 10% intervals
        text_width = self.text_rect.width
        for i in range(1, 10):
            x_pos = self.text_rect.left + (text_width * (i / 10))
            pygame.draw.line(surface, grid_color,
                           (x_pos, self.text_rect.top),
                           (x_pos, self.text_rect.bottom), 1)
        
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
            
            # Draw selection highlight if this line has selection
            if self.selection.is_active():
                for sel_idx, sel_start_x, sel_end_x in self.selection.get_visual_ranges():
                    if sel_idx == display_idx:
                        # Create selection rectangle
                        sel_rect = pygame.Rect(
                            self.text_rect.left + 5 + sel_start_x,
                            y,
                            sel_end_x - sel_start_x,
                            self.line_height
                        )
                        # Draw selection highlight
                        selection_color = (173, 214, 255) if is_light_theme else (59, 105, 152)
                        pygame.draw.rect(surface, selection_color, sel_rect)
            
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