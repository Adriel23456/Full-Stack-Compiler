# File: CompilerLogic/optimizer.py
"""
LLVM IR Optimizer for VGraph compiler
Applies various optimization passes to improve code efficiency
"""
import os
from llvmlite import ir, binding as llvm
from config import BASE_DIR

# Initialize LLVM
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

class Optimizer:
    """
    Optimizes LLVM IR using various optimization passes
    """
    def __init__(self):
        self.input_path = os.path.join(BASE_DIR, "out", "vGraph.ll")
        self.output_path = os.path.join(BASE_DIR, "out", "vGraph_opt.ll")
        
        # Create target machine for optimization
        target = llvm.Target.from_default_triple()
        self.target_machine = target.create_target_machine()
        
    def optimize(self, optimization_level=2):
        """
        Apply optimization passes to the IR
        
        Args:
            optimization_level: 0=none, 1=basic, 2=standard, 3=aggressive
            
        Returns:
            tuple: (success: bool, message: str, output_path: str)
        """
        try:
            # Read the input IR
            if not os.path.exists(self.input_path):
                return False, "IR file not found. Please generate IR first.", None
                
            with open(self.input_path, 'r') as f:
                ir_string = f.read()
            
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
            
            # Write optimized IR
            with open(self.output_path, 'w') as f:
                f.write(optimized_ir)
            
            # Generate detailed optimization report
            report = self._generate_optimization_report(ir_string, optimized_ir, optimization_level)
            
            message = (f"Optimization complete (Level {optimization_level})\n"
                      f"Lines: {original_lines} → {optimized_lines} ({reduction:.1f}% reduction)\n"
                      f"Output: {os.path.basename(self.output_path)}")
            
            # Also save the report
            report_path = os.path.join(BASE_DIR, "assets", "optimization_report.txt")
            with open(report_path, 'w') as f:
                f.write(report)
                f.write(f"\n\n{message}")
            
            return True, message, self.output_path
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return False, f"Optimization failed: {str(e)}", None
    
    def _generate_optimization_report(self, original_ir, optimized_ir, level):
        """Generate a detailed report of optimizations applied"""
        report = []
        report.append("=" * 60)
        report.append("LLVM IR OPTIMIZATION REPORT")
        report.append("=" * 60)
        report.append(f"Optimization Level: {level}")
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
            report.append("✓ Constant merging")
            report.append("✓ Dead argument elimination")
            report.append("✓ Global dead code elimination")
            report.append("✓ Global optimization")
            
        if level >= 2:
            report.append("✓ Function inlining")
            report.append("✓ Control flow simplification")
            report.append("✓ Instruction combining")
            report.append("✓ Global value numbering")
            report.append("✓ Dead code elimination")
            
        if level >= 3:
            report.append("✓ Aggressive dead code elimination")
            report.append("✓ Loop unrolling")
            report.append("✓ Loop invariant code motion")
        
        return "\n".join(report)
    
    def get_optimization_levels(self):
        """Return available optimization levels with descriptions"""
        return {
            0: "No optimization",
            1: "Basic optimization (fast compile)",
            2: "Standard optimization (balanced)",
            3: "Aggressive optimization (best performance)"
        }