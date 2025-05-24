# File: CompilerLogic/codeGenerator.py
"""
Assembly Code Generator for VGraph compiler
Converts LLVM IR to x86-64 assembly using llvmlite
"""
import os
from llvmlite import binding as llvm
from config import BASE_DIR

# Initialize LLVM
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

class CodeGenerator:
    """
    Generates x86-64 assembly code from optimized LLVM IR
    """
    def __init__(self):
        self.input_path = os.path.join(BASE_DIR, "out", "vGraph_opt.ll")
        self.output_path = os.path.join(BASE_DIR, "out", "vGraph.asm")
        
        # Create target machine for x86-64
        target = llvm.Target.from_default_triple()
        self.target_machine = target.create_target_machine(
            opt=3,  # Optimization level
            codemodel='default',
            features=''
        )
        
    def generate_assembly(self):
        """
        Generate x86-64 assembly from LLVM IR
        
        Returns:
            tuple: (success: bool, message: str, output_path: str)
        """
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
                
                # Post-process assembly for NASM compatibility
                asm_string = self._post_process_assembly(asm_string)
                
            except Exception as e:
                return False, f"Assembly generation failed: {str(e)}", None
            
            # Write assembly file
            with open(self.output_path, 'w') as f:
                f.write(asm_string)
            
            # Count statistics
            lines = len(asm_string.splitlines())
            functions = asm_string.count('.globl')
            
            message = (f"Assembly generation complete!\n"
                      f"Generated {lines} lines of x86-64 assembly\n"
                      f"Functions: {functions}\n"
                      f"Output: {os.path.basename(self.output_path)}")
            
            # Generate report
            self._generate_assembly_report(asm_string)
            
            return True, message, self.output_path
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return False, f"Code generation failed: {str(e)}", None
    
    def _post_process_assembly(self, asm_string):
        """
        Post-process assembly for better compatibility with NASM
        Note: llvmlite generates AT&T syntax, but we'll keep it for simplicity
        """
        lines = asm_string.splitlines()
        processed_lines = []
        
        for line in lines:
            # Skip some LLVM-specific directives that NASM doesn't understand
            if line.strip().startswith('.ident') or line.strip().startswith('.note'):
                continue
            
            # Process the line
            processed_lines.append(line)
        
        # Add NASM-style header if needed (but we're using AT&T syntax with gas)
        header = [
            "# VGraph Assembly Code",
            "# Generated from LLVM IR",
            "# Target: x86-64",
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
        report.append(f"Output: {self.output_path}")
        report.append("")
        report.append("Assembly Statistics:")
        report.append("-" * 40)
        
        for key, value in stats.items():
            report.append(f"{key.replace('_', ' ').title():<20}: {value:>10}")
        
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