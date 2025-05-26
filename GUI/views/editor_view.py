from GUI.components.pop_up_dialog import PopupDialog
from GUI.components.execution_popup import ExecutionPopup 
from GUI.views.config_view import ConfigView
from GUI.views.credits_view import CreditsView
from GUI.view_base import ViewBase
from GUI.views.grammar_view import GrammarView
from GUI.models.fileExplorer import FileExplorer
from GUI.design_base import design
from GUI.components.button import Button, ToolbarButton
from GUI.components.textbox import TextBox
from GUI.models.execute_model import ExecuteModel
from CompilerLogic.lexicalAnalyzer import LexicalAnalyzer
from config import States
import pygame
import os

"""
Editor view for the Full Stack Compiler
"""
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
        self.credits_view = None
        self.grammar_view = None

        self.execute_model = ExecuteModel()
        
        # File tracking
        self.current_file_path = None
        self.file_status = "unsaved"  # Options: "unsaved", "saved", "modified"
        self.status_indicator_rect = None
    
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
            fixed_width=button_width,
            fixed_height=button_height     # Fija la altura
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
        
        # Create status indicator (centered between compile/grammar and execute buttons)
        status_indicator_size = 50
        self.status_indicator_rect = pygame.Rect(
            (self.grammar_button.rect.right + self.execute_button.rect.left - status_indicator_size) // 2,
            bottom_y + (button_height - status_indicator_size) // 2,
            status_indicator_size,
            status_indicator_size
        )

        # Set initial content if not already set
        if not hasattr(self, '_initialized_content'):
            self.text_editor.set_text("#Example of a comment\n(int) x1, y1, x2, y2, angle, depth;")
            self.text_editor.is_focused = True
            self._initialized_content = True

    
    def handle_events(self, events):
        """
        Handle pygame events
        
        Args:
            events: List of pygame events
        """
        # ───── Pop-up modal: absorbe todos los eventos ─────
        if hasattr(self, 'popup') and self.popup.active:
            self.popup.handle_events(events)   # siempre delega
            return True                        # y evita que lleguen al resto

        # If config view is active, let it handle events first
        if self.config_view:
            if self.config_view.handle_events(events):
                return True
            
            # Always return if config view is active to prevent interactions with main view
            return True
        
        # If credits view is active, let it handle events first
        if self.credits_view:
            if self.credits_view.handle_events(events):
                return True
            
            # Always return if credits view is active to prevent interactions with main view
            return True
        
        # If grammar view is active, let it handle events first
        if self.grammar_view:
            if self.grammar_view.handle_events(events):
                return True
            
            # Always return if grammar view is active to prevent interactions with main view
            return True
            
        for event in events:
            if event.type == pygame.QUIT:
                self.view_controller.quit()
            
            # Check for CTRL+S key combination
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                # If file is already saved/loaded, use that path, otherwise open dialog
                self.save_file(use_current_path=self.current_file_path is not None)
                return True
            
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
            
            # If text is edited, mark as modified
            if self.text_editor.handle_event(event):
                self.on_text_modified()
                continue
            
            # Then check button events
            if self.save_button.handle_event(event):
                self.save_file(use_current_path=self.current_file_path is not None)
                
            if self.load_button.handle_event(event):
                self.load_file()
            
            if self.configure_button.handle_event(event):
                self.open_config_view()
            
            if self.credits_button.handle_event(event):
                self.open_credits_view()
            
            # Manejar botones de símbolos
            for i, button in enumerate(self.symbol_buttons):
                if button.handle_event(event):
                    symbol = ["(", ")", "{", "}", "[", "]"][i]
                    self.insert_symbol(symbol)
            if self.compile_button.handle_event(event):
                # Run lexical analysis when compile button is pressed
                self.run_lexical_analysis()
                
            if self.grammar_button.handle_event(event):
                self.open_grammar_view()
            
            if self.execute_button.handle_event(event):
                # crear pop-up si no existe ya
                if not hasattr(self, 'popup') or not self.popup.active:
                    self.popup = ExecutionPopup(
                        self.screen,
                        self.execute_model,
                        on_close=lambda: None
                    )
    
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
        
        # Update credits view if active
        if self.credits_view:
            self.credits_view.update(dt)
            
        # Update grammar view if active
        if self.grammar_view:
            self.grammar_view.update(dt)
        
        # Update popup if active
        if hasattr(self, 'popup') and self.popup.active:
            self.popup.update()
            if not self.popup.active:
                delattr(self, 'popup')
            
        # Update text editor
        self.text_editor.update()
    
    def render(self):
        """
        Render the view on screen con protección contra errores
        """
        try:
            # Clear the screen with background color
            self.screen.fill(design.colors["background"])
            
            try:
                # Draw toolbar background - usar el ancho completo de la pantalla
                screen_width = self.screen.get_width()
                toolbar_rect = pygame.Rect(0, 0, screen_width, design.toolbar_height)
                pygame.draw.rect(self.screen, design.colors["toolbar"], toolbar_rect)
            except Exception as e:
                print(f"Error dibujando toolbar: {e}")
            
            # Draw all UI components con protección individual
            try:
                self.save_button.render(self.screen)
            except Exception as e:
                print(f"Error dibujando save_button: {e}")
                
            try:
                self.load_button.render(self.screen)
            except Exception as e:
                print(f"Error dibujando load_button: {e}")
                
            try:
                self.configure_button.render(self.screen)
            except Exception as e:
                print(f"Error dibujando configure_button: {e}")
                
            try:
                self.credits_button.render(self.screen)
            except Exception as e:
                print(f"Error dibujando credits_button: {e}")
            
            # Render botones de símbolos con protección
            try:
                for button in self.symbol_buttons:
                    try:
                        button.render(self.screen)
                    except Exception as e:
                        print(f"Error dibujando symbol_button: {e}")
            except Exception as e:
                print(f"Error accediendo a symbol_buttons: {e}")
                
            try:
                self.compile_button.render(self.screen)
            except Exception as e:
                print(f"Error dibujando compile_button: {e}")
                
            try:
                self.grammar_button.render(self.screen)
            except Exception as e:
                print(f"Error dibujando grammar_button: {e}")
                
            try:
                self.execute_button.render(self.screen)
            except Exception as e:
                print(f"Error dibujando execute_button: {e}")
            
            # Protección especial para el editor de texto (donde probablemente está el error)
            try:
                if hasattr(self, 'text_editor'):
                    self.text_editor.render(self.screen)
            except IndexError as e:
                print(f"Error de índice en text_editor.render(): {e}")
                # Intentar reiniciar el editor a un estado seguro
                try:
                    self.text_editor.lines = ["Error al renderizar. Editor reiniciado."]
                    self.text_editor.cursor_line = 0
                    self.text_editor.cursor_col = 0
                    self.text_editor.scroll_y = 0
                    self.text_editor.update_wrapped_lines()
                    # Intentar renderizar nuevamente con el estado reiniciado
                    self.text_editor.render(self.screen)
                except Exception as e2:
                    print(f"Error al intentar recuperar editor: {e2}")
            except Exception as e:
                print(f"Error general en text_editor.render(): {e}")
            
            # Draw status indicator
            try:
                if hasattr(self, "status_indicator_rect") and self.status_indicator_rect:
                    # Choose color based on file status
                    if self.file_status == "unsaved":
                        indicator_color = (255, 0, 0)  # Red
                    elif self.file_status == "saved":
                        indicator_color = (0, 255, 0)  # Green
                    elif self.file_status == "modified":
                        indicator_color = (255, 255, 0)  # Yellow
                    
                    # Draw the indicator
                    pygame.draw.rect(self.screen, indicator_color, self.status_indicator_rect, 0, 10)
                    pygame.draw.rect(self.screen, (0, 0, 0), self.status_indicator_rect, 2, 10)
            except Exception as e:
                print(f"Error dibujando status indicator: {e}")
            
            # Render config view on top if active
            try:
                if self.config_view:
                    self.config_view.render()
            except Exception as e:
                print(f"Error en config_view.render(): {e}")
                self.config_view = None
            
            # Render credits view on top if active
            try:
                if self.credits_view:
                    self.credits_view.render()
            except Exception as e:
                print(f"Error en credits_view.render(): {e}")
                self.credits_view = None
                
            # Render grammar view on top if active
            try:
                if self.grammar_view:
                    self.grammar_view.render()
            except Exception as e:
                print(f"Error en grammar_view.render(): {e}")
                self.grammar_view = None
            
            # Render grammar view on top if active
            try:
                if hasattr(self, 'popup') and self.popup.active:
                    self.popup.update()
                    self.popup.render()
            except Exception as e:
                print(f"Error en popUp.render(): {e}")
        
        except Exception as e:
            print(f"Error crítico en render: {e}")
    
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
        
        self.on_text_modified()
    
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
    
    def open_credits_view(self):
        """Open the credits view"""
        self.credits_view = CreditsView(
            self,
            on_close=self.close_credits_view
        )

    def close_credits_view(self):
        """Close the credits view"""
        self.credits_view = None
    
    def save_file(self, use_current_path=False):
        """
        Save file to disk using a separate thread
        Args:
            use_current_path: If True, use the current file path (if available)
        """
        # Si usamos path actual y tenemos uno, guardamos directamente
        if use_current_path and self.current_file_path:
            try:
                # Get text content
                text_content = self.text_editor.get_text()
                # Write to file
                with open(self.current_file_path, 'w', encoding='utf-8') as file:
                    file.write(text_content)
                self.set_file_status("saved")
                return True
            except Exception as e:
                print(f"Error saving file: {e}")
                return False
        
        # Determine initial directory
        current_dir = os.getcwd()
        
        # Define el callback para procesar el resultado del diálogo
        def save_callback(file_path):
            if file_path:
                try:
                    # Get text content
                    text_content = self.text_editor.get_text()
                    # Write to file
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(text_content)
                    # Store the file path
                    self.current_file_path = file_path
                    self.set_file_status("saved")
                except Exception as e:
                    print(f"Error saving file: {e}")
        
        # Inicia el diálogo en un hilo separado
        # Nota: esta llamada no es bloqueante y devolverá inmediatamente
        FileExplorer.save_file_dialog(initial_dir=current_dir, callback=save_callback)
        return True

    def load_file(self):
        """
        Versión ultra-robusta para cargar archivos que previene errores de índice
        """
        # Obtener el directorio de ejemplos
        examples_dir = os.path.join(os.getcwd(), "Examples")
        # Crear el directorio si no existe
        if not os.path.exists(examples_dir):
            os.makedirs(examples_dir)
        
        # Definir una función completamente protegida para procesar el resultado
        def safe_load_callback(file_path):
            if not file_path:
                return
                
            # Guardar la información global del programa que necesitaremos restaurar
            try:
                # Crear una copia de seguridad del estado actual
                backup_status = self.file_status
                backup_path = self.current_file_path
                
                # Intentar leer el archivo seleccionado
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        text_content = file.read()
                except Exception as e:
                    print(f"Error al leer el archivo: {e}")
                    return
                    
                # Verificar que tenemos el objeto text_editor disponible
                if not hasattr(self, 'text_editor'):
                    print("Error: El editor de texto no está inicializado")
                    return
                    
                # Iniciar un bloque protegido para establecer el contenido
                try:
                    # Método más seguro: reconstruir el editor con el nuevo texto
                    # 1. Guarda la posición original de desplazamiento
                    original_scroll_y = 0
                    if hasattr(self.text_editor, 'scroll_y'):
                        original_scroll_y = self.text_editor.scroll_y
                    
                    # 2. Establecer el texto de manera segura
                    # Este método debe estar definido en TextBox para simplemente 
                    # asignar líneas sin procesar wrapping o actualizar visualmente
                    self.text_editor.lines = text_content.split('\n')
                    if not self.text_editor.lines:
                        self.text_editor.lines = [""]
                    
                    # 3. Resetear el cursor a una posición segura
                    self.text_editor.cursor_line = 0
                    self.text_editor.cursor_col = 0
                    
                    # 4. Forzar una actualización completa de las líneas envueltas
                    # Si esto falla, intentar un enfoque aún más simple
                    try:
                        self.text_editor.update_wrapped_lines()
                    except Exception as e:
                        print(f"Error al actualizar líneas: {e}")
                        # Reinicio de emergencia
                        self.text_editor.lines = [""]
                        self.text_editor.update_wrapped_lines()
                    
                    # 5. Restaurar el desplazamiento (o establecer a 0 si hay problema)
                    try:
                        if original_scroll_y > 0:
                            self.text_editor.scroll_y = min(original_scroll_y, 
                                                max(0, len(self.text_editor.wrapped_lines) - self.text_editor.visible_lines))
                        self.text_editor.calculate_scrollbar()
                    except Exception:
                        self.text_editor.scroll_y = 0
                        self.text_editor.calculate_scrollbar()
                    
                    # Actualizar la información del archivo
                    self.current_file_path = file_path
                    self.set_file_status("saved")
                    
                except Exception as e:
                    # Si algo falla, reiniciar a un estado conocido y seguro
                    print(f"Error al actualizar editor con archivo: {e}")
                    
                    # Restaurar el estado anterior
                    self.file_status = backup_status
                    self.current_file_path = backup_path
                    
                    # Establecer un contenido seguro
                    try:
                        self.text_editor.lines = ["Error al cargar el archivo."]
                        self.text_editor.cursor_line = 0
                        self.text_editor.cursor_col = 0
                        self.text_editor.update_wrapped_lines()
                    except Exception:
                        # Si incluso esto falla, vamos a un estado aún más básico
                        print("Error crítico - reiniciando editor")
                        # No hacemos nada más - dejar que la aplicación siga ejecutándose
            
            except Exception as e:
                # Captura de último recurso - para no caerse nunca
                print(f"Error inesperado: {e}")
        
        # Iniciar el diálogo de archivo en un hilo separado
        # Usar try/except para capturar cualquier error en la creación del hilo
        try:
            FileExplorer.open_file_dialog(initial_dir=examples_dir, callback=safe_load_callback)
            return True
        except Exception as e:
            print(f"Error al mostrar diálogo de archivo: {e}")
            return False
    
    def set_file_status(self, status):
        """
        Set the file status
        
        Args:
            status: Status to set ("unsaved", "saved", "modified")
        """
        self.file_status = status
    
    def on_text_modified(self):
        """Handle when text is modified"""
        if hasattr(self, "file_status") and self.file_status == "saved":
            self.set_file_status("modified")
    
    def open_grammar_view(self):
        """Open the grammar view"""
        self.grammar_view = GrammarView(
            self,
            on_close=self.close_grammar_view
        )

    def close_grammar_view(self):
        """Close the grammar view"""
        self.grammar_view = None
    
    def run_lexical_analysis(self):
        """
        Run lexical analysis on the current editor text
        First saves the file if modified, then runs analysis
        """
        # Auto-save if file is modified and has a path
        if self.file_status == "modified" and self.current_file_path:
            self.save_file(use_current_path=True)
        # If file is unsaved or hasn't been saved yet, prompt user to save
        elif (self.file_status == "unsaved" or self.file_status == "modified") and not self.current_file_path:
            # Save to a default location in Examples if needed
            self.popup = PopupDialog(self.screen, "Please save before compiling")
            return True
            
        # Continue with the actual analysis
        self.run_lexical_analysis_internal()

    def run_lexical_analysis_internal(self):
        """
        Internal method to run lexical analysis after any needed saving
        """
        # Get the current text
        code_text = self.text_editor.get_text()
        
        # Initialize lexical analyzer
        analyzer = LexicalAnalyzer()
        
        try:
            # Mark this view instance for the view controller to use
            self.view_controller.editor_view_instance = self
            
            # Run analysis 
            success, errors, token_graph_path = analyzer.analyze(code_text)
            
            # Clear any existing highlights first
            if hasattr(self.text_editor, 'clear_error_highlights'):
                self.text_editor.clear_error_highlights()
                
            if success and not errors:
                # If analysis succeeded with no errors, change to lexical analysis view
                self.view_controller.token_graph_path = token_graph_path
                self.view_controller.change_state(States.LEXICAL_ANALYSIS)
            else:
                # If there were errors, stay in editor view and highlight errors
                if errors and hasattr(self.text_editor, 'highlight_errors'):
                    # Make sure line numbers are valid
                    for error in errors:
                        if error.get('line', 1) < 1:
                            error['line'] = 1
                    
                    # Highlight errors in editor
                    self.text_editor.highlight_errors(errors)
                
                # Display a message about the errors
                print(f"Lexical analysis found {len(errors)} errors:")
                for error in errors:
                    print(f"  Line {error.get('line')}, Column {error.get('column')}: {error.get('message')}")
        except Exception as e:
            print(f"Error running lexical analysis: {e}")
            import traceback
            traceback.print_exc()