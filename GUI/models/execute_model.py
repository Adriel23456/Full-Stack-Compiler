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
    
    def run_vgraph_executable(self):
        """
        Run the vGraph.exe executable in a new terminal window
        """
        try:
            # Define the path to the executable and out directory
            exe_dir = os.path.join(BASE_DIR, "out")
            exe_path = os.path.join(exe_dir, "vGraph.exe")
            
            # Ensure the executable exists
            if not os.path.exists(exe_path):
                print(f"Error: Executable not found at {exe_path}")
                return False
            
            # Set execute permissions using chmod
            subprocess.run(["chmod", "+x", exe_path], check=True)
            
            # Try different terminal emulators that might be available on Ubuntu
            terminals = ["gnome-terminal", "xterm", "konsole", "xfce4-terminal"]
            
            for terminal in terminals:
                try:
                    # Check if the terminal is available
                    if subprocess.run(["which", terminal], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                        # Run the executable in a new terminal - IMPORTANTE: Usar el directorio 'out' como CWD
                        if terminal == "gnome-terminal":
                            self.vgraph_process = subprocess.Popen([
                                terminal, "--", "bash", "-c", f"cd {exe_dir} && ./vGraph.exe; echo 'Press Enter to close'; read"
                            ])
                        elif terminal == "konsole" or terminal == "xfce4-terminal":
                            self.vgraph_process = subprocess.Popen([
                                terminal, "-e", f"bash -c \"cd {exe_dir} && ./vGraph.exe; echo 'Press Enter to close'; read\""
                            ])
                        else:  # xterm
                            self.vgraph_process = subprocess.Popen([
                                terminal, "-e", f"bash -c 'cd {exe_dir} && ./vGraph.exe; echo \"Press Enter to close\"; read'"
                            ])
                        
                        print(f"Started vGraph.exe in {terminal} (working dir: {exe_dir})")
                        return True
                except Exception as e:
                    print(f"Failed to launch using {terminal}: {e}")
                    continue
            
            print("No suitable terminal emulator found. Trying to run directly...")
            # Fallback: just run it directly from the correct directory
            self.vgraph_process = subprocess.Popen(["./vGraph.exe"], cwd=exe_dir)
            print(f"Started vGraph.exe directly without terminal (working dir: {exe_dir})")
            return True
            
        except Exception as e:
            print(f"Error running vGraph.exe: {e}")
            return False
    
    def start_image_viewer(self):
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

# Agregar el directorio base al path para importar correctamente
sys.path.insert(0, "{BASE_DIR}")

# Ahora podemos importar config
from config import FPS, WINDOW_TITLE, IMAGE_BIN_PATH, BASE_DIR

# Forzar driver de video compatible
os.environ.setdefault('SDL_VIDEODRIVER', 'x11')

# Importar pygame después de configurar el entorno
import pygame
from ExternalPrograms.imageViewer import ImageViewer

WIDTH, HEIGHT = 800, 600

def main():
    # Verificar que el archivo de imagen existe
    print(f"Buscando archivo de imagen en: {{IMAGE_BIN_PATH}}")
    
    # Inicializar pygame (display y eventos)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 24)
    pygame.display.set_caption(WINDOW_TITLE + " - Image Viewer")
    clock = pygame.time.Clock()

    # Crear y arrancar el lector de imágenes en un hilo
    viewer = ImageViewer(width=WIDTH, height=HEIGHT)
    viewer.start()
    
    # Permitir que el visualizador se inicialice completamente
    print("Esperando para iniciar visualización...")
    time.sleep(1)
    
    # Variables para manejar errores
    last_surface_time = time.time()
    consecutive_failures = 0
    max_failures = 30  # Máximo de errores consecutivos antes de reiniciar

    running = True
    print("Iniciando bucle de visualización...")
    
    while running:
        # Manejo de eventos
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                running = False
            elif evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_ESCAPE:
                    running = False

        # Obtener y mostrar el último frame leído
        surf = viewer.get_surface()
        if surf:
            screen.blit(surf, (0, 0))
            pygame.display.flip()
            last_surface_time = time.time()
            consecutive_failures = 0
        else:
            # Manejar fallo en obtener superficie
            consecutive_failures += 1
            current_time = time.time()
            
            # Si han pasado más de 5 segundos sin superficie válida
            if current_time - last_surface_time > 5:
                print("Advertencia: No se ha recibido frame válido en 5 segundos")
                print(f"Verificando si existe: {{IMAGE_BIN_PATH}} = {{os.path.exists(IMAGE_BIN_PATH)}}")
                last_surface_time = current_time
            
            # Si hay demasiados fallos consecutivos, mostrar mensaje
            if consecutive_failures >= max_failures:
                print("Muchos errores consecutivos - Reiniciando visualizador...")
                viewer.stop()
                time.sleep(1)  # Esperar un segundo
                viewer = ImageViewer(width=WIDTH, height=HEIGHT)
                viewer.start()
                consecutive_failures = 0

        # Mantener la tasa de fotogramas
        clock.tick(FPS)
        
        # Mostrar FPS actuales cada segundo
        if int(pygame.time.get_ticks() / 1000) % 5 == 0:
            print(f"FPS: {{int(clock.get_fps())}}", end="\\r")

    # Detener el hilo de lectura y cerrar pygame
    print("\\nFinalizando visualizador...")
    viewer.stop()
    pygame.quit()
    print("Test finalizado.")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error en ejecución principal: {{e}}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)
""")
            
            # Make the script executable
            os.chmod(script_path, 0o755)
            
            # Try different terminal emulators
            terminals = ["gnome-terminal", "xterm", "konsole", "xfce4-terminal"]
            
            for terminal in terminals:
                try:
                    # Check if the terminal is available
                    if subprocess.run(["which", terminal], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                        # Agregar PYTHONPATH para asegurar que puede encontrar los módulos
                        env = os.environ.copy()
                        if "PYTHONPATH" in env:
                            env["PYTHONPATH"] = f"{BASE_DIR}:{env['PYTHONPATH']}"
                        else:
                            env["PYTHONPATH"] = BASE_DIR
                            
                        # Run the script in a new terminal with correct environment
                        if terminal == "gnome-terminal":
                            self.viewer_process = subprocess.Popen([
                                terminal, "--", "python3", script_path
                            ], env=env)
                        elif terminal == "konsole" or terminal == "xfce4-terminal":
                            cmd = f"PYTHONPATH={BASE_DIR} python3 {script_path}"
                            self.viewer_process = subprocess.Popen([
                                terminal, "-e", cmd
                            ], env=env)
                        else:  # xterm
                            cmd = f"PYTHONPATH={BASE_DIR} python3 {script_path}"
                            self.viewer_process = subprocess.Popen([
                                terminal, "-e", cmd
                            ], env=env)
                        
                        print(f"Started Image Viewer in {terminal}")
                        return True
                except Exception as e:
                    print(f"Failed to launch using {terminal}: {e}")
                    continue
            
            print("No suitable terminal emulator found. Trying to run directly...")
            # Fallback: run in background with correct environment
            env = os.environ.copy()
            if "PYTHONPATH" in env:
                env["PYTHONPATH"] = f"{BASE_DIR}:{env['PYTHONPATH']}"
            else:
                env["PYTHONPATH"] = BASE_DIR
            self.viewer_process = subprocess.Popen(["python3", script_path], env=env)
            print(f"Started Image Viewer directly")
            return True
            
        except Exception as e:
            print(f"Error starting image viewer: {e}")
            return False
    
    def execute(self):
        """
        Execute both the vGraph executable and the image viewer
        """
        # Run vGraph.exe
        success1 = self.run_vgraph_executable()
        
        # Small delay to ensure executable has time to start
        import time
        time.sleep(1)
        
        # Start image viewer
        success2 = self.start_image_viewer()
        
        return success1 and success2