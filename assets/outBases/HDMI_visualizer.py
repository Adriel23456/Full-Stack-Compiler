#!/usr/bin/env python3
"""
HDMI_visualizer.py - Visualizador HDMI de archivos image.bin
Este programa busca un archivo image.bin en su mismo directorio y envía
su contenido a un puerto HDMI seleccionado.
El archivo debe contener datos RGB raw de 800x600 píxeles.
"""

import os
import sys
import time
import threading
import mmap
import ctypes
import struct
import platform

# Importar SDL2
try:
    import sdl2
    import sdl2.ext
except ImportError:
    print("Error: PySDL2 no está instalado.")
    print("Instálalo con: pip install PySDL2")
    sys.exit(1)

# Intentar importar fcntl (solo disponible en Unix/Linux)
try:
    import fcntl
    HAS_FCNTL = True
except ImportError:
    HAS_FCNTL = False

# Configuración
FPS = 30
WINDOW_TITLE = "HDMI Image Visualizer"
WIDTH, HEIGHT = 800, 600
IMAGE_FILENAME = "image.bin"

class ImageReader:
    """
    Lector de archivo image.bin usando mmap para mejor rendimiento
    """
    
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.expected_size = width * height * 3  # RGB
        self.frame_lock = threading.Lock()
        self.raw_frame = None
        self._stop_event = threading.Event()
        self.thread = None
        self.bin_path = None
        self.mmap_file = None
        self.file_handle = None
        
    def start(self, bin_path):
        """Inicia el hilo de lectura del binario"""
        self.bin_path = bin_path
        print(f"[HDMI] ImageReader inicializado. Leyendo desde: {self.bin_path}")
        
        # Intentar abrir con mmap
        try:
            self.file_handle = open(self.bin_path, 'r+b')
            self.mmap_file = mmap.mmap(self.file_handle.fileno(), self.expected_size)
            print("[HDMI] Usando mmap para lectura optimizada")
        except:
            print("[HDMI] No se pudo usar mmap, usando lectura normal")
            if self.file_handle:
                self.file_handle.close()
            self.file_handle = None
            self.mmap_file = None
        
        self.thread = threading.Thread(target=self._reader, daemon=True)
        self.thread.start()
        return True
        
    def stop(self):
        """Detiene el hilo de lectura"""
        self._stop_event.set()
        if self.thread:
            self.thread.join()
        if self.mmap_file:
            self.mmap_file.close()
        if self.file_handle:
            self.file_handle.close()
            
    def _reader(self):
        """Loop de lectura continua del archivo"""
        print("[HDMI] Iniciando hilo de lectura de imagen...")
        
        while not self._stop_event.is_set():
            try:
                if self.mmap_file:
                    # Lectura con mmap
                    self.mmap_file.seek(0)
                    data = self.mmap_file.read(self.expected_size)
                    with self.frame_lock:
                        self.raw_frame = data
                else:
                    # Lectura normal
                    if os.path.exists(self.bin_path):
                        file_size = os.path.getsize(self.bin_path)
                        if file_size == self.expected_size:
                            with open(self.bin_path, 'rb') as f:
                                if HAS_FCNTL:
                                    try:
                                        fcntl.flock(f.fileno(), fcntl.LOCK_SH | fcntl.LOCK_NB)
                                    except:
                                        pass
                                
                                data = f.read(self.expected_size)
                                if len(data) == self.expected_size:
                                    with self.frame_lock:
                                        self.raw_frame = data
                                
                                if HAS_FCNTL:
                                    try:
                                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                                    except:
                                        pass
            except Exception as e:
                if not self._stop_event.is_set():
                    print(f"[HDMI] Error leyendo: {e}")
                
            # Espera para ajustar tasa de lectura
            self._stop_event.wait(1 / FPS)
            
    def get_frame(self):
        """Obtiene el frame actual"""
        with self.frame_lock:
            return self.raw_frame

def get_executable_dir():
    """Obtiene el directorio donde se encuentra el ejecutable"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def detect_displays():
    """Detecta los displays disponibles usando SDL2"""
    displays = []
    num_displays = sdl2.SDL_GetNumVideoDisplays()
    
    print(f"\n[HDMI] Detectando displays...")
    print(f"[HDMI] Número de displays encontrados: {num_displays}")
    
    for i in range(num_displays):
        # Obtener información del display
        display_name = sdl2.SDL_GetDisplayName(i)
        if display_name:
            display_name = display_name.decode('utf-8')
        else:
            display_name = f"Display {i}"
        
        # Obtener bounds del display
        bounds = sdl2.SDL_Rect()
        if sdl2.SDL_GetDisplayBounds(i, bounds) == 0:
            resolution = f"{bounds.w}x{bounds.h}"
            position = f"({bounds.x}, {bounds.y})"
        else:
            resolution = "Unknown"
            position = "(0, 0)"
        
        # Obtener modo de display actual
        mode = sdl2.SDL_DisplayMode()
        if sdl2.SDL_GetCurrentDisplayMode(i, mode) == 0:
            refresh_rate = mode.refresh_rate
        else:
            refresh_rate = 0
        
        display_info = {
            'index': i,
            'name': display_name,
            'resolution': resolution,
            'position': position,
            'refresh_rate': refresh_rate,
            'bounds': bounds
        }
        displays.append(display_info)
        
        print(f"  [{i+1}] {display_name}")
        print(f"      Resolución: {resolution} @ {refresh_rate}Hz")
        print(f"      Posición: {position}")
    
    return displays

def select_display(displays):
    """Permite al usuario seleccionar un display"""
    if len(displays) == 0:
        print("[HDMI] Error: No se encontraron displays")
        return None
    
    if len(displays) == 1:
        print(f"\n[HDMI] Solo hay un display disponible, usando: {displays[0]['name']}")
        return displays[0]
    
    print("\n[HDMI] Selecciona el display HDMI donde enviar la imagen:")
    print("[HDMI] Normalmente el display 1 es el principal y 2+ son externos")
    
    while True:
        try:
            choice = input(f"\nIngresa el número del display (1-{len(displays)}): ")
            idx = int(choice) - 1
            if 0 <= idx < len(displays):
                selected = displays[idx]
                print(f"\n[HDMI] Display seleccionado: {selected['name']}")
                return selected
            else:
                print(f"[HDMI] Por favor ingresa un número entre 1 y {len(displays)}")
        except ValueError:
            print("[HDMI] Por favor ingresa un número válido")
        except KeyboardInterrupt:
            print("\n[HDMI] Operación cancelada")
            return None

def main():
    """Función principal"""
    # Obtener directorio del ejecutable
    exe_dir = get_executable_dir()
    image_bin_path = os.path.join(exe_dir, IMAGE_FILENAME)
    
    print("=" * 60)
    print("HDMI Image Visualizer")
    print("=" * 60)
    print(f"[HDMI] Directorio: {exe_dir}")
    print(f"[HDMI] Buscando archivo: {image_bin_path}")
    
    # Verificar que existe el archivo
    if not os.path.exists(image_bin_path):
        print(f"\n[HDMI] Error: No se encontró el archivo '{IMAGE_FILENAME}'")
        print(f"[HDMI] Asegúrate de que esté en: {exe_dir}")
        input("\nPresiona Enter para salir...")
        return
    
    # Verificar tamaño
    expected_size = WIDTH * HEIGHT * 3
    file_size = os.path.getsize(image_bin_path)
    if file_size != expected_size:
        print(f"\n[HDMI] Advertencia: Tamaño inesperado")
        print(f"  Actual: {file_size} bytes")
        print(f"  Esperado: {expected_size} bytes")
    
    # Inicializar SDL2
    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        print(f"[HDMI] Error inicializando SDL2: {sdl2.SDL_GetError()}")
        return
    
    try:
        # Detectar displays
        displays = detect_displays()
        if not displays:
            print("[HDMI] No se detectaron displays")
            return
        
        # Seleccionar display
        selected_display = select_display(displays)
        if not selected_display:
            return
        
        # Crear ventana fullscreen en el display seleccionado
        print(f"\n[HDMI] Creando ventana en {selected_display['name']}...")
        
        # Posición de la ventana en el display seleccionado
        window_x = selected_display['bounds'].x + 50  # Pequeño offset
        window_y = selected_display['bounds'].y + 50
        
        # Crear ventana
        window = sdl2.SDL_CreateWindow(
            WINDOW_TITLE.encode('utf-8'),
            window_x, window_y,
            WIDTH, HEIGHT,
            sdl2.SDL_WINDOW_SHOWN | sdl2.SDL_WINDOW_ALWAYS_ON_TOP
        )
        
        if not window:
            print(f"[HDMI] Error creando ventana: {sdl2.SDL_GetError()}")
            return
        
        # Crear renderer
        renderer = sdl2.SDL_CreateRenderer(
            window, -1,
            sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC
        )
        
        if not renderer:
            print(f"[HDMI] Error creando renderer: {sdl2.SDL_GetError()}")
            sdl2.SDL_DestroyWindow(window)
            return
        
        # Crear textura para la imagen
        texture = sdl2.SDL_CreateTexture(
            renderer,
            sdl2.SDL_PIXELFORMAT_RGB24,
            sdl2.SDL_TEXTUREACCESS_STREAMING,
            WIDTH, HEIGHT
        )
        
        if not texture:
            print(f"[HDMI] Error creando textura: {sdl2.SDL_GetError()}")
            sdl2.SDL_DestroyRenderer(renderer)
            sdl2.SDL_DestroyWindow(window)
            return
        
        # Iniciar lector de imagen
        reader = ImageReader(WIDTH, HEIGHT)
        reader.start(image_bin_path)
        
        # Esperar un momento
        time.sleep(0.5)
        
        print(f"\n[HDMI] Transmitiendo a {selected_display['name']}...")
        print("[HDMI] Presiona Ctrl+C para salir")
        print("[HDMI] Presiona F para alternar pantalla completa")
        
        # Variables de control
        running = True
        fullscreen = False
        clock_start = time.time()
        frame_count = 0
        
        # Event loop
        event = sdl2.SDL_Event()
        
        while running:
            # Procesar eventos
            while sdl2.SDL_PollEvent(event) != 0:
                if event.type == sdl2.SDL_QUIT:
                    running = False
                elif event.type == sdl2.SDL_KEYDOWN:
                    if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                        running = False
                    elif event.key.keysym.sym == sdl2.SDLK_f:
                        # Alternar fullscreen
                        fullscreen = not fullscreen
                        if fullscreen:
                            sdl2.SDL_SetWindowFullscreen(window, sdl2.SDL_WINDOW_FULLSCREEN)
                        else:
                            sdl2.SDL_SetWindowFullscreen(window, 0)
            
            # Obtener frame
            frame_data = reader.get_frame()
            if frame_data:
                # Actualizar textura con los datos RGB
                pixels = ctypes.c_void_p()   # ② reserva puntero vacío
                pitch = sdl2.c_int()
                
                if sdl2.SDL_LockTexture(
                        texture,
                        None,
                        ctypes.byref(pixels),   # ③ usa ctypes.byref   ⬅⬅
                        ctypes.byref(pitch)):   #     idem
                    # SDL devolvió ≠ 0  →  error
                    print(f"[HDMI] Error al hacer lock de la textura: {sdl2.SDL_GetError().decode()}")
                else:
                    expected_pitch = WIDTH * 3
                    fb_ptr = pixels.value      # dirección del framebuffer en C

                    # Copia directa si el pitch coincide
                    if pitch.value == expected_pitch:
                        ctypes.memmove(fb_ptr, frame_data, len(frame_data))  # ④
                    else:
                        # Copia línea por línea si el stride es distinto
                        for y in range(HEIGHT):
                            src = ctypes.addressof(ctypes.c_char.from_buffer(frame_data, y * expected_pitch))
                            dst = fb_ptr + y * pitch.value
                            ctypes.memmove(dst, src, expected_pitch)

                    sdl2.SDL_UnlockTexture(texture)

                    # Render
                    sdl2.SDL_RenderClear(renderer)
                    sdl2.SDL_RenderCopy(renderer, texture, None, None)
                    sdl2.SDL_RenderPresent(renderer)
                    
                    frame_count += 1
            
            # Mostrar FPS cada segundo
            current_time = time.time()
            if current_time - clock_start >= 1.0:
                fps = frame_count / (current_time - clock_start)
                print(f"\r[HDMI] FPS: {fps:.1f}", end='', flush=True)
                clock_start = current_time
                frame_count = 0
            
            # Limitar FPS
            sdl2.SDL_Delay(int(1000 / FPS))
        
        print("\n\n[HDMI] Cerrando...")
        
        # Limpiar
        reader.stop()
        sdl2.SDL_DestroyTexture(texture)
        sdl2.SDL_DestroyRenderer(renderer)
        sdl2.SDL_DestroyWindow(window)
        
    except KeyboardInterrupt:
        print("\n\n[HDMI] Interrupción por usuario")
    except Exception as e:
        print(f"\n[HDMI] Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        sdl2.SDL_Quit()
        
    print("[HDMI] Programa terminado")

if __name__ == "__main__":
    main()