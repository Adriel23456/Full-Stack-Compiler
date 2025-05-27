# File: GUI/models/execute_model.py
"""
Model for executing compiler and image viewer
Handles launching external programs in separate terminals
Cross-platform compatible (Windows/Linux/MacOS)
"""
import os
import subprocess
import tempfile
import platform
import sys
from config import BASE_DIR

class ExecuteModel:
    """
    Model for executing compiler and image viewer
    Cross-platform compatible
    """

    def __init__(self):
        """
        Initialize the execute model with platform detection
        """
        self.client_process = None
        
        # Detect operating system
        self.platform = platform.system().lower()
        self.is_windows = self.platform == 'windows'
        self.is_linux = self.platform == 'linux'
        self.is_mac = self.platform == 'darwin'
        
        # Set executable names based on platform
        if self.is_windows:
            self.client_executable = "Client_execute_windows.exe"
            self.hdmi_executable = "HDMI_execute_windows.exe"
        elif self.is_linux:
            self.client_executable = "Client_execute_linux"
            self.hdmi_executable = "HDMI_execute_linux"
        else:
            # For macOS and other unsupported platforms
            self.client_executable = None
            self.hdmi_executable = None
        
        print(f"Platform detected: {platform.system()}")

    # ──────────────────────────────────────────────────────────────
    #  Platform-specific terminal launcher
    # ──────────────────────────────────────────────────────────────
    def _launch_in_terminal(self, executable_path: str, title: str) -> bool:
        """
        Launch executable in platform-specific terminal
        """
        try:
            out_dir = os.path.join(BASE_DIR, 'out')
            
            if self.is_windows:
                # Windows: Use cmd.exe with proper path handling
                # Get just the executable name
                exe_name = os.path.basename(executable_path)
                
                # Create a batch script to handle the execution properly
                batch_content = f"""@echo off
cd /d "{out_dir}"
echo Launching {title}...
echo ==============================
"{exe_name}"
echo ==============================
echo {title} finished.
echo Press any key to close...
pause > nul
"""
                
                # Create temporary batch file
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.bat', delete=False) as batch_file:
                    batch_file.write(batch_content)
                    batch_path = batch_file.name
                
                try:
                    # Execute the batch file
                    process = subprocess.Popen(
                        [batch_path],
                        creationflags=subprocess.CREATE_NEW_CONSOLE if hasattr(subprocess, 'CREATE_NEW_CONSOLE') else 0,
                        shell=True
                    )
                    
                    # Clean up batch file after a delay (let it start first)
                    import threading
                    def cleanup():
                        import time
                        time.sleep(2)
                        try:
                            os.unlink(batch_path)
                        except:
                            pass
                    threading.Thread(target=cleanup, daemon=True).start()
                    
                    return True
                except Exception as e:
                    print(f"Error executing batch file: {e}")
                    # Try direct execution as fallback
                    try:
                        os.unlink(batch_path)
                    except:
                        pass
                    
                    # Fallback: Direct execution with START command
                    try:
                        cmd = f'start "vGraph {title}" /D "{out_dir}" /WAIT "{exe_name}"'
                        subprocess.Popen(cmd, shell=True, cwd=out_dir)
                        return True
                    except Exception as e2:
                        print(f"Fallback execution also failed: {e2}")
                        return False
                    
            elif self.is_linux:
                # Linux: Try different terminal emulators in order of preference
                terminals = [
                    ('gnome-terminal', ['gnome-terminal', '--', 'bash', '-c']),
                    ('konsole', ['konsole', '-e', 'bash', '-c']),
                    ('xfce4-terminal', ['xfce4-terminal', '-e', 'bash -c']),
                    ('xterm', ['xterm', '-e', 'bash', '-c']),
                    ('terminator', ['terminator', '-e', 'bash -c'])
                ]
                
                # Commands to execute in terminal
                bash_commands = [
                    f'cd "{out_dir}"',
                    f'echo "Launching {title}..."',
                    f'echo "{"─" * 30}"',
                    f'"{executable_path}"',
                    f'echo "{"─" * 30}"',
                    f'echo "{title} finished."',
                    'echo "Press Enter to close"',
                    'read'
                ]
                bash_script = ' && '.join(bash_commands)
                
                # Try each terminal until one works
                for term_name, term_cmd in terminals:
                    # Check if terminal is available
                    check_result = subprocess.run(
                        ['which', term_cmd[0]], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE
                    )
                    
                    if check_result.returncode == 0:
                        try:
                            # Adjust command based on terminal
                            if term_name in ['xterm', 'xfce4-terminal', 'terminator']:
                                # These terminals need the command as a single string
                                full_cmd = term_cmd[:-1] + [f'{term_cmd[-1]} "{bash_script}"']
                            else:
                                # Others take the script as a separate argument
                                full_cmd = term_cmd + [bash_script]
                            
                            process = subprocess.Popen(full_cmd)
                            return True
                        except Exception as e:
                            print(f"Failed to launch in {term_name}: {e}")
                            continue
                
                # If no terminal works, try direct execution
                print("Warning: No terminal emulator found. Running directly...")
                process = subprocess.run(
                    executable_path, 
                    cwd=out_dir,
                    shell=False
                )
                return process.returncode == 0
                
            else:
                # macOS and other platforms not yet implemented
                print(f"OS {platform.system()} integration: Not yet implemented")
                return False
                
        except Exception as e:
            print(f"Error launching in terminal: {e}")
            return False

    # ──────────────────────────────────────────────────────────────
    #  Execute Client executable
    # ──────────────────────────────────────────────────────────────
    def execute_client(self) -> bool:
        """
        Execute the Client launcher (cross-platform)
        """
        try:
            # Check if platform is supported
            if self.client_executable is None:
                print(f"OS {platform.system()} integration: Not yet implemented")
                return False
            
            # Build path to executable
            client_path = os.path.join(BASE_DIR, "out", self.client_executable)
            
            # Verify executable exists
            if not os.path.exists(client_path):
                print(f"Error: {self.client_executable} not found at {client_path}")
                print(f"Please ensure {self.client_executable} is built and placed in the out/ directory.")
                return False
            
            # Make sure it's executable on Unix-like systems
            if self.is_linux or self.is_mac:
                try:
                    os.chmod(client_path, 0o755)
                except:
                    pass
            
            # Launch in terminal
            return self._launch_in_terminal(client_path, "vGraph Client")

        except Exception as e:
            print(f"Error executing client: {e}")
            return False
        
    # ──────────────────────────────────────────────────────────────
    #  Execute HDMI executable
    # ──────────────────────────────────────────────────────────────
    def execute_hdmi(self) -> bool:
        """
        Execute the HDMI launcher (cross-platform)
        """
        try:
            # Check if platform is supported
            if self.hdmi_executable is None:
                print(f"OS {platform.system()} integration: Not yet implemented")
                return False
            
            # Build path to executable
            hdmi_path = os.path.join(BASE_DIR, "out", self.hdmi_executable)
            
            # Verify executable exists
            if not os.path.exists(hdmi_path):
                print(f"Error: {self.hdmi_executable} not found at {hdmi_path}")
                print(f"Please ensure {self.hdmi_executable} is built and placed in the out/ directory.")
                return False
            
            # Make sure it's executable on Unix-like systems
            if self.is_linux or self.is_mac:
                try:
                    os.chmod(hdmi_path, 0o755)
                except:
                    pass
            
            # Launch in terminal
            return self._launch_in_terminal(hdmi_path, "vGraph HDMI")

        except Exception as e:
            print(f"Error executing HDMI: {e}")
            return False