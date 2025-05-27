"""
Assembly Code Generator for VGraph compiler
Converts LLVM IR to x86-64 assembly and builds executable
Cross-platform compatible (Windows/Linux/MacOS)
"""
import os
import sys
import subprocess
import platform
import tempfile
import shutil
from pathlib import Path

# Try to import required modules with fallbacks
try:
    from llvmlite import binding as llvm
    LLVMLITE_AVAILABLE = True
except ImportError:
    LLVMLITE_AVAILABLE = False
    print("Warning: llvmlite module not found. Install with: pip install llvmlite")

from config import BASE_DIR

class CodeGenerator:
    """
    Generates x86-64 assembly code from optimized LLVM IR and builds executable
    Cross-platform compatible
    """
    def __init__(self):
        # Platform detection
        self.platform = platform.system().lower()
        self.is_windows = self.platform == 'windows'
        self.is_linux = self.platform == 'linux'
        self.is_mac = self.platform == 'darwin'
        
        # Setup platform-specific configurations
        self._setup_platform_specifics()
        
        # File encoding for cross-platform compatibility
        self.file_encoding = 'utf-8'
        
        # Initialize LLVM if available
        if LLVMLITE_AVAILABLE:
            self._initialize_llvm()
    
    def _setup_platform_specifics(self):
        """Setup platform-specific configurations"""
        # Ensure output directory exists
        self.output_dir = os.path.join(BASE_DIR, "out")
        self.assets_dir = os.path.join(BASE_DIR, "assets")
        self.runtime_dir = os.path.join(BASE_DIR, "CompilerLogic", "Ir")
        
        self._ensure_directory_exists(self.output_dir)
        self._ensure_directory_exists(self.assets_dir)
        
        # Setup file paths with platform-appropriate extensions
        self.input_path = os.path.join(self.output_dir, "vGraph_opt.ll")
        self.asm_path = os.path.join(self.output_dir, "vGraph.asm")
        self.obj_path = os.path.join(self.output_dir, "vGraph.o")
        
        # Platform-specific executable
        exe_ext = ".exe"
        self.exe_path = os.path.join(self.output_dir, f"vGraph{exe_ext}")
        
        # Runtime paths
        plat_tag = self.platform          # 'windows' | 'linux' | 'darwin'
        self.runtime_c_path  = os.path.join(self.runtime_dir, "runtime.c")
        self.runtime_o_path  = os.path.join(self.runtime_dir, f"runtime_{plat_tag}.o")
        self.runtime_lib_path = os.path.join(self.runtime_dir, f"libvgraphrt_{plat_tag}.a")
        
        # Platform-specific build tools
        self._setup_build_tools()
    
    def _setup_build_tools(self):
        """Setup platform-specific build tools"""
        self.build_tools = {
            'c_compiler': None,
            'assembler': None,
            'linker': None,
            'archiver': None
        }
        
        if self.is_windows:
            # Try to find Windows build tools
            self._detect_windows_tools()
        else:
            # Unix-like systems
            self._detect_unix_tools()
    
    def _detect_windows_tools(self):
        """Detect Windows build tools"""
        # Try different compiler options in order of preference
        compilers = ['clang', 'gcc', 'cl']
        for compiler in compilers:
            if self._command_exists(compiler):
                self.build_tools['c_compiler'] = compiler
                break
        
        # Assembler options for Windows
        assemblers = ['clang', 'gcc', 'ml64', 'as']
        for assembler in assemblers:
            if self._command_exists(assembler):
                self.build_tools['assembler'] = assembler
                break
        
        # Linker and archiver
        if self._command_exists('gcc'):
            self.build_tools['linker'] = 'gcc'
            self.build_tools['archiver'] = 'ar'
        elif self._command_exists('clang'):
            self.build_tools['linker'] = 'clang'
            self.build_tools['archiver'] = 'llvm-ar'
        elif self._command_exists('link'):
            self.build_tools['linker'] = 'link'
            self.build_tools['archiver'] = 'lib'
    
    def _detect_unix_tools(self):
        """Detect Unix build tools"""
        # Try different compiler options
        compilers = ['clang', 'gcc']
        for compiler in compilers:
            if self._command_exists(compiler):
                self.build_tools['c_compiler'] = compiler
                break
        
        # Assembler (usually as or integrated in compiler)
        if self._command_exists('as'):
            self.build_tools['assembler'] = 'as'
        else:
            self.build_tools['assembler'] = self.build_tools['c_compiler']
        
        # Linker and archiver
        self.build_tools['linker'] = self.build_tools['c_compiler']
        self.build_tools['archiver'] = 'ar'
    
    def _command_exists(self, command):
        """Check if a command exists in PATH"""
        try:
            subprocess.run([command, '--version'], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         check=True, timeout=5)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def _ensure_directory_exists(self, directory):
        """Ensure directory exists with proper cross-platform handling"""
        try:
            os.makedirs(directory, exist_ok=True)
            
            # Set appropriate permissions on Unix-like systems
            if not self.is_windows:
                try:
                    os.chmod(directory, 0o755)
                except (OSError, PermissionError):
                    pass  # Ignore permission errors
                    
        except Exception as e:
            print(f"Warning: Could not create directory {directory}: {e}")
    
    def _initialize_llvm(self):
        """Initialize LLVM with error handling"""
        try:
            llvm.initialize()
            llvm.initialize_native_target()
            llvm.initialize_native_asmprinter()
            
            # Create target machine for x86-64
            target = llvm.Target.from_default_triple()
            self.target_machine = target.create_target_machine(
                opt=3,  # Optimization level
                codemodel='default',
                features=''
            )
            
        except Exception as e:
            print(f"Warning: LLVM initialization failed: {e}")
            self.target_machine = None
    
    def _sanitize_text(self, text):
        """Sanitize text for cross-platform file writing"""
        if not text:
            return ""
        
        # Replace problematic characters
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ñ': 'n',
            'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ñ': 'N'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Ensure only printable ASCII or common Unicode
        result = ""
        for char in text:
            if ord(char) < 128 and (char.isprintable() or char.isspace()):
                result += char
            elif char in '\n\r\t':
                result += char
            else:
                result += '?'  # Replace problematic characters
        
        return result
    
    def _write_file_safely(self, filepath, content):
        """Write file with cross-platform encoding safety"""
        try:
            # Sanitize content
            safe_content = self._sanitize_text(content)
            
            # Ensure directory exists
            self._ensure_directory_exists(os.path.dirname(filepath))
            
            # Write with explicit UTF-8 encoding and Unix line endings
            with open(filepath, 'w', encoding=self.file_encoding, newline='\n') as f:
                f.write(safe_content)
            
            return True
        except Exception as e:
            print(f"Error writing file {filepath}: {e}")
            return False
    
    def _read_file_safely(self, filepath):
        """Read file with cross-platform encoding safety"""
        try:
            # Try UTF-8 first
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                # Fallback to system default encoding
                with open(filepath, 'r', encoding=sys.getdefaultencoding()) as f:
                    return f.read()
            except UnicodeDecodeError:
                # Last resort: read as latin-1 (never fails)
                with open(filepath, 'r', encoding='latin-1') as f:
                    return f.read()
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            return None
    
    def generate_assembly(self):
        """
        Generate x86-64 assembly from LLVM IR and build executable
        
        Returns:
            tuple: (success: bool, message: str, output_path: str)
        """
        # Check dependencies first
        if not LLVMLITE_AVAILABLE:
            return False, "LLVM code generation requires llvmlite. Please install with: pip install llvmlite", None
        
        try:
            # Step 1: Generate assembly
            success, message, _ = self._generate_asm()
            if not success:
                return False, message, None
            
            # Step 2: Build runtime if needed
            success, message = self._build_runtime()
            if not success:
                return False, message, None
            
            # Step 3: Assemble to object file
            success, message = self._assemble()
            if not success:
                return False, message, None
            
            # Step 4: Link to create executable
            success, message = self._link()
            if not success:
                return False, message, None
            
            # Generate final report
            final_message = self._sanitize_text(
                f"Build complete!\n"
                f"Assembly: {os.path.basename(self.asm_path)}\n"
                f"Object: {os.path.basename(self.obj_path)}\n"
                f"Executable: {os.path.basename(self.exe_path)}\n"
                f"Ready to run!"
            )
            
            return True, final_message, self.exe_path
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            error_msg = f"Code generation failed: {str(e)}"
            return False, self._sanitize_text(error_msg), None
    
    def _generate_asm(self):
        """Generate assembly from LLVM IR"""
        try:
            # Check if input file exists
            if not os.path.exists(self.input_path):
                return False, "Optimized IR file not found. Please run optimizer first.", None
            
            # Read the optimized IR safely
            ir_string = self._read_file_safely(self.input_path)
            if ir_string is None:
                return False, "Failed to read IR file.", None
            
            # Parse the IR
            try:
                llvm_module = llvm.parse_assembly(ir_string)
            except Exception as e:
                return False, f"Failed to parse IR: {str(e)}", None
            
            # Verify the module
            try:
                llvm_module.verify()
            except Exception as e:
                return False, f"IR verification failed: {str(e)}", None
            
            # Generate assembly code
            try:
                # Get assembly string
                asm_string = self.target_machine.emit_assembly(llvm_module)
                
                # Post-process assembly for compatibility
                asm_string = self._post_process_assembly(asm_string)
                
            except Exception as e:
                return False, f"Assembly generation failed: {str(e)}", None
            
            # Write assembly file safely
            if not self._write_file_safely(self.asm_path, asm_string):
                return False, "Failed to write assembly file.", None
            
            # Generate report
            self._generate_assembly_report(asm_string)
            
            return True, "Assembly generated successfully", self.asm_path
            
        except Exception as e:
            return False, f"Assembly generation error: {str(e)}", None
    
    def _build_runtime(self):
        """
        Build the VGraph runtime library (obj + .a) para la plataforma actual
        usando artefactos separados (runtime_<plat>.o / libvgraphrt_<plat>.a).
        """
        try:
            # Re-compilar SOLO si aún no existe el .o/.a para esta plataforma
            needs_rebuild = (
                not os.path.exists(self.runtime_o_path) or
                not os.path.exists(self.runtime_lib_path) or
                os.path.getmtime(self.runtime_o_path) < os.path.getmtime(self.runtime_c_path)
            )

            if not needs_rebuild:
                return True, "Runtime already up to date"

            # Detectar compilador C
            compiler = self.build_tools.get('c_compiler')
            if not compiler:
                return False, "No C compiler found. Install gcc, clang, or MSVC"

            # Compilar runtime.c → runtime_<plat>.o
            success, msg = self._compile_runtime(compiler)
            if not success:
                return False, msg

            # Empaquetar en libvgraphrt_<plat>.a (si archiver disponible)
            archiver = self.build_tools.get('archiver')
            if archiver and archiver != 'lib':          # ar / llvm-ar en Unix
                lib_cmd = [archiver, 'rcs', self.runtime_lib_path, self.runtime_o_path]
                subprocess.run(lib_cmd, cwd=self.runtime_dir,
                            capture_output=True, text=True)
            elif archiver == 'lib':                      # MSVC lib.exe
                lib_cmd = [archiver, f'/OUT:{self.runtime_lib_path}', self.runtime_o_path]
                subprocess.run(lib_cmd, cwd=self.runtime_dir,
                            capture_output=True, text=True)

            return True, "Runtime built successfully"

        except Exception as e:
            return False, f"Runtime build error: {e}"

    
    def _compile_runtime(self, compiler):
        """Compile the runtime with the detected compiler"""
        try:
            # Platform-specific compilation flags
            if self.is_windows:
                if compiler == 'cl':
                    # MSVC compiler
                    cmd = [compiler, '/c', '/O2', self.runtime_c_path, f'/Fo{self.runtime_o_path}']
                else:
                    # GCC/Clang on Windows
                    cmd = [compiler, '-O2', '-c', self.runtime_c_path, '-o', self.runtime_o_path]
            else:
                # Unix-like systems
                cmd = [compiler, '-O2', '-fPIC', '-c', self.runtime_c_path, '-o', self.runtime_o_path]
            
            result = subprocess.run(
                cmd,
                cwd=self.runtime_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                return False, f"Runtime compilation failed: {result.stderr}"
            
            # Create static library if archiver is available
            archiver = self.build_tools.get('archiver')
            if archiver and archiver != 'lib':  # Unix ar or llvm-ar
                lib_cmd = [archiver, 'rcs', self.runtime_lib_path, self.runtime_o_path]
                subprocess.run(lib_cmd, cwd=self.runtime_dir, capture_output=True)
            
            return True, "Runtime built successfully"
            
        except subprocess.TimeoutExpired:
            return False, "Runtime compilation timed out"
        except Exception as e:
            return False, f"Runtime compilation error: {str(e)}"
    
    def _assemble(self):
        """Assemble the .asm file to .o object file"""
        try:
            assembler = self.build_tools.get('assembler')
            if not assembler:
                return False, "No assembler found"
            
            # Platform-specific assembly commands
            if assembler == 'as':
                # GNU assembler
                cmd = [assembler, self.asm_path, '-o', self.obj_path]
            elif assembler in ['gcc', 'clang']:
                # Use compiler to assemble
                cmd = [assembler, '-c', self.asm_path, '-o', self.obj_path]
            elif assembler == 'ml64':
                # Microsoft assembler
                cmd = [assembler, '/c', self.asm_path, f'/Fo{self.obj_path}']
            else:
                return False, f"Unsupported assembler: {assembler}"
            
            result = subprocess.run(
                cmd,
                cwd=self.output_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                return False, f"Assembly failed: {result.stderr}"
            
            if not os.path.exists(self.obj_path):
                return False, "Object file was not created"
            
            return True, "Assembly successful"
            
        except subprocess.TimeoutExpired:
            return False, "Assembly timed out"
        except Exception as e:
            return False, f"Assembly error: {str(e)}"
    
    def _link(self):
        """Link object files to create executable"""
        try:
            linker = self.build_tools.get('linker')
            if not linker:
                return False, "No linker found"
            
            # Platform-specific linking
            if linker in ['gcc', 'clang']:
                cmd = [
                    linker,
                    self.obj_path,
                    self.runtime_o_path,
                    '-lm',      # Math library
                    '-o', self.exe_path
                ]
                
                # Add platform-specific flags
                if self.is_linux:
                    cmd.append('-no-pie')
                elif self.is_windows:
                    # Windows-specific flags for MinGW/Clang
                    pass
                    
            elif linker == 'link':
                # MSVC linker
                cmd = [
                    linker,
                    self.obj_path,
                    self.runtime_o_path,
                    f'/OUT:{self.exe_path}'
                ]
            else:
                return False, f"Unsupported linker: {linker}"
            
            result = subprocess.run(
                cmd,
                cwd=self.output_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                return False, f"Linking failed: {result.stderr}"
            
            if not os.path.exists(self.exe_path):
                return False, "Executable was not created"
            
            # Make executable on Unix-like systems
            if not self.is_windows:
                try:
                    os.chmod(self.exe_path, 0o755)
                except OSError:
                    pass
            
            return True, "Linking successful"
            
        except subprocess.TimeoutExpired:
            return False, "Linking timed out"
        except Exception as e:
            return False, f"Linking error: {str(e)}"
    
    def _post_process_assembly(self, asm_string):
        """Post-process assembly for better compatibility"""
        lines = asm_string.splitlines()
        processed_lines = []
        
        for line in lines:
            # Skip some LLVM-specific directives that cause issues
            if line.strip().startswith('.ident') or line.strip().startswith('.note'):
                continue
            
            # Process the line
            processed_lines.append(line)
        
        # Add header comments
        header = [
            "# VGraph Assembly Code",
            "# Generated from LLVM IR",
            f"# Target: x86-64 ({self.platform})",
            "# Syntax: AT&T (GNU Assembler)",
            "",
        ]
        
        return '\n'.join(header + processed_lines)
    
    def _generate_assembly_report(self, asm_string):
        """Generate a report about the generated assembly"""
        lines = asm_string.splitlines()
        
        # Count various assembly elements
        stats = {
            'total_lines': len(lines),
            'code_lines': len([l for l in lines if l.strip() and not l.strip().startswith('#') and not l.strip().startswith('.')]),
            'functions': 0,
            'labels': 0,
            'calls': 0,
            'jumps': 0,
            'moves': 0,
            'arithmetic': 0,
            'stack_ops': 0,
        }
        
        for line in lines:
            line = line.strip()
            if line.startswith('.globl'):
                stats['functions'] += 1
            elif line.endswith(':') and not line.startswith('.'):
                stats['labels'] += 1
            elif 'call' in line:
                stats['calls'] += 1
            elif any(j in line for j in ['jmp', 'je', 'jne', 'jl', 'jg', 'jle', 'jge']):
                stats['jumps'] += 1
            elif 'mov' in line:
                stats['moves'] += 1
            elif any(op in line for op in ['add', 'sub', 'mul', 'div', 'imul', 'idiv']):
                stats['arithmetic'] += 1
            elif any(op in line for op in ['push', 'pop']):
                stats['stack_ops'] += 1
        
        report = []
        report.append("=" * 60)
        report.append("ASSEMBLY CODE GENERATION REPORT")
        report.append("=" * 60)
        report.append(f"Platform: {self.platform}")
        report.append(f"Input: {self.input_path}")
        report.append(f"Output: {self.asm_path}")
        report.append(f"Object: {self.obj_path}")
        report.append(f"Executable: {self.exe_path}")
        report.append("")
        report.append("Build Tools Used:")
        report.append("-" * 40)
        for tool_type, tool_name in self.build_tools.items():
            if tool_name:
                report.append(f"{tool_type.replace('_', ' ').title():<20}: {tool_name}")
        report.append("")
        report.append("Assembly Statistics:")
        report.append("-" * 40)
        
        for key, value in stats.items():
            report.append(f"{key.replace('_', ' ').title():<20}: {value:>10}")
        
        report.append("")
        report.append("Build Steps:")
        report.append("-" * 40)
        report.append("1. Generate assembly from LLVM IR")
        report.append("2. Build runtime library (if needed)")
        report.append("3. Assemble to object file")
        report.append("4. Link with runtime to create executable")
        report.append("")
        report.append("Target Architecture: x86-64")
        report.append("Assembly Syntax: AT&T (GNU Assembler)")
        report.append("")
        
        # List functions found
        report.append("Functions found:")
        report.append("-" * 40)
        for line in lines:
            if '.globl' in line:
                func_name = line.split()[-1]
                report.append(f"  - {func_name}")
        
        report_path = os.path.join(self.assets_dir, "assembly_report.txt")
        self._write_file_safely(report_path, '\n'.join(report))
    
    def get_system_info(self):
        """Get system information for debugging"""
        return {
            'platform': self.platform,
            'is_windows': self.is_windows,
            'is_linux': self.is_linux,
            'is_mac': self.is_mac,
            'build_tools': self.build_tools,
            'llvmlite_available': LLVMLITE_AVAILABLE,
            'python_version': sys.version,
            'paths': {
                'input': self.input_path,
                'assembly': self.asm_path,
                'object': self.obj_path,
                'executable': self.exe_path,
                'runtime_c': self.runtime_c_path,
                'runtime_o': self.runtime_o_path
            }
        }