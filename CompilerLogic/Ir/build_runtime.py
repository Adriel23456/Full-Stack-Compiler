#!/usr/bin/env python3
"""
Build script for VGraph runtime library
Cross-platform compatible (Windows/Linux/MacOS)
Replaces build_runtime.sh with Python for better cross-platform support
"""
import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

class RuntimeBuilder:
    """
    Cross-platform runtime builder for VGraph
    """
    def __init__(self):
        # Platform detection
        self.platform = platform.system().lower()
        self.is_windows = self.platform == 'windows'
        self.is_linux = self.platform == 'linux'
        self.is_mac = self.platform == 'darwin'
        
        # Get script directory
        self.script_dir = Path(__file__).parent.absolute()
        
        # File paths
        plat_tag = self.platform                  # windows | linux | darwin
        self.runtime_c  = self.script_dir / "runtime.c"
        self.runtime_o  = self.script_dir / f"runtime_{plat_tag}.o"
        self.runtime_lib = self.script_dir / f"libvgraphrt_{plat_tag}.a"

        
        print(f"[Build] VGraph Runtime Builder")
        print(f"[Build] Platform: {self.platform}")
        print(f"[Build] Script directory: {self.script_dir}")
        
        # Detect build tools
        self.compiler = self._detect_compiler()
        self.archiver = self._detect_archiver()
    
    def _detect_compiler(self):
        """Detect available C compiler"""
        compilers = ['clang', 'gcc', 'cl']  # Order of preference
        
        for compiler in compilers:
            if self._command_exists(compiler):
                print(f"[Build] Found compiler: {compiler}")
                return compiler
        
        print("[Build] ERROR: No C compiler found")
        print("[Build] Please install one of: clang, gcc, or Visual Studio Build Tools")
        return None
    
    def _detect_archiver(self):
        """Detect available archiver"""
        archivers = ['ar', 'llvm-ar', 'lib']
        
        for archiver in archivers:
            if self._command_exists(archiver):
                print(f"[Build] Found archiver: {archiver}")
                return archiver
        
        print("[Build] WARNING: No archiver found")
        return None
    
    def _command_exists(self, command):
        """Check if a command exists in PATH"""
        try:
            # Use 'where' on Windows, 'which' on Unix
            if self.is_windows:
                subprocess.run(['where', command], 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             check=True, timeout=5)
            else:
                subprocess.run(['which', command], 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             check=True, timeout=5)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def _get_compiler_flags(self):
        """Get platform-specific compiler flags"""
        if self.compiler == 'cl':
            # Microsoft Visual C++
            return ['/O2', '/c']
        else:
            # GCC/Clang
            base_flags = ['-O2', '-c']
            
            # Add position-independent code flag for shared libraries on Unix
            if not self.is_windows:
                base_flags.append('-fPIC')
            
            return base_flags
    
    def _compile_runtime(self):
        """Compile runtime.c to runtime.o"""
        if not self.compiler:
            return False, "No compiler available"
        
        if not self.runtime_c.exists():
            return False, f"Source file not found: {self.runtime_c}"
        
        # Build command
        flags = self._get_compiler_flags()
        
        if self.compiler == 'cl':
            # MSVC syntax
            cmd = [self.compiler] + flags + [str(self.runtime_c), f'/Fo{self.runtime_o}']
        else:
            # GCC/Clang syntax
            cmd = [self.compiler] + flags + [str(self.runtime_c), '-o', str(self.runtime_o)]
        
        print(f"[Build] Command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=str(self.script_dir),
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"[Build] ERROR: Compilation failed")
                print(f"[Build] stdout: {result.stdout}")
                print(f"[Build] stderr: {result.stderr}")
                return False, f"Compilation failed: {result.stderr}"
            
            if not self.runtime_o.exists():
                return False, "Object file was not created"
            
            print(f"[Build] SUCCESS: {self.runtime_o.name} created")
            return True, "Compilation successful"
            
        except subprocess.TimeoutExpired:
            return False, "Compilation timed out"
        except Exception as e:
            return False, f"Compilation error: {str(e)}"
    
    def _create_library(self):
        """Create static library from object file"""
        if not self.archiver:
            print("[Build] WARNING: No archiver available, skipping library creation")
            return True, "Library creation skipped (no archiver)"
        
        if not self.runtime_o.exists():
            return False, "Object file not found"
        
        print(f"[Build] Creating static library {self.runtime_lib.name}...")
        
        # Build archiver command
        if self.archiver == 'lib':
            # Microsoft lib tool
            cmd = [self.archiver, f'/OUT:{self.runtime_lib}', str(self.runtime_o)]
        else:
            # Unix ar or llvm-ar
            cmd = [self.archiver, 'rcs', str(self.runtime_lib), str(self.runtime_o)]
        
        print(f"[Build] Command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=str(self.script_dir),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"[Build] ERROR: Library creation failed")
                print(f"[Build] stderr: {result.stderr}")
                return False, f"Library creation failed: {result.stderr}"
            
            if not self.runtime_lib.exists():
                return False, "Library file was not created"
            
            print(f"[Build] SUCCESS: {self.runtime_lib.name} created")
            return True, "Library creation successful"
            
        except subprocess.TimeoutExpired:
            return False, "Library creation timed out"
        except Exception as e:
            return False, f"Library creation error: {str(e)}"
    
    def build(self):
        """Build the runtime library"""
        print(f"[Build] Starting VGraph runtime build...")
        print(f"[Build] Working directory: {self.script_dir}")
        
        # Step 1: Compile runtime.c
        success, message = self._compile_runtime()
        if not success:
            print(f"[Build] FAILED: {message}")
            return False
        
        # Step 2: Create static library
        success, message = self._create_library()
        if not success:
            print(f"[Build] FAILED: {message}")
            return False
        
        print(f"[Build] SUCCESS: Runtime build completed")
        print(f"[Build] Output files:")
        if self.runtime_o.exists():
            print(f"[Build]   - {self.runtime_o}")
        if self.runtime_lib.exists():
            print(f"[Build]   - {self.runtime_lib}")
        
        return True
    
    def clean(self):
        """Clean build artifacts (todos los .o/.a por plataforma)"""
        print("[Build] Cleaning build artifacts...")

        for p in self.script_dir.glob("runtime_*.o"):
            try:
                p.unlink()
                print(f"[Build] Removed: {p.name}")
            except Exception as e:
                print(f"[Build] Warning: Could not remove {p.name}: {e}")

        for p in self.script_dir.glob("libvgraphrt_*.a"):
            try:
                p.unlink()
                print(f"[Build] Removed: {p.name}")
            except Exception as e:
                print(f"[Build] Warning: Could not remove {p.name}: {e}")

        print("[Build] Clean completed")

    
    def info(self):
        """Print build information"""
        print(f"[Build] VGraph Runtime Build Information")
        print(f"[Build] =" * 50)
        print(f"[Build] Platform: {self.platform}")
        print(f"[Build] Script directory: {self.script_dir}")
        print(f"[Build] Compiler: {self.compiler or 'Not found'}")
        print(f"[Build] Archiver: {self.archiver or 'Not found'}")
        print(f"[Build] Source file: {self.runtime_c} ({'exists' if self.runtime_c.exists() else 'missing'})")
        print(f"[Build] Object file: {self.runtime_o} ({'exists' if self.runtime_o.exists() else 'missing'})")
        print(f"[Build] Library file: {self.runtime_lib} ({'exists' if self.runtime_lib.exists() else 'missing'})")
        
        if self.compiler:
            try:
                result = subprocess.run([self.compiler, '--version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    version_line = result.stdout.split('\n')[0]
                    print(f"[Build] Compiler version: {version_line}")
            except:
                pass


def main():
    """Main function"""
    builder = RuntimeBuilder()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'clean':
            builder.clean()
        elif command == 'info':
            builder.info()
        elif command == 'build':
            success = builder.build()
            sys.exit(0 if success else 1)
        else:
            print(f"Usage: {sys.argv[0]} [build|clean|info]")
            sys.exit(1)
    else:
        # Default action: build
        success = builder.build()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()