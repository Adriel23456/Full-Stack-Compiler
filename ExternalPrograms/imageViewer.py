import os
import threading
import mmap
import pygame
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
        self.frame_lock = threading.Lock()
        self.raw_frame = None
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self._reader, daemon=True)

    def start(self):
        """Inicia el hilo de lectura del binario"""
        self.thread.start()

    def stop(self):
        """Señala al hilo de lectura que debe detenerse y espera su terminación"""
        self._stop_event.set()
        self.thread.join()

    def _reader(self):
        """Loop de lectura continua del archivo .bin"""
        while not self._stop_event.is_set():
            if os.path.exists(self.bin_path):
                try:
                    with open(self.bin_path, 'rb') as f:
                        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                        data = mm.read(self.width * self.height * 3)
                        mm.close()
                    with self.frame_lock:
                        self.raw_frame = data
                except Exception as e:
                    print(f"[ImageViewer] Error leyendo binario: {e}")
            # Espera para ajustar tasa de lectura
            self._stop_event.wait(1 / FPS)

    def get_surface(self):
        """Devuelve un Surface de pygame generado desde el último frame leído"""
        with self.frame_lock:
            data = self.raw_frame
        if data:
            return pygame.image.frombuffer(data, (self.width, self.height), 'RGB')
        return None