# File: GUI/views/optimizer_view.py
import os
import pygame
from CompilerLogic.codeGenerator import CodeGenerator
from GUI.components.pop_up_dialog import PopupDialog
from GUI.view_base import ViewBase
from GUI.components.button import Button
from GUI.design_base import design
from GUI.views.report_view import ReportView
from config import States, BASE_DIR


class OptimizerView(ViewBase):
    """
    Muestra (con scroll) el contenido textual de out/vGraph_opt.ll.
    Incluye números de línea y un botón "Open Details" que abre un
    popup modal con el reporte de optimización.
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

        # Modal
        self.popup = None
        self.report_view = None

    # ────────────────────────────────────────────────────────────
    def _find_ir_path(self) -> str | None:
        default = os.path.join(BASE_DIR, "out", "vGraph_opt.ll")
        return default if os.path.exists(default) else None

    # ────────────────────────────────────────────────────────────
    def _load_ir_lines(self) -> list[str]:
        if not self.ir_path:
            return self.NOT_FOUND_MSG
        try:
            TAB_SIZE = 4
            with open(self.ir_path, "r", encoding="utf-8") as fh:
                raw = fh.read()
                if raw == "":
                    return ["(empty file)"]
                return [ln.expandtabs(TAB_SIZE) for ln in raw.split('\n')]
        except Exception as exc:
            return [f"Error reading IR: {exc}"]

    # ────────────────────────────────────────────────────────────
    def setup(self):
        self.ir_path = self._find_ir_path()
        self.lines = self._load_ir_lines()

        scr = self.screen.get_rect()
        button_w, button_h, margin = 150, 40, 20

        # Botones
        self.back_btn = Button(
            pygame.Rect(margin,
                        scr.bottom - button_h - margin,
                        button_w, button_h),
            "Back to Home"
        )
        # Nuevo botón Open Details (centrado)
        center_x = (scr.width - button_w) // 2
        self.details_btn = Button(
            pygame.Rect(center_x,
                        scr.bottom - button_h - margin,
                        button_w, button_h),
            "Open Details"
        )
        self.next_btn = Button(
            pygame.Rect(scr.right - button_w - margin,
                        scr.bottom - button_h - margin,
                        button_w, button_h),
            "Next",
            fixed_width=button_w,
            fixed_height=button_h
        )

        # Área texto
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
    def handle_events(self, events):
        # 1) Si hay popup activo, delegar primero
        if self.report_view:
            self.report_view.handle_events(events)
            return True

        for ev in events:
            if ev.type == pygame.QUIT:
                self.view_controller.quit()

            if self.back_btn.handle_event(ev):
                self.view_controller.change_state(States.EDITOR)

            if self.details_btn.handle_event(ev):
                # Abrir modal con ruta explícita al reporte
                report_path = os.path.join(BASE_DIR, "assets", "optimization_report.txt")
                self.report_view = ReportView(
                    self, report_path=report_path, on_close=self._close_report_view
                )
                return True

            if self.next_btn.handle_event(ev):
                # Generar ensamblador
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

            # Scroll rueda
            if ev.type == pygame.MOUSEWHEEL:
                self.scroll_y = max(
                    0, min(self.max_scroll,
                           self.scroll_y - ev.y * self.scroll_speed)
                )

            # Drag thumb
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

    # ────────────────────────────────────────────────────────────
    def _close_report_view(self):
        self.report_view = None

    # ────────────────────────────────────────────────────────────
    def update(self, dt):
        if self.report_view:
            self.report_view  # no lógica dinámica necesaria

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

        # Título
        title = design.get_font("large").render(
            "Optimized LLVM IR", True, design.colors["text"])
        self.screen.blit(
            title, title.get_rect(midtop=(self.screen_rect.centerx, 15)))

        # Marco texto
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
            txt = self.code_font.render(self.lines[i],
                                        True, (0, 0, 0))
            clip.blit(txt, (self.line_number_width, y))
            y += self.line_height

        if self.max_scroll > 0:
            self._draw_scrollbar()

        # Botones
        self.back_btn.render(self.screen)
        self.details_btn.render(self.screen)
        self.next_btn.render(self.screen)

        if self.popup:
            if self.popup.render():
                self.popup = None

        # Modals
        if self.report_view:
            self.report_view.render()