from GUI.views.config_view import ConfigView

"""
Editor view for the Full Stack Compiler
"""
import pygame
from GUI.view_base import ViewBase
from GUI.design_base import design
from GUI.components.button import Button, ToolbarButton
from GUI.components.textbox import TextBox
from config import States

class EditorView(ViewBase):
    """
    Main editor view for the application
    """
    def __init__(self, view_controller):
        """
        Initialize the editor view
        
        Args:
            view_controller: View Controller with FSM
        """
        super().__init__(view_controller)
        self.config_view = None
    
    def setup(self):
        """
        Set up the editor view
        """
        # Get the current screen dimensions
        screen_rect = self.screen.get_rect()
        screen_width = screen_rect.width
        screen_height = screen_rect.height

        # Calculate layout dimensions proportionally to screen size
        toolbar_height = design.toolbar_height
        button_height = 40
        button_width = max(120, int(screen_width * 0.12))  # Minimum width but scales with screen
        button_margin = max(20, int(screen_width * 0.02))  # Scales margin with screen

        # Create toolbar buttons - calculate proper spacing
        toolbar_button_width = max(100, int(screen_width * 0.09))
        toolbar_button_margin = max(10, int(screen_width * 0.01))
        toolbar_y = 5

        # Position the main toolbar buttons with proper spacing
        self.save_button = ToolbarButton(
            pygame.Rect(button_margin, toolbar_y, toolbar_button_width, toolbar_height - 10),
            "Save",
            fixed_height=toolbar_height - 10     # Fija la altura
        )

        self.load_button = ToolbarButton(
            pygame.Rect(self.save_button.rect.right + toolbar_button_margin, toolbar_y,
                        toolbar_button_width, toolbar_height - 10),
            "Load",
            fixed_height=toolbar_height - 10     # Fija la altura
        )

        self.configure_button = ToolbarButton(
            pygame.Rect(self.load_button.rect.right + toolbar_button_margin, toolbar_y,
                        toolbar_button_width, toolbar_height - 10),
            "Configure",
            fixed_height=toolbar_height - 10     # Fija la altura
        )

        self.credits_button = ToolbarButton(
            pygame.Rect(self.configure_button.rect.right + toolbar_button_margin, toolbar_y,
                        toolbar_button_width, toolbar_height - 10),
            "Credits",
            fixed_height=toolbar_height - 10     # Fija la altura
        )

        # NUEVO ENFOQUE PARA LOS BOTONES DE SÍMBOLOS
        # Queremos que los botones de símbolos estén alineados a la derecha del toolbar,
        # dejando un margen de 8px entre ellos y el borde derecho,
        # y que estén separados 8px del último botón principal (credits_button).
        margin_between = 8   # Espacio entre el último botón del toolbar y el grupo de símbolos

        # Calcular el ancho disponible: desde el final del botón "Credits" + 8px, hasta el borde derecho menos 8px.
        available_width = screen_width - (self.credits_button.rect.right + margin_between) - button_margin

        num_symbols = 6
        num_spaces = num_symbols - 1
        symbol_margin = 4  # Espaciado fijo entre cada botón de símbolo

        # Calcular ancho para cada botón, limitándolo entre 20 y 40px.
        symbol_width = int((available_width - (num_spaces * symbol_margin)) / num_symbols)
        symbol_width = max(20, min(symbol_width, 40))
        total_symbols_width = num_symbols * symbol_width + num_spaces * symbol_margin

        # Para alinear a la derecha, la posición inicial se calcula para que el grupo termine a 8px del borde.
        symbols_offset_x = screen_width - total_symbols_width - button_margin

        self.symbol_buttons = []
        symbols = ["(", ")", "{", "}", "[", "]"]

        current_x = symbols_offset_x
        for symbol in symbols:
            self.symbol_buttons.append(
                ToolbarButton(
                    pygame.Rect(current_x, toolbar_y, symbol_width, toolbar_height - 10),
                    symbol,
                    fixed_width=symbol_width,          # Fija el ancho para evitar que se recalcule
                    fixed_height=toolbar_height - 10     # Fija la altura
                )
            )
            current_x += symbol_width + symbol_margin

        # Create compile and execute buttons at the bottom
        bottom_y = screen_height - button_height - 15

        self.compile_button = Button(
            pygame.Rect(button_margin, bottom_y, button_width, button_height),
            "Compile",
            fixed_height=button_height,     # Fija la altura
        )

        self.grammar_button = Button(
            pygame.Rect(self.compile_button.rect.right + toolbar_button_margin, bottom_y, button_width, button_height),
            "Grammar",
            fixed_height=button_height,     # Fija la altura
        )

        # Alinear exactamente el botón Execute con el borde derecho del TextBox
        self.execute_button = Button(
            pygame.Rect(screen_width - button_margin - button_width, bottom_y,
                        button_width, button_height),
            "Execute",
            fixed_height=button_height,     # Fija la altura
        )

        # Create the main text editor area - scale with window size
        editor_top = toolbar_height + 10
        # Se deja un espacio vertical de 5px entre el TextBox y los botones inferiores
        editor_bottom = bottom_y - 5
        editor_height = editor_bottom - editor_top

        # El TextBox tendrá el mismo ancho que la distancia entre los márgenes
        self.text_editor = TextBox(
            pygame.Rect(button_margin, editor_top,
                        screen_width - 2 * button_margin, editor_height)
        )

        # Set initial content if not already set
        if not hasattr(self, '_initialized_content'):
            self.text_editor.set_text("Welcome to the Full Stack Compiler!\nStart typing here...")
            self.text_editor.is_focused = True
            self._initialized_content = True

    
    def handle_events(self, events):
        """
        Handle pygame events
        
        Args:
            events: List of pygame events
        """
        # If config view is active, let it handle events first
        if self.config_view:
            if self.config_view.handle_events(events):
                return True
            
            # Always return if config view is active to prevent interactions with main view
            return True
            
        for event in events:
            if event.type == pygame.QUIT:
                self.view_controller.quit()
            
            # Handle ESC key to exit fullscreen or 1920x1080
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Check if in fullscreen mode or in 1920x1080
                screen_width = pygame.display.get_surface().get_width()
                screen_height = pygame.display.get_surface().get_height()
                
                if (pygame.display.get_surface().get_flags() & pygame.FULLSCREEN) or (abs(screen_width - 1920) < 50 and abs(screen_height - 1080) < 50):
                    # Preservar el contenido actual del editor
                    current_text = ""
                    if hasattr(self, 'text_editor'):
                        current_text = self.text_editor.get_text()
                        cursor_line = self.text_editor.cursor_line
                        cursor_col = self.text_editor.cursor_col
                    
                    # Cambiar a ventana mediana
                    pygame.display.set_mode((1500, 900))
                    design.settings["window_size"] = "medium"
                    design.save_settings()
                    
                    # Recalcular interfaz
                    self.setup()
                    
                    # Restaurar el contenido del editor y la posición del cursor
                    if current_text:
                        self.text_editor.set_text(current_text)
                        self.text_editor.cursor_line = min(cursor_line, len(self.text_editor.lines) - 1)
                        self.text_editor.cursor_col = min(cursor_col, len(self.text_editor.lines[self.text_editor.cursor_line]))
                        self.text_editor.update_visual_cursor()
                    
                    return True
            
            # Reset cursor to IBEAM when over text editor area
            if event.type == pygame.MOUSEMOTION:
                if self.text_editor.text_rect.collidepoint(event.pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
            # Handle text editor events first (highest priority)
            if self.text_editor.handle_event(event):
                continue
            
            # Then check button events
            if self.save_button.handle_event(event):
                print("Save button clicked")
                
            if self.load_button.handle_event(event):
                print("Load button clicked")
            
            if self.configure_button.handle_event(event):
                self.open_config_view()
            
            if self.credits_button.handle_event(event):
                print("Credits button clicked")
            
            # Manejar botones de símbolos
            for i, button in enumerate(self.symbol_buttons):
                if button.handle_event(event):
                    symbol = ["(", ")", "{", "}", "[", "]"][i]
                    self.insert_symbol(symbol)
            if self.compile_button.handle_event(event):
                print("Compile button clicked")
                
            if self.grammar_button.handle_event(event):
                print("Grammar button clicked")
            
            if self.execute_button.handle_event(event):
                print("Execute button clicked")
                # Obtener y mostrar el texto del editor
                text_content = self.text_editor.get_text()
                print("Editor content:")
                print(text_content)
    
    def open_config_view(self):
        """Open the configuration view"""
        self.config_view = ConfigView(
            self,
            on_close=self.close_config_view,
            on_apply=self.apply_config_changes
        )

    def close_config_view(self):
        """Close the configuration view without applying changes"""
        self.config_view = None

    def apply_config_changes(self):
        """Apply configuration changes and close the view"""
        # Guardar el contenido actual del editor
        current_text = ""
        cursor_line = 0
        cursor_col = 0
        if hasattr(self, 'text_editor'):
            current_text = self.text_editor.get_text()
            cursor_line = self.text_editor.cursor_line
            cursor_col = self.text_editor.cursor_col
        
        # Get the selected window size from the settings
        window_size = design.get_window_size()  # Usar la variable global design
        current_size = (pygame.display.get_surface().get_width(), 
                    pygame.display.get_surface().get_height())
        current_flags = pygame.display.get_surface().get_flags()
        is_fullscreen = (current_flags & pygame.FULLSCREEN)
        
        # Handle window size changes
        need_resize = False
        
        # Check if we need to toggle fullscreen
        if isinstance(window_size, tuple) and len(window_size) == 3 and window_size[2] == pygame.FULLSCREEN:
            if not is_fullscreen:
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                need_resize = True
        else:
            # Check if we need to exit fullscreen
            if is_fullscreen:
                pygame.display.set_mode(window_size)
                need_resize = True
            # Check if we need to change window size
            elif isinstance(window_size, tuple) and len(window_size) == 2 and window_size != current_size:
                pygame.display.set_mode(window_size)
                need_resize = True
        
        # Forzar reinicialización de fuentes - CORREGIDO
        # No importar design localmente, usar la variable global
        # Reinicializar las fuentes mediante los métodos existentes
        design._initialized = False
        design.__init__()  # Reinicializar completamente
        
        # En lugar de intentar actualizar cada componente individualmente,
        # siempre reconstruimos la interfaz completa para asegurar consistencia
        # Reconstruir toda la interfaz
        self.setup()
        
        # Restaurar el contenido del editor y la posición del cursor
        if current_text:
            self.text_editor.set_text(current_text)
            self.text_editor.cursor_line = min(cursor_line, len(self.text_editor.lines) - 1)
            self.text_editor.cursor_col = min(cursor_col, len(self.text_editor.lines[self.text_editor.cursor_line]))
            self.text_editor.update_visual_cursor()
            self.text_editor.ensure_cursor_visible()
        
        # Si la ventana no cambió de tamaño pero otros aspectos sí, 
        # asegurarse de que el TextBox tenga las dimensiones correctas
        if not need_resize:
            screen_rect = self.screen.get_rect()
            button_margin = max(20, int(screen_rect.width * 0.02))
            button_height = 40
            bottom_y = screen_rect.height - button_height - button_margin
            editor_top = design.toolbar_height + 10
            editor_height = bottom_y - editor_top
            
            self.text_editor.resize(pygame.Rect(
                button_margin, editor_top,
                screen_rect.width - 2 * button_margin, editor_height
            ))
        
        # Close the config view
        self.config_view = None
        
    def update_ui_fonts(self):
        """Update font for all UI components"""
        # Update fonts for all buttons
        self.save_button.adjust_size()
        self.load_button.adjust_size()
        self.configure_button.adjust_size()
        self.credits_button.adjust_size()
        
        for button in self.symbol_buttons:
            button.adjust_size()
        
        self.compile_button.adjust_size()
        self.grammar_button.adjust_size()
        self.execute_button.adjust_size()
        
        # Update textbox font
        self.text_editor.update_font()
        
        # Recalcular posiciones para mantener el espaciado (especialmente el de 5px entre TextBox y botones)
        self.update_layout()
    
    def update(self, dt):
        """
        Update view logic
        
        Args:
            dt: Time elapsed since last update (delta time)
        """
        # Update config view if active
        if self.config_view:
            self.config_view.update(dt)
            
        # Update text editor
        self.text_editor.update()
    
    def render(self):
        """
        Render the view on screen
        """
        # Clear the screen with background color
        self.screen.fill(design.colors["background"])
        
        # Draw toolbar background - usar el ancho completo de la pantalla
        screen_width = self.screen.get_width()
        toolbar_rect = pygame.Rect(0, 0, screen_width, design.toolbar_height)
        pygame.draw.rect(self.screen, design.colors["toolbar"], toolbar_rect)
        
        # Draw all UI components
        self.save_button.render(self.screen)
        self.load_button.render(self.screen)
        self.configure_button.render(self.screen)
        self.credits_button.render(self.screen)
        # Render botones de símbolos
        for button in self.symbol_buttons:
            button.render(self.screen)
        self.compile_button.render(self.screen)
        self.grammar_button.render(self.screen)
        self.execute_button.render(self.screen)
        self.text_editor.render(self.screen)
        # Render config view on top if active
        if self.config_view:
            self.config_view.render()
    
    def insert_symbol(self, symbol):
        """
        Insert a symbol at the cursor position
        
        Args:
            symbol: Symbol to insert
        """
        # Asegurarse de que el textbox esté enfocado
        self.text_editor.is_focused = True
        
        # Si hay una selección activa, reemplazarla por el símbolo
        if self.text_editor.selection.is_active():
            self.text_editor.selection.delete_selected_text()
        
        # Insertar el símbolo en la posición del cursor
        line = self.text_editor.lines[self.text_editor.cursor_line]
        self.text_editor.lines[self.text_editor.cursor_line] = (
            line[:self.text_editor.cursor_col] + 
            symbol + 
            line[self.text_editor.cursor_col:]
        )
        
        # Avanzar el cursor más allá del símbolo insertado
        self.text_editor.cursor_col += len(symbol)
        
        # Actualizar las líneas envueltas
        self.text_editor.update_wrapped_lines()
        
        # Asegurarse de que el cursor sea visible
        self.text_editor.ensure_cursor_visible()
        
        # Reiniciar el parpadeo del cursor para que sea visible inmediatamente
        self.text_editor.cursor_blink = True
        self.text_editor.cursor_blink_time = pygame.time.get_ticks()
    
    def update_layout(self):
        # Obtener dimensiones actuales de la pantalla
        screen_rect = self.screen.get_rect()
        screen_width = screen_rect.width
        screen_height = screen_rect.height
        button_margin = max(20, int(screen_width * 0.02))
        button_height = 40
        button_width = max(120, int(screen_width * 0.12))
        bottom_y = screen_height - button_height - button_margin

        # Actualizar posición de los botones inferiores
        self.compile_button.rect.topleft = (button_margin, bottom_y)
        self.grammar_button.rect.topleft = (button_margin * 2 + button_width, bottom_y)
        self.execute_button.rect.topleft = (screen_width - button_width - button_margin, bottom_y)

        # Actualizar el área del TextBox: dejar un espacio vertical fijo de 5px
        editor_top = design.toolbar_height + 10
        editor_bottom = bottom_y - 5  # Aquí se deja el espacio de 5px
        editor_height = editor_bottom - editor_top
        self.text_editor.resize(pygame.Rect(
            button_margin, editor_top,
            screen_width - 2 * button_margin, editor_height
        ))