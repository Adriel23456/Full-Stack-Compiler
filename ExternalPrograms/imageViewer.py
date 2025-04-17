import os
import threading
import mmap
import pygame
import time
import fcntl
from config import IMAGE_BIN_PATH, FPS, WINDOW_TITLE

class ImageViewer:
    """
    Lector de binario de imagen en un hilo y expositor en pygame.
    Main inicia el hilo, y el renderizado ocurre en el hilo principal.
    """
    def __init__(self, width=800, height=600):
        self.bin_path = IMAGE_BIN_PATH
        self.width = width
        self.height = height
        self.expected_size = width * height * 3  # Tamaño esperado del archivo (RGB)
        self.frame_lock = threading.Lock()
        self.raw_frame = None
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self._reader, daemon=True)
        print(f"ImageViewer inicializado. Leyendo desde: {self.bin_path}")

    def start(self):
        """Inicia el hilo de lectura del binario"""
        self.thread.start()

    def stop(self):
        """Señala al hilo de lectura que debe detenerse y espera su terminación"""
        self._stop_event.set()
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
                            # Intentar obtener un bloqueo compartido (no bloqueante)
                            fcntl.flock(f.fileno(), fcntl.LOCK_SH | fcntl.LOCK_NB)
                            # Si llegamos aquí, obtuvimos el bloqueo
                            
                            # Leer los datos
                            data = f.read(self.expected_size)
                            
                            # Verificar que leímos la cantidad correcta de datos
                            if len(data) == self.expected_size:
                                with self.frame_lock:
                                    self.raw_frame = data
                            else:
                                print(f"[ImageViewer] Error: Datos leídos incompletos ({len(data)} bytes)")
                                
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