"""
Keyboard input handler for TextBox component
"""
import pygame

class KeyHandler:
    """
    Handles keyboard input for TextBox
    """
    def __init__(self, textbox):
        self.textbox = textbox
        
        # Key repeat tracking
        self.key_states = {}  # Tracks the state of each key for manual repeat
        from config import KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL
        self.repeat_delay = KEY_REPEAT_DELAY
        self.repeat_interval = KEY_REPEAT_INTERVAL
        
        # Numpad key mapping
        self.numpad_map = {
            pygame.K_KP0: (pygame.K_0, '0'),
            pygame.K_KP1: (pygame.K_1, '1'),
            pygame.K_KP2: (pygame.K_2, '2'),
            pygame.K_KP3: (pygame.K_3, '3'),
            pygame.K_KP4: (pygame.K_4, '4'),
            pygame.K_KP5: (pygame.K_5, '5'),
            pygame.K_KP6: (pygame.K_6, '6'),
            pygame.K_KP7: (pygame.K_7, '7'),
            pygame.K_KP8: (pygame.K_8, '8'),
            pygame.K_KP9: (pygame.K_9, '9'),
            pygame.K_KP_PERIOD: (pygame.K_PERIOD, '.'),
            pygame.K_KP_DIVIDE: (pygame.K_SLASH, '/'),
            pygame.K_KP_MULTIPLY: (pygame.K_ASTERISK, '*'),
            pygame.K_KP_MINUS: (pygame.K_MINUS, '-'),
            pygame.K_KP_PLUS: (pygame.K_PLUS, '+'),
            pygame.K_KP_ENTER: (pygame.K_RETURN, '\n')
        }
    
    def handle_keydown_event(self, event):
        """Handle key down events"""
        if not self.textbox.is_focused:
            return False
            
        # Reset cursor blink
        self.textbox.cursor_blink = True
        self.textbox.cursor_blink_time = pygame.time.get_ticks()
        
        # If typing and cursor not visible, make it visible
        if not self.textbox.is_cursor_visible():
            self.textbox.ensure_cursor_visible()
        
        # Register this key as pressed
        if hasattr(event, 'key'):
            # Check if it's a numpad key
            if event.key in self.numpad_map:
                std_key, unicode_val = self.numpad_map[event.key]
                if event.key not in self.key_states:
                    self.key_states[event.key] = {
                        'time': pygame.time.get_ticks(),
                        'unicode': unicode_val,
                        'repeat_count': 0,
                        'std_key': std_key
                    }
            else:
                if event.key not in self.key_states:
                    self.key_states[event.key] = {
                        'time': pygame.time.get_ticks(),
                        'unicode': event.unicode,
                        'repeat_count': 0
                    }
                else:
                    # Update for a repeated key
                    self.key_states[event.key]['repeat_count'] += 1
        
        # Handle the key
        return self.handle_keydown(event)
    
    def handle_keyup_event(self, event):
        """Handle key up events"""
        if event.key in self.key_states:
            del self.key_states[event.key]
        
        return False
    
    def process_key_repeat(self, key, unicode=""):
        """Process a key repeat action"""
        # Create a simulated key event
        event = pygame.event.Event(pygame.KEYDOWN, {
            'key': key,
            'unicode': unicode
        })
        
        # Handle it
        self.handle_keydown(event)
    
    def handle_keydown(self, event):
        """Process a keystroke"""
        # Check for special keys
        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            # If selection is active, delete selected text first
            if self.textbox.selection.is_active():
                self.textbox.selection.delete_selected_text()
            
            # Split line at cursor
            current_line = self.textbox.lines[self.textbox.cursor_line]
            self.textbox.lines[self.textbox.cursor_line] = current_line[:self.textbox.cursor_col]
            self.textbox.lines.insert(self.textbox.cursor_line + 1, current_line[self.textbox.cursor_col:])
            
            # Move cursor to beginning of new line
            self.textbox.cursor_line += 1
            self.textbox.cursor_col = 0
            
            # Clear selection
            self.textbox.selection.clear()
            
            # Update wrapped lines
            self.textbox.update_wrapped_lines()
            
            # Make sure cursor is visible
            self.textbox.ensure_cursor_visible()
            
            return True
        
        elif event.key == pygame.K_TAB:
            # If selection is active, delete selected text first
            if self.textbox.selection.is_active():
                self.textbox.selection.delete_selected_text()
            
            # Insert tab character at cursor (4 spaces)
            current_line = self.textbox.lines[self.textbox.cursor_line]
            tab_spaces = "    "  # 4 spaces for a tab
            self.textbox.lines[self.textbox.cursor_line] = current_line[:self.textbox.cursor_col] + tab_spaces + current_line[self.textbox.cursor_col:]
            self.textbox.cursor_col += len(tab_spaces)
            
            # Clear selection
            self.textbox.selection.clear()
            
            # Update wrapped lines
            self.textbox.update_wrapped_lines()
            
            # Make sure cursor is visible
            self.textbox.ensure_cursor_visible()
            
            return True
            
        elif event.key == pygame.K_BACKSPACE:
            # If selection is active, delete selected text
            if self.textbox.selection.is_active():
                self.textbox.selection.delete_selected_text()
                return True
                
            if self.textbox.cursor_col > 0:
                # Delete character before cursor
                current_line = self.textbox.lines[self.textbox.cursor_line]
                self.textbox.lines[self.textbox.cursor_line] = current_line[:self.textbox.cursor_col-1] + current_line[self.textbox.cursor_col:]
                self.textbox.cursor_col -= 1
            elif self.textbox.cursor_line > 0:
                # At beginning of line, join with previous line
                prev_line = self.textbox.lines[self.textbox.cursor_line - 1]
                current_line = self.textbox.lines[self.textbox.cursor_line]
                self.textbox.cursor_col = len(prev_line)
                self.textbox.lines[self.textbox.cursor_line - 1] = prev_line + current_line
                self.textbox.lines.pop(self.textbox.cursor_line)
                self.textbox.cursor_line -= 1
            
            # Clear selection
            self.textbox.selection.clear()
            
            # Update wrapped lines
            self.textbox.update_wrapped_lines()
            
            # Make sure cursor is visible
            self.textbox.ensure_cursor_visible()
            
            return True
            
        elif event.key == pygame.K_DELETE:
            # If selection is active, delete selected text
            if self.textbox.selection.is_active():
                self.textbox.selection.delete_selected_text()
                return True
                
            current_line = self.textbox.lines[self.textbox.cursor_line]
            if self.textbox.cursor_col < len(current_line):
                # Delete character at cursor
                self.textbox.lines[self.textbox.cursor_line] = current_line[:self.textbox.cursor_col] + current_line[self.textbox.cursor_col+1:]
            elif self.textbox.cursor_line < len(self.textbox.lines) - 1:
                # At end of line, join with next line
                next_line = self.textbox.lines[self.textbox.cursor_line + 1]
                self.textbox.lines[self.textbox.cursor_line] = current_line + next_line
                self.textbox.lines.pop(self.textbox.cursor_line + 1)
            
            # Clear selection
            self.textbox.selection.clear()
            
            # Update wrapped lines
            self.textbox.update_wrapped_lines()
            
            return True
            
        elif event.key == pygame.K_LEFT:
            # If selection is active and shift is not pressed, move to start of selection
            if self.textbox.selection.is_active() and not (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                start_line, start_col, end_line, end_col = self.textbox.selection.get_normalized_selection()
                self.textbox.cursor_line = start_line
                self.textbox.cursor_col = start_col
                self.textbox.selection.clear()
                self.textbox.update_visual_cursor()
                self.textbox.ensure_cursor_visible()
                return True
            
            # Move cursor left
            if self.textbox.cursor_col > 0:
                self.textbox.cursor_col -= 1
            elif self.textbox.cursor_line > 0:
                self.textbox.cursor_line -= 1
                self.textbox.cursor_col = len(self.textbox.lines[self.textbox.cursor_line])
            
            # Update selection if shift is held
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if not self.textbox.selection.is_active():
                    # Start new selection
                    self.textbox.selection.set_selection_start(
                        self.textbox.cursor_line,
                        self.textbox.cursor_col + 1  # +1 because we just moved left
                    )
                    self.textbox.selection.active = True
                
                # Update selection end
                self.textbox.selection.update_selection_end(
                    self.textbox.cursor_line,
                    self.textbox.cursor_col
                )
            elif self.textbox.selection.is_active():
                # Clear selection if shift is not held
                self.textbox.selection.clear()
            
            # Update visual cursor
            self.textbox.update_visual_cursor()
            
            # Make sure cursor is visible
            self.textbox.ensure_cursor_visible()
            
            return True
            
        elif event.key == pygame.K_RIGHT:
            # If selection is active and shift is not pressed, move to end of selection
            if self.textbox.selection.is_active() and not (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                start_line, start_col, end_line, end_col = self.textbox.selection.get_normalized_selection()
                self.textbox.cursor_line = end_line
                self.textbox.cursor_col = end_col
                self.textbox.selection.clear()
                self.textbox.update_visual_cursor()
                self.textbox.ensure_cursor_visible()
                return True
                
            current_line = self.textbox.lines[self.textbox.cursor_line]
            if self.textbox.cursor_col < len(current_line):
                self.textbox.cursor_col += 1
            elif self.textbox.cursor_line < len(self.textbox.lines) - 1:
                self.textbox.cursor_line += 1
                self.textbox.cursor_col = 0
            
            # Update selection if shift is held
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if not self.textbox.selection.is_active():
                    # Start new selection
                    self.textbox.selection.set_selection_start(
                        self.textbox.cursor_line,
                        self.textbox.cursor_col - 1  # -1 because we just moved right
                    )
                    self.textbox.selection.active = True
                
                # Update selection end
                self.textbox.selection.update_selection_end(
                    self.textbox.cursor_line,
                    self.textbox.cursor_col
                )
            elif self.textbox.selection.is_active():
                # Clear selection if shift is not held
                self.textbox.selection.clear()
            
            # Update visual cursor
            self.textbox.update_visual_cursor()
            
            # Make sure cursor is visible
            self.textbox.ensure_cursor_visible()
            
            return True
            
        elif event.key == pygame.K_UP:
            # Need to handle wrapping - move to previous wrapped line
            if self.textbox.visual_cursor_line > 0:
                prev_wrapped = self.textbox.wrapped_lines[self.textbox.visual_cursor_line - 1]
                prev_line_idx, prev_start_idx, prev_text = prev_wrapped
                
                # Store current position for selection
                prev_line = self.textbox.cursor_line
                prev_col = self.textbox.cursor_col
                
                # Set logical cursor position
                self.textbox.cursor_line = prev_line_idx
                self.textbox.cursor_col = min(prev_start_idx + self.textbox.visual_cursor_col, prev_start_idx + len(prev_text))
                
                # Update selection if shift is held
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if not self.textbox.selection.is_active():
                        # Start new selection
                        self.textbox.selection.set_selection_start(prev_line, prev_col)
                        self.textbox.selection.active = True
                    
                    # Update selection end
                    self.textbox.selection.update_selection_end(
                        self.textbox.cursor_line,
                        self.textbox.cursor_col
                    )
                elif self.textbox.selection.is_active():
                    # Clear selection if shift is not held
                    self.textbox.selection.clear()
                
                # Update visual cursor
                self.textbox.update_visual_cursor()
                
                # Make sure cursor is visible
                self.textbox.ensure_cursor_visible()
            
            return True
            
        elif event.key == pygame.K_DOWN:
            # Need to handle wrapping - move to next wrapped line
            if self.textbox.visual_cursor_line < len(self.textbox.wrapped_lines) - 1:
                next_wrapped = self.textbox.wrapped_lines[self.textbox.visual_cursor_line + 1]
                next_line_idx, next_start_idx, next_text = next_wrapped
                
                # Store current position for selection
                prev_line = self.textbox.cursor_line
                prev_col = self.textbox.cursor_col
                
                # Set logical cursor position
                self.textbox.cursor_line = next_line_idx
                self.textbox.cursor_col = min(next_start_idx + self.textbox.visual_cursor_col, next_start_idx + len(next_text))
                
                # Update selection if shift is held
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if not self.textbox.selection.is_active():
                        # Start new selection
                        self.textbox.selection.set_selection_start(prev_line, prev_col)
                        self.textbox.selection.active = True
                    
                    # Update selection end
                    self.textbox.selection.update_selection_end(
                        self.textbox.cursor_line,
                        self.textbox.cursor_col
                    )
                elif self.textbox.selection.is_active():
                    # Clear selection if shift is not held
                    self.textbox.selection.clear()
                
                # Update visual cursor
                self.textbox.update_visual_cursor()
                
                # Make sure cursor is visible
                self.textbox.ensure_cursor_visible()
            
            return True
            
        elif event.key == pygame.K_HOME:
            # Find the start of the current wrapped line
            wrapped = self.textbox.wrapped_lines[self.textbox.visual_cursor_line]
            line_idx, start_idx, text = wrapped
            
            # Store current position for selection
            prev_col = self.textbox.cursor_col
            
            # Move to start of wrapped line
            self.textbox.cursor_col = start_idx
            
            # Update selection if shift is held
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if not self.textbox.selection.is_active():
                    # Start new selection
                    self.textbox.selection.set_selection_start(line_idx, prev_col)
                    self.textbox.selection.active = True
                
                # Update selection end
                self.textbox.selection.update_selection_end(
                    self.textbox.cursor_line,
                    self.textbox.cursor_col
                )
            elif self.textbox.selection.is_active():
                # Clear selection if shift is not held
                self.textbox.selection.clear()
            
            # Update visual cursor
            self.textbox.update_visual_cursor()
            
            return True
            
        elif event.key == pygame.K_END:
            # Find the end of the current wrapped line
            wrapped = self.textbox.wrapped_lines[self.textbox.visual_cursor_line]
            line_idx, start_idx, text = wrapped
            
            # Store current position for selection
            prev_col = self.textbox.cursor_col
            
            # Move to end of wrapped line
            self.textbox.cursor_col = start_idx + len(text)
            
            # Update selection if shift is held
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if not self.textbox.selection.is_active():
                    # Start new selection
                    self.textbox.selection.set_selection_start(line_idx, prev_col)
                    self.textbox.selection.active = True
                
                # Update selection end
                self.textbox.selection.update_selection_end(
                    self.textbox.cursor_line,
                    self.textbox.cursor_col
                )
            elif self.textbox.selection.is_active():
                # Clear selection if shift is not held
                self.textbox.selection.clear()
            
            # Update visual cursor
            self.textbox.update_visual_cursor()
            
            return True
            
        elif event.key == pygame.K_PAGEUP:
            # Move cursor up by visible_lines
            target_visual_line = max(0, self.textbox.visual_cursor_line - self.textbox.visible_lines)
            
            if target_visual_line != self.textbox.visual_cursor_line:
                # Move to the target line
                wrapped = self.textbox.wrapped_lines[target_visual_line]
                line_idx, start_idx, text = wrapped
                
                # Store current position for selection
                prev_line = self.textbox.cursor_line
                prev_col = self.textbox.cursor_col
                
                # Try to maintain horizontal position
                self.textbox.cursor_line = line_idx
                self.textbox.cursor_col = min(start_idx + self.textbox.visual_cursor_col, start_idx + len(text))
                
                # Update selection if shift is held
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if not self.textbox.selection.is_active():
                        # Start new selection
                        self.textbox.selection.set_selection_start(prev_line, prev_col)
                        self.textbox.selection.active = True
                    
                    # Update selection end
                    self.textbox.selection.update_selection_end(
                        self.textbox.cursor_line,
                        self.textbox.cursor_col
                    )
                elif self.textbox.selection.is_active():
                    # Clear selection if shift is not held
                    self.textbox.selection.clear()
                
                # Update visual cursor
                self.textbox.update_visual_cursor()
                
                # Also scroll the view
                self.textbox.scroll_y = max(0, self.textbox.scroll_y - self.textbox.visible_lines)
                
                # Update scrollbar
                self.textbox.calculate_scrollbar()
            
            return True
            
        elif event.key == pygame.K_PAGEDOWN:
            # Move cursor down by visible_lines
            target_visual_line = min(len(self.textbox.wrapped_lines) - 1, self.textbox.visual_cursor_line + self.textbox.visible_lines)
            
            if target_visual_line != self.textbox.visual_cursor_line:
                # Move to the target line
                wrapped = self.textbox.wrapped_lines[target_visual_line]
                line_idx, start_idx, text = wrapped
                
                # Store current position for selection
                prev_line = self.textbox.cursor_line
                prev_col = self.textbox.cursor_col
                
                # Try to maintain horizontal position
                self.textbox.cursor_line = line_idx
                self.textbox.cursor_col = min(start_idx + self.textbox.visual_cursor_col, start_idx + len(text))
                
                # Update selection if shift is held
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if not self.textbox.selection.is_active():
                        # Start new selection
                        self.textbox.selection.set_selection_start(prev_line, prev_col)
                        self.textbox.selection.active = True
                    
                    # Update selection end
                    self.textbox.selection.update_selection_end(
                        self.textbox.cursor_line,
                        self.textbox.cursor_col
                    )
                elif self.textbox.selection.is_active():
                    # Clear selection if shift is not held
                    self.textbox.selection.clear()
                
                # Update visual cursor
                self.textbox.update_visual_cursor()
                
                # Also scroll the view
                self.textbox.scroll_y = min(max(0, len(self.textbox.wrapped_lines) - self.textbox.visible_lines), 
                                           self.textbox.scroll_y + self.textbox.visible_lines)
                
                # Update scrollbar
                self.textbox.calculate_scrollbar()
            
            return True
        
        # Handle normal key input (including numpad)
        elif event.unicode and event.unicode.isprintable():
            # If selection is active, delete selected text first
            if self.textbox.selection.is_active():
                self.textbox.selection.delete_selected_text()
            
            # Insert character at cursor
            current_line = self.textbox.lines[self.textbox.cursor_line]
            self.textbox.lines[self.textbox.cursor_line] = current_line[:self.textbox.cursor_col] + event.unicode + current_line[self.textbox.cursor_col:]
            self.textbox.cursor_col += 1
            
            # Clear selection
            self.textbox.selection.clear()
            
            # Update wrapped lines
            self.textbox.update_wrapped_lines()
            
            # Make sure cursor is visible
            self.textbox.ensure_cursor_visible()
            
            return True
        
        return False
    
    def update(self, current_time):
        """Update key handler state"""
        # Handle key repeats with direct polling
        keys = pygame.key.get_pressed()
        
        # Check numpad keys specifically
        for numpad_key, (std_key, unicode_val) in self.numpad_map.items():
            if keys[numpad_key]:
                if numpad_key not in self.key_states:
                    # First press
                    self.key_states[numpad_key] = {
                        'time': current_time,
                        'unicode': unicode_val,
                        'repeat_count': 0,
                        'std_key': std_key
                    }
                    # Process the key immediately
                    self.process_key_repeat(std_key, unicode_val)
                else:
                    # Key is already pressed, handle repeat
                    state = self.key_states[numpad_key]
                    elapsed = current_time - state['time']
                    
                    if elapsed >= self.repeat_delay:
                        target_repeats = int((elapsed - self.repeat_delay) / self.repeat_interval) + 1
                        while state['repeat_count'] < target_repeats:
                            self.process_key_repeat(std_key, unicode_val)
                            state['repeat_count'] += 1
            elif numpad_key in self.key_states:
                # Key was released
                del self.key_states[numpad_key]
        
        # Handle other keys
        for key, state in list(self.key_states.items()):
            # Skip numpad keys (handled above)
            if key in self.numpad_map:
                continue
                
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