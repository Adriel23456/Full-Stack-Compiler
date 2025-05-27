#!/usr/bin/env python3
"""
Complete Setup script for Full Stack Compiler dependencies
Cross-platform compatible (Windows/Linux/MacOS)
Handles ALL program requirements including system packages and development tools
"""
import sys
import subprocess
import platform
import os
import urllib.request
import tempfile
import shutil
import json
from pathlib import Path

class ComprehensiveDependencyInstaller:
    def __init__(self):
        self.platform = platform.system().lower()
        self.is_windows = self.platform == 'windows'
        self.is_linux = self.platform == 'linux'
        self.is_mac = self.platform == 'darwin'
        
        # Get Linux distribution info
        self.linux_distro = None
        if self.is_linux:
            try:
                with open('/etc/os-release', 'r') as f:
                    for line in f:
                        if line.startswith('ID='):
                            self.linux_distro = line.split('=')[1].strip().strip('"')
                            break
            except:
                self.linux_distro = 'unknown'
        
        print(f"🖥️  Detected platform: {self.platform}")
        if self.is_linux:
            print(f"🐧 Linux distribution: {self.linux_distro}")
        print(f"🐍 Python version: {sys.version}")
        print("-" * 60)
        
        # Setup platform-specific paths
        self.setup_paths()
        
        # Track installation status
        self.installation_log = []
        self.failed_installations = []
    
    def setup_paths(self):
        """Setup platform-specific paths and commands"""
        if self.is_windows:
            self.temp_dir = tempfile.gettempdir()
            self.antlr_jar_path = os.path.join(self.temp_dir, 'antlr-4.9.2-complete.jar')
            self.home_dir = os.path.expanduser('~')
            self.profile_file = None  # Windows uses environment variables differently
        else:
            self.temp_dir = '/tmp'
            self.antlr_jar_path = '/tmp/antlr-4.9.2-complete.jar'
            self.home_dir = os.path.expanduser('~')
            self.profile_file = os.path.join(self.home_dir, '.bashrc')
    
    def log_status(self, message, success=True):
        """Log installation status"""
        status = "✅" if success else "❌"
        print(f"{status} {message}")
        self.installation_log.append((message, success))
        if not success:
            self.failed_installations.append(message)
    
    def run_command(self, cmd, shell=False, check=True, timeout=300):
        """Run a command safely with timeout"""
        try:
            if isinstance(cmd, str) and not shell:
                cmd = cmd.split()
            
            result = subprocess.run(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                check=check, 
                timeout=timeout,
                shell=shell
            )
            return result
        except subprocess.TimeoutExpired:
            print(f"⏰ Command timed out: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
            return None
        except subprocess.CalledProcessError as e:
            print(f"💥 Command failed: {e}")
            return None
        except FileNotFoundError:
            print(f"🔍 Command not found: {cmd[0] if isinstance(cmd, list) else cmd}")
            return None
    
    def check_python_version(self):
        """Check if Python version is compatible"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            self.log_status("Python 3.7+ is required", False)
            return False
        self.log_status("Python version is compatible")
        return True
    
    def install_python_packages(self):
        """Install all required Python packages"""
        print("\n🐍 Installing Python packages...")
        
        # Complete list of required packages with specific versions where needed
        packages = [
            'pygame',
            'llvmlite',
            'antlr4-python3-runtime==4.9.2',
            'pydot',
            'pyudev',
            'PySDL2',
            'PySDL2-dll'
        ]
        
        # Upgrade pip first
        print("📦 Upgrading pip...")
        result = self.run_command([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        if result and result.returncode == 0:
            self.log_status("pip upgraded successfully")
        else:
            self.log_status("Failed to upgrade pip", False)
        
        success_count = 0
        for package in packages:
            print(f"📦 Installing {package}...")
            result = self.run_command([sys.executable, '-m', 'pip', 'install', package])
            if result and result.returncode == 0:
                self.log_status(f"{package} installed successfully")
                success_count += 1
            else:
                self.log_status(f"Failed to install {package}", False)
        
        return success_count == len(packages)
    
    def install_linux_system_packages(self):
        """Install Linux system packages"""
        if not self.is_linux:
            return True
        
        print("\n🐧 Installing Linux system packages...")
        
        # Detect package manager
        package_managers = {
            'apt': ['ubuntu', 'debian', 'mint'],
            'yum': ['centos', 'rhel'],
            'dnf': ['fedora'],
            'pacman': ['arch', 'manjaro'],
            'zypper': ['opensuse', 'suse']
        }
        
        pm = None
        for manager, distros in package_managers.items():
            if any(d in self.linux_distro.lower() for d in distros):
                pm = manager
                break
        
        if not pm:
            pm = 'apt'  # Default fallback
            print(f"⚠️  Unknown distribution, trying {pm}")
        
        print(f"📦 Using package manager: {pm}")
        
        # Package lists for different package managers
        packages = {
            'apt': [
                'default-jre',
                'xclip', 
                'gnome-terminal',
                'libsdl2-dev',
                'libsdl2-image-dev', 
                'libsdl2-ttf-dev',
                'clang',
                'gcc',
                'g++',
                'libdrm-dev',
                'graphviz',  # For pydot
                'build-essential',  # General build tools
                'cmake',  # Often needed for building
                'pkg-config'  # Package configuration
            ],
            'yum': [
                'java-11-openjdk',
                'xclip',
                'gnome-terminal', 
                'SDL2-devel',
                'SDL2_image-devel',
                'SDL2_ttf-devel',
                'clang',
                'gcc',
                'gcc-c++',
                'libdrm-devel',
                'graphviz',
                'cmake',
                'pkgconfig'
            ],
            'dnf': [
                'java-11-openjdk',
                'xclip',
                'gnome-terminal',
                'SDL2-devel', 
                'SDL2_image-devel',
                'SDL2_ttf-devel',
                'clang',
                'gcc',
                'gcc-c++',
                'libdrm-devel',
                'graphviz',
                'cmake',
                'pkgconf-pkg-config'
            ],
            'pacman': [
                'jre-openjdk',
                'xclip',
                'gnome-terminal',
                'sdl2',
                'sdl2_image', 
                'sdl2_ttf',
                'clang',
                'gcc',
                'libdrm',
                'graphviz',
                'cmake',
                'pkgconfig'
            ]
        }
        
        if pm not in packages:
            print(f"❌ Unsupported package manager: {pm}")
            return False
        
        package_list = packages[pm]
        
        # Update package lists first
        print("🔄 Updating package lists...")
        if pm == 'apt':
            update_cmd = ['sudo', 'apt', 'update']
        elif pm == 'yum':
            update_cmd = ['sudo', 'yum', 'makecache']
        elif pm == 'dnf':
            update_cmd = ['sudo', 'dnf', 'makecache']
        elif pm == 'pacman':
            update_cmd = ['sudo', 'pacman', '-Sy']
        
        result = self.run_command(update_cmd)
        if result and result.returncode == 0:
            self.log_status("Package lists updated")
        else:
            self.log_status("Failed to update package lists", False)
        
        # Install packages
        success_count = 0
        for package in package_list:
            print(f"📦 Installing {package}...")
            
            if pm == 'apt':
                install_cmd = ['sudo', 'apt', 'install', '-y', package]
            elif pm in ['yum', 'dnf']:
                install_cmd = ['sudo', pm, 'install', '-y', package]
            elif pm == 'pacman':
                install_cmd = ['sudo', 'pacman', '-S', '--noconfirm', package]
            
            result = self.run_command(install_cmd)
            if result and result.returncode == 0:
                self.log_status(f"{package} installed successfully")
                success_count += 1
            else:
                self.log_status(f"Failed to install {package}", False)
        
        return success_count > (len(package_list) * 0.8)  # 80% success rate
    
    def install_windows_dependencies(self):
        """Install Windows-specific dependencies"""
        if not self.is_windows:
            return True
        
        print("\n🖥️  Setting up Windows dependencies...")
        
        # Check for Java
        java_result = self.run_command(['java', '-version'])
        if not java_result:
            self.log_status("Java not found - please install manually", False)
            print("📋 Download Java from: https://adoptium.net/")
        else:
            self.log_status("Java is available")
        
        # Check for Visual Studio Build Tools or similar
        compilers = ['cl', 'gcc', 'clang']
        compiler_found = False
        for compiler in compilers:
            result = self.run_command([compiler, '--version'])
            if result:
                self.log_status(f"Compiler {compiler} is available")
                compiler_found = True
                break
        
        if not compiler_found:
            self.log_status("No compiler found", False)
            print("📋 Install Visual Studio Build Tools or MinGW-w64")
            print("   Visual Studio: https://visualstudio.microsoft.com/downloads/")
            print("   MinGW-w64: https://www.mingw-w64.org/downloads/")
        
        # Check for Git (often needed)
        git_result = self.run_command(['git', '--version'])
        if git_result:
            self.log_status("Git is available")
        else:
            self.log_status("Git not found - install from https://git-scm.com/", False)
        
        return True
    
    def install_macos_dependencies(self):
        """Install macOS-specific dependencies"""
        if not self.is_mac:
            return True
        
        print("\n🍎 Setting up macOS dependencies...")
        
        # Check for Homebrew
        brew_result = self.run_command(['brew', '--version'])
        if not brew_result:
            print("🍺 Homebrew not found. Installing...")
            install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            result = self.run_command(install_cmd, shell=True)
            if result and result.returncode == 0:
                self.log_status("Homebrew installed successfully")
            else:
                self.log_status("Failed to install Homebrew", False)
                return False
        else:
            self.log_status("Homebrew is available")
        
        # Install packages via Homebrew
        packages = [
            'openjdk',
            'sdl2',
            'sdl2_image',
            'sdl2_ttf', 
            'llvm',
            'graphviz',
            'cmake'
        ]
        
        for package in packages:
            print(f"🍺 Installing {package}...")
            result = self.run_command(['brew', 'install', package])
            if result and result.returncode == 0:
                self.log_status(f"{package} installed successfully")
            else:
                self.log_status(f"Failed to install {package}", False)
        
        # Check for Xcode command line tools
        xcode_result = self.run_command(['xcode-select', '--print-path'])
        if xcode_result:
            self.log_status("Xcode command line tools are available")
        else:
            print("🔧 Installing Xcode command line tools...")
            result = self.run_command(['xcode-select', '--install'])
            self.log_status("Xcode command line tools installation started")
        
        return True
    
    def download_antlr_jar(self):
        """Download ANTLR jar file"""
        print("\n☕ Setting up ANTLR...")
        
        if os.path.exists(self.antlr_jar_path):
            self.log_status(f"ANTLR jar already exists at: {self.antlr_jar_path}")
            return True
        
        print("📥 Downloading ANTLR jar file...")
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.antlr_jar_path), exist_ok=True)
            
            url = 'https://www.antlr.org/download/antlr-4.9.2-complete.jar'
            urllib.request.urlretrieve(url, self.antlr_jar_path)
            self.log_status(f"ANTLR jar downloaded to: {self.antlr_jar_path}")
            return True
        except Exception as e:
            self.log_status(f"Failed to download ANTLR jar: {e}", False)
            return False
    
    def setup_antlr_environment(self):
        """Setup ANTLR environment variables and aliases"""
        if not os.path.exists(self.antlr_jar_path):
            self.log_status("ANTLR jar not found, skipping environment setup", False)
            return False
        
        print("\n⚙️  Setting up ANTLR environment...")
        
        if self.is_windows:
            # For Windows, we'll provide instructions since modifying system env vars requires admin
            print("📋 Windows Environment Setup Instructions:")
            print(f"   1. Add to CLASSPATH: .;{self.antlr_jar_path}")
            print("   2. Add these to your PATH or create batch files:")
            print(f"      antlr4.bat: java -jar {self.antlr_jar_path} %*")
            print(f"      grun.bat: java org.antlr.v4.gui.TestRig %*")
            self.log_status("Windows environment instructions provided")
            return True
        
        else:
            # Linux/Mac - modify .bashrc or .zshrc
            shell = os.environ.get('SHELL', '/bin/bash')
            if 'zsh' in shell:
                profile_file = os.path.join(self.home_dir, '.zshrc')
            else:
                profile_file = self.profile_file
            
            if not profile_file or not os.path.exists(os.path.dirname(profile_file)):
                self.log_status("Shell profile file not found", False)
                return False
            
            # Read existing profile
            existing_content = ""
            if os.path.exists(profile_file):
                with open(profile_file, 'r') as f:
                    existing_content = f.read()
            
            # Check if ANTLR setup already exists
            if 'antlr-4.9.2-complete.jar' in existing_content:
                self.log_status("ANTLR environment already configured")
                return True
            
            # Add ANTLR configuration
            antlr_config = f'''
# ANTLR Configuration (added by Full Stack Compiler setup)
export CLASSPATH=".:{self.antlr_jar_path}:$CLASSPATH"
alias antlr4="java -jar {self.antlr_jar_path}"
alias grun="java org.antlr.v4.gui.TestRig"
'''
            
            try:
                with open(profile_file, 'a') as f:
                    f.write(antlr_config)
                self.log_status(f"ANTLR environment added to {profile_file}")
                
                # Try to source the profile (may not work in all terminals)
                source_cmd = f"source {profile_file}"
                self.run_command(source_cmd, shell=True, check=False)
                
                print(f"🔄 Please run: source {profile_file}")
                print("   Or restart your terminal for changes to take effect")
                return True
            except Exception as e:
                self.log_status(f"Failed to update {profile_file}: {e}", False)
                return False
    
    def verify_installation(self):
        """
        Verify that key components are working **y** asegúrate de que los
        binarios indicados tengan permisos de ejecución en Linux.
        """
        print("\n🔍 Verifying installation...")

        # ── 1) Pruebas de importación de módulos Python ─────────────────────
        python_modules = ['pygame', 'llvmlite', 'antlr4', 'pydot']
        for module in python_modules:
            try:
                __import__(module)
                self.log_status(f"Python module {module} imports successfully")
            except ImportError:
                self.log_status(f"Python module {module} failed to import", False)

        # ── 2) Verificar Java / ANTLR ───────────────────────────────────────
        java_result = self.run_command(['java', '-version'])
        self.log_status("Java is working" if java_result else "Java is not working", bool(java_result))

        if os.path.exists(self.antlr_jar_path):
            antlr_test = self.run_command(['java', '-jar', self.antlr_jar_path], check=False)
            self.log_status("ANTLR jar is accessible" if antlr_test else "ANTLR jar test failed", bool(antlr_test))
        else:
            self.log_status("ANTLR jar not found", False)

        # ── 3) Asegurar permisos de ejecución en Linux ─────────────────────
        if self.is_linux:
            print("\n🔧 Ensuring execute permissions on generated binaries...")
            binaries = [
                Path("out/Client_execute_linux"),
                Path("out/Client_visualizer.exe"),
                Path("out/HDMI_execute_linux"),
                Path("out/HDMI_visualizer.exe"),
                Path("out/vGraph.exe")
            ]

            for bin_path in binaries:
                try:
                    if bin_path.exists():
                        # Añade bits de ejecución (u+rwx,g+rx,o+rx)
                        bin_path.chmod(bin_path.stat().st_mode | 0o755)
                        self.log_status(f"Set +x : {bin_path}")
                    else:
                        self.log_status(f"File not found (skip chmod): {bin_path}", False)
                except Exception as e:
                    self.log_status(f"chmod failed for {bin_path}: {e}", False)

        # ── 4) Resultado final ─────────────────────────────────────────────
        return len(self.failed_installations) == 0
    
    def print_summary(self):
        """Print installation summary"""
        print("\n" + "=" * 60)
        print("📊 INSTALLATION SUMMARY")
        print("=" * 60)
        
        success_count = sum(1 for _, success in self.installation_log if success)
        total_count = len(self.installation_log)
        
        print(f"✅ Successful: {success_count}/{total_count}")
        if self.failed_installations:
            print(f"❌ Failed: {len(self.failed_installations)}")
            print("\nFailed installations:")
            for failure in self.failed_installations:
                print(f"   • {failure}")
        
        if len(self.failed_installations) == 0:
            print("\n🎉 ALL DEPENDENCIES INSTALLED SUCCESSFULLY!")
            print("Your Full Stack Compiler should now work perfectly!")
        elif len(self.failed_installations) < total_count * 0.3:  # Less than 30% failed
            print("\n✅ SETUP MOSTLY SUCCESSFUL!")
            print("Most dependencies are installed. Check failed items above.")
        else:
            print("\n⚠️  SETUP COMPLETED WITH ISSUES")
            print("Several dependencies failed to install. Manual intervention may be required.")
        
        print("\n💡 Next steps:")
        print("1. Restart your terminal/IDE")
        print("2. Run your Full Stack Compiler:")
        print("   python main.py")
        if self.is_linux:
            print("3. If ANTLR commands don't work, run: source ~/.bashrc")
        print("4. Re-run this setup script to check for remaining issues")
    
    def run_complete_setup(self):
        """Run the complete setup process"""
        print("🚀 FULL STACK COMPILER - COMPREHENSIVE SETUP")
        print("=" * 60)
        
        # Step 1: Check Python
        if not self.check_python_version():
            return False
        
        # Step 2: Install system packages (platform-specific)
        if self.is_linux:
            self.install_linux_system_packages()
        elif self.is_windows:
            self.install_windows_dependencies()
        elif self.is_mac:
            self.install_macos_dependencies()
        
        # Step 3: Install Python packages
        self.install_python_packages()
        
        # Step 4: Setup ANTLR
        self.download_antlr_jar()
        self.setup_antlr_environment()
        
        # Step 5: Verify installation
        verification_success = self.verify_installation()
        
        # Step 6: Print summary
        self.print_summary()
        
        return verification_success

def main():
    """Main function"""
    installer = ComprehensiveDependencyInstaller()
    
    # Ask for confirmation on Linux/Mac since sudo is required
    if installer.is_linux or installer.is_mac:
        response = input("\n❓ This script will install system packages using sudo. Continue? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("❌ Setup cancelled by user")
            return
    
    success = installer.run_complete_setup()
    return success

if __name__ == "__main__":
    main()