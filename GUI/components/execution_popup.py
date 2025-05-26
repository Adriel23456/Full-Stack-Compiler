# GUI/components/execution_popup.py
import pygame
from GUI.design_base import design
from GUI.components.button import Button


class ExecutionPopup:
    """
    Modal que ofrece elegir el tipo de ejecución:
      • Client Execution
      • HDMI Execution
      • Cancel (✕) en la esquina superior-derecha
    """

    def __init__(self, screen, execute_model, on_close=None):
        self.screen = screen
        self.execute_model = execute_model
        self.on_close = on_close
        self.active = True  # mientras sea True se sigue mostrando

        # ─────────────────────── Ventana ───────────────────────
        scr_rect = self.screen.get_rect()

        # 35 % del ancho de pantalla, limitado a [550 … 900] px
        self.width = 380
        # alto suficiente para título + dos botones
        self.height = 300

        self.rect = pygame.Rect(
            scr_rect.centerx - self.width // 2,
            scr_rect.centery - self.height // 2,
            self.width,
            self.height,
        )

        # ─────────────────────── Botones ───────────────────────
        btn_w, btn_h = 220, 60
        first_y = self.rect.top + 140  # separación bajo el título
        gap_y = 10

        self.client_btn = Button(
            pygame.Rect(self.rect.centerx - btn_w // 2, first_y, btn_w, btn_h),
            "Client Execution",
        )

        self.hdmi_btn = Button(
            pygame.Rect(
                self.rect.centerx - btn_w // 2,
                first_y + btn_h + gap_y,
                btn_w,
                btn_h,
            ),
            "HDMI Execution",
        )

        # Botón ✕ (cerrar) — 28 × 28 px
        self.cancel_btn = Button(
            pygame.Rect(self.rect.right - 48,
                        self.rect.top + 12,
                        35, 35),
            "✕",
            fixed_width=35,
            fixed_height=35
        )

    # ───────────────────────── Eventos ─────────────────────────
    def handle_events(self, events):
        for event in events:
            # Cerrar con ✕ o ESC
            if self.cancel_btn.handle_event(event) or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                self.close()
                return True

            if self.client_btn.handle_event(event):
                self.execute_model.execute_client()
                self.close()
                return True

            if self.hdmi_btn.handle_event(event):
                self.execute_model.execute_hdmi()
                self.close()
                return True

        return True  # absorbe todos los eventos aunque no los use

    # ───────────────────────── Dibujo ──────────────────────────
    def render(self):
        # Fondo semitransparente sobre toda la pantalla
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        # Ventana
        pygame.draw.rect(self.screen, design.colors["background"], self.rect, 0, 8)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.rect, 2, 8)

        # Título
        font = design.get_font("large")
        title = font.render("Choose execution mode", True, design.colors["text"])
        title_rect = title.get_rect(centerx=self.rect.centerx, top=self.rect.top + 45)
        self.screen.blit(title, title_rect)

        # Botones
        self.cancel_btn.render(self.screen)
        self.client_btn.render(self.screen)
        self.hdmi_btn.render(self.screen)

    # ───────────────────────── Loop ────────────────────────────
    def update(self):
        pass  # sin lógica temporal por ahora

    def close(self):
        self.active = False
        if self.on_close:
            self.on_close()
