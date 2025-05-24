# File: GUI/views/code_generator_view.py
import os
import pygame
from GUI.components.pop_up_dialog import PopupDialog
from GUI.view_base import ViewBase
from GUI.components.button import Button
from GUI.design_base import design
from config import States, BASE_DIR


class CodeGeneratorView(ViewBase):
    """
    Muestra el contenido textual de out/vGraph.asm con scroll y formato mejorado.
    """
    NOT_FOUND_MSG = ["ASM file not found - compile first."]

    # ────────────────────────────────────────────────────────────
    def __init__(self, view_controller):
        super().__init__(view_controller)

        # Resuelve la ruta al .asm
        self.asm_path: str | None = self._find_asm_path()

        # Carga las líneas
        self.lines: list[str] = self._load_asm_lines()

        # Estado de scroll
        self.scroll_y = 0
        self.max_scroll = 0
        self.scroll_speed = 30

        # Scroll-bar
        self.scrollbar_rect = None
        self.thumb_rect = None
        self.scrollbar_dragging = False
        self.drag_offset = 0

        # Colores para sintaxis
        self.syntax_colors = {
            'comment':     (100, 150, 100),   # Verde oscuro para comentarios
            'directive':   (150, 50, 150),    # Púrpura para directivas
            'label':       (200, 100, 0),     # Naranja para etiquetas
            'instruction': (50, 50, 200),     # Azul para instrucciones
            'register':    (200, 50, 50),     # Rojo para registros
            'number':      (0, 150, 150),     # Cian para números
            'string':      (150, 100, 50),    # Marrón para cadenas
            'default':     (0, 0, 0)          # Negro por defecto
        }

        # Conjunto de instrucciones x86-64 comunes
        self.instructions = {
            'mov', 'movl', 'movq', 'movb', 'movw', 'movabs', 'movabsq',
            'push', 'pushq', 'pushl', 'pop', 'popq', 'popl',
            'add', 'addl', 'addq', 'sub', 'subl', 'subq',
            'mul', 'imul', 'div', 'idiv',
            'and', 'or', 'xor', 'not', 'neg',
            'shl', 'shr', 'sal', 'sar',
            'cmp', 'test',
            'jmp', 'je', 'jne', 'jl', 'jg', 'jle', 'jge', 'jz', 'jnz',
            'call', 'ret', 'leave',
            'lea', 'leal', 'leaq',
            'int', 'syscall',
            'nop', 'hlt'
        }

        # Conjunto de registros x86-64
        self.registers = {
            # 64-bit
            '%rax', '%rbx', '%rcx', '%rdx', '%rsi', '%rdi', '%rbp', '%rsp',
            '%r8', '%r9', '%r10', '%r11', '%r12', '%r13', '%r14', '%r15',
            '%rip',
            # 32-bit
            '%eax', '%ebx', '%ecx', '%edx', '%esi', '%edi', '%ebp', '%esp',
            # 16-bit
            '%ax', '%bx', '%cx', '%dx', '%si', '%di', '%bp', '%sp',
            # 8-bit
            '%al', '%ah', '%bl', '%bh', '%cl', '%ch', '%dl', '%dh',
            # Segment registers
            '%cs', '%ds', '%es', '%fs', '%gs', '%ss'
        }

    # ────────────────────────────────────────────────────────────
    def _find_asm_path(self) -> str | None:
        default = os.path.join(BASE_DIR, "out", "vGraph.asm")
        return default if os.path.exists(default) else None

    # ────────────────────────────────────────────────────────────
    def _load_asm_lines(self) -> list[str]:
        """
        Lee el fichero ASM y devuelve **todas** las líneas, incluida la última
        vacía cuando el archivo termina en '\n'. Además convierte TABs → espacios.
        """
        if not self.asm_path:
            return self.NOT_FOUND_MSG
        try:
            with open(self.asm_path, "r", encoding="utf-8") as fh:
                TAB_SIZE = 4
                raw_text = fh.read()
                if raw_text == "":
                    return ["(empty file)"]

                # split('\n') conserva la línea vacía final (si existe)
                lines = raw_text.split('\n')
                return [ln.expandtabs(TAB_SIZE) for ln in lines]
        except Exception as exc:
            return [f"Error reading ASM: {exc}"]

    # ────────────────────────────────────────────────────────────
    def setup(self):
        """Recalcula layout y vuelve a cargar el fichero por si cambió."""
        # (re)cargar líneas
        self.asm_path = self._find_asm_path()
        self.lines = self._load_asm_lines()

        # Layout dinámico
        scr = self.screen.get_rect()
        button_w, button_h, margin = 150, 40, 20

        # Botón Back
        self.back_btn = Button(
            pygame.Rect(scr.right - button_w - margin,
                        scr.bottom - button_h - margin,
                        button_w, button_h),
            "Back To Home",
            fixed_width=button_w,
            fixed_height=button_h
        )

        # Área de texto con margen para números de línea
        top = 60
        self.line_number_width = 60  # Ancho del margen para números
        self.text_rect = pygame.Rect(
            margin, top,
            scr.width - margin * 2,
            scr.height - top - button_h - margin * 2
        )

        # Área específica para el código (sin incluir números de línea)
        self.code_rect = pygame.Rect(
            self.text_rect.x + self.line_number_width,
            self.text_rect.y,
            self.text_rect.width - self.line_number_width - 15,  # 15 px para scrollbar
            self.text_rect.height
        )

        # Fuente monoespaciada más GRANDE
        self.code_font = pygame.font.Font(
            pygame.font.match_font("monospace"), 16  # 12 → 16 pt
        )
        self.line_height = self.code_font.get_linesize()

        # Scroll máximo
        self.max_scroll = max(
            0, len(self.lines) * self.line_height - self.text_rect.height
        )

    # ────────────────────────────────────────────────────────────
    def get_line_color(self, line: str) -> tuple[int, int, int]:
        """Determina el color de una línea según su contenido."""
        line = line.strip()

        if line.startswith('#'):              # Comentario
            return self.syntax_colors['comment']
        if line.startswith('.'):              # Directiva
            return self.syntax_colors['directive']
        if line.endswith(':'):               # Etiqueta
            return self.syntax_colors['label']

        first_word = line.split()[0] if line.split() else ''
        if first_word.lower() in self.instructions:  # Instrucción
            return self.syntax_colors['instruction']

        return self.syntax_colors['default']

    # ────────────────────────────────────────────────────────────
    def render_line_with_syntax(self, surface, line: str, x: int, y: int):
        """Dibuja una línea con resaltado de sintaxis y mantiene sangría."""
        if not line:      # Línea vacía
            return

        base_color = self.get_line_color(line)

        # ---------------------------   Mantener indentación   ------------------
        space_w = self.code_font.size(' ')[0]
        indent_spaces = len(line) - len(line.lstrip(' '))
        current_x = x + indent_spaces * space_w
        stripped = line.lstrip()

        # Si la línea entera es un comentario/directiva/etiqueta, dibujar de golpe
        if stripped.startswith('#') or stripped.startswith('.') or stripped.endswith(':'):
            text_surf = self.code_font.render(stripped, True, base_color)
            surface.blit(text_surf, (current_x, y))
            return

        # ----------------------------------------------------------------------
        #       Tokenización y coloreado de instrucciones / registros / números
        # ----------------------------------------------------------------------
        parts = stripped.split()
        for i, part in enumerate(parts):
            if i == 0 and part.lower() in self.instructions:
                color = self.syntax_colors['instruction']
            elif part in self.registers:
                color = self.syntax_colors['register']
            elif part.startswith('$') or part.startswith('0x') or part.replace('-', '').isdigit():
                color = self.syntax_colors['number']
            elif part.startswith('"') or part.startswith("'"):
                color = self.syntax_colors['string']
            else:
                color = base_color

            token_surf = self.code_font.render(part + ' ', True, color)
            surface.blit(token_surf, (current_x, y))
            current_x += token_surf.get_width()

    # ────────────────────────────────────────────────────────────
    def handle_events(self, events):
        for ev in events:
            if ev.type == pygame.QUIT:
                self.view_controller.quit()

            if self.back_btn.handle_event(ev):
                self.view_controller.change_state(States.EDITOR)

            # Rueda del mouse
            if ev.type == pygame.MOUSEWHEEL:
                if self.text_rect.collidepoint(pygame.mouse.get_pos()):
                    self.scroll_y = max(
                        0,
                        min(self.max_scroll, self.scroll_y - ev.y * self.scroll_speed)
                    )

            # Drag sobre el thumb de la scrollbar
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if self.thumb_rect and self.thumb_rect.collidepoint(ev.pos):
                    self.scrollbar_dragging = True
                    self.drag_offset = ev.pos[1] - self.thumb_rect.y

            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.scrollbar_dragging = False

            if ev.type == pygame.MOUSEMOTION and self.scrollbar_dragging:
                new_y = ev.pos[1] - self.drag_offset
                track_h = self.scrollbar_rect.height - self.thumb_rect.height
                ratio = max(0, min(1, (new_y - self.scrollbar_rect.y) / track_h))
                self.scroll_y = int(ratio * self.max_scroll)

    # ────────────────────────────────────────────────────────────
    def update(self, dt):
        pass  # Lógica de actualización no requerida por ahora

    # ────────────────────────────────────────────────────────────
    def _draw_scrollbar(self):
        """Dibuja la barra de scroll y su «thumb»."""
        bar_w = 10
        self.scrollbar_rect = pygame.Rect(
            self.text_rect.right - bar_w,
            self.text_rect.top,
            bar_w,
            self.text_rect.height
        )
        pygame.draw.rect(self.screen, design.colors["button"], self.scrollbar_rect)

        if self.max_scroll == 0:
            return  # No se necesita thumb

        # Tamaño y posición del thumb
        ratio_visible = self.text_rect.height / (self.text_rect.height + self.max_scroll)
        thumb_h = max(20, int(self.scrollbar_rect.height * ratio_visible))
        track_h = self.scrollbar_rect.height - thumb_h
        thumb_y = self.scrollbar_rect.y + int(track_h * (self.scroll_y / self.max_scroll))

        self.thumb_rect = pygame.Rect(self.scrollbar_rect.x, thumb_y, bar_w, thumb_h)
        pygame.draw.rect(self.screen, design.colors["button_hover"], self.thumb_rect, 0, 3)

    # ────────────────────────────────────────────────────────────
    def render(self):
        self.screen.fill(design.colors["background"])

        # Título
        title_surf = design.get_font("large").render(
            "Code Generator View (x86-64 ~ GNU Assembler)",
            True, design.colors["text"]
        )
        self.screen.blit(
            title_surf,
            title_surf.get_rect(midtop=(self.screen_rect.centerx, 15))
        )

        # Marco del área de texto
        pygame.draw.rect(self.screen, (255, 255, 255), self.text_rect)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.text_rect, 1)

        # Superficie recortada para dibujar solo dentro del área
        text_surface = self.screen.subsurface(self.text_rect)
        text_surface.fill((255, 255, 255))

        # Fondo gris claro para los números de línea
        line_num_rect = pygame.Rect(0, 0, self.line_number_width - 5, self.text_rect.height)
        pygame.draw.rect(text_surface, (240, 240, 240), line_num_rect)
        pygame.draw.line(
            text_surface, (200, 200, 200),
            (self.line_number_width - 5, 0),
            (self.line_number_width - 5, self.text_rect.height)
        )

        # Líneas visibles
        start_line = int(self.scroll_y / self.line_height)
        end_line = min(len(self.lines),
                       start_line + int(self.text_rect.height / self.line_height) + 2)

        y = -self.scroll_y % self.line_height
        for i in range(start_line, end_line):
            if 0 <= i < len(self.lines):
                # Número de línea
                ln_text = self.code_font.render(f"{i + 1:4d}", True, (100, 100, 100))
                text_surface.blit(ln_text, (5, y))

                # Código con sintaxis resaltada
                self.render_line_with_syntax(
                    text_surface,
                    self.lines[i],
                    self.line_number_width,
                    y
                )
            y += self.line_height

        # Scroll-bar
        if self.max_scroll > 0:
            self._draw_scrollbar()

        # Botón «Back»
        self.back_btn.render(self.screen)

        # Pop-up (si existe)
        if hasattr(self, "popup") and self.popup:
            if self.popup.render():   # True → cerrar popup
                self.popup = None