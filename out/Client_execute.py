#!/usr/bin/env python3
"""
Client_execute.py - Lanzador automático de vGraph y Client_visualizer
Este programa busca y ejecuta vGraph.exe y Client_visualizer.exe en su mismo directorio
"""

import os
import sys
import subprocess
import time
import platform

def get_executable_dir():
    """Obtiene el directorio donde se encuentra este ejecutable/script"""
    if getattr(sys, 'frozen', False):
        # Si es un ejecutable compilado con PyInstaller
        return os.path.dirname(sys.executable)
    else:
        # Si es un script Python normal
        return os.path.dirname(os.path.abspath(__file__))

def check_files_exist(exe_dir):
    """Verifica que existan los ejecutables necesarios"""
    vgraph_path = os.path.join(exe_dir, "vGraph.exe")
    visualizer_path = os.path.join(exe_dir, "Client_visualizer.exe")
    
    print(f"[Client] Directorio actual: {exe_dir}")
    print(f"[Client] Buscando archivos...")
    
    # Verificar vGraph.exe
    if not os.path.exists(vgraph_path):
        print(f"[Error] No se encontró vGraph.exe")
        print(f"        Ruta esperada: {vgraph_path}")
        return False, None, None
    else:
        print(f"[OK] vGraph.exe encontrado")
    
    # Verificar Client_visualizer.exe
    if not os.path.exists(visualizer_path):
        print(f"[Error] No se encontró Client_visualizer.exe")
        print(f"        Ruta esperada: {visualizer_path}")
        return False, None, None
    else:
        print(f"[OK] Client_visualizer.exe encontrado")
    
    return True, vgraph_path, visualizer_path

def launch_in_terminal(exe_path, title="Terminal"):
    """Lanza un ejecutable en una nueva terminal"""
    system = platform.system()
    
    try:
        if system == "Linux":
            # Intentar con gnome-terminal primero
            if subprocess.run(["which", "gnome-terminal"], 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE).returncode == 0:
                # Comandos para gnome-terminal
                cmd = [
                    "gnome-terminal",
                    "--title", title,
                    "--", "bash", "-c",
                    f"cd '{os.path.dirname(exe_path)}' && '{exe_path}'; echo 'Presiona Enter para cerrar'; read"
                ]
                subprocess.Popen(cmd)
                return True
            
            # Intentar con xterm
            elif subprocess.run(["which", "xterm"], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE).returncode == 0:
                cmd = [
                    "xterm",
                    "-title", title,
                    "-e", f"bash -c 'cd \"{os.path.dirname(exe_path)}\" && \"{exe_path}\"; echo \"Presiona Enter para cerrar\"; read'"
                ]
                subprocess.Popen(cmd)
                return True
            
            # Intentar con konsole (KDE)
            elif subprocess.run(["which", "konsole"], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE).returncode == 0:
                cmd = [
                    "konsole",
                    "--title", title,
                    "-e", f"bash -c 'cd \"{os.path.dirname(exe_path)}\" && \"{exe_path}\"; echo \"Presiona Enter para cerrar\"; read'"
                ]
                subprocess.Popen(cmd)
                return True
            
            else:
                # Si no hay terminal gráfica, ejecutar en background
                print(f"[Advertencia] No se encontró terminal gráfica, ejecutando en background")
                subprocess.Popen([exe_path], cwd=os.path.dirname(exe_path))
                return True
                
        elif system == "Windows":
            # En Windows, usar start con cmd
            cmd = [
                "cmd", "/c", "start", title,
                "cmd", "/k", f"cd /d \"{os.path.dirname(exe_path)}\" && \"{exe_path}\""
            ]
            subprocess.Popen(cmd, shell=True)
            return True
            
        elif system == "Darwin":  # macOS
            # Usar Terminal.app en macOS
            script = f'''
            tell app "Terminal"
                do script "cd '{os.path.dirname(exe_path)}' && '{exe_path}'"
                set custom title of window 1 to "{title}"
            end tell
            '''
            subprocess.Popen(["osascript", "-e", script])
            return True
            
        else:
            print(f"[Error] Sistema operativo no soportado: {system}")
            return False
            
    except Exception as e:
        print(f"[Error] No se pudo lanzar {exe_path}: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("Client Execute - Lanzador de vGraph")
    print("=" * 60)
    
    # Obtener directorio actual
    exe_dir = get_executable_dir()
    
    # Verificar que existan los archivos
    exists, vgraph_path, visualizer_path = check_files_exist(exe_dir)
    
    if not exists:
        print("\n[Error] No se encontraron todos los archivos necesarios.")
        print("Asegúrate de que vGraph.exe y Client_visualizer.exe estén en el mismo")
        print(f"directorio que este programa: {exe_dir}")
        input("\nPresiona Enter para salir...")
        return 1
    
    print("\n[Client] Iniciando procesos...")
    
    # Lanzar vGraph.exe
    print("[Client] Lanzando vGraph.exe...")
    if launch_in_terminal(vgraph_path, "vGraph Engine"):
        print("[OK] vGraph.exe lanzado correctamente")
    else:
        print("[Error] No se pudo lanzar vGraph.exe")
        input("\nPresiona Enter para salir...")
        return 1
    
    # Lanzar Client_visualizer.exe
    print("[Client] Lanzando Client_visualizer.exe...")
    if launch_in_terminal(visualizer_path, "vGraph Client_visualizer"):
        print("[OK] Client_visualizer.exe lanzado correctamente")
    else:
        print("[Error] No se pudo lanzar Client_visualizer.exe")
        input("\nPresiona Enter para salir...")
        return 1
    
    print("\n" + "=" * 60)
    print("✓ Ambos procesos se han lanzado correctamente")
    print("✓ Este lanzador se cerrará automáticamente en 3 segundos...")
    print("✓ Los procesos vGraph y Client_visualizer continuarán ejecutándose")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[Client] Operación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n[Error fatal] {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para salir...")
        sys.exit(1)