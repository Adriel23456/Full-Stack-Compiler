"""Fachada para la etapa Middle‑End."""
from CompilerLogic.ir import IRGenerator
from config import CompilerData

class IntermediateCodeGenerator:
    @staticmethod
    def emit_ir(output_path="out/vGraph.ll"):
        if CompilerData.semantic_errors:
            print("❌ IR abortado – errores semánticos presentes")
            return None

        gen = IRGenerator(CompilerData.ast, CompilerData.symbol_table)
        llvm_ir = str(gen.module)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(llvm_ir)
        print(f"✅ IR guardado en {output_path}")
        return llvm_ir