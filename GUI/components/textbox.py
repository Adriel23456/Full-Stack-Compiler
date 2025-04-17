"""
TextBox implementation with word wrapping based on Windows Notepad behavior
"""
import pygame
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
        self.wrap_width = int(self.text_rect.width) - 5 #5px margin
        
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
        self.font = design.get_font("large")
        self.base_line_height = self.font.get_height()
        # Apply line height multiplier from config
        self.line_height = self.base_line_height * LINE_HEIGHT_MULTIPLIER
        self.visible_lines = self.text_rect.height // self.line_height
        
        # Line separator thickness
        self.line_thickness = LINE_SEPARATOR_THICKNESS
        
        # Text content storage variable
        self.text_content = ""
        
        # History for undo functionality
        self.history = [""]  # Comenzar con un estado vacío
        self.history_index = 0
        self.history_max_size = 200
        
        # Initialize components
        self.selection = TextSelection(self)
        self.key_handler = KeyHandler(self)
        
        # Mouse state
        self.scrollbar_dragging = False
        self.scrollbar_click_y = 0
        self.scrollbar_thumb_y = 0
        self.scrollbar_thumb_height = 30  # Will be calculated based on content

        self.error_highlights = []
        
        # Initialize wrapped lines
        self.update_wrapped_lines()
    
    def save_to_history(self):
        """Save current state to history"""
        current_text = self.get_text()
        
        # No guardar si el texto no ha cambiado
        if self.history and current_text == self.history[self.history_index]:
            return
        
        # Si hemos retrocedido en el historial y luego hicimos un cambio,
        # necesitamos eliminar el historial "futuro"
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        # Añadir el estado actual al historial
        self.history.append(current_text)
        
        # Limitar el tamaño del historial
        if len(self.history) > self.history_max_size:
            self.history.pop(0)
            self.history_index = len(self.history) - 1
        else:
            self.history_index = len(self.history) - 1

    def undo(self):
        """Undo last change"""
        if self.history_index > 0:
            # Guardar la posición actual de visualización
            current_visual_line = self.visual_cursor_line
            current_scroll_y = self.scroll_y
            
            # Retroceder un estado
            self.history_index -= 1
            
            # Guardar el texto actual y la posición del cursor
            current_lines = len(self.lines)
            current_cursor_line = self.cursor_line
            current_cursor_col = self.cursor_col
            
            # Restaurar el texto del historial
            old_text = self.history[self.history_index]
            self.lines = old_text.split('\n')
            if not self.lines:
                self.lines = [""]
            
            # Ajustar el cursor dentro de los límites válidos
            self.cursor_line = min(current_cursor_line, len(self.lines) - 1)
            self.cursor_col = min(current_cursor_col, len(self.lines[self.cursor_line]))
            
            # Actualizar líneas envueltas
            # Hacemos una copia temporal del scroll_y para restaurarlo después
            temp_scroll_y = self.scroll_y
            self.update_wrapped_lines()
            self.scroll_y = temp_scroll_y
            
            # Asegurar que el cursor sea visible pero manteniendo la posición
            # del scroll lo más cercana posible a la original
            self.ensure_cursor_visible()
            # Ensure scroll_y stays within valid bounds after content changes
            max_scroll = max(0, len(self.wrapped_lines) - self.visible_lines)
            self.scroll_y = min(self.scroll_y, max_scroll)
            self.calculate_scrollbar()
            
            return True
        return False
    
    def update_wrapped_lines(self):
        """Update the wrapped lines based on current content"""
        try:
            self.wrapped_lines = []
            
            # Aplicar límite estricto de líneas
            if len(self.lines) > 2500:
                self.lines = self.lines[:2500]
                # Asegurar que el cursor esté en una posición válida
                if self.cursor_line >= len(self.lines):
                    self.cursor_line = len(self.lines) - 1
                    self.cursor_col = len(self.lines[self.cursor_line])
            
            # Asegurarse de que siempre tengamos al menos una línea
            if not self.lines:
                self.lines = [""]
                self.cursor_line = 0
                self.cursor_col = 0
            
            # Asegurarse de que la línea actual sea válida
            if self.cursor_line >= len(self.lines):
                self.cursor_line = len(self.lines) - 1
            
            # Asegurarse de que la columna actual sea válida
            if self.cursor_col > len(self.lines[self.cursor_line]):
                self.cursor_col = len(self.lines[self.cursor_line])
            
            # Procesar cada línea para wrapping
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
            
            # Asegurarse de que siempre haya al menos una línea envuelta
            if not self.wrapped_lines:
                self.wrapped_lines = [(0, 0, "")]
            
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
        
        except Exception as e:
            # En caso de error, restablecemos a un estado seguro
            print(f"Error en update_wrapped_lines: {e}")
            self.lines = [""]
            self.cursor_line = 0
            self.cursor_col = 0
            self.wrapped_lines = [(0, 0, "")]
            self.scroll_y = 0
            self.calculate_scrollbar()
    
    def update_text_content(self):
        """Update the text_content variable with all current text including newlines"""
        new_content = '\n'.join(self.lines)
        
        # Guardar en el historial solo si el contenido cambió
        if new_content != self.text_content:
            self.text_content = new_content
            self.save_to_history()
        else:
            self.text_content = new_content
    
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
        try:
            # Verificar que los valores de cursor sean válidos
            if self.cursor_line >= len(self.lines):
                self.cursor_line = max(0, len(self.lines) - 1)
            
            if self.cursor_col > len(self.lines[self.cursor_line]):
                self.cursor_col = len(self.lines[self.cursor_line])
            
            # Asegurarse de que wrapped_lines no esté vacío
            if not self.wrapped_lines:
                self.wrapped_lines = [(0, 0, "")]
                self.visual_cursor_line = 0
                self.visual_cursor_col = 0
                return
            
            # Find the wrapped line containing the cursor
            found = False
            for i, (line_idx, start_idx, text) in enumerate(self.wrapped_lines):
                if line_idx == self.cursor_line:
                    if start_idx <= self.cursor_col and (start_idx + len(text) >= self.cursor_col or start_idx + len(text) == len(self.lines[line_idx])):
                        # Found the wrapped line containing the cursor
                        self.visual_cursor_line = i
                        self.visual_cursor_col = self.cursor_col - start_idx
                        found = True
                        break
            
            # Si no se encontró una línea adecuada, usar la primera línea envuelta
            if not found:
                self.visual_cursor_line = 0
                self.visual_cursor_col = 0
        
        except Exception as e:
            print(f"Error en update_visual_cursor: {e}")
            # En caso de error, restaurar a un estado seguro
            self.visual_cursor_line = 0
            self.visual_cursor_col = 0
                
    def calculate_scrollbar(self):
        """Calculate scrollbar dimensions"""
        try:
            if len(self.wrapped_lines) <= self.visible_lines:
                # All lines fit in view, no need for scrollbar
                self.scrollbar_thumb_height = self.scrollbar_rect.height
                self.scrollbar_thumb_y = 0
            else:
                # Calculate thumb size as proportion of visible to total content
                self.scrollbar_thumb_height = max(30, int(self.scrollbar_rect.height * 
                                                (self.visible_lines / max(1, len(self.wrapped_lines)))))
                
                # Calculate thumb position
                max_scroll_range = max(1, len(self.wrapped_lines) - self.visible_lines)
                scroll_ratio = self.scroll_y / max_scroll_range
                    
                max_thumb_travel = max(1, self.scrollbar_rect.height - self.scrollbar_thumb_height)
                self.scrollbar_thumb_y = int(scroll_ratio * max_thumb_travel)
        except Exception as e:
            # En caso de error, establecer valores seguros por defecto
            print(f"Error en calculate_scrollbar: {e}")
            self.scrollbar_thumb_height = max(30, self.scrollbar_rect.height // 4)
            self.scrollbar_thumb_y = 0
    
    def set_text(self, text):
        """Set the text content of the editor"""
        try:
            # Si el texto es None, establecer como cadena vacía
            if text is None:
                text = ""
            
            # Dividir el texto en líneas
            lines = text.split('\n')
            
            # Si no hay líneas, asegurarse de tener al menos una línea vacía
            if not lines:
                lines = [""]
            
            # Establecer las líneas
            self.lines = lines
            
            # Enforce maximum line limit
            if len(self.lines) > 2500:
                self.lines = self.lines[:2500]
            
            # Reset cursor and scroll con verificación de límites
            self.cursor_line = min(self.cursor_line, len(self.lines) - 1)
            
            # Asegurarse de que cursor_line sea válido
            if self.cursor_line < 0:
                self.cursor_line = 0
            
            # Asegurarse de que cursor_col sea válido para la línea actual
            if self.cursor_line < len(self.lines):
                self.cursor_col = min(self.cursor_col, len(self.lines[self.cursor_line]))
            else:
                self.cursor_col = 0
            
            # Resetear scroll
            self.scroll_y = 0
            
            # Update wrapped lines con manejo de excepciones
            self.update_wrapped_lines()
        
        except Exception as e:
            print(f"Error en set_text: {e}")
            # En caso de error, restaurar a un estado seguro
            self.lines = [""]
            self.cursor_line = 0
            self.cursor_col = 0
            self.scroll_y = 0
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
        try:
            # Verificar primero si tenemos líneas para trabajar
            if not self.wrapped_lines:
                return 0, 0
                
            # Calculate the wrapped line clicked
            rel_y = mouse_pos[1] - self.text_rect.top
            
            # Asegurarse de que line_height no sea cero
            if self.line_height <= 0:
                self.line_height = 1  # Valor seguro por defecto
                
            wrapped_line_idx = self.scroll_y + rel_y // self.line_height
            wrapped_line_idx = min(max(0, wrapped_line_idx), len(self.wrapped_lines) - 1)
            
            # Get the wrapped line info
            line_idx, start_idx, text = self.wrapped_lines[wrapped_line_idx]
            
            # Calculate the closest character position
            rel_x = mouse_pos[0] - self.text_rect.left - 5  # Adjust for padding
            
            # Si la línea está vacía, devolver simplemente la posición de inicio
            if not text:
                return line_idx, start_idx
            
            # Usar un método más simple y fiable: encontrar la mejor posición probando cada posibilidad
            best_col = 0
            min_distance = float('inf')
            
            # Probar cada posible posición de columna y encontrar la más cercana al punto donde se hizo clic
            for col in range(len(text) + 1):
                # Obtener la posición x de esta columna
                x_pos = self.font.size(text[:col])[0]
                
                # Calcular distancia a la posición del mouse
                distance = abs(x_pos - rel_x)
                
                # Si esta posición está más cerca que la mejor encontrada hasta ahora, actualizarla
                if distance < min_distance:
                    min_distance = distance
                    best_col = col
            
            return line_idx, start_idx + best_col
            
        except ZeroDivisionError:
            # Si ocurre una división por cero, devolver la posición actual del cursor
            return self.cursor_line, self.cursor_col
        except Exception as e:
            # Para cualquier otro error, imprimir e intentar devolver una posición segura
            print(f"Error en posición del mouse: {e}")
            return self.cursor_line, self.cursor_col
    
    def handle_event(self, event):
        """Handle pygame events"""
        # First check for typing or cursor movement
        if event.type == pygame.KEYDOWN:
            return self.key_handler.handle_keydown_event(event)
        
        # Handle key release to stop repeating
        elif event.type == pygame.KEYUP:
            return self.key_handler.handle_keyup_event(event)
        
        # Handle mouse wheel for scrolling - MANTIENE LA SELECCIÓN ACTIVA
        elif event.type == pygame.MOUSEWHEEL:
            # Obtener el estado actual de selección y cursor
            was_selecting = self.selection.is_selection_mode()
            was_active = self.selection.is_active()
            
            # Guardar completamente el estado de selección
            selection_state = None
            if was_selecting or was_active:
                selection_state = {
                    'mode': self.selection.selection_mode,
                    'active': self.selection.active,
                    'start_line': self.selection.start_line,
                    'start_col': self.selection.start_col,
                    'end_line': self.selection.end_line,
                    'end_col': self.selection.end_col,
                    'start_time': self.selection.selection_start_time,
                    'visual_ranges': self.selection.visual_ranges.copy()
                }
            
            # Realizar el scroll
            self.scroll_y = max(0, min(len(self.wrapped_lines) - self.visible_lines, 
                                    self.scroll_y - event.y * 3))
            # Actualizar scrollbar
            self.calculate_scrollbar()
            
            # Restaurar completamente el estado de selección
            if selection_state:
                self.selection.selection_mode = selection_state['mode']
                self.selection.active = selection_state['active']
                self.selection.start_line = selection_state['start_line']
                self.selection.start_col = selection_state['start_col']
                self.selection.end_line = selection_state['end_line']
                self.selection.end_col = selection_state['end_col']
                self.selection.selection_start_time = selection_state['start_time']
                self.selection.visual_ranges = selection_state['visual_ranges']
            
            return True
        
        # Handle mouse motion
        elif event.type == pygame.MOUSEMOTION:
            return self.handle_mouse_motion(event)
        
        # Handle mouse clicks on the text area
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Solo botón izquierdo
            return self.handle_mouse_down(event)
        
        # Handle mouse up
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Solo botón izquierdo
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
        if left_button_pressed and self.selection.is_selection_mode():
            # Auto-scrolling con tres niveles de velocidad cuando el mouse está cerca de los bordes
            auto_scroll_distance = 0
            
            # Distancia del mouse al borde superior
            top_distance = event.pos[1] - self.text_rect.top
            # Distancia del mouse al borde inferior
            bottom_distance = self.text_rect.bottom - event.pos[1]
            
            # Determinar velocidad de scroll para el borde superior
            if top_distance < 45:
                # Nivel 3: Rápido - cuando está a 0-45 píxeles
                auto_scroll_distance = -1.5
            elif top_distance < 75:
                # Nivel 2: Medio - cuando está a 45-75 píxeles
                auto_scroll_distance = -1
            elif top_distance < 90:
                # Nivel 1: Lento - cuando está a 75-90 píxeles
                auto_scroll_distance = -0.5
            
            # Determinar velocidad de scroll para el borde inferior (si no hay ya un scroll hacia arriba)
            if auto_scroll_distance == 0 and bottom_distance < 45:
                # Nivel 3: Rápido - cuando está a 0-45 píxeles
                auto_scroll_distance = 1.5
            elif auto_scroll_distance == 0 and bottom_distance < 75:
                # Nivel 2: Medio - cuando está a 45-75 píxeles
                auto_scroll_distance = 1
            elif auto_scroll_distance == 0 and bottom_distance < 90:
                # Nivel 1: Lento - cuando está a 75-90 píxeles
                auto_scroll_distance = 0.5
            
            # Aplicar auto-scroll si es necesario
            if auto_scroll_distance != 0:
                self.scroll_y = int(max(0, min(len(self.wrapped_lines) - self.visible_lines, 
                                        self.scroll_y + auto_scroll_distance)))
                # Update scrollbar
                self.calculate_scrollbar()
            
            # Ahora maneja el movimiento de selección normal
            if self.text_rect.collidepoint(event.pos):
                # Get logical position at mouse
                end_line, end_col = self.get_position_at_mouse(event.pos)
                
                # Update selection end
                self.selection.update_selection_end(end_line, end_col)
                
                # Update cursor position to match selection end
                self.cursor_line = end_line
                self.cursor_col = end_col
                self.update_visual_cursor()
            
            return True
            
        # Handle scrollbar dragging
        if self.scrollbar_dragging:
            try:
                # Calculate new thumb position
                new_thumb_y = event.pos[1] - self.scrollbar_click_y
                
                # Constrain to scrollbar
                new_thumb_y = max(0, min(self.scrollbar_rect.height - max(10, self.scrollbar_thumb_height), new_thumb_y))
                
                # Calculate new scroll position
                scroll_height = max(1, self.scrollbar_rect.height - self.scrollbar_thumb_height)
                ratio = new_thumb_y / scroll_height
                max_scroll = max(0, len(self.wrapped_lines) - self.visible_lines)
                self.scroll_y = int(ratio * max_scroll)
                
                # Update scrollbar
                self.calculate_scrollbar()
                
                return True
            except Exception as e:
                print(f"Error en arrastre de scrollbar: {e}")
                self.scrollbar_dragging = False
                return False
            
        return False
    
    def handle_mouse_down(self, event):
        """Handle mouse button down events"""
        # Check if clicking in text area
        if self.text_rect.collidepoint(event.pos):
            # Set focus
            self.is_focused = True
            
            # Get logical position at mouse
            line_idx, col_idx = self.get_position_at_mouse(event.pos)
            
            # Check if Shift is held - if so, start selection from current cursor position
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if not self.selection.is_active():
                    # Start new selection from current cursor position
                    self.selection.set_selection_start(self.cursor_line, self.cursor_col)
                    self.selection.active = True
                
                # Set the end of selection at the click position
                self.selection.update_selection_end(line_idx, col_idx)
                
                # Update cursor position to match click position
                self.cursor_line = line_idx
                self.cursor_col = col_idx
                
                # Update visual cursor and visuals
                self.update_visual_cursor()
                self.selection.update_visuals()
            else:
                # Normal behavior - set cursor position
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
            try:
                # Check if clicking on thumb
                thumb_rect = pygame.Rect(
                    self.scrollbar_rect.x,
                    self.scrollbar_rect.y + self.scrollbar_thumb_y,
                    self.scrollbar_rect.width,
                    max(10, self.scrollbar_thumb_height)  # Asegurar altura mínima
                )
                
                if thumb_rect.collidepoint(event.pos):
                    # Start dragging
                    self.scrollbar_dragging = True
                    self.scrollbar_click_y = event.pos[1] - self.scrollbar_thumb_y
                else:
                    # Click in scrollbar but not on thumb - jump to position
                    rel_y = event.pos[1] - self.scrollbar_rect.top
                    
                    # Calculate ratio of click to scrollbar height
                    ratio = rel_y / max(1, self.scrollbar_rect.height)
                    
                    # Set scroll position
                    total_lines = max(1, len(self.wrapped_lines))
                    visible_lines = max(1, self.visible_lines)
                    max_scroll = max(0, total_lines - visible_lines)
                    self.scroll_y = max(0, min(max_scroll, int(ratio * total_lines)))
                    
                    # Update scrollbar
                    self.calculate_scrollbar()
                return True
            except Exception as e:
                print(f"Error en el manejo del scrollbar: {e}")
                return False
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
        """
        Render the textbox con máxima protección contra errores
        """
        try:
            # Draw background
            pygame.draw.rect(surface, design.colors["textbox_bg"], self.rect)

            if hasattr(self, 'error_highlights') and self.error_highlights:
                for highlight in self.error_highlights:
                    # Get the line and column of the error
                    error_line = highlight['line']
                    error_col = highlight['column']
                    error_len = highlight['length']
                    
                    # Find all wrapped lines that correspond to this original line
                    for i, wrapped_info in enumerate(self.wrapped_lines):
                        # Extract information from wrapped_lines
                        # Note: wrapped_lines format is [(line_idx, start_col, text), ...]
                        if len(wrapped_info) >= 3:  # Make sure the tuple has at least 3 elements
                            wrapped_line_idx, wrapped_start_col, wrapped_text = wrapped_info
                            
                            # Check if this wrapped line belongs to the error line
                            if wrapped_line_idx == error_line:
                                # Calculate end column for this wrapped segment
                                wrapped_end_col = wrapped_start_col + len(wrapped_text)
                                
                                # Check if error overlaps with this segment
                                if (error_col < wrapped_end_col and 
                                    error_col + error_len > wrapped_start_col):
                                    
                                    # Calculate visible part of the error in this segment
                                    highlight_start = max(error_col, wrapped_start_col) - wrapped_start_col
                                    highlight_end = min(error_col + error_len, wrapped_end_col) - wrapped_start_col
                                    
                                    # If this wrapped line is visible on screen
                                    if self.scroll_y <= i < self.scroll_y + self.visible_lines:
                                        # Calculate display position
                                        y_pos = self.text_rect.top + (i - self.scroll_y) * self.line_height
                                        
                                        # Get text width before highlight
                                        if highlight_start > 0:
                                            start_width = self.font.size(wrapped_text[:highlight_start])[0]
                                        else:
                                            start_width = 0
                                            
                                        # Get highlight width
                                        if highlight_end > highlight_start:
                                            highlight_width = self.font.size(wrapped_text[highlight_start:highlight_end])[0]
                                        else:
                                            highlight_width = self.font.size("W")[0]  # Use a default width
                                        
                                        # Create highlight rectangle
                                        highlight_rect = pygame.Rect(
                                            self.text_rect.left + 5 + start_width,
                                            y_pos,
                                            highlight_width,
                                            self.line_height
                                        )
                                        
                                        # Draw the highlight
                                        pygame.draw.rect(surface, (255, 150, 150), highlight_rect)

            
            # Draw line numbers background
            pygame.draw.rect(surface, design.colors["toolbar"], self.line_numbers_rect)
            
            # Draw text area border
            pygame.draw.rect(surface, design.colors["textbox_border"], self.rect, 1)
            
            # Determine line colors based on theme
            is_light_theme = design.colors["background"][0] > 128
            line_color = (180, 180, 180) if is_light_theme else (80, 80, 80)
            
            # Verificar que wrapped_lines es una lista válida
            if not hasattr(self, 'wrapped_lines') or not isinstance(self.wrapped_lines, list):
                print("Error: wrapped_lines no es válido")
                self.wrapped_lines = [(0, 0, "")]
            
            # Verificar líneas y cursor
            if not hasattr(self, 'lines') or not isinstance(self.lines, list) or len(self.lines) == 0:
                print("Error: lines no es válido")
                self.lines = [""]
            
            if not hasattr(self, 'cursor_line') or not isinstance(self.cursor_line, int):
                print("Error: cursor_line no es válido")
                self.cursor_line = 0
            
            if not hasattr(self, 'cursor_col') or not isinstance(self.cursor_col, int):
                print("Error: cursor_col no es válido")
                self.cursor_col = 0
                
            # Asegurar que el cursor esté dentro de los límites
            if self.cursor_line >= len(self.lines):
                self.cursor_line = max(0, len(self.lines) - 1)
                
            if self.cursor_line < 0:
                self.cursor_line = 0
                
            if self.cursor_line < len(self.lines) and self.cursor_col > len(self.lines[self.cursor_line]):
                self.cursor_col = len(self.lines[self.cursor_line])
                
            if self.cursor_col < 0:
                self.cursor_col = 0
            
            # Verificar scroll_y
            if not hasattr(self, 'scroll_y') or not isinstance(self.scroll_y, int):
                print("Error: scroll_y no es válido")
                self.scroll_y = 0
                
            if not hasattr(self, 'visible_lines') or not isinstance(self.visible_lines, int) or self.visible_lines <= 0:
                print("Error: visible_lines no es válido")
                self.visible_lines = max(1, self.text_rect.height // max(1, self.line_height))
                
            # Asegurar que scroll_y esté dentro de los límites
            max_scroll = max(0, len(self.wrapped_lines) - self.visible_lines)
            if self.scroll_y > max_scroll:
                self.scroll_y = max_scroll
                
            if self.scroll_y < 0:
                self.scroll_y = 0
            
            # Draw visible wrapped lines
            for i in range(min(self.visible_lines, len(self.wrapped_lines) - self.scroll_y)):
                try:
                    display_idx = self.scroll_y + i
                    
                    # Verificar que display_idx es válido
                    if display_idx < 0 or display_idx >= len(self.wrapped_lines):
                        continue
                    
                    y = self.text_rect.top + i * self.line_height
                    
                    # Draw line separator at top of this line
                    pygame.draw.line(surface, line_color, 
                                (self.line_numbers_rect.left, y), 
                                (self.text_rect.right, y), self.line_thickness)
                    
                    # Get wrapped line info
                    line_idx, start_idx, text = self.wrapped_lines[display_idx]
                    
                    # Verificar que line_idx es válido
                    if line_idx < 0 or line_idx >= len(self.lines):
                        continue
                    
                    # Draw line number (only for start of logical lines)
                    if start_idx == 0:  # This is the first wrapped segment of a logical line
                        line_num_text = f"Line {line_idx + 1}"
                        line_num_surf = design.get_font("small").render(line_num_text, True, design.colors["textbox_text"])
                        # Alinear a la izquierda con un margen, en lugar de centrar
                        line_num_x = self.line_numbers_rect.left + 10  # Margen de 10px desde la izquierda
                        line_num_y = y + (self.line_height - line_num_surf.get_height()) // 2  # Centrar verticalmente
                        surface.blit(line_num_surf, (line_num_x, line_num_y))
                    
                    # Draw selection highlight if this line has selection
                    if hasattr(self, 'selection') and self.selection.is_active():
                        try:
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
                        except Exception as e:
                            print(f"Error dibujando selección: {e}")
                    
                    # Draw text - center vertically in the larger line height
                    try:
                        text_surf = self.font.render(text, True, design.colors["textbox_text"])
                        text_y = y + (self.line_height - self.base_line_height) // 2  # Center text vertically
                        surface.blit(text_surf, (self.text_rect.left + 5, text_y))
                    except Exception as e:
                        print(f"Error dibujando texto: {e}")
                    
                    # Draw cursor if on this line and cursor is visible and textbox is focused
                    try:
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
                    except Exception as e:
                        print(f"Error dibujando cursor: {e}")
                
                except Exception as e:
                    print(f"Error dibujando línea {i}: {e}")
                    continue
            
            # Draw bottom line separator for last visible line
            if self.visible_lines > 0 and self.scroll_y + self.visible_lines <= len(self.wrapped_lines):
                y = self.text_rect.top + self.visible_lines * self.line_height
                pygame.draw.line(surface, line_color, 
                            (self.line_numbers_rect.left, y), 
                            (self.text_rect.right, y), self.line_thickness)
            
            # Draw scrollbar if needed
            try:
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
            except Exception as e:
                print(f"Error dibujando scrollbar: {e}")
        
        except Exception as e:
            print(f"Error crítico en TextBox.render(): {e}")
    
    def update_font(self):
        """Update font based on current settings"""
        # Get font from design system
        self.font = design.get_font("large")
        
        # Update font-related metrics
        self.base_line_height = self.font.get_height()
        # Apply line height multiplier from config
        self.line_height = self.base_line_height * LINE_HEIGHT_MULTIPLIER
        self.visible_lines = self.text_rect.height // self.line_height
        
        # Update wrapped lines to account for new font size
        self.update_wrapped_lines()
    
    def resize(self, new_rect):
        """
        Resize the textbox to new dimensions
        
        Args:
            new_rect: New rectangle dimensions
        """
        # Store the overall rectangle
        self.rect = pygame.Rect(new_rect)
        
        # Split into line numbers area and text area
        self.line_numbers_rect = pygame.Rect(new_rect.x, new_rect.y, self.line_numbers_width, new_rect.height)
        self.text_rect = pygame.Rect(new_rect.x + self.line_numbers_width, new_rect.y, 
                                    new_rect.width - self.line_numbers_width - 15, new_rect.height)
        self.scrollbar_rect = pygame.Rect(new_rect.right - 15, new_rect.y, 15, new_rect.height)
        
        # Update wrap width
        self.wrap_width = int(self.text_rect.width) - 5 #5px margin
        
        # Update visible lines
        self.visible_lines = self.text_rect.height // self.line_height
        
        # Update wrapped lines for new width
        self.update_wrapped_lines()
        
        # Ensure cursor is visible
        self.ensure_cursor_visible()
    
    def highlight_error(self, line, column, length=1):
        """
        Highlight an error in the text
        
        Args:
            line: Line number (1-based)
            column: Column number (0-based)
            length: Length of the text to highlight
        """
        # Convert to 0-based line index
        line_idx = line - 1
        
        # Ensure the line exists
        if line_idx < 0 or line_idx >= len(self.lines):
            print(f"Error: Cannot highlight line {line}, only {len(self.lines)} lines exist")
            # Use first line if the specified line doesn't exist
            line_idx = 0
        
        # Ensure we don't highlight beyond the end of the line
        line_text = self.lines[line_idx]
        if column >= len(line_text):
            column = max(0, len(line_text) - 1)
        
        # Limit highlight length to not go beyond the end of the line
        actual_length = min(length, len(line_text) - column)
        if actual_length <= 0:
            actual_length = 1  # Ensure we highlight at least one character
        
        # Add highlight to the error highlights list
        self.error_highlights.append({
            'line': line_idx,
            'column': column,
            'length': actual_length
        })

    def highlight_errors(self, errors):
        """
        Highlight multiple errors at once
        
        Args:
            errors: List of error dictionaries with line, column, and length keys
        """
        # Clear existing highlights
        self.clear_error_highlights()
        
        # Add each error highlight
        for error in errors:
            line = error.get('line', 1)  # Default to line 1 if not specified
            if line < 1:
                line = 1  # Ensure line is at least 1
                
            column = error.get('column', 0)
            length = error.get('length', 1)
            
            # Ensure length is at least 1
            if length < 1:
                length = 1
                
            self.highlight_error(line, column, length)

    def clear_error_highlights(self):
        """
        Clear all error highlights
        """
        self.error_highlights = []