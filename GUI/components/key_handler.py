"""
Keyboard input handler for TextBox component
Cross-platform compatible (Windows/Linux/MacOS)
"""
import pygame
import platform
import subprocess
import sys
import os
from config import KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL

class KeyHandler:
    """
    Handles keyboard input for TextBox - Cross-platform compatible
    """
    def __init__(self, textbox):
        self.textbox = textbox
        
        # Platform detection
        self.platform = platform.system().lower()
        self.is_windows = self.platform == 'windows'
        self.is_linux = self.platform == 'linux'
        self.is_mac = self.platform == 'darwin'
        
        # Key repeat tracking
        self.key_states = {}  # Tracks the state of each key for manual repeat
        self.repeat_delay = KEY_REPEAT_DELAY
        self.repeat_interval = KEY_REPEAT_INTERVAL
        
        # Clipboard method preference (will be set on first use)
        self.clipboard_method = None
        self.clipboard_available = False
        
        # Initialize clipboard
        self._init_clipboard()
        
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
    
    def _init_clipboard(self):
        """Initialize clipboard support for the current platform"""
        try:
            # Try to initialize pygame scrap (works on most platforms)
            pygame.scrap.init()
            self.clipboard_available = True
            self.clipboard_method = 'pygame'
        except:
            self.clipboard_available = False
            self.clipboard_method = None
        
        # Platform-specific clipboard initialization
        if self.is_windows:
            self._init_windows_clipboard()
        elif self.is_mac:
            self._init_mac_clipboard()
        elif self.is_linux:
            self._init_linux_clipboard()
    
    def _init_windows_clipboard(self):
        """Initialize Windows-specific clipboard"""
        try:
            # Try win32clipboard first
            import win32clipboard
            self.clipboard_method = 'win32'
            self.clipboard_available = True
        except ImportError:
            try:
                # Fallback to tkinter
                import tkinter as tk
                self.clipboard_method = 'tkinter'
                self.clipboard_available = True
            except ImportError:
                # Keep pygame as fallback
                pass
    
    def _init_mac_clipboard(self):
        """Initialize macOS-specific clipboard"""
        try:
            # Test if pbcopy/pbpaste are available
            subprocess.run(['pbcopy'], input=b'', check=True, 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.clipboard_method = 'pbcopy'
            self.clipboard_available = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Keep pygame as fallback
            pass
    
    def _init_linux_clipboard(self):
        """Initialize Linux-specific clipboard"""
        # Try different clipboard tools in order of preference
        tools = ['xclip', 'xsel', 'wl-copy']  # wl-copy for Wayland
        
        for tool in tools:
            try:
                subprocess.run([tool, '--version'], check=True, 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.clipboard_method = tool
                self.clipboard_available = True
                break
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
    
    def _copy_windows(self, text):
        """Copy text to clipboard on Windows"""
        if self.clipboard_method == 'win32':
            try:
                import win32clipboard
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(text)
                win32clipboard.CloseClipboard()
                return True
            except Exception:
                pass
        
        if self.clipboard_method == 'tkinter':
            try:
                import tkinter as tk
                root = tk.Tk()
                root.withdraw()
                root.clipboard_clear()
                root.clipboard_append(text)
                root.update()
                root.destroy()
                return True
            except Exception:
                pass
        
        return False
    
    def _paste_windows(self):
        """Paste text from clipboard on Windows"""
        if self.clipboard_method == 'win32':
            try:
                import win32clipboard
                win32clipboard.OpenClipboard()
                data = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                return data
            except Exception:
                pass
        
        if self.clipboard_method == 'tkinter':
            try:
                import tkinter as tk
                root = tk.Tk()
                root.withdraw()
                data = root.clipboard_get()
                root.destroy()
                return data
            except Exception:
                pass
        
        return None
    
    def _copy_mac(self, text):
        """Copy text to clipboard on macOS"""
        try:
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(input=text.encode('utf-8'))
            return process.returncode == 0
        except Exception:
            return False
    
    def _paste_mac(self):
        """Paste text from clipboard on macOS"""
        try:
            process = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
            data, _ = process.communicate()
            if process.returncode == 0:
                return data.decode('utf-8')
        except Exception:
            pass
        return None
    
    def _copy_linux(self, text):
        """Copy text to clipboard on Linux"""
        if self.clipboard_method == 'xclip':
            try:
                process = subprocess.Popen(['xclip', '-selection', 'clipboard'], 
                                         stdin=subprocess.PIPE)
                process.communicate(input=text.encode('utf-8'))
                return process.returncode == 0
            except Exception:
                pass
        
        if self.clipboard_method == 'xsel':
            try:
                process = subprocess.Popen(['xsel', '--clipboard', '--input'], 
                                         stdin=subprocess.PIPE)
                process.communicate(input=text.encode('utf-8'))
                return process.returncode == 0
            except Exception:
                pass
        
        if self.clipboard_method == 'wl-copy':
            try:
                process = subprocess.Popen(['wl-copy'], stdin=subprocess.PIPE)
                process.communicate(input=text.encode('utf-8'))
                return process.returncode == 0
            except Exception:
                pass
        
        return False
    
    def _paste_linux(self):
        """Paste text from clipboard on Linux"""
        if self.clipboard_method == 'xclip':
            try:
                process = subprocess.Popen(['xclip', '-selection', 'clipboard', '-o'], 
                                         stdout=subprocess.PIPE)
                data, _ = process.communicate()
                if process.returncode == 0:
                    return data.decode('utf-8')
            except Exception:
                pass
        
        if self.clipboard_method == 'xsel':
            try:
                process = subprocess.Popen(['xsel', '--clipboard', '--output'], 
                                         stdout=subprocess.PIPE)
                data, _ = process.communicate()
                if process.returncode == 0:
                    return data.decode('utf-8')
            except Exception:
                pass
        
        if self.clipboard_method == 'wl-copy':
            try:
                process = subprocess.Popen(['wl-paste'], stdout=subprocess.PIPE)
                data, _ = process.communicate()
                if process.returncode == 0:
                    return data.decode('utf-8')
            except Exception:
                pass
        
        return None
    
    def _copy_pygame_fallback(self, text):
        """Fallback copy using pygame"""
        try:
            pygame.scrap.put(pygame.SCRAP_TEXT, text.encode('utf-8'))
            return True
        except Exception:
            return False
    
    def _paste_pygame_fallback(self):
        """Fallback paste using pygame"""
        try:
            clipboard_data = pygame.scrap.get(pygame.SCRAP_TEXT)
            if clipboard_data:
                # Try various encodings
                for encoding in ['utf-8', 'latin-1', 'cp1252', 'ascii']:
                    try:
                        return clipboard_data.decode(encoding)
                    except UnicodeDecodeError:
                        continue
                # Last resort
                return clipboard_data.decode('latin-1', errors='replace')
        except Exception:
            pass
        return None
        
    def copy_selected_text(self):
        """Copy selected text to clipboard with platform-specific handling"""
        if not self.textbox.selection.is_active():
            return False
        
        selected_text = self.textbox.selection.get_selected_text()
        if not selected_text:
            return False
        
        # Try platform-specific method first
        success = False
        if self.is_windows:
            success = self._copy_windows(selected_text)
        elif self.is_mac:
            success = self._copy_mac(selected_text)
        elif self.is_linux:
            success = self._copy_linux(selected_text)
        
        # Fallback to pygame
        if not success and self.clipboard_available:
            success = self._copy_pygame_fallback(selected_text)
        
        return success

    def paste_text_from_clipboard(self):
        """Paste text from clipboard with cross-platform compatibility"""
        try:
            clipboard_text = None
            
            # Try platform-specific method first
            if self.is_windows:
                clipboard_text = self._paste_windows()
            elif self.is_mac:
                clipboard_text = self._paste_mac()
            elif self.is_linux:
                clipboard_text = self._paste_linux()
            
            # Fallback to pygame
            if not clipboard_text and self.clipboard_available:
                clipboard_text = self._paste_pygame_fallback()
            
            if not clipboard_text:
                return False
            
            # Clean up the text
            clipboard_text = clipboard_text.replace('\0', '')
            clipboard_text = clipboard_text.replace('\r\n', '\n')
            clipboard_text = clipboard_text.replace('\r', '\n')
            
            # Filter unwanted control characters but keep essential whitespace
            printable_chars = []
            for char in clipboard_text:
                if char.isprintable() or char in ['\n', '\t']:
                    printable_chars.append(char)
            clipboard_text = ''.join(printable_chars)
            
            if not clipboard_text:
                return False
            
            # If selection is active, delete selected text first
            if self.textbox.selection.is_active():
                self.textbox.selection.delete_selected_text()
            
            # Handle multi-line paste
            if '\n' in clipboard_text:
                paste_lines = clipboard_text.split('\n')
                
                # Check line limit
                current_line_count = len(self.textbox.lines)
                lines_to_add = len(paste_lines) - 1
                if current_line_count + lines_to_add > 2500:
                    max_lines = 2500 - current_line_count
                    paste_lines = paste_lines[:max(1, max_lines+1)]
                
                # Process the paste
                current_line = self.textbox.lines[self.textbox.cursor_line]
                first_part = current_line[:self.textbox.cursor_col]
                self.textbox.lines[self.textbox.cursor_line] = first_part + paste_lines[0]
                
                # Insert remaining lines
                for i, line in enumerate(paste_lines[1:-1], 1):
                    self.textbox.lines.insert(self.textbox.cursor_line + i, line)
                
                # Handle last line
                if len(paste_lines) > 1:
                    last_part = current_line[self.textbox.cursor_col:]
                    last_line = paste_lines[-1] + last_part
                    self.textbox.lines.insert(self.textbox.cursor_line + len(paste_lines) - 1, last_line)
                
                # Update cursor position
                self.textbox.cursor_line = min(self.textbox.cursor_line + len(paste_lines) - 1, 2499)
                self.textbox.cursor_col = len(paste_lines[-1])
            else:
                # Single line paste
                current_line = self.textbox.lines[self.textbox.cursor_line]
                self.textbox.lines[self.textbox.cursor_line] = current_line[:self.textbox.cursor_col] + clipboard_text + current_line[self.textbox.cursor_col:]
                self.textbox.cursor_col += len(clipboard_text)
            
            # Update UI
            self.textbox.selection.clear()
            self.textbox.update_wrapped_lines()
            self.textbox.ensure_cursor_visible()
            
            return True
        
        except Exception as e:
            # Silent fallback for any unexpected errors
            return False
    
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
        
        # Procesar atajos antes de registrar la tecla para evitar repetición no deseada
        if pygame.key.get_mods() & pygame.KMOD_CTRL:
            if event.key in [pygame.K_c, pygame.K_v, pygame.K_x, pygame.K_a]:
                return self.handle_keydown(event)
        
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
        if hasattr(self.textbox, 'error_highlights') and self.textbox.error_highlights:
            self.textbox.clear_error_highlights()
        # Check for keyboard shortcuts (CTRL+Key)
        if pygame.key.get_mods() & pygame.KMOD_CTRL:
            # CTRL+Z (Undo)
            if event.key == pygame.K_z:
                return self.textbox.undo()
            
            # CTRL+C (Copy)
            if event.key == pygame.K_c:
                return self.copy_selected_text()
            
            # CTRL+V (Paste)
            elif event.key == pygame.K_v:
                return self.paste_text_from_clipboard()
            
            # CTRL+X (Cut)
            elif event.key == pygame.K_x:
                if self.copy_selected_text():
                    self.textbox.selection.delete_selected_text()
                    return True
            
            # CTRL+A (Select All)
            elif event.key == pygame.K_a:
                # Set selection start to beginning of document
                self.textbox.selection.start_line = 0
                self.textbox.selection.start_col = 0
                
                # Set selection end to end of document
                last_line = len(self.textbox.lines) - 1
                last_col = len(self.textbox.lines[last_line])
                
                # Activate selection
                self.textbox.selection.active = True
                self.textbox.selection.end_line = last_line
                self.textbox.selection.end_col = last_col
                
                # Update visual selection
                self.textbox.selection.update_visuals()
                
                # Position cursor at end of selection
                self.textbox.cursor_line = last_line
                self.textbox.cursor_col = last_col
                self.textbox.update_visual_cursor()
                
                return True
            
        # Check for special keys
        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            # If selection is active, delete selected text first
            if self.textbox.selection.is_active():
                self.textbox.selection.delete_selected_text()
            
            # Check if we're at the maximum line limit
            if len(self.textbox.lines) >= 2500:
                return True
            
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
        
        # First, handle Ctrl+Z separately with its own logic
        ctrl_pressed = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
        
        # Solo manejar CTRL+Z y CTRL+V con repetición
        if ctrl_pressed:
            # Variable para rastrear la tecla Z
            if "ctrl_z_time" not in self.__dict__:
                self.ctrl_z_time = 0
                self.ctrl_z_repeat_count = 0
                
            # Variable para rastrear la tecla V
            if "ctrl_v_time" not in self.__dict__:
                self.ctrl_v_time = 0
                self.ctrl_v_repeat_count = 0
                
            # Manejar repetición de CTRL+Z
            if keys[pygame.K_z]:
                if self.ctrl_z_time == 0:  # Primera pulsación
                    self.ctrl_z_time = current_time
                else:
                    elapsed = current_time - self.ctrl_z_time
                    if elapsed >= self.repeat_delay:
                        target_repeats = int((elapsed - self.repeat_delay) / self.repeat_interval) + 1
                        while self.ctrl_z_repeat_count < target_repeats:
                            self.textbox.undo()
                            self.ctrl_z_repeat_count += 1
            else:
                self.ctrl_z_time = 0
                self.ctrl_z_repeat_count = 0
                
            # Manejar repetición de CTRL+V
            if keys[pygame.K_v]:
                if self.ctrl_v_time == 0:  # Primera pulsación
                    self.ctrl_v_time = current_time
                else:
                    elapsed = current_time - self.ctrl_v_time
                    if elapsed >= self.repeat_delay:
                        target_repeats = int((elapsed - self.repeat_delay) / self.repeat_interval) + 1
                        while self.ctrl_v_repeat_count < target_repeats:
                            self.paste_text_from_clipboard()
                            self.ctrl_v_repeat_count += 1
            else:
                self.ctrl_v_time = 0
                self.ctrl_v_repeat_count = 0