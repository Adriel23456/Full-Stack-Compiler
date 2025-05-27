"""
Main entry point of the program
Initializes pygame and the View Controller.

Added: cross‑platform GPU acceleration via SDL2 render drivers
----------------------------------------------------------------
* Selects the best hardware backend for the current OS using
  the SDL_RENDER_DRIVER environment variable (Metal on macOS,
  Direct3D on Windows, OpenGL on Linux/Unix).
* Enables double‑buffering and requests vsync where available.
* Keeps a graceful software fallback, so the program remains
  100 % backward‑compatible on machines without a discrete GPU
  or with very old drivers.
"""
import os
import sys
import pygame
from GUI.views.code_generator_view import CodeGeneratorView
from GUI.views.ir_view import IRView
from GUI.views.optimizer_view import OptimizerView
from config import WINDOW_TITLE, States
from GUI.view_controller import ViewController
from GUI.views.editor_view import EditorView
from GUI.views.lexical_analysis_view import LexicalAnalysisView
from GUI.views.syntactic_analysis_view import SyntacticAnalysisView
from GUI.views.semantic_analysis_view import SemanticAnalysisView
from GUI.design_base import design

# ──────────────────────────────────────────────────────────────
# SDL / GPU configuration helpers
# ──────────────────────────────────────────────────────────────

def _configure_gpu():
    """Set SDL hints so that, when possible, SDL2/pygame will
    initialise a hardware‑accelerated renderer instead of a
    purely software surface. Falls back transparently if the
    requested backend is unavailable.
    """

    # Pick the most typical HW driver per platform.
    if sys.platform.startswith("win"):
        # Direct3D 11 > Direct3D 9 > OpenGL
        os.environ.setdefault("SDL_RENDER_DRIVER", "direct3d")
    elif sys.platform == "darwin":
        # Apple removed OpenGL from the public headers; Metal is the default.
        os.environ.setdefault("SDL_RENDER_DRIVER", "metal")
    else:
        # Linux / *BSD – usually accelerated OpenGL is available.
        os.environ.setdefault("SDL_RENDER_DRIVER", "opengl")

    # Ask SDL to use linear filtering when scaling
    os.environ.setdefault("SDL_RENDER_SCALE_QUALITY", "1")
    # Request vsync if the driver supports it (ignored otherwise)
    os.environ.setdefault("SDL_HINT_RENDER_VSYNC", "1")
    # Keep the original window‑centering behaviour
    os.environ.setdefault("SDL_VIDEO_CENTERED", "1")

# ---------------------------------------------------------------------------

def main():
    """Main program function"""

    # Configure the GPU/SDL hints *before* importing/initialising pygame
    _configure_gpu()

    # Initialize pygame
    pygame.init()
    pygame.font.init()                      # Explicit font init
    pygame.key.set_repeat(0)                # Disable built‑in key repeat

    # Get configured window size
    window_size = design.get_window_size()

    # Try to create a double‑buffered, hardware accelerated window.
    # If the backend supports the new "vsync" keyword (pygame ≥ 2.0.1), use it.
    display_flags = pygame.DOUBLEBUF | pygame.RESIZABLE
    try:
        screen = pygame.display.set_mode(window_size, display_flags, vsync=1)
    except TypeError:
        # Older pygame – no vsync kwarg
        screen = pygame.display.set_mode(window_size, display_flags)

    pygame.display.set_caption(WINDOW_TITLE)

    # Clipboard module (may fail silently on headless/X11 without selection)
    try:
        pygame.scrap.init()
    except pygame.error:
        pass

    try:
        # Create View Controller
        controller = ViewController()

        # Register the possible states
        controller.add_state(States.EDITOR, EditorView)
        controller.add_state(States.LEXICAL_ANALYSIS, LexicalAnalysisView)
        controller.add_state(States.SYNTACTIC_ANALYSIS, SyntacticAnalysisView)
        controller.add_state(States.SEMANTIC_ANALYSIS, SemanticAnalysisView)
        controller.add_state(States.IR_VIEW, IRView)
        controller.add_state(States.OPTIMIZER_VIEW, OptimizerView)
        controller.add_state(States.CODE_GENERATOR_VIEW, CodeGeneratorView)

        # Provide the main surface to the controller if it expects it
        if hasattr(controller, "set_surface"):
            controller.set_surface(screen)

        # Set initial state to Editor
        controller.set_initial_state(States.EDITOR)

        # Run main loop with extra protection
        _safe_run(controller)

    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        pygame.quit()
        sys.exit()

# ──────────────────────────────────────────────────────────────
# Protected main loop
# ──────────────────────────────────────────────────────────────

def _safe_run(controller):
    """Main loop wrapped in broad exception handling so that
    unforeseen errors don’t bring down the whole application.
    """

    clock = pygame.time.Clock()

    while controller.running:
        try:
            dt = clock.tick(60) / 1000.0  # Delta time in seconds

            # Event handling
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    controller.quit()

            # Delegate to current view
            if hasattr(controller, "current_view"):
                try:
                    controller.current_view.handle_events(events)
                except Exception as e:
                    print(f"Error en handle_events: {e}")

            # State transitions
            try:
                controller.handle_state_change()
            except Exception as e:
                print(f"Error en handle_state_change: {e}")

            # Update & render current view
            if hasattr(controller, "current_view"):
                try:
                    # Update
                    try:
                        controller.current_view.update(dt)
                    except Exception as e:
                        print(f"Error en update: {e}")

                    # Render
                    try:
                        controller.current_view.render()
                    except Exception as e:
                        print(f"Error en render: {e}")
                except Exception as e:
                    print(f"Error general en ejecución del view: {e}")

            # Present frame – double‑buffer swap (vsync if available)
            try:
                pygame.display.flip()
            except Exception as e:
                print(f"Error en pygame.display.flip(): {e}")

        except Exception as e:
            print(f"Error crítico en el bucle principal: {e}")
            pygame.time.wait(100)  # Prevent 100 % CPU on persistent failure

# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()