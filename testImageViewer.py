#!/usr/bin/env python3
"""
testImageViewer.py

Script de prueba para ImageViewer con threading.
Inicia un hilo de lectura de imagen, y en el hilo principal corre pygame.
"""
import os
import pygame
import time
import sys
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
            print(f"FPS: {int(clock.get_fps())}", end="\r")

    # Detener el hilo de lectura y cerrar pygame
    print("\nFinalizando visualizador...")
    viewer.stop()
    pygame.quit()
    print("Test finalizado.")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error en ejecución principal: {e}")
        pygame.quit()
        sys.exit(1)