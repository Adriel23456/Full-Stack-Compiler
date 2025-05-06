"""
Semantic analyzer module for the Full Stack Compiler
Handles semantic analysis of code, type checking, and semantic error detection
"""
import os
import sys
from antlr4 import *
from antlr4.tree.Trees import Trees
import pydot
from config import BASE_DIR, ASSETS_DIR

class SemanticAnalyzer:
    """
    Handles semantic analysis of code
    """
    def __init__(self):
        """
        Initializes the semantic analyzer
        """
        self.errors = []
        self.semantic_analysis_path = os.path.join(ASSETS_DIR, "Images", "semantic_analysis.png")
        self.enhanced_symbol_table_path = os.path.join(ASSETS_DIR, "Images", "enhanced_symbol_table.png")
        self.enhanced_symbol_table = {}
        self.current_scope = ["global"]
        self.type_system = {
            "int": {"compatible_with": ["int"]},
            "color": {"compatible_with": ["color"]},
            "bool": {"compatible_with": ["bool"]}
        }
        
        # Ensure Images directory exists
        images_dir = os.path.join(ASSETS_DIR, "Images")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
    
    def analyze(self, parse_tree, symbol_table):
        """
        Perform semantic analysis on the parse tree
        
        Args:
            parse_tree: ANTLR parse tree from syntactic analyzer
            symbol_table: Symbol table from syntactic analyzer
            
        Returns:
            tuple: (success, errors, semantic_analysis_path, enhanced_symbol_table_path)
        """
        # Reset state
        self.errors = []
        
        # Verify if parse_tree is None
        if parse_tree is None:
            error_message = "Error de análisis semántico: Árbol sintáctico no disponible"
            self.errors.append({
                'message': error_message,
                'line': 1,
                'column': 0,
                'length': 10
            })
            # Create visualizations with error info
            self._create_semantic_analysis_graph()
            self._create_enhanced_symbol_table_visualization(symbol_table or {})
            return False, self.errors, self.semantic_analysis_path, self.enhanced_symbol_table_path
            
        # Initialize the enhanced symbol table from the provided symbol table
        self.enhanced_symbol_table = symbol_table.copy() if symbol_table else {}
        
        try:
            # Import ANTLR-generated visitor
            sys.path.append(os.path.abspath(ASSETS_DIR))
            from VGraphVisitor import VGraphVisitor
            from VGraphParser import VGraphParser
            
            # Implement basic semantic checking (first phase)
            # Check variable declarations, scope, and usage
            self._check_basic_semantics(parse_tree)
            
            # If we have errors, stop the analysis and report them
            if self.errors:
                self._create_semantic_analysis_graph()
                self._create_enhanced_symbol_table_visualization(self.enhanced_symbol_table)
                return False, self.errors, self.semantic_analysis_path, self.enhanced_symbol_table_path
            
            # Create visualizations for successful analysis
            self._create_semantic_analysis_graph()
            self._create_enhanced_symbol_table_visualization(self.enhanced_symbol_table)
            
            return True, [], self.semantic_analysis_path, self.enhanced_symbol_table_path
            
        except Exception as e:
            print(f"Error during semantic analysis: {e}")
            import traceback
            traceback.print_exc()
            
            # Add a generic error
            error_message = f"Error durante el análisis semántico: {str(e)}"
            self.errors.append({
                'message': error_message,
                'line': 1,
                'column': 0,
                'length': 10
            })
            
            # Create visualizations with error info
            self._create_semantic_analysis_graph()
            self._create_enhanced_symbol_table_visualization(self.enhanced_symbol_table)
            
            return False, self.errors, self.semantic_analysis_path, self.enhanced_symbol_table_path
    
    def _check_basic_semantics(self, parse_tree):
        """
        Implement basic semantic checking for variable declarations and usage
        This is a simplified placeholder for the first phase of semantic analysis
        """
        # For demonstration, add a simulated error
        # In a real implementation, this would analyze the parse tree
        # For now, we'll simulate finding an undeclared variable
        self.errors.append({
            'message': "Variable 'x' utilizada pero no ha sido declarada",
            'line': 5,
            'column': 1,
            'length': 10
        })
    
    def _create_semantic_analysis_graph(self):
        """
        Create a visualization of the semantic analysis results using pydot
        """
        try:
            graph = pydot.Dot(graph_type='digraph', rankdir='TB')
            
            # If we have errors, show them in the graph
            if self.errors:
                # Add title for errors
                error_title = pydot.Node(
                    "error_title",
                    label="Semantic Analysis Errors",
                    shape="plaintext",
                    fontsize="18",
                    fontcolor="red"
                )
                graph.add_node(error_title)
                
                # Create HTML table for errors
                html_parts = [
                    '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
                    '<TR>'
                      '<TD BGCOLOR="#ffcccb"><B>Line</B></TD>'
                      '<TD BGCOLOR="#ffcccb"><B>Column</B></TD>'
                      '<TD BGCOLOR="#ffcccb"><B>Error Message</B></TD>'
                    '</TR>'
                ]
                
                for error in self.errors:
                    html_parts.append(
                        f'<TR>'
                          f'<TD>{error["line"]}</TD>'
                          f'<TD>{error["column"]}</TD>'
                          f'<TD>{error["message"]}</TD>'
                        f'</TR>'
                    )
                
                html_parts.append('</TABLE>>')
                table_label = "".join(html_parts)
                
                errors_node = pydot.Node(
                    "errors_table",
                    label=table_label,
                    shape="plaintext"
                )
                graph.add_node(errors_node)
                
                # Connect title to table
                graph.add_edge(pydot.Edge("error_title", "errors_table"))
            else:
                # If no errors, show success message
                success_node = pydot.Node(
                    "success",
                    label="Semantic Analysis Completed Successfully\nNo Errors Found",
                    shape="box",
                    style="filled",
                    fillcolor="lightgreen"
                )
                graph.add_node(success_node)
                
                # Add statistics about symbols analyzed
                stats_html = f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
                stats_html += f'<TR><TD BGCOLOR="#d0ffd0"><B>Total Symbols Analyzed</B></TD><TD>{len(self.enhanced_symbol_table)}</TD></TR>'
                
                # Count variables, functions, etc.
                var_count = sum(1 for info in self.enhanced_symbol_table.values() if info.get('type') == 'variable')
                func_count = sum(1 for info in self.enhanced_symbol_table.values() if info.get('type') == 'function')
                param_count = sum(1 for info in self.enhanced_symbol_table.values() if info.get('type') == 'parameter')
                
                stats_html += f'<TR><TD BGCOLOR="#d0ffd0"><B>Variables</B></TD><TD>{var_count}</TD></TR>'
                stats_html += f'<TR><TD BGCOLOR="#d0ffd0"><B>Functions</B></TD><TD>{func_count}</TD></TR>'
                stats_html += f'<TR><TD BGCOLOR="#d0ffd0"><B>Parameters</B></TD><TD>{param_count}</TD></TR>'
                stats_html += '</TABLE>>'
                
                stats_node = pydot.Node(
                    "stats",
                    label=stats_html,
                    shape="plaintext"
                )
                graph.add_node(stats_node)
                
                graph.add_edge(pydot.Edge("success", "stats"))
            
            # Save the graph
            graph.write_png(self.semantic_analysis_path)
            
        except Exception as e:
            print(f"Error creating semantic analysis graph: {e}")
            import traceback
            traceback.print_exc()
            self._create_error_image(f"Error creating semantic analysis graph: {e}", 
                                   self.semantic_analysis_path)
    
    def _create_enhanced_symbol_table_visualization(self, symbol_table):
        """
        Create a visualization of the enhanced symbol table using pydot with an HTML table label.
        """
        try:
            graph = pydot.Dot(graph_type='digraph', rankdir='TB')

            # Nodo título
            title_node = pydot.Node(
                "title",
                label="Enhanced Symbol Table",
                shape="plaintext",
                fontsize="18",
                fontcolor="blue"
            )
            graph.add_node(title_node)

            # Construimos el label HTML de la tabla
            html_parts = [
                '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
                '<TR>'
                  '<TD BGCOLOR="#d0e0ff"><B>ID</B></TD>'
                  '<TD BGCOLOR="#d0e0ff"><B>Type</B></TD>'
                  '<TD BGCOLOR="#d0e0ff"><B>Scope</B></TD>'
                  '<TD BGCOLOR="#d0e0ff"><B>Line</B></TD>'
                  '<TD BGCOLOR="#d0e0ff"><B>Data Type</B></TD>'
                  '<TD BGCOLOR="#d0e0ff"><B>Status</B></TD>'
                '</TR>'
            ]

            # Una fila por cada símbolo
            for symbol, info in symbol_table.items():
                sym = symbol.replace("<", "&lt;").replace(">", "&gt;")
                typ = info.get('type', 'unknown').replace("<", "&lt;").replace(">", "&gt;")
                scp = info.get('scope', 'global').replace("<", "&lt;").replace(">", "&gt;")
                line = info.get('line', 0)
                # Campos adicionales para la tabla mejorada
                data_type = info.get('data_type', 'unknown')
                status = info.get('status', 'declared')

                html_parts.append(
                    f'<TR>'
                      f'<TD>{sym}</TD>'
                      f'<TD>{typ}</TD>'
                      f'<TD>{scp}</TD>'
                      f'<TD>{line}</TD>'
                      f'<TD>{data_type}</TD>'
                      f'<TD>{status}</TD>'
                    f'</TR>'
                )

            # Cerramos la tabla y el label HTML
            html_parts.append('</TABLE>>')
            table_label = "".join(html_parts)

            # Creamos el nodo con HTML-like label
            table_node = pydot.Node(
                "symbol_table",
                label=table_label,
                shape="plaintext"
            )
            graph.add_node(table_node)

            # Conectamos título y tabla (invisible)
            graph.add_edge(pydot.Edge("title", "symbol_table", style="invis"))

            # Guardamos
            graph.write_png(self.enhanced_symbol_table_path)

        except Exception as e:
            print(f"Error visualizing enhanced symbol table: {e}")
            import traceback
            traceback.print_exc()
            self._create_error_image(f"Error visualizing enhanced symbol table: {e}", 
                                   self.enhanced_symbol_table_path)
    
    def _create_error_image(self, error_message, output_path):
        """
        Create a simple error image when visualization fails
        
        Args:
            error_message: Error message to display
            output_path: Path to save the error image
        """
        try:
            graph = pydot.Dot(graph_type='digraph')
            node = pydot.Node("error", label=error_message, shape="box", 
                             style="filled", fillcolor="red")
            graph.add_node(node)
            graph.write_png(output_path)
        except Exception as e:
            print(f"Error creating error image: {e}")