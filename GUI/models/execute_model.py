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
        self.client_process = None

    # ──────────────────────────────────────────────────────────────
    #  Ejecutar Client_execute.exe
    # ──────────────────────────────────────────────────────────────
    def execute_client(self) -> bool:
        """
        Execute the Client_execute.exe launcher
        """
        try:
            # Ruta al Client_execute.exe
            client_path = os.path.join(BASE_DIR, "out", "Client_execute.exe")
            
            # Verificar que existe el ejecutable
            if not os.path.exists(client_path):
                print(f"Error: Client_execute.exe not found at {client_path}")
                print("Please ensure Client_execute.exe is built and placed in the out/ directory.")
                return False

            # Comandos a ejecutar en el terminal
            cmds = [
                f"cd {os.path.join(BASE_DIR, 'out')}",
                f"echo 'Launching vGraph Client...'",
                f"echo '─────────────────────────────────'",
                f"./Client_execute.exe",
                f"echo '─────────────────────────────────'",
                f"echo 'Client launcher finished.'",
                "echo 'Press Enter to close'; read"
            ]
            bash_cmd = " && ".join(cmds)

            # Verificar disponibilidad de gnome-terminal
            if subprocess.run(["which", "gnome-terminal"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
                print("Warning: gnome-terminal not available. Running in current terminal...")
                # Fallback: ejecutar directamente
                try:
                    result = subprocess.run(client_path, cwd=os.path.join(BASE_DIR, "out"))
                    return result.returncode == 0
                except Exception as e:
                    print(f"Error running Client_execute.exe: {e}")
                    return False

            # Lanzar gnome-terminal
            self.client_process = subprocess.Popen(
                ["gnome-terminal", "--", "bash", "-c", bash_cmd]
            )
            print(f"Client_execute.exe launched in gnome-terminal")
            return True

        except Exception as e:
            print(f"Error executing Client_execute.exe: {e}")
            return False
        
    # ──────────────────────────────────────────────────────────────
    #  Ejecutar HDMI_execute.exe
    # ──────────────────────────────────────────────────────────────
    def execute_hdmi(self) -> bool:
        """
        Execute the HDMI_execute.exe launcher
        """
        try:
            # Ruta al HDMI_execute.exe
            hdmi_path = os.path.join(BASE_DIR, "out", "HDMI_execute.exe")
            
            # Verificar que existe el ejecutable
            if not os.path.exists(hdmi_path):
                print(f"Error: HDMI_execute.exe not found at {hdmi_path}")
                print("Please ensure HDMI_execute.exe is built and placed in the out/ directory.")
                return False

            # Comandos a ejecutar en el terminal
            cmds = [
                f"cd {os.path.join(BASE_DIR, 'out')}",
                f"echo 'Launching vGraph Client...'",
                f"echo '─────────────────────────────────'",
                f"./HDMI_execute.exe",
                f"echo '─────────────────────────────────'",
                f"echo 'Client launcher finished.'",
                "echo 'Press Enter to close'; read"
            ]
            bash_cmd = " && ".join(cmds)

            # Verificar disponibilidad de gnome-terminal
            if subprocess.run(["which", "gnome-terminal"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
                print("Warning: gnome-terminal not available. Running in current terminal...")
                # Fallback: ejecutar directamente
                try:
                    result = subprocess.run(hdmi_path, cwd=os.path.join(BASE_DIR, "out"))
                    return result.returncode == 0
                except Exception as e:
                    print(f"Error running HDMI_execute.exe: {e}")
                    return False

            # Lanzar gnome-terminal
            self.client_process = subprocess.Popen(
                ["gnome-terminal", "--", "bash", "-c", bash_cmd]
            )
            print(f"HDMI_execute.exe launched in gnome-terminal")
            return True

        except Exception as e:
            print(f"Error executing HDMI_execute.exe: {e}")
            return False