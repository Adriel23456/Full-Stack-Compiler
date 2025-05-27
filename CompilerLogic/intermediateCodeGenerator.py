"""
Facade between the semantic phase and the LLVM-IR generator.
Adds **verbose debug prints** so any crash inside IR emission is
reported in the console and also surfaced to the GUI.
Cross-platform compatible (Windows/Linux/MacOS)
"""

from __future__ import annotations

import os
import sys
import platform
import tempfile
import traceback
from pathlib import Path
from typing import Any

# Try to import required modules with fallbacks
try:
    from llvmlite import ir, binding as llvm
    LLVMLITE_AVAILABLE = True
except ImportError:
    LLVMLITE_AVAILABLE = False
    print("Warning: llvmlite module not found. Install with: pip install llvmlite")

from config import BASE_DIR, CompilerData
from CompilerLogic.SemanticComponents.symbolTable import SymbolTable

# Only import IRGenerator if llvmlite is available
if LLVMLITE_AVAILABLE:
    from CompilerLogic.Ir.irBuilder import IRGenerator


class IntermediateCodeGenerator:
    """
    Single public entry-point → `emit_ir()` - Cross-platform compatible
    MAINTAINS EXACT SAME API AS ORIGINAL FOR RETROCOMPATIBILITY
    """

    # ────────────────────────────────────────────────────────────
    @staticmethod
    def _ensure_symbol_table(raw: Any) -> SymbolTable:
        """Guarantee a SymbolTable instance (wrap plain dict if needed)."""
        if isinstance(raw, SymbolTable):
            return raw
        return SymbolTable(raw or {})

    @staticmethod
    def _get_platform_info():
        """Get platform information for cross-platform handling"""
        platform_name = platform.system().lower()
        return {
            'platform': platform_name,
            'is_windows': platform_name == 'windows',
            'is_linux': platform_name == 'linux',
            'is_mac': platform_name == 'darwin'
        }

    @staticmethod
    def _ensure_directory_exists(directory):
        """Ensure directory exists with proper cross-platform handling"""
        try:
            os.makedirs(directory, exist_ok=True)
            
            # Set appropriate permissions on Unix-like systems
            platform_info = IntermediateCodeGenerator._get_platform_info()
            if not platform_info['is_windows']:
                try:
                    os.chmod(directory, 0o755)
                except (OSError, PermissionError):
                    pass  # Ignore permission errors
                    
        except Exception as e:
            print(f"Warning: Could not create directory {directory}: {e}")

    @staticmethod
    def _sanitize_error_message(message):
        """
        Sanitize error messages for cross-platform display
        """
        if not message:
            return ""
        
        # Replace problematic characters
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ñ': 'n',
            'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ñ': 'N'
        }
        
        for old, new in replacements.items():
            message = message.replace(old, new)
        
        # Ensure only ASCII printable characters
        result = ""
        for char in message:
            if ord(char) < 128 and (char.isprintable() or char.isspace()):
                result += char
            else:
                result += '?'  # Replace problematic characters
        
        return result

    @staticmethod
    def _check_dependencies():
        """Check if required dependencies are available"""
        missing_deps = []
        
        if not LLVMLITE_AVAILABLE:
            missing_deps.append('llvmlite')
        
        return missing_deps

    @staticmethod
    def _install_missing_dependencies():
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

    # ────────────────────────────────────────────────────────────
    @staticmethod
    def emit_ir(output_path: str | None = None) -> str | None:
        """
        Generate LLVM IR from the current AST.

        Returns the IR text or **None** when generation fails.
        All exceptions are caught and transformed into `CompilerData.semantic_errors`.
        
        EXACT SAME API AS ORIGINAL - RETROCOMPATIBLE
        """

        # Check dependencies first
        if not LLVMLITE_AVAILABLE:
            missing_deps = IntermediateCodeGenerator._install_missing_dependencies()
            if 'llvmlite' in missing_deps:
                error_msg = "LLVM IR generation requires llvmlite. Please install with: pip install llvmlite"
                CompilerData.semantic_errors.append({
                    "message": error_msg,
                    "line": 1,
                    "column": 0,
                    "length": 1,
                })
                return None

        # 1) check pending semantic errors
        if CompilerData.semantic_errors:
            return None

        # 2) collect data from previous phases
        ast    = CompilerData.ast
        parser = CompilerData.parser
        if ast is None or parser is None:
            error_msg = "No AST or parser available for IR generation"
            CompilerData.semantic_errors.append({
                "message": error_msg,
                "line": 1,
                "column": 0,
                "length": 1,
            })
            return None

        symtab = IntermediateCodeGenerator._ensure_symbol_table(CompilerData.symbol_table)

        # 3) generate IR
        try:
            ir_text = IRGenerator(ast, symtab, parser).generate()
        except Exception as exc:  # pylint: disable=broad-except
            traceback.print_exc()

            # store as synthetic semantic error so GUI highlights something
            error_msg = f"Excepcion en IR: {exc}"
            # Remove non-ASCII characters for cross-platform compatibility
            error_msg = IntermediateCodeGenerator._sanitize_error_message(error_msg)
            
            CompilerData.semantic_errors.append({
                "message": error_msg,
                "line": 1,
                "column": 0,
                "length": 1,
            })
            return None

        # 4) write to disk with cross-platform improvements
        if output_path is None:
            output_path = os.path.join(BASE_DIR, "out", "vGraph.ll")
        
        try:
            # Ensure output directory exists (cross-platform)
            IntermediateCodeGenerator._ensure_directory_exists(os.path.dirname(output_path))
            
            # Write with explicit UTF-8 encoding for cross-platform compatibility
            with open(output_path, "w", encoding="utf-8", newline='\n') as fh:
                fh.write(ir_text)
            
        except Exception as e:
            error_msg = f"Failed to write IR to file: {e}"
            CompilerData.semantic_errors.append({
                "message": IntermediateCodeGenerator._sanitize_error_message(error_msg),
                "line": 1,
                "column": 0,
                "length": 1,
            })
            return None

        return ir_text

    # ────────────────────────────────────────────────────────────
    # OPTIONAL: Additional utility methods for debugging (don't break existing code)
    # ────────────────────────────────────────────────────────────
    
    @staticmethod
    def get_system_info():
        """
        Get system information for debugging
        
        Returns:
            dict: System information
        """
        platform_info = IntermediateCodeGenerator._get_platform_info()
        return {
            'platform': platform_info['platform'],
            'is_windows': platform_info['is_windows'],
            'is_linux': platform_info['is_linux'],
            'is_mac': platform_info['is_mac'],
            'llvmlite_available': LLVMLITE_AVAILABLE,
            'python_version': sys.version,
            'missing_dependencies': IntermediateCodeGenerator._check_dependencies()
        }