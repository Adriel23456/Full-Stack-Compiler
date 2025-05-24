# File: GUI/views/optimizer_view.py
import os
import pygame
from CompilerLogic.codeGenerator import CodeGenerator
from GUI.components.pop_up_dialog import PopupDialog
from GUI.view_base import ViewBase
from GUI.components.button import Button
from GUI.design_base import design
from config import States, BASE_DIR


class OptimizerView(ViewBase):
    """
    Muestra (con scroll) el contenido textual de out/vGraph_opt.ll.
    Añade números de línea, fuente monoespaciada grande y conserva la
    indentación (reemplazando TABs por espacios).
    """
    NOT_FOUND_MSG = ["IR file not found – compile first."]

    # ────────────────────────────────────────────────────────────
    def __init__(self, view_controller):
        super().__init__(view_controller)

        # Resuelve la ruta al .ll optimizado
        self.ir_path: str | None = self._find_ir_path()

        # Carga las líneas (o mensaje de error)
        self.lines: list[str] = self._load_ir_lines()

        # Estado de scroll
        self.scroll_y = 0
        self.max_scroll = 0
        self.scroll_speed = 30

        # Scroll-bar
        self.scrollbar_rect = None
        self.thumb_rect = None
        self.scrollbar_dragging = False
        self.drag_offset = 0

    # ────────────────────────────────────────────────────────────
    def _find_ir_path(self) -> str | None:
        """
        Devuelve la ruta a out/vGraph_opt.ll si existe; de lo contrario None.
        """
        default = os.path.join(BASE_DIR, "out", "vGraph_opt.ll")
        return default if os.path.exists(default) else None

    # ────────────────────────────────────────────────────────────
    def _load_ir_lines(self) -> list[str]:
        """
        Lee el fichero IR optimizado y devuelve TODAS las líneas, incluida la
        vacía final cuando el archivo termina en '\n'. También convierte
        TABs → espacios para mantener la sangría sin caracteres «?».
        """
        if not self.ir_path:
            return self.NOT_FOUND_MSG
        try:
            with open(self.ir_path, "r", encoding="utf-8") as fh:
                TAB_SIZE = 4
                raw = fh.read()
                if raw == "":
                    return ["(empty file)"]
                return [ln.expandtabs(TAB_SIZE) for ln in raw.split('\n')]
        except Exception as exc:
            return [f"Error reading IR: {exc}"]

    # ────────────────────────────────────────────────────────────
    def setup(self):
        """Recalcula layout y vuelve a cargar el fichero por si cambió."""
        self.ir_path = self._find_ir_path()
        self.lines = self._load_ir_lines()

        # Layout dinámico ----------------------------------------
        scr = self.screen.get_rect()
        button_w, button_h, margin = 150, 40, 20

        # Botones
        self.back_btn = Button(
            pygame.Rect(margin, scr.bottom - button_h - margin,
                        button_w, button_h),
            "Back to Home"
        )
        self.next_btn = Button(
            pygame.Rect(scr.right - button_w - margin,
                        scr.bottom - button_h - margin,
                        button_w, button_h),
            "Next",
            fixed_width=button_w,
            fixed_height=button_h
        )

        # Área de texto general
        top = 60
        self.line_number_width = 60
        self.text_rect = pygame.Rect(
            margin, top,
            scr.width - margin * 2,
            scr.height - top - button_h - margin * 2
        )
        # Área exclusiva para código (sin números de línea)
        self.code_rect = pygame.Rect(
            self.text_rect.x + self.line_number_width,
            self.text_rect.y,
            self.text_rect.width - self.line_number_width - 15,  # 15 px scrollbar
            self.text_rect.height
        )

        # Fuente monoespaciada grande
        self.code_font = pygame.font.Font(
            pygame.font.match_font("monospace"), 16
        )
        self.line_height = self.code_font.get_linesize()

        # Scroll máximo
        self.max_scroll = max(
            0,
            len(self.lines) * self.line_height - self.text_rect.height
        )

    # ────────────────────────────────────────────────────────────
    def handle_events(self, events):
        for ev in events:
            if ev.type == pygame.QUIT:
                self.view_controller.quit()

            if self.back_btn.handle_event(ev):
                self.view_controller.change_state(States.EDITOR)

            if self.next_btn.handle_event(ev):
                # Ejecutar el generador de ensamblador
                code_gen = CodeGenerator()
                success, message, _ = code_gen.generate_assembly()
                if success:
                    self.view_controller.change_state(States.CODE_GENERATOR_VIEW)
                else:
                    self.popup = PopupDialog(
                        self.screen,
                        f"Assembly generation failed: {message}",
                        5000
                    )

            # Rueda del mouse
            if ev.type == pygame.MOUSEWHEEL:
                self.scroll_y = max(
                    0,
                    min(self.max_scroll, self.scroll_y - ev.y * self.scroll_speed)
                )

            # Drag del thumb
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
        pygame.draw.rect(self.screen, design.colors["button"], self.scrollbar_rect)

        if self.max_scroll == 0:
            return

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
            "Optimized LLVM IR",
            True, design.colors["text"]
        )
        self.screen.blit(
            title_surf,
            title_surf.get_rect(midtop=(self.screen_rect.centerx, 15))
        )

        # Marco del área de texto
        pygame.draw.rect(self.screen, (255, 255, 255), self.text_rect)
        pygame.draw.rect(self.screen, design.colors["textbox_border"],
                         self.text_rect, 1)

        # Sub-superficie con clipping
        clip = self.screen.subsurface(self.text_rect)
        clip.fill((255, 255, 255))

        # Fondo gris para números de línea
        ln_bg = pygame.Rect(0, 0,
                            self.line_number_width - 5,
                            self.text_rect.height)
        pygame.draw.rect(clip, (240, 240, 240), ln_bg)
        pygame.draw.line(clip, (200, 200, 200),
                         (self.line_number_width - 5, 0),
                         (self.line_number_width - 5, self.text_rect.height))

        # Dibujar líneas visibles
        start = int(self.scroll_y / self.line_height)
        end = min(len(self.lines),
                  start + int(self.text_rect.height / self.line_height) + 2)
        y = -self.scroll_y % self.line_height
        for i in range(start, end):
            # N.º de línea
            ln_surf = self.code_font.render(f"{i + 1:4d}",
                                            True, (100, 100, 100))
            clip.blit(ln_surf, (5, y))

            # Contenido
            code_surf = self.code_font.render(self.lines[i],
                                              True, (0, 0, 0))
            clip.blit(code_surf, (self.line_number_width, y))
            y += self.line_height

        # Scroll-bar
        if self.max_scroll > 0:
            self._draw_scrollbar()

        # Botones
        self.back_btn.render(self.screen)
        self.next_btn.render(self.screen)

        # Popup (si existe)
        if hasattr(self, "popup") and self.popup:
            if self.popup.render():
                self.popup = None