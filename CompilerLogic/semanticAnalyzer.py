# CompilerLogic/semanticAnalyzer.py (actualización)

"""
Semantic analyzer module for the Full Stack Compiler
Handles semantic analysis of code and generates semantic graphs and enhanced symbol tables
"""
import os
import sys
import pydot
from antlr4 import *
from antlr4.tree.Trees import Trees
from config import BASE_DIR, ASSETS_DIR, SEMANTIC_GRAPH_PATH, ENHANCED_SYMBOL_TABLE_PATH, CompilerData

# Importar los componentes del análisis semántico
from CompilerLogic.SemanticComponents.symbolTable import SymbolTable
from CompilerLogic.SemanticComponents.typeChecker import TypeChecker
from CompilerLogic.SemanticComponents.scopeChecker import ScopeChecker
from CompilerLogic.SemanticComponents.errorReporter import ErrorReporter
from CompilerLogic.SemanticComponents.astVisitor import ASTVisitor
from CompilerLogic.SemanticComponents.astUtil import print_ast, get_node_text

class SemanticAnalyzer:
    """
    Handles semantic analysis of code
    """
    def __init__(self):
        """
        Initializes the semantic analyzer
        """
        self.semantic_graph_path = SEMANTIC_GRAPH_PATH
        self.enhanced_symbol_table_path = ENHANCED_SYMBOL_TABLE_PATH
        
        # Ensure Images directory exists
        images_dir = os.path.join(ASSETS_DIR, "Images")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
    
    def analyze(self, source_code=None):
        """
        Analyze the AST from syntactic analysis semantically
        """
        
        # Reset estado semántico
        CompilerData.reset_semantic()
        
        try:
            if not CompilerData.ast or not CompilerData.symbol_table:
                error = {
                    'message': "No hay árbol de parseo o tabla de símbolos disponible. Ejecute primero el análisis sintáctico.",
                    'line': 1,
                    'column': 0,
                    'length': 1
                }
                CompilerData.semantic_errors = [error]
                return False, [error], None, None

            # Crear los componentes del análisis semántico
            try:
                symbol_table = SymbolTable(CompilerData.symbol_table)
            except Exception as e:
                import traceback
                traceback.print_exc()
                raise
            
            if hasattr(CompilerData, 'variable_renames'):
                symbol_table.variable_renames = CompilerData.variable_renames.copy()
                
            # Construir el mapa inverso para búsquedas
            symbol_table.inverse_renames = {}
            for scope, renames in symbol_table.variable_renames.items():
                for original, renamed in renames.items():
                    symbol_table.inverse_renames[renamed] = original
            
            error_reporter = ErrorReporter()
            type_checker = TypeChecker(symbol_table, error_reporter)
            scope_checker = ScopeChecker(symbol_table, error_reporter)
            visitor = ASTVisitor(symbol_table, type_checker, scope_checker, error_reporter)
            # Analizar el AST
            visitor.visit(CompilerData.ast, CompilerData.parser)
            
            # Verificar si hay errores (no advertencias)
            has_errors = error_reporter.has_errors()
            all_errors = error_reporter.get_errors()
            
            # Separar errores de advertencias
            errors = [e for e in all_errors if not e.get('is_warning', False)]

            # Actualizar errores en CompilerData (solo errores, no advertencias)
            CompilerData.semantic_errors = errors
            
            # Generar visualizaciones
            self._generate_semantic_graph(symbol_table)
            self._generate_enhanced_symbol_table(symbol_table, all_errors)
            
            # Guardar rutas en CompilerData
            CompilerData.semantic_graph_path = self.semantic_graph_path
            CompilerData.enhanced_symbol_table_path = self.enhanced_symbol_table_path
            
            # Solo fallar si hay errores reales, no advertencias
            if has_errors:
                return False, errors, self.semantic_graph_path, self.enhanced_symbol_table_path
            else:
                # Éxito - solo había advertencias o ningún problema
                return True, [], self.semantic_graph_path, self.enhanced_symbol_table_path
            
        except Exception as e:
            print(f"Error en análisis semántico: {e}")
            import traceback
            traceback.print_exc()
            
            error = {
                'message': f"Error en análisis semántico: {str(e)}",
                'line': 1,
                'column': 0,
                'length': 1
            }
            CompilerData.semantic_errors = [error]
            
            return False, [error], None, None
    
    def _generate_semantic_graph(self, symbol_table):
        """
        Generate a semantic analysis graph
        """
        try:
            graph = pydot.Dot(
                graph_type='digraph', 
                rankdir='TB',
                bgcolor="#f0f0f0",
                label="Semantic Analysis",
                fontsize="16"
            )
            
            # Crear nodos para cada ámbito
            scope_nodes = {}
            
            # Ámbito global
            global_scope = pydot.Node(
                "scope_global",
                label="Global Scope",
                shape="ellipse",
                style="filled",
                fillcolor="lightblue",
                fontsize="14"
            )
            graph.add_node(global_scope)
            scope_nodes["global"] = "scope_global"
            
            # Otros ámbitos
            all_symbols = symbol_table.get_all_symbols()
            for scope_name in all_symbols.keys():
                if scope_name != "global":
                    scope_node = pydot.Node(
                        f"scope_{scope_name}",
                        label=f"{scope_name} Scope",
                        shape="ellipse",
                        style="filled",
                        fillcolor="lightgreen",
                        fontsize="14"
                    )
                    graph.add_node(scope_node)
                    scope_nodes[scope_name] = f"scope_{scope_name}"
                    
                    # Conectar con ámbito global (las funciones son definidas en ámbito global)
                    if scope_name in symbol_table.functions:
                        edge = pydot.Edge(
                            "scope_global",
                            f"scope_{scope_name}",
                            label="defines",
                            fontsize="12"
                        )
                        graph.add_edge(edge)
            
            # Agregar variables y funciones
            for scope_name, symbols in all_symbols.items():
                for name, info in symbols.items():
                    var_type = info.get('type', 'unknown')
                    
                    # Elegir color según el tipo
                    if var_type == "int":
                        color = "lightblue"
                    elif var_type == "color":
                        color = "lightpink"
                    elif var_type == "bool":
                        color = "lightgreen"
                    elif var_type == "function":
                        color = "lightyellow"
                    elif var_type == "parameter":
                        color = "lightcyan"
                    else:
                        color = "lightgray"
                    
                    # Crear nodo para el símbolo
                    initialized = "Yes" if info.get('initialized', False) else "No"
                    used = "Yes" if info.get('used', False) else "No"
                    
                    node_label = f"{name}\\nType: {var_type}\\nInitialized: {initialized}\\nUsed: {used}"
                    
                    var_node = pydot.Node(
                        f"var_{scope_name}_{name}",
                        label=node_label,
                        shape="box",
                        style="filled",
                        fillcolor=color,
                        fontsize="12"
                    )
                    graph.add_node(var_node)
                    
                    # Conectar con su ámbito
                    edge = pydot.Edge(
                        scope_nodes[scope_name],
                        f"var_{scope_name}_{name}",
                        label="contains",
                        fontsize="10"
                    )
                    graph.add_edge(edge)
            
            # Guardar el gráfico
            graph.write_png(self.semantic_graph_path)
            
        except Exception as e:
            print(f"Error generating semantic graph: {e}")
            import traceback
            traceback.print_exc()
            self._create_error_image(f"Error generating semantic graph: {e}", self.semantic_graph_path)
    
    def _generate_enhanced_symbol_table(self, symbol_table, errors):
        """
        Generate an enhanced symbol table
        """
        try:
            graph = pydot.Dot(
                graph_type='digraph',
                rankdir='TB',
                bgcolor="#f0f0f0"
            )
            
            # Título
            title_node = pydot.Node(
                "title",
                label="Enhanced Symbol Table with Type Information",
                shape="plaintext",
                fontsize="18",
                fontcolor="blue"
            )
            graph.add_node(title_node)
            
            # Crear tabla HTML
            html_parts = [
                '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
                '<TR>'
                '<TD BGCOLOR="#d0e0ff"><B>Identifier</B></TD>'
                '<TD BGCOLOR="#d0e0ff"><B>Type</B></TD>'
                '<TD BGCOLOR="#d0e0ff"><B>Scope</B></TD>'
                '<TD BGCOLOR="#d0e0ff"><B>Line</B></TD>'
                '<TD BGCOLOR="#d0e0ff"><B>Initialized</B></TD>'
                '<TD BGCOLOR="#d0e0ff"><B>Used</B></TD>'
                '<TD BGCOLOR="#d0e0ff"><B>Status</B></TD>'
                '</TR>'
            ]
            
            # Obtener todos los símbolos
            all_symbols = symbol_table.get_all_symbols()
            all_rows = []
            
            for scope_name, symbols in all_symbols.items():
                for name, info in symbols.items():
                    # Escape HTML characters
                    name_esc = name.replace("<", "&lt;").replace(">", "&gt;")
                    var_type = info.get('type', 'unknown')
                    line = info.get('line', 0)
                    initialized = "Yes" if info.get('initialized', False) else "No"
                    used = "Yes" if info.get('used', False) else "No"
                    
                    # Determine status
                    status = "Valid"  # Por defecto, válido
                    status_color = "#90EE90"  # Light green
                    
                    if var_type == "unknown":
                        status = "Undeclared"
                        status_color = "#FFCCCB"  # Light red
                    elif not info.get('initialized', False):
                        status = "Not Initialized"
                        status_color = "#FFCCCB"  # Light red
                    elif not info.get('used', False):
                        status = "Unused"
                        status_color = "#FFFFB1"  # Light yellow
                    elif info.get('used', False) and not info.get('initialized', False):
                        if var_type not in ["function", "parameter"]:
                            status = "Used Before Init"
                            status_color = "#FFD580"  # Light orange
                    
                    # Agregar fila a la lista
                    all_rows.append({
                        "name": name_esc,
                        "type": var_type,
                        "scope": scope_name,
                        "line": line,
                        "initialized": initialized,
                        "used": used,
                        "status": status,
                        "status_color": status_color
                    })
            
            # Ordenar por ámbito y nombre
            all_rows.sort(key=lambda x: (x["scope"], x["name"]))
            
            # Construir las filas HTML
            for row in all_rows:
                html_parts.append(
                    f'<TR>'
                    f'<TD>{row["name"]}</TD>'
                    f'<TD>{row["type"]}</TD>'
                    f'<TD>{row["scope"]}</TD>'
                    f'<TD>{row["line"]}</TD>'
                    f'<TD>{row["initialized"]}</TD>'
                    f'<TD>{row["used"]}</TD>'
                    f'<TD BGCOLOR="{row["status_color"]}">{row["status"]}</TD>'
                    f'</TR>'
                )
            
            # Cerrar tabla HTML
            html_parts.append('</TABLE>>')
            table_label = "".join(html_parts)
            
            # Crear nodo con tabla HTML
            table_node = pydot.Node(
                "symbol_table",
                label=table_label,
                shape="plaintext"
            )
            graph.add_node(table_node)
            
            # Conectar nodos (invisible edge)
            graph.add_edge(pydot.Edge("title", "symbol_table", style="invis"))
            
            # Si hay errores o advertencias, agregarlos separadamente
            if errors:
                actual_errors = [e for e in errors if not e.get('is_warning', False)]
                warnings = [e for e in errors if e.get('is_warning', False)]
                
                if actual_errors:
                    error_html = [
                        '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
                        '<TR>'
                        '<TD BGCOLOR="#FFB6C1"><B>Semantic Errors</B></TD>'
                        '</TR>'
                    ]
                    
                    for error in actual_errors:
                        error_html.append(
                            f'<TR>'
                            f'<TD ALIGN="LEFT">Line {error["line"]}: {error["message"]}</TD>'
                            f'</TR>'
                        )
                    
                    error_html.append('</TABLE>>')
                    error_label = "".join(error_html)
                    
                    error_node = pydot.Node(
                        "errors",
                        label=error_label,
                        shape="plaintext"
                    )
                    graph.add_node(error_node)
                    graph.add_edge(pydot.Edge("symbol_table", "errors", style="invis"))
                
                if warnings:
                    warning_html = [
                        '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
                        '<TR>'
                        '<TD BGCOLOR="#FFE4B5"><B>Semantic Warnings</B></TD>'
                        '</TR>'
                    ]
                    
                    for warning in warnings:
                        warning_html.append(
                            f'<TR>'
                            f'<TD ALIGN="LEFT">Line {warning["line"]}: {warning["message"]}</TD>'
                            f'</TR>'
                        )
                    
                    warning_html.append('</TABLE>>')
                    warning_label = "".join(warning_html)
                    
                    warning_node = pydot.Node(
                        "warnings",
                        label=warning_label,
                        shape="plaintext"
                    )
                    graph.add_node(warning_node)
                    
                    if actual_errors:
                        graph.add_edge(pydot.Edge("errors", "warnings", style="invis"))
                    else:
                        graph.add_edge(pydot.Edge("symbol_table", "warnings", style="invis"))
            
            # Guardar el gráfico
            graph.write_png(self.enhanced_symbol_table_path)
            
        except Exception as e:
            print(f"Error generating enhanced symbol table: {e}")
            import traceback
            traceback.print_exc()
            self._create_error_image(f"Error generating enhanced symbol table: {e}", self.enhanced_symbol_table_path)
    
    def _create_error_image(self, error_message, output_path):
        """
        Create a simple error image
        
        Args:
            error_message: Error message to display
            output_path: Path to save the error image
        """
        try:
            graph = pydot.Dot(graph_type='digraph')
            node = pydot.Node(
                "error", 
                label=error_message, 
                shape="box", 
                style="filled", 
                fillcolor="red"
            )
            graph.add_node(node)
            graph.write_png(output_path)
        except Exception as e:
            print(f"Error creating error image: {e}")