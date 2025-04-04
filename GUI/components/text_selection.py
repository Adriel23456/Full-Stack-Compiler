"""
Text selection handling for TextBox component
"""
import pygame

class TextSelection:
    """
    Handles text selection functionality for TextBox
    """
    def __init__(self, textbox):
        self.textbox = textbox
        
        # Selection state
        self.active = False
        self.start_line = 0
        self.start_col = 0
        self.end_line = 0
        self.end_col = 0
        self.visual_ranges = []  # List of (display_idx, start_x, end_x)
        
        # Mouse tracking for selection
        self.selection_start_time = 0
        self.selection_mode = False
    
    def is_active(self):
        """Check if selection is active"""
        return self.active
    
    def is_selection_mode(self):
        """Check if selection mode is active (mouse dragging)"""
        return self.selection_mode
    
    def has_selection_start(self):
        """Check if selection start point is set"""
        return self.selection_start_time > 0
    
    def get_selection_start_time(self):
        """Get the time when selection started"""
        return self.selection_start_time
        
    def get_visual_ranges(self):
        """Get visual ranges for rendering selection"""
        return self.visual_ranges
    
    def get_selected_text(self):
        """Get the selected text if a selection is active"""
        if not self.active:
            return ""
        
        # Ensure start is before end
        start_line, start_col, end_line, end_col = self.get_normalized_selection()
        
        if start_line == end_line:
            # Selection is within a single line
            return self.textbox.lines[start_line][start_col:end_col]
        
        # Multi-line selection
        result = [self.textbox.lines[start_line][start_col:]]  # First line
        
        # Middle lines (if any)
        for line_idx in range(start_line + 1, end_line):
            result.append(self.textbox.lines[line_idx])
        
        # Last line
        result.append(self.textbox.lines[end_line][:end_col])
        
        return '\n'.join(result)
    
    def set_selection_start(self, line, col):
        """Set the start point for a potential selection"""
        self.start_line = line
        self.start_col = col
        self.selection_start_time = pygame.time.get_ticks()
        self.selection_mode = False  # Asegúrate de que el modo de selección inicie desactivado
    
    def reset_selection_start(self):
        """Reset the selection start point"""
        self.selection_start_time = 0
    
    def create_selection(self, end_line, end_col):
        """Create a selection from start to end point"""
        self.active = True
        self.end_line = end_line
        self.end_col = end_col
        self.update_visuals()
    
    def update_selection_end(self, end_line, end_col):
        """Update the end point of the selection"""
        self.end_line = end_line
        self.end_col = end_col
        self.update_visuals()
    
    def clear(self):
        """Clear the active selection"""
        self.active = False
        self.visual_ranges = []
    
    def start_selection_mode(self):
        """Start text selection mode (for mouse dragging)"""
        self.selection_mode = True
        self.active = True
        self.end_line = self.start_line
        self.end_col = self.start_col
        self.update_visuals()
    
    def end_selection_mode(self):
        """End text selection mode (after mouse release)"""
        self.selection_mode = False
    
    def check_for_selection_mode(self, current_time):
        """Check if selection mode should be activated"""
        if not self.textbox.is_focused or self.selection_start_time == 0 or self.selection_mode:
            return
            
        # 85ms para el tiempo de mantener presionado
        if current_time - self.selection_start_time >= 85:  
            self.start_selection_mode()
    
    def delete_selected_text(self):
        """Delete the selected text and position cursor at the start of selection"""
        if not self.active:
            return
        
        # Get normalized selection coordinates (start before end)
        start_line, start_col, end_line, end_col = self.get_normalized_selection()
        
        # Position cursor at start of selection
        self.textbox.cursor_line = start_line
        self.textbox.cursor_col = start_col
        
        if start_line == end_line:
            # Selection is within a single line
            current_line = self.textbox.lines[start_line]
            self.textbox.lines[start_line] = current_line[:start_col] + current_line[end_col:]
        else:
            # Multi-line selection
            # First line partial
            first_line = self.textbox.lines[start_line][:start_col]
            # Last line partial
            last_line = self.textbox.lines[end_line][end_col:]
            
            # Replace with combined content
            self.textbox.lines[start_line] = first_line + last_line
            
            # Remove all lines in between
            for _ in range(end_line - start_line):
                self.textbox.lines.pop(start_line + 1)
        
        # Clear selection
        self.clear()
        
        # Update wrapped lines
        self.textbox.update_wrapped_lines()
    
    def get_normalized_selection(self):
        """Return selection coordinates with start before end"""
        if self.start_line < self.end_line or \
           (self.start_line == self.end_line and 
            self.start_col <= self.end_col):
            return (self.start_line, self.start_col,
                    self.end_line, self.end_col)
        else:
            return (self.end_line, self.end_col,
                    self.start_line, self.start_col)
    
    def get_x_for_column(self, text, col):
        """Get the x coordinate for a given column in a text line"""
        if col <= 0:
            return 0
        if col >= len(text):
            return self.textbox.font.size(text)[0]
        
        return self.textbox.font.size(text[:col])[0]
    
    def update_visuals(self):
        """Update visual ranges for rendering the selection"""
        if not self.active:
            self.visual_ranges = []
            return
        
        # Get normalized selection coordinates
        start_line, start_col, end_line, end_col = self.get_normalized_selection()
        
        # Clear previous visual ranges
        self.visual_ranges = []
        
        # Find visual ranges for all affected wrapped lines
        for display_idx, (line_idx, start_idx, text) in enumerate(self.textbox.wrapped_lines):
            # Skip lines outside the selection
            if line_idx < start_line or line_idx > end_line:
                continue
            
            # Calculate selection start and end for this wrapped line
            if line_idx == start_line and start_idx <= start_col and start_idx + len(text) > start_col:
                # This wrapped line contains the selection start
                sel_start_x = self.get_x_for_column(text, start_col - start_idx)
                
                if line_idx == end_line and start_idx <= end_col and start_idx + len(text) >= end_col:
                    # This wrapped line also contains the selection end
                    sel_end_x = self.get_x_for_column(text, min(end_col - start_idx, len(text)))
                else:
                    # Selection continues beyond this wrapped line
                    sel_end_x = self.get_x_for_column(text, len(text))
                
                self.visual_ranges.append((display_idx, sel_start_x, sel_end_x))
            
            elif line_idx == end_line and start_idx <= end_col:
                # This wrapped line contains the selection end
                if start_idx < end_col:
                    sel_start_x = self.get_x_for_column(text, 0)
                    sel_end_x = self.get_x_for_column(text, min(end_col - start_idx, len(text)))
                    self.visual_ranges.append((display_idx, sel_start_x, sel_end_x))
            
            elif line_idx > start_line and line_idx < end_line:
                # This wrapped line is completely within the selection
                sel_start_x = self.get_x_for_column(text, 0)
                sel_end_x = self.get_x_for_column(text, len(text))
                self.visual_ranges.append((display_idx, sel_start_x, sel_end_x))