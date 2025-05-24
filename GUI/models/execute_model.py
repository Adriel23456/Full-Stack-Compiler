# File: GUI/models/execute_model.py
"""
Model for executing compiler and image viewer
Handles launching external programs in separate terminals
"""
import os
import subprocess
import tempfile
from config import BASE_DIR


class ExecuteModel:
    """
    Model for executing compiler and image viewer
    """

    def __init__(self):
        """
        Initialize the execute model
        """
        self.vgraph_process = None
        self.viewer_process = None

    # ──────────────────────────────────────────────────────────────
    #  vGraph: ensamblar + enlazar + ejecutar en GNOME-terminal
    # ──────────────────────────────────────────────────────────────
    def run_vgraph_executable(self) -> bool:
        """
        Abre un GNOME-terminal, ensambla el código ASM y ejecuta vGraph.exe
        """
        try:
            # Rutas
            exe_dir = os.path.join(BASE_DIR, "out")
            exe_path = os.path.join(exe_dir, "vGraph.exe")
            asm_path = os.path.join(exe_dir, "vGraph.asm")
            obj_path = os.path.join(exe_dir, "vGraph.o")
            runtime_path = os.path.join(BASE_DIR, "CompilerLogic", "ir", "runtime.o")
            build_script = os.path.join(BASE_DIR, "CompilerLogic", "ir", "build_runtime.sh")

            # Verificar que existe el archivo ASM
            if not os.path.exists(asm_path):
                print(f"Error: No se encuentra {asm_path}. Genere el código ensamblador primero.")
                return False

            # Comandos a lanzar en orden dentro del terminal
            # Nota: Usamos 'as' (GNU assembler) porque llvmlite genera sintaxis AT&T
            cmds = [
                f"cd {BASE_DIR}",
                f"echo 'Building VGraph runtime...'",
                f"bash {build_script}",
                f"echo 'Assembling {asm_path}...'",
                f"as {asm_path} -o {obj_path}",  # GNU assembler para sintaxis AT&T
                f"echo 'Linking executable...'",
                f"gcc {obj_path} {runtime_path} -lm -no-pie -o {exe_path}",  # -no-pie para evitar PIE
                f"echo 'Running VGraph...'",
                f"{exe_path}",
                "echo 'Presiona Enter para cerrar'; read"
            ]
            bash_cmd = " && ".join(cmds)

            # Verificar disponibilidad de gnome-terminal
            if subprocess.run(["which", "gnome-terminal"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
                print("Error: gnome-terminal no está disponible en este sistema.")
                # Fallback: ejecutar en terminal actual
                for cmd in cmds[:-1]:  # Omitir el 'read' final
                    print(f"Ejecutando: {cmd}")
                    result = subprocess.run(cmd, shell=True, cwd=BASE_DIR)
                    if result.returncode != 0:
                        print(f"Error al ejecutar: {cmd}")
                        return False
                return True

            # Lanzar gnome-terminal
            self.vgraph_process = subprocess.Popen(
                ["gnome-terminal", "--", "bash", "-c", bash_cmd]
            )
            print(f"vGraph.exe lanzado en gnome-terminal (ensamblado desde {asm_path})")
            return True

        except Exception as e:
            print(f"Error al ejecutar vGraph.exe: {e}")
            return False

    # ──────────────────────────────────────────────────────────────
    #  Image Viewer – sin cambios
    # ──────────────────────────────────────────────────────────────
    def start_image_viewer(self) -> bool:
        """
        Start the image viewer in a separate process with its own terminal
        """
        try:
            # Create a temporary script to run the image viewer
            fd, script_path = tempfile.mkstemp(suffix='.py', prefix='imageviewer_')
            os.close(fd)

            # Write the image viewer script to the temporary file
            with open(script_path, 'w') as f:
                f.write(f"""#!/usr/bin/env python3
import os
import sys
import time

sys.path.insert(0, "{BASE_DIR}")

from config import FPS, WINDOW_TITLE, IMAGE_BIN_PATH, BASE_DIR

os.environ.setdefault('SDL_VIDEODRIVER', 'x11')

import pygame
from ExternalPrograms.imageViewer import ImageViewer

WIDTH, HEIGHT = 800, 600

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 24)
    pygame.display.set_caption(WINDOW_TITLE + " - Image Viewer")
    clock = pygame.time.Clock()

    viewer = ImageViewer(width=WIDTH, height=HEIGHT)
    viewer.start()

    time.sleep(1)

    last_surface_time = time.time()
    consecutive_failures = 0
    max_failures = 30

    running = True
    while running:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                running = False
            elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
                running = False

        surf = viewer.get_surface()
        if surf:
            screen.blit(surf, (0, 0))
            pygame.display.flip()
            last_surface_time = time.time()
            consecutive_failures = 0
        else:
            consecutive_failures += 1
            if time.time() - last_surface_time > 5:
                print("Advertencia: No se ha recibido frame válido en 5 segundos")
                last_surface_time = time.time()
            if consecutive_failures >= max_failures:
                print("Muchos errores consecutivos - Reiniciando visualizador...")
                viewer.stop()
                time.sleep(1)
                viewer = ImageViewer(width=WIDTH, height=HEIGHT)
                viewer.start()
                consecutive_failures = 0

        clock.tick(FPS)

    viewer.stop()
    pygame.quit()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)
""")

            os.chmod(script_path, 0o755)

            # Lanzar en gnome-terminal si está disponible
            if subprocess.run(["which", "gnome-terminal"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                env = os.environ.copy()
                env["PYTHONPATH"] = f"{BASE_DIR}:{env.get('PYTHONPATH', '')}"
                self.viewer_process = subprocess.Popen(
                    ["gnome-terminal", "--", "python3", script_path],
                    env=env
                )
                print("Image Viewer lanzado en gnome-terminal")
                return True

            # Fallback: ejecutar directamente
            env = os.environ.copy()
            env["PYTHONPATH"] = f"{BASE_DIR}:{env.get('PYTHONPATH', '')}"
            self.viewer_process = subprocess.Popen(["python3", script_path], env=env)
            print("Image Viewer lanzado directamente")
            return True

        except Exception as e:
            print(f"Error al iniciar el visualizador de imágenes: {e}")
            return False

    # ──────────────────────────────────────────────────────────────
    #  Ejecutar ambos procesos
    # ──────────────────────────────────────────────────────────────
    def execute(self) -> bool:
        """
        Execute both the vGraph executable and the image viewer
        """
        import time
        ok_vgraph = self.run_vgraph_executable()
        time.sleep(1)  # pequeño respiro
        ok_viewer = self.start_image_viewer()
        return ok_vgraph and ok_viewer