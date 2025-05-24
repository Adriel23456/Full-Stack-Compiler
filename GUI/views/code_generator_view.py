# File: GUI/views/code_generator_view.py
import os
import pygame
from GUI.components.pop_up_dialog import PopupDialog
from GUI.view_base import ViewBase
from GUI.components.button import Button
from GUI.design_base import design
from GUI.views.report_view import ReportView
from config import States, BASE_DIR


class CodeGeneratorView(ViewBase):
    """
    Muestra el contenido textual de out/vGraph.asm con scroll, resaltado de
    sintaxis y números de línea. Incluye un botón «Open Details» que abre
    un reporte modal con assets/assembly_report.txt.
    """

    NOT_FOUND_MSG = ["ASM file not found - compile first."]

    # ────────────────────────────────────────────────────────────
    def __init__(self, view_controller):
        super().__init__(view_controller)

        # Ruta al ASM
        self.asm_path: str | None = self._find_asm_path()
        self.lines: list[str] = self._load_asm_lines()

        # Scroll
        self.scroll_y = 0
        self.max_scroll = 0
        self.scroll_speed = 30
        self.scrollbar_rect = None
        self.thumb_rect = None
        self.scrollbar_dragging = False
        self.drag_offset = 0

        # Modals / popups
        self.report_view = None
        self.popup = None

        # Colores para sintaxis
        self.syntax_colors = {
            'comment':     (100, 150, 100),
            'directive':   (150, 50, 150),
            'label':       (200, 100, 0),
            'instruction': (50, 50, 200),
            'register':    (200, 50, 50),
            'number':      (0, 150, 150),
            'string':      (150, 100, 50),
            'default':     (0, 0, 0)
        }

        # Instrucciones x86-64 más comunes
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

        # Registros x86-64
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
            # Segment
            '%cs', '%ds', '%es', '%fs', '%gs', '%ss'
        }

    # ────────────────────────────────────────────────────────────
    def _find_asm_path(self) -> str | None:
        default = os.path.join(BASE_DIR, "out", "vGraph.asm")
        return default if os.path.exists(default) else None

    # ────────────────────────────────────────────────────────────
    def _load_asm_lines(self) -> list[str]:
        if not self.asm_path:
            return self.NOT_FOUND_MSG
        try:
            TAB_SIZE = 4
            with open(self.asm_path, "r", encoding="utf-8") as fh:
                raw = fh.read()
                if raw == "":
                    return ["(empty file)"]
                return [ln.expandtabs(TAB_SIZE) for ln in raw.split('\n')]
        except Exception as exc:
            return [f"Error reading ASM: {exc}"]

    # ────────────────────────────────────────────────────────────
    def setup(self):
        self.asm_path = self._find_asm_path()
        self.lines = self._load_asm_lines()

        scr = self.screen.get_rect()
        button_w, button_h, margin = 150, 40, 20

        # Botón Back (derecha)
        self.back_btn = Button(
            pygame.Rect(scr.right - button_w - margin,
                        scr.bottom - button_h - margin,
                        button_w, button_h),
            "Back To Home",
            fixed_width=button_w,
            fixed_height=button_h
        )
        # Botón Open Details (centro)
        center_x = (scr.width - button_w) // 2
        self.details_btn = Button(
            pygame.Rect(center_x,
                        scr.bottom - button_h - margin,
                        button_w, button_h),
            "Open Details",
            fixed_width=button_w,
            fixed_height=button_h
        )

        # Área de texto
        top = 60
        self.line_number_width = 60
        self.text_rect = pygame.Rect(
            margin, top,
            scr.width - margin * 2,
            scr.height - top - button_h - margin * 2
        )
        self.code_rect = pygame.Rect(
            self.text_rect.x + self.line_number_width,
            self.text_rect.y,
            self.text_rect.width - self.line_number_width - 15,
            self.text_rect.height
        )

        self.code_font = pygame.font.Font(
            pygame.font.match_font("monospace"), 16)
        self.line_height = self.code_font.get_linesize()

        self.max_scroll = max(
            0, len(self.lines) * self.line_height - self.text_rect.height
        )

    # ────────────────────────────────────────────────────────────
    def get_line_color(self, line: str) -> tuple[int, int, int]:
        line = line.strip()
        if line.startswith('#'):
            return self.syntax_colors['comment']
        if line.startswith('.'):
            return self.syntax_colors['directive']
        if line.endswith(':'):
            return self.syntax_colors['label']
        first_word = line.split()[0] if line.split() else ''
        if first_word.lower() in self.instructions:
            return self.syntax_colors['instruction']
        return self.syntax_colors['default']

    # ────────────────────────────────────────────────────────────
    def render_line_with_syntax(self, surface, line: str, x: int, y: int):
        if line == "":
            return
        base_color = self.get_line_color(line)

        space_w = self.code_font.size(' ')[0]
        indent_spaces = len(line) - len(line.lstrip(' '))
        current_x = x + indent_spaces * space_w
        stripped = line.lstrip()

        if stripped.startswith('#') or stripped.startswith('.') or stripped.endswith(':'):
            surf = self.code_font.render(stripped, True, base_color)
            surface.blit(surf, (current_x, y))
            return

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
            tok = self.code_font.render(part + ' ', True, color)
            surface.blit(tok, (current_x, y))
            current_x += tok.get_width()

    # ────────────────────────────────────────────────────────────
    def handle_events(self, events):
        # Modal activo → captura primero
        if self.report_view:
            self.report_view.handle_events(events)
            return True

        for ev in events:
            if ev.type == pygame.QUIT:
                self.view_controller.quit()

            if self.back_btn.handle_event(ev):
                self.view_controller.change_state(States.EDITOR)

            if self.details_btn.handle_event(ev):
                report_path = os.path.join(BASE_DIR, "assets",
                                           "assembly_report.txt")
                self.report_view = ReportView(
                    self, report_path=report_path,
                    on_close=self._close_report_view
                )
                return True

            # Scroll rueda
            if ev.type == pygame.MOUSEWHEEL:
                if self.text_rect.collidepoint(pygame.mouse.get_pos()):
                    self.scroll_y = max(
                        0,
                        min(self.max_scroll,
                            self.scroll_y - ev.y * self.scroll_speed)
                    )

            # Drag scrollbar
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if self.thumb_rect and self.thumb_rect.collidepoint(ev.pos):
                    self.scrollbar_dragging = True
                    self.drag_offset = ev.pos[1] - self.thumb_rect.y
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.scrollbar_dragging = False
            if ev.type == pygame.MOUSEMOTION and self.scrollbar_dragging:
                new_y = ev.pos[1] - self.drag_offset
                track_h = self.scrollbar_rect.height - self.thumb_rect.height
                ratio = max(0, min(1,
                                   (new_y - self.scrollbar_rect.y) / track_h))
                self.scroll_y = int(ratio * self.max_scroll)

    # -----------------------------------------------------------
    def _close_report_view(self):
        self.report_view = None

    # ────────────────────────────────────────────────────────────
    def update(self, dt):
        pass

    # ────────────────────────────────────────────────────────────
    def _draw_scrollbar(self):
        bar_w = 10
        self.scrollbar_rect = pygame.Rect(
            self.text_rect.right - bar_w,
            self.text_rect.top,
            bar_w,
            self.text_rect.height
        )
        pygame.draw.rect(self.screen, design.colors["button"],
                         self.scrollbar_rect)
        if self.max_scroll == 0:
            return
        ratio = self.text_rect.height / (self.text_rect.height + self.max_scroll)
        thumb_h = max(20, int(self.scrollbar_rect.height * ratio))
        track_h = self.scrollbar_rect.height - thumb_h
        thumb_y = self.scrollbar_rect.y + int(
            track_h * (self.scroll_y / self.max_scroll))
        self.thumb_rect = pygame.Rect(self.scrollbar_rect.x, thumb_y,
                                      bar_w, thumb_h)
        pygame.draw.rect(self.screen, design.colors["button_hover"],
                         self.thumb_rect, 0, 3)

    # ────────────────────────────────────────────────────────────
    def render(self):
        self.screen.fill(design.colors["background"])

        title = design.get_font("large").render(
            "Code Generator View (x86-64 • GNU Assembler)",
            True, design.colors["text"])
        self.screen.blit(
            title, title.get_rect(midtop=(self.screen_rect.centerx, 15)))

        # Marco del área de texto
        pygame.draw.rect(self.screen, (255, 255, 255), self.text_rect)
        pygame.draw.rect(self.screen, design.colors["textbox_border"],
                         self.text_rect, 1)

        clip = self.screen.subsurface(self.text_rect)
        clip.fill((255, 255, 255))

        ln_bg = pygame.Rect(0, 0,
                            self.line_number_width - 5,
                            self.text_rect.height)
        pygame.draw.rect(clip, (240, 240, 240), ln_bg)
        pygame.draw.line(clip, (200, 200, 200),
                         (self.line_number_width - 5, 0),
                         (self.line_number_width - 5, self.text_rect.height))

        start = int(self.scroll_y / self.line_height)
        end = min(len(self.lines),
                  start + int(self.text_rect.height / self.line_height) + 2)
        y = -self.scroll_y % self.line_height
        for i in range(start, end):
            ln = self.code_font.render(f"{i + 1:4d}",
                                       True, (100, 100, 100))
            clip.blit(ln, (5, y))
            self.render_line_with_syntax(clip, self.lines[i],
                                         self.line_number_width, y)
            y += self.line_height

        if self.max_scroll > 0:
            self._draw_scrollbar()

        # Botones
        self.back_btn.render(self.screen)
        self.details_btn.render(self.screen)

        if self.popup and self.popup.render():
            self.popup = None

        # Modal encima
        if self.report_view:
            self.report_view.render()