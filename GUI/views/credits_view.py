import pygame
from GUI.design_base import design
from GUI.components.button import Button

class CreditsView:
    """
    Modal credits view that overlays on top of the main application
    """
    def __init__(self, parent_view, on_close=None):
        """
        Initialize the credits view
        
        Args:
            parent_view: Parent view that opened this credits view
            on_close: Callback function when credits is closed
        """
        self.parent_view = parent_view
        self.screen = pygame.display.get_surface()
        self.on_close = on_close
        
        # Scrollbar dragging state
        self.scrollbar_dragging = False
        self.scrollbar_rect = None
        self.thumb_rect = None
        self.drag_offset_y = 0
        
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
        
        # Text content - properly formatted in English
        self.text_content = """
Author: Adriel S. Chaves Salazar

Synopsis:
__________
This program helps to understand the integration of a Full Stack Compiler section by section, where the following steps of compiler programming will be integrated:
1. Lexical Analysis
2. Syntactic Analysis
3. Semantic Analysis
4. Optimization
5. Instruction Selection
6. Register Assignment
7. Programming / Instructions

Additionally, the possibility to choose between a CISC or RISC assembly code language, with RISC-V and x86, will be established.

As a final feature, the program has functionality to visualize the execution of the assembly program in real-time and analyze the computer's movement when executing the program that was provided in high-level language.

State of the Art:
________________
A compiler is a program that takes source code written in a high-level programming language as input and generates an equivalent program in machine code as a result. This translation process is performed once, and the resulting program can be executed multiple times without needing to recompile, offering greater efficiency in execution time.

The compilation stages are divided into several steps:
The process is traditionally divided into three major phases: Front-end, Middle-end, and Back-end. The Front-end handles the analysis of the source code, the Middle-end performs platform-independent optimizations, and the Back-end generates the machine code specific to the target architecture.

Lexical analysis, also known as scanning or tokenization, is the first stage in both compilers and interpreters. This phase is responsible for reading the source code as a sequence of characters and grouping them into meaningful lexical units called tokens.

Syntactic analysis, also known as parsing, is the second stage of the process and is responsible for determining if the token sequence generated in the previous stage complies with the grammatical rules of the language. The component responsible for this task is the parser or syntactic analyzer, which uses a context-free grammar to define the formation rules for expressions, declarations, blocks, and other language structures.

The result of syntactic analysis is a concrete syntax tree (Parse Tree), which represents the hierarchical structure of the program according to the grammatical rules of the language. This tree shows how each component of the program (expressions, declarations, blocks, etc.) relates to others following the grammar rules.

Semantic analysis constitutes the third stage of the process and is responsible for determining the meaning of syntactically correct constructions in the program.

During this stage, it verifies that operations are performed with compatible types, that variables are declared before use, that identifiers are used consistently with their declaration, among other semantic checks.

A fundamental component of semantic analysis is the symbol table, a data structure that stores information about the identifiers (variables, functions, types, etc.) declared in the program, including their type, scope, and other relevant attributes.

The result of semantic analysis is an abstract syntax tree (AST), which represents the essential structure of the program, eliminating unnecessary syntactic details and preparing the information for the following stages of the process.

It is worth noting that there are different methods to implement semantic verification, which gives rise to the classification of different types of compilers: single-pass compilers and two or more pass compilers. Figure 7 shows a reduced representation of both compilers.

Single-pass compilers: These compilers directly connect the code generation phase with semantic analysis. Single-pass compilers are faster than two or more pass compilers, but are known to be more difficult to design and build.

Two or more pass compilers: In this approach, the semantic analyzer generates abstract or intermediate code. The intermediate representation serves as a bridge for final code generation. This intermediate representation is important as it facilitates code optimization, generating efficient programs.

The symbol table is a data structure that contains information about an identifier during the compilation process. The main objective of the symbol table is to collect complete information about all identifiers that appear in the source program text. This entity exists during compilation and is destroyed when the source code is translated to assembly code.

The standard attributes preserved for each identifier include:
- Identifier specification: what type of element it is (variable, function, procedure, etc.).
- Type: identifies the data type of the identifier (integer, real, boolean, etc.).
- Dimension or size: indicates how much memory this identifier consumes, especially important for arrays or data structures.
- Starting address for generating object code: specifies the memory address where the identifier is located.
- Additional information lists: includes very specific information about the identifier or the programming language.

It should be mentioned that the attributes of the symbol table can vary considerably, depending on the compiled programming language, its specific characteristics, and the development methodology used to build the translator.
"""
        
        # Scrolling variables
        self.scroll_y = 0
        self.max_scroll_y = 0
        self.scroll_speed = 20
        
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
        # Reset cursor to arrow when credits view is active
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

    def render(self):
        """Render the credits view"""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Draw credits window background
        pygame.draw.rect(self.screen, design.colors["background"], self.rect, 0, 10)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.rect, 2, 10)
        
        # Draw title
        title_font = design.get_font("large")
        title_text = title_font.render("Credits", True, design.colors["text"])
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