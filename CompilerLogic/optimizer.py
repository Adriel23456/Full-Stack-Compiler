"""
LLVM IR Optimizer for VGraph compiler
Applies various optimization passes to improve code efficiency
Cross-platform compatible (Windows/Linux/MacOS)
"""
import os
import sys
import platform
import tempfile
from pathlib import Path

# Try to import required modules with fallbacks
try:
    from llvmlite import ir, binding as llvm
    LLVMLITE_AVAILABLE = True
except ImportError:
    LLVMLITE_AVAILABLE = False
    print("Warning: llvmlite module not found. Install with: pip install llvmlite")

from config import BASE_DIR

class Optimizer:
    """
    Optimizes LLVM IR using various optimization passes - Cross-platform compatible
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
        
        self._ensure_directory_exists(self.output_dir)
        self._ensure_directory_exists(self.assets_dir)
        
        # Setup file paths
        self.input_path = os.path.join(self.output_dir, "vGraph.ll")
        self.output_path = os.path.join(self.output_dir, "vGraph_opt.ll")
        self.report_path = os.path.join(self.assets_dir, "optimization_report.txt")
    
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
            
            # Create target machine for optimization
            target = llvm.Target.from_default_triple()
            self.target_machine = target.create_target_machine()
            
        except Exception as e:
            print(f"Warning: LLVM initialization failed: {e}")
            self.target_machine = None
    
    def _check_dependencies(self):
        """Check if required dependencies are available"""
        missing_deps = []
        
        if not LLVMLITE_AVAILABLE:
            missing_deps.append('llvmlite')
        
        return missing_deps
    
    def _install_missing_dependencies(self):
        """Try to install missing Python dependencies automatically"""
        missing_deps = []
        
        if not LLVMLITE_AVAILABLE:
            try:
                print("Installing llvmlite...")
                import subprocess
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'llvmlite'], 
                             check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print("Successfully installed llvmlite")
                print("Note: Please restart the application for changes to take effect")
            except subprocess.CalledProcessError:
                missing_deps.append('llvmlite')
        
        return missing_deps
    
    def _sanitize_text(self, text):
        """
        Sanitize text for cross-platform file writing
        """
        if not text:
            return ""
        
        # Replace problematic Unicode characters with safe alternatives
        replacements = {
            '\u2713': '[OK]',  # ✓ -> [OK]
            '\u2717': '[X]',   # ✗ -> [X]
            '\u2714': '[OK]',  # ✔ -> [OK]
            '\u2718': '[X]',   # ✘ -> [X]
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
        """
        Write file with cross-platform encoding safety
        """
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
        """
        Read file with cross-platform encoding safety
        """
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
        
    def optimize(self, optimization_level=2):
        """
        Apply optimization passes to the IR
        
        Args:
            optimization_level: 0=none, 1=basic, 2=standard, 3=aggressive
            
        Returns:
            tuple: (success: bool, message: str, output_path: str)
        """
        # Check dependencies first
        if not LLVMLITE_AVAILABLE:
            missing_deps = self._install_missing_dependencies()
            if 'llvmlite' in missing_deps:
                return False, "LLVM optimization requires llvmlite. Please install with: pip install llvmlite", None
        
        try:
            # Read the input IR
            if not os.path.exists(self.input_path):
                return False, "IR file not found. Please generate IR first.", None
            
            ir_string = self._read_file_safely(self.input_path)
            if ir_string is None:
                return False, "Failed to read IR file.", None
            
            # Parse the IR
            try:
                llvm_module = llvm.parse_assembly(ir_string)
            except Exception as e:
                return False, f"Failed to parse IR: {str(e)}", None
            
            # Verify the module before optimization
            try:
                llvm_module.verify()
            except Exception as e:
                return False, f"IR verification failed: {str(e)}", None
            
            # Create pass managers
            pm_builder = llvm.create_pass_manager_builder()
            pm_builder.opt_level = optimization_level
            
            # Module pass manager
            module_pm = llvm.create_module_pass_manager()
            pm_builder.populate(module_pm)
            
            # Function pass manager for function-level optimizations
            function_pm = llvm.create_function_pass_manager(llvm_module)
            pm_builder.populate(function_pm)
            
            # Add specific optimization passes based on level
            if optimization_level >= 1:
                # Basic optimizations
                module_pm.add_constant_merge_pass()
                module_pm.add_dead_arg_elimination_pass()
                module_pm.add_global_dce_pass()
                module_pm.add_global_optimizer_pass()
                
            if optimization_level >= 2:
                # Standard optimizations
                module_pm.add_function_inlining_pass(threshold=225)
                module_pm.add_cfg_simplification_pass()
                module_pm.add_instruction_combining_pass()
                module_pm.add_gvn_pass()
                module_pm.add_dead_code_elimination_pass()
                
            if optimization_level >= 3:
                # Aggressive optimizations
                module_pm.add_aggressive_dead_code_elimination_pass()
                module_pm.add_loop_unroll_pass()
                module_pm.add_licm_pass()  # Loop invariant code motion
                
            # Apply function-level optimizations
            function_pm.initialize()
            for func in llvm_module.functions:
                if not func.is_declaration:
                    function_pm.run(func)
            function_pm.finalize()
            
            # Apply module-level optimizations
            module_pm.run(llvm_module)
            
            # Get optimized IR string
            optimized_ir = str(llvm_module)
            
            # Calculate statistics
            original_lines = len(ir_string.splitlines())
            optimized_lines = len(optimized_ir.splitlines())
            reduction = ((original_lines - optimized_lines) / original_lines * 100) if original_lines > 0 else 0
            
            # Write optimized IR safely
            if not self._write_file_safely(self.output_path, optimized_ir):
                return False, "Failed to write optimized IR file.", None
            
            # Generate detailed optimization report
            report = self._generate_optimization_report(ir_string, optimized_ir, optimization_level)
            
            message = (f"Optimization complete (Level {optimization_level})\n"
                      f"Lines: {original_lines} -> {optimized_lines} ({reduction:.1f}% reduction)\n"
                      f"Output: {os.path.basename(self.output_path)}")
            
            # Save the report safely
            report_content = report + f"\n\n{message}"
            if not self._write_file_safely(self.report_path, report_content):
                print("Warning: Could not save optimization report")
            
            return True, message, self.output_path
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            error_msg = f"Optimization failed: {str(e)}"
            return False, self._sanitize_text(error_msg), None
    
    def _generate_optimization_report(self, original_ir, optimized_ir, level):
        """Generate a detailed report of optimizations applied"""
        report = []
        report.append("=" * 60)
        report.append("LLVM IR OPTIMIZATION REPORT")
        report.append("=" * 60)
        report.append(f"Optimization Level: {level}")
        report.append(f"Platform: {self.platform}")
        report.append(f"Input: {self.input_path}")
        report.append(f"Output: {self.output_path}")
        report.append("")
        
        # Count various IR elements
        def count_elements(ir_text):
            lines = ir_text.splitlines()
            stats = {
                'functions': sum(1 for l in lines if l.strip().startswith('define ')),
                'globals': sum(1 for l in lines if l.strip().startswith('@') and '=' in l),
                'alloca': sum(1 for l in lines if 'alloca' in l),
                'load': sum(1 for l in lines if ' load ' in l),
                'store': sum(1 for l in lines if ' store ' in l),
                'calls': sum(1 for l in lines if ' call ' in l),
                'branches': sum(1 for l in lines if l.strip().startswith('br ')),
                'basic_blocks': sum(1 for l in lines if l.strip().endswith(':')),
                'total_lines': len([l for l in lines if l.strip()])
            }
            return stats
        
        orig_stats = count_elements(original_ir)
        opt_stats = count_elements(optimized_ir)
        
        report.append("Optimization Statistics:")
        report.append("-" * 40)
        report.append(f"{'Metric':<20} {'Before':>10} {'After':>10} {'Change':>10}")
        report.append("-" * 40)
        
        for metric in ['functions', 'globals', 'alloca', 'load', 'store', 'calls', 'branches', 'basic_blocks', 'total_lines']:
            before = orig_stats[metric]
            after = opt_stats[metric]
            change = after - before
            change_str = f"{change:+d}" if change != 0 else "0"
            report.append(f"{metric:<20} {before:>10} {after:>10} {change_str:>10}")
        
        report.append("")
        report.append("Optimizations Applied:")
        report.append("-" * 40)
        
        if level >= 1:
            report.append("[OK] Constant merging")
            report.append("[OK] Dead argument elimination")
            report.append("[OK] Global dead code elimination")
            report.append("[OK] Global optimization")
            
        if level >= 2:
            report.append("[OK] Function inlining")
            report.append("[OK] Control flow simplification")
            report.append("[OK] Instruction combining")
            report.append("[OK] Global value numbering")
            report.append("[OK] Dead code elimination")
            
        if level >= 3:
            report.append("[OK] Aggressive dead code elimination")
            report.append("[OK] Loop unrolling")
            report.append("[OK] Loop invariant code motion")
        
        return "\n".join(report)
    
    def get_optimization_levels(self):
        """Return available optimization levels with descriptions"""
        return {
            0: "No optimization",
            1: "Basic optimization (fast compile)",
            2: "Standard optimization (balanced)",
            3: "Aggressive optimization (best performance)"
        }
    
    def get_system_info(self):
        """
        Get system information for debugging
        
        Returns:
            dict: System information
        """
        return {
            'platform': self.platform,
            'is_windows': self.is_windows,
            'is_linux': self.is_linux,
            'is_mac': self.is_mac,
            'output_dir': self.output_dir,
            'assets_dir': self.assets_dir,
            'file_encoding': self.file_encoding,
            'llvmlite_available': LLVMLITE_AVAILABLE,
            'python_version': sys.version,
            'missing_dependencies': self._check_dependencies(),
            'target_machine_available': hasattr(self, 'target_machine') and self.target_machine is not None
        }