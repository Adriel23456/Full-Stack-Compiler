# File: CompilerLogic/intermediateCodeGenerator.py
"""
Facade between the semantic phase and the LLVM-IR generator.
Adds **verbose debug prints** so any crash inside IR emission is
reported in the console and also surfaced to the GUI.
"""

from __future__ import annotations

import os
import traceback
from typing import Any

from config import BASE_DIR, CompilerData
from CompilerLogic.SemanticComponents.symbolTable import SymbolTable
from CompilerLogic.Ir.irBuilder import IRGenerator


class IntermediateCodeGenerator:
    """
    Single public entry-point → `emit_ir()`
    """

    # ────────────────────────────────────────────────────────────
    @staticmethod
    def _ensure_symbol_table(raw: Any) -> SymbolTable:
        """Guarantee a SymbolTable instance (wrap plain dict if needed)."""
        if isinstance(raw, SymbolTable):
            return raw
        return SymbolTable(raw or {})

    # ────────────────────────────────────────────────────────────
    @staticmethod
    def emit_ir(output_path: str | None = None) -> str | None:
        """
        Generate LLVM IR from the current AST.

        Returns the IR text or **None** when generation fails.
        All exceptions are caught and transformed into `CompilerData.semantic_errors`.
        """

        # 1) check pending semantic errors
        if CompilerData.semantic_errors:
            return None

        # 2) collect data from previous phases
        ast    = CompilerData.ast
        parser = CompilerData.parser
        if ast is None or parser is None:
            return None

        symtab = IntermediateCodeGenerator._ensure_symbol_table(CompilerData.symbol_table)

        # 3) generate IR
        try:
            ir_text = IRGenerator(ast, symtab, parser).generate()
        except Exception as exc:  # pylint: disable=broad-except
            traceback.print_exc()

            # store as synthetic semantic error so GUI highlights something
            CompilerData.semantic_errors.append({
                "message": f"Excepción en IR: {exc}",
                "line": 1,
                "column": 0,
                "length": 1,
            })
            return None

        # 4) write to disk
        if output_path is None:
            output_path = os.path.join(BASE_DIR, "out", "vGraph.ll")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as fh:
            fh.write(ir_text)

        return ir_text