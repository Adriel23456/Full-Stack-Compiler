"""
Report View - ventana modal reutilizable para mostrar archivos de texto
con números de línea y scroll (soporta caracteres Unicode como ✓).
"""
import os
import pygame
from GUI.design_base import design
from GUI.components.button import Button


class ReportView:
    """Ventana modal que bloquea la vista padre mientras está abierta."""

    NOT_FOUND = ["Report not found"]

    # --------------------------------------------------------------
    def __init__(self, parent_view, report_path, on_close=None):
        """
        :param parent_view: vista que abre el popup
        :param report_path: ruta ABSOLUTA al archivo de texto
        :param on_close: callback al cerrar
        """
        self.parent_view = parent_view
        self.screen = pygame.display.get_surface()
        self.on_close = on_close
        self.report_path = report_path

        # Cargar texto
        self.lines = self._load_report_lines()

        # Fuente ────────────────────────────────────────────────
        # ★ Intentamos una lista de fuentes con buena cobertura Unicode
        font_path = pygame.font.match_font(
            "DejaVuSansMono,DejaVu Sans Mono,Consolas,Courier New,monospace"
        )
        if font_path is None:
            # Fallback: fuente por defecto del sistema
            self.font = pygame.font.SysFont(None, 16)
        else:
            self.font = pygame.font.Font(font_path, 16)
        # ────────────────────────────────────────────────────────
        self.line_h = self.font.get_linesize()

        # Scroll
        self.scroll_y = 0
        self.scroll_speed = 30
        self.max_scroll = 0

        # Layout
        self._create_layout()

        # Scrollbar
        self.scrollbar_rect = None
        self.thumb_rect = None
        self.dragging = False
        self.drag_offset = 0

    # --------------------------------------------------------------
    def _load_report_lines(self):
        TAB_SIZE = 4
        if not os.path.exists(self.report_path):
            return self.NOT_FOUND
        try:
            with open(self.report_path, "r", encoding="utf-8") as fh:
                raw = fh.read()
                if raw == "":
                    return ["(empty file)"]
                return [ln.expandtabs(TAB_SIZE) for ln in raw.split("\n")]
        except Exception as exc:
            return [f"Error reading report: {exc}"]

    # --------------------------------------------------------------
    def _create_layout(self):
        w, h = 900, 650
        self.rect = pygame.Rect(
            (self.screen.get_width() - w) // 2,
            (self.screen.get_height() - h) // 2,
            w, h
        )
        margin = 30
        self.text_rect = pygame.Rect(
            self.rect.x + margin,
            self.rect.y + margin,
            self.rect.width - 2 * margin,
            self.rect.height - 2 * margin - 50
        )

        # Botón Close
        self.close_btn = Button(
            pygame.Rect(self.rect.centerx - 75,
                        self.rect.bottom - 40 - 15,
                        150, 40),
            "Close"
        )

        # Datos de scroll
        self.line_num_w = 60
        self.max_scroll = max(
            0, len(self.lines) * self.line_h - self.text_rect.height
        )

    # --------------------------------------------------------------
    def handle_events(self, events):
        for ev in events:
            if self.close_btn.handle_event(ev):
                if self.on_close:
                    self.on_close()
                return True

            if ev.type == pygame.MOUSEWHEEL:
                if self.text_rect.collidepoint(pygame.mouse.get_pos()):
                    self.scroll_y = max(
                        0,
                        min(self.max_scroll,
                            self.scroll_y - ev.y * self.scroll_speed)
                    )

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if self.thumb_rect and self.thumb_rect.collidepoint(ev.pos):
                    self.dragging = True
                    self.drag_offset = ev.pos[1] - self.thumb_rect.y
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.dragging = False
            if ev.type == pygame.MOUSEMOTION and self.dragging:
                new_y = ev.pos[1] - self.drag_offset
                track_h = self.scrollbar_rect.height - self.thumb_rect.height
                ratio = max(0, min(1,
                                   (new_y - self.scrollbar_rect.y) / track_h))
                self.scroll_y = int(ratio * self.max_scroll)

        return True

    # --------------------------------------------------------------
    def render(self):
        # Fondo semitransparente
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        # Ventana
        pygame.draw.rect(self.screen, design.colors["background"],
                         self.rect, 0, 10)
        pygame.draw.rect(self.screen, design.colors["textbox_border"],
                         self.rect, 2, 10)

        # Área de texto
        pygame.draw.rect(self.screen, (255, 255, 255), self.text_rect)
        pygame.draw.rect(self.screen, design.colors["textbox_border"],
                         self.text_rect, 1)

        clip = self.screen.subsurface(self.text_rect)
        clip.fill((255, 255, 255))

        # Fondo gris para números de línea
        ln_bg = pygame.Rect(0, 0,
                            self.line_num_w - 5,
                            self.text_rect.height)
        pygame.draw.rect(clip, (240, 240, 240), ln_bg)
        pygame.draw.line(clip, (200, 200, 200),
                         (self.line_num_w - 5, 0),
                         (self.line_num_w - 5, self.text_rect.height))

        # Dibujar líneas visibles
        start = int(self.scroll_y / self.line_h)
        end = min(len(self.lines),
                  start + int(self.text_rect.height / self.line_h) + 2)
        y = -self.scroll_y % self.line_h
        for i in range(start, end):
            ln_s = self.font.render(f"{i + 1:4d}", True, (100, 100, 100))
            clip.blit(ln_s, (5, y))
            txt_s = self.font.render(self.lines[i], True, (0, 0, 0))
            clip.blit(txt_s, (self.line_num_w, y))
            y += self.line_h

        # Scrollbar
        if self.max_scroll > 0:
            self._draw_scrollbar()

        # Botón
        self.close_btn.render(self.screen)

    # --------------------------------------------------------------
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

        ratio_vis = self.text_rect.height / (self.text_rect.height +
                                             self.max_scroll)
        thumb_h = max(20, int(self.scrollbar_rect.height * ratio_vis))
        track_h = self.scrollbar_rect.height - thumb_h
        thumb_y = self.scrollbar_rect.y + int(
            track_h * (self.scroll_y / self.max_scroll))
        self.thumb_rect = pygame.Rect(self.scrollbar_rect.x, thumb_y,
                                      bar_w, thumb_h)
        pygame.draw.rect(self.screen, design.colors["button_hover"],
                         self.thumb_rect, 0, 3)