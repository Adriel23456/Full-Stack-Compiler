"""
Editor view for the Full Stack Compiler
"""
import pygame
from GUI.view_base import ViewBase
from GUI.design_base import design
from GUI.components.button import Button, ToolbarButton
from GUI.components.textbox import TextBox
from config import States, SCREEN_WIDTH, SCREEN_HEIGHT

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
    
    def setup(self):
        """
        Set up the editor view
        """
        # Calculate layout dimensions
        toolbar_height = design.toolbar_height
        button_height = 40
        button_width = 120
        button_margin = 20
        
        # Create toolbar buttons
        toolbar_button_width = 100
        toolbar_button_margin = 10
        toolbar_y = 5
        
        self.save_button = ToolbarButton(
            pygame.Rect(toolbar_button_margin, toolbar_y, toolbar_button_width, toolbar_height - 10),
            "Save"
        )
        
        self.load_button = ToolbarButton(
            pygame.Rect(toolbar_button_margin * 2 + toolbar_button_width, toolbar_y, 
                   toolbar_button_width, toolbar_height - 10),
            "Load"
        )
        
        self.configure_button = ToolbarButton(
            pygame.Rect(toolbar_button_margin * 3 + toolbar_button_width * 2, toolbar_y, 
                   toolbar_button_width, toolbar_height - 10),
            "Configure"
        )
        
        self.credits_button = ToolbarButton(
            pygame.Rect(toolbar_button_margin * 4 + toolbar_button_width * 3, toolbar_y, 
                   toolbar_button_width, toolbar_height - 10),
            "Credits"
        )
        
        # Crear botones de símbolos de paréntesis
        symbol_button_width = 40
        symbol_button_margin = 5
        symbol_start_x = SCREEN_WIDTH - (symbol_button_width * 6 + symbol_button_margin * 5) - toolbar_button_margin
        
        self.symbol_buttons = []
        symbols = ["(", ")", "{", "}", "[", "]"]
        
        for i, symbol in enumerate(symbols):
            x = symbol_start_x + i * (symbol_button_width + symbol_button_margin)
            self.symbol_buttons.append(
                ToolbarButton(
                    pygame.Rect(x, toolbar_y, symbol_button_width, toolbar_height - 10),
                    symbol
                )
            )
        
        # Create compile and execute buttons at the bottom
        bottom_y = SCREEN_HEIGHT - button_height - button_margin
        
        self.compile_button = Button(
            pygame.Rect(button_margin, bottom_y, button_width, button_height),
            "Compile"
        )
        
        self.grammar_button = Button(
            pygame.Rect(button_margin * 2 + button_width, bottom_y, button_width, button_height),
            "Grammar"
        )
        
        self.execute_button = Button(
            pygame.Rect(SCREEN_WIDTH - button_width - button_margin, bottom_y, 
                   button_width, button_height),
            "Execute"
        )
        
        # Create the main text editor area
        editor_top = toolbar_height + 10
        editor_bottom = bottom_y - 10
        editor_height = editor_bottom - editor_top
        
        self.text_editor = TextBox(
            pygame.Rect(button_margin, editor_top, 
                       SCREEN_WIDTH - 2 * button_margin, editor_height)
        )
        
        # Set initial content
        self.text_editor.set_text("Welcome to the Full Stack Compiler!\nStart typing here...")
        self.text_editor.is_focused = True
    
    def handle_events(self, events):
        """
        Handle pygame events
        
        Args:
            events: List of pygame events
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.view_controller.quit()
            
            # Handle text editor events first (highest priority)
            if self.text_editor.handle_event(event):
                continue
            
            # Then check button events
            if self.save_button.handle_event(event):
                print("Save button clicked")
                
            if self.load_button.handle_event(event):
                print("Load button clicked")
            
            if self.configure_button.handle_event(event):
                print("Configure button clicked")
            
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
    
    def update(self, dt):
        """
        Update view logic
        
        Args:
            dt: Time elapsed since last update (delta time)
        """
        # Update text editor
        self.text_editor.update()
    
    def render(self):
        """
        Render the view on screen
        """
        # Clear the screen with background color
        self.screen.fill(design.colors["background"])
        
        # Draw toolbar background
        toolbar_rect = pygame.Rect(0, 0, SCREEN_WIDTH, design.toolbar_height)
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