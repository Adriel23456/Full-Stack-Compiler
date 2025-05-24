# File: CompilerLogic/codeGenerator.py
"""
Assembly Code Generator for VGraph compiler
Converts LLVM IR to x86-64 assembly and builds executable
"""
import os
import subprocess
from llvmlite import binding as llvm
from config import BASE_DIR

# Initialize LLVM
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

class CodeGenerator:
    """
    Generates x86-64 assembly code from optimized LLVM IR and builds executable
    """
    def __init__(self):
        self.input_path = os.path.join(BASE_DIR, "out", "vGraph_opt.ll")
        self.asm_path = os.path.join(BASE_DIR, "out", "vGraph.asm")
        self.obj_path = os.path.join(BASE_DIR, "out", "vGraph.o")
        self.exe_path = os.path.join(BASE_DIR, "out", "vGraph.exe")
        self.runtime_path = os.path.join(BASE_DIR, "CompilerLogic", "Ir", "runtime.o")
        self.build_script = os.path.join(BASE_DIR, "CompilerLogic", "Ir", "build_runtime.sh")
        
        # Create target machine for x86-64
        target = llvm.Target.from_default_triple()
        self.target_machine = target.create_target_machine(
            opt=3,  # Optimization level
            codemodel='default',
            features=''
        )
        
    def generate_assembly(self):
        """
        Generate x86-64 assembly from LLVM IR and build executable
        
        Returns:
            tuple: (success: bool, message: str, output_path: str)
        """
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
            final_message = (
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
            return False, f"Code generation failed: {str(e)}", None
    
    def _generate_asm(self):
        """Generate assembly from LLVM IR"""
        try:
            # Check if input file exists
            if not os.path.exists(self.input_path):
                return False, "Optimized IR file not found. Please run optimizer first.", None
                
            # Read the optimized IR
            with open(self.input_path, 'r') as f:
                ir_string = f.read()
            
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
            
            # Write assembly file
            with open(self.asm_path, 'w') as f:
                f.write(asm_string)
            
            # Generate report
            self._generate_assembly_report(asm_string)
            
            return True, "Assembly generated successfully", self.asm_path
            
        except Exception as e:
            return False, f"Assembly generation error: {str(e)}", None
    
    def _build_runtime(self):
        """Build the VGraph runtime library if needed"""
        try:
            # Check if runtime.o already exists
            if os.path.exists(self.runtime_path):
                runtime_mtime = os.path.getmtime(self.runtime_path)
                runtime_c_path = os.path.join(os.path.dirname(self.runtime_path), "runtime.c")
                if os.path.exists(runtime_c_path):
                    c_mtime = os.path.getmtime(runtime_c_path)
                    if runtime_mtime > c_mtime:
                        # runtime.o is newer than runtime.c, no need to rebuild
                        return True, "Runtime already up to date"
            
            # Run build script
            result = subprocess.run(
                ["bash", self.build_script],
                cwd=BASE_DIR,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return False, f"Runtime build failed: {result.stderr}"
            
            return True, "Runtime built successfully"
            
        except Exception as e:
            return False, f"Runtime build error: {str(e)}"
    
    def _assemble(self):
        """Assemble the .asm file to .o object file"""
        try:
            # Use GNU assembler (as) for AT&T syntax
            cmd = ["as", self.asm_path, "-o", self.obj_path]
            
            result = subprocess.run(
                cmd,
                cwd=BASE_DIR,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return False, f"Assembly failed: {result.stderr}"
            
            if not os.path.exists(self.obj_path):
                return False, "Object file was not created"
            
            return True, "Assembly successful"
            
        except Exception as e:
            return False, f"Assembly error: {str(e)}"
    
    def _link(self):
        """Link object files to create executable"""
        try:
            # Use gcc to link (it handles C runtime and libraries)
            cmd = [
                "gcc",
                self.obj_path,
                self.runtime_path,
                "-lm",      # Math library
                "-no-pie",  # No position independent executable
                "-o", self.exe_path
            ]
            
            result = subprocess.run(
                cmd,
                cwd=BASE_DIR,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return False, f"Linking failed: {result.stderr}"
            
            if not os.path.exists(self.exe_path):
                return False, "Executable was not created"
            
            # Make executable
            os.chmod(self.exe_path, 0o755)
            
            return True, "Linking successful"
            
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
            "# Target: x86-64",
            "# Syntax: AT&T (GNU Assembler)",
            "",
        ]
        
        return '\n'.join(header + processed_lines)
    
    def _generate_assembly_report(self, asm_string):
        """Generate a report about the generated assembly"""
        report_path = os.path.join(BASE_DIR, "assets", "assembly_report.txt")
        
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
        report.append(f"Input: {self.input_path}")
        report.append(f"Output: {self.asm_path}")
        report.append(f"Object: {self.obj_path}")
        report.append(f"Executable: {self.exe_path}")
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
        
        with open(report_path, 'w') as f:
            f.write('\n'.join(report))