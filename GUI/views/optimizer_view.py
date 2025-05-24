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
    Muestra el contenido textual de out/vGraph_opt.ll con scroll.
    No necesita que se le inyecte la ruta: la resuelve sola.
    """
    NOT_FOUND_MSG = ["IR file not found – compile first."]

    # ────────────────────────────────────────────────────────────
    def __init__(self, view_controller):
        super().__init__(view_controller)

        # Resuelve la ruta al .ll (si existe)
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
        1)  Si el controlador almacenó `ir_path`, úsalo.
        2)  Si existe out/vGraph_opt.ll, devuélvelo.
        3)  Si no, None.
        """
        # 1) Ruta por defecto
        default = os.path.join(BASE_DIR, "out", "vGraph_opt.ll")
        return default if os.path.exists(default) else None

    # ────────────────────────────────────────────────────────────
    def _load_ir_lines(self) -> list[str]:
        if not self.ir_path:
            return self.NOT_FOUND_MSG
        try:
            with open(self.ir_path, "r", encoding="utf-8") as fh:
                return fh.read().splitlines() or ["(empty file)"]
        except Exception as exc:             # archivo bloqueado o leer falló
            return [f"Error reading IR: {exc}"]

    # ────────────────────────────────────────────────────────────
    def setup(self):
        """Recalcula layout y vuelve a cargar el fichero por si cambió."""
        # (re)-cargar líneas por si el usuario volvió a compilar
        self.ir_path = self._find_ir_path()
        self.lines = self._load_ir_lines()

        # Layout dinámico
        scr = self.screen.get_rect()
        button_w, button_h, margin = 150, 40, 20

        # Botones
        self.back_btn = Button(
            pygame.Rect(margin, scr.bottom - button_h - margin, button_w, button_h),
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

        # Área de texto
        top = 60
        self.text_rect = pygame.Rect(
            margin, top,
            scr.width - margin * 2,
            scr.height - top - button_h - margin * 2
        )

        # Scroll máximo
        font = design.get_font("small")
        self.max_scroll = max(0,
                              len(self.lines) * font.get_linesize()
                              - self.text_rect.height)

    # ────────────────────────────────────────────────────────────
    def handle_events(self, events):
        for ev in events:
            if ev.type == pygame.QUIT:
                self.view_controller.quit()

            if self.back_btn.handle_event(ev):
                self.view_controller.change_state(States.EDITOR)

            if self.next_btn.handle_event(ev):
                # Ejecutar el generador de código ensamblador
                code_gen = CodeGenerator()
                success, message, output_path = code_gen.generate_assembly()
                
                if success:
                    # Mostrar popup de éxito
                    popup = PopupDialog(
                        self.screen,
                        message,
                        5000  # 5 segundos
                    )
                    self.popup = popup
                    print(f"[OptimizerView] Assembly generation successful: {message}")
                    
                    # Cambiar a la vista de ensamblador (si existe) o ejecutar
                    # Por ahora, vamos directo a la ejecución
                    #if hasattr(self.view_controller, 'assembly_view_state'):
                    #    self.view_controller.change_state(States.ASSEMBLY_VIEW)
                else:
                    # Mostrar popup de error
                    popup = PopupDialog(
                        self.screen,
                        f"Assembly generation failed: {message}",
                        5000
                    )
                    self.popup = popup
                    print(f"[OptimizerView] Assembly generation failed: {message}")

            # Rueda del mouse
            if ev.type == pygame.MOUSEWHEEL:
                self.scroll_y = max(
                    0,
                    min(self.max_scroll, self.scroll_y - ev.y * self.scroll_speed)
                )

            # Drag manual sobre thumb
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
    def update(self, dt):  # No lógica aun
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
            "Intermediate Optimized Representation (LLVM IR Optimized)",
            True, design.colors["text"]
        )
        self.screen.blit(title_surf, title_surf.get_rect(midtop=(self.screen_rect.centerx, 15)))

        # Marco del área de texto
        pygame.draw.rect(self.screen, (255, 255, 255), self.text_rect)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.text_rect, 1)

        # Sub-superficie con clipping
        clip = self.screen.subsurface(self.text_rect)
        clip.fill((255, 255, 255))

        font = design.get_font("small")
        line_h = font.get_linesize()
        y = -self.scroll_y
        for line in self.lines:
            if -line_h < y < self.text_rect.height:
                clip.blit(font.render(line, True, (0, 0, 0)), (5, y))
            y += line_h

        # Scrollbar
        if self.max_scroll > 0:
            self._draw_scrollbar()

        # Botones
        self.back_btn.render(self.screen)
        self.next_btn.render(self.screen)

        # Renderizar popup si existe
        if hasattr(self, 'popup') and self.popup:
            if self.popup.render():
                self.popup = None  # Eliminar cuando expire