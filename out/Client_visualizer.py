#!/usr/bin/env python3
"""
Visualizer.py - Visualizador independiente de archivos image.bin
Este programa busca un archivo image.bin en su mismo directorio y muestra su contenido.
El archivo debe contener datos RGB raw de 800x600 píxeles.
"""

import os
import sys
import time
import threading
import pygame

# Intentar importar fcntl (solo disponible en Unix/Linux)
try:
    import fcntl
    HAS_FCNTL = True
except ImportError:
    HAS_FCNTL = False

# Configuración
FPS = 30
WINDOW_TITLE = "Image Bin Visualizer"
WIDTH, HEIGHT = 800, 600
IMAGE_FILENAME = "image.bin"

class ImageViewer:
    """
    Lector de binario de imagen en un hilo y expositor en pygame.
    Main inicia el hilo, y el renderizado ocurre en el hilo principal.
    """
    
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.expected_size = width * height * 3  # Tamaño esperado del archivo (RGB)
        self.frame_lock = threading.Lock()
        self.raw_frame = None
        self._stop_event = threading.Event()
        self.thread = None
        self.bin_path = None
        
    def start(self, bin_path):
        """Inicia el hilo de lectura del binario"""
        self.bin_path = bin_path
        print(f"ImageViewer inicializado. Leyendo desde: {self.bin_path}")
        self.thread = threading.Thread(target=self._reader, daemon=True)
        self.thread.start()
        return True
        
    def stop(self):
        """Señala al hilo de lectura que debe detenerse y espera su terminación"""
        self._stop_event.set()
        if self.thread:
            self.thread.join()
            
    def _reader(self):
        """Loop de lectura continua del archivo .bin con manejo de errores mejorado"""
        print("Iniciando hilo de lectura de imagen...")
        
        while not self._stop_event.is_set():
            if os.path.exists(self.bin_path):
                try:
                    # Verificar tamaño del archivo antes de intentar leerlo
                    file_size = os.path.getsize(self.bin_path)
                    if file_size != self.expected_size:
                        print(f"[ImageViewer] Advertencia: Tamaño de archivo incorrecto ({file_size} bytes, esperados {self.expected_size})")
                        time.sleep(0.1)  # Esperar un poco y reintentar
                        continue
                        
                    with open(self.bin_path, 'rb') as f:
                        try:
                            if HAS_FCNTL:
                                # En Linux/Unix, usar file locking
                                fcntl.flock(f.fileno(), fcntl.LOCK_SH | fcntl.LOCK_NB)
                            
                            # Leer los datos
                            data = f.read(self.expected_size)
                            
                            # Verificar que leímos la cantidad correcta de datos
                            if len(data) == self.expected_size:
                                with self.frame_lock:
                                    self.raw_frame = data
                            else:
                                print(f"[ImageViewer] Error: Datos leídos incompletos ({len(data)} bytes)")
                                
                            if HAS_FCNTL:
                                # Liberar el bloqueo
                                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                            
                        except IOError:
                            # No pudimos obtener el bloqueo, el archivo está siendo escrito
                            pass
                            
                except Exception as e:
                    print(f"[ImageViewer] Error leyendo binario: {e}")
            else:
                print(f"[ImageViewer] Archivo no encontrado: {self.bin_path}")
                
            # Espera para ajustar tasa de lectura
            self._stop_event.wait(1 / FPS)
            
    def get_surface(self):
        """Devuelve un Surface de pygame generado desde el último frame leído, con validación"""
        surface = None
        with self.frame_lock:
            data = self.raw_frame
            
        if data and len(data) == self.expected_size:
            try:
                surface = pygame.image.frombuffer(data, (self.width, self.height), 'RGB')
            except ValueError as e:
                print(f"[ImageViewer] Error creando superficie: {e}")
                
        return surface

def get_executable_dir():
    """Obtiene el directorio donde se encuentra el ejecutable"""
    if getattr(sys, 'frozen', False):
        # Si es un ejecutable compilado con PyInstaller
        return os.path.dirname(sys.executable)
    else:
        # Si es un script Python normal
        return os.path.dirname(os.path.abspath(__file__))

def main():
    """Función principal"""
    # Obtener directorio del ejecutable
    exe_dir = get_executable_dir()
    image_bin_path = os.path.join(exe_dir, IMAGE_FILENAME)
    
    print(f"Directorio del ejecutable: {exe_dir}")
    print(f"Buscando archivo: {image_bin_path}")
    
    # Verificar que existe el archivo
    if not os.path.exists(image_bin_path):
        print(f"\nError: No se encontró el archivo '{IMAGE_FILENAME}'")
        print(f"Asegúrate de que el archivo esté en el mismo directorio que este programa:")
        print(f"  {exe_dir}")
        input("\nPresiona Enter para salir...")
        return
    
    # Verificar el tamaño del archivo
    expected_size = WIDTH * HEIGHT * 3
    file_size = os.path.getsize(image_bin_path)
    if file_size != expected_size:
        print(f"\nAdvertencia: El archivo tiene un tamaño inesperado.")
        print(f"  Tamaño actual: {file_size} bytes")
        print(f"  Tamaño esperado: {expected_size} bytes (RGB {WIDTH}x{HEIGHT})")
        print("\nIntentando continuar de todos modos...")
    
    # Inicializar pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    
    # Crear visualizador
    viewer = ImageViewer(WIDTH, HEIGHT)
    viewer.start(image_bin_path)
        
    # Esperar un momento para que se carguen los primeros frames
    time.sleep(1)
    
    # Variables de control
    running = True
    last_frame_time = 0
    consecutive_failures = 0
    max_failures = 30
    show_info = True
    font = pygame.font.Font(None, 24)
    
    # Loop principal
    while running:
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_i:
                    show_info = not show_info
        
        # Obtener y mostrar frame
        surf = viewer.get_surface()
        if surf:
            screen.blit(surf, (0, 0))
            last_frame_time = time.time()
            consecutive_failures = 0
        else:
            consecutive_failures += 1
            
            # Si no hay frames por mucho tiempo, mostrar mensaje
            if time.time() - last_frame_time > 5:
                screen.fill((0, 0, 0))
                text = font.render("Esperando frames válidos...", True, (255, 255, 255))
                text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
                screen.blit(text, text_rect)
                last_frame_time = time.time()
                
            # Si hay muchos errores consecutivos, mostrar advertencia
            if consecutive_failures >= max_failures:
                print("Muchos errores consecutivos - Verificando archivo...")
                consecutive_failures = 0
        
        # Mostrar información si está activada
        if show_info:
            info_text = f"FPS: {int(clock.get_fps())} | Archivo: {IMAGE_FILENAME}"
            text_surface = font.render(info_text, True, (0, 255, 0))
            text_bg = pygame.Surface((text_surface.get_width() + 10, text_surface.get_height() + 4))
            text_bg.fill((0, 0, 0))
            text_bg.set_alpha(128)
            screen.blit(text_bg, (5, 8))
            screen.blit(text_surface, (10, 10))
            
            help_text = "ESC: Salir | I: Toggle info"
            help_surface = font.render(help_text, True, (0, 255, 0))
            help_bg = pygame.Surface((help_surface.get_width() + 10, help_surface.get_height() + 4))
            help_bg.fill((0, 0, 0))
            help_bg.set_alpha(128)
            screen.blit(help_bg, (5, HEIGHT - 32))
            screen.blit(help_surface, (10, HEIGHT - 30))
        
        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(FPS)
    
    # Limpiar y salir
    viewer.stop()
    pygame.quit()
    print("\nPrograma terminado correctamente")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError fatal: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para salir...")
        sys.exit(1)