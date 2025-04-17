#!/usr/bin/env python3
"""
testImageViewer.py

Script de prueba para ImageViewer con threading.
Inicia un hilo de lectura de imagen, y en el hilo principal corre pygame.
"""
import os
import pygame
from config import FPS, WINDOW_TITLE
from ExternalPrograms.imageViewer import ImageViewer

# Forzar driver de video compatible
os.environ.setdefault('SDL_VIDEODRIVER', 'x11')

WIDTH, HEIGHT = 800, 600


def main():
    # Inicializar pygame (display y eventos)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 24)
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    # Crear y arrancar el lector de imágenes en un hilo
    viewer = ImageViewer(width=WIDTH, height=HEIGHT)
    viewer.start()

    running = True
    while running:
        # Manejo de eventos
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                running = False

        # Obtener y mostrar el último frame leído
        surf = viewer.get_surface()
        if surf:
            screen.blit(surf, (0, 0))
            pygame.display.flip()

        clock.tick(FPS)

    # Detener el hilo de lectura y cerrar pygame
    viewer.stop()
    pygame.quit()
    print("Test finalizado.")


if __name__ == '__main__':
    main()