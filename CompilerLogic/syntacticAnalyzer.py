"""
Syntactic analyzer module for the Full Stack Compiler
Handles syntactic analysis of code and generates parse trees and symbol tables
"""
import os
import sys
import subprocess
from antlr4 import *
from antlr4.tree.Trees import Trees
from antlr4.error.ErrorListener import ErrorListener
import pydot
from config import BASE_DIR, ASSETS_DIR, States

class SyntacticAnalyzer:
    """
    Handles syntactic analysis of code
    """
    def __init__(self):
        """
        Initializes the syntactic analyzer
        """
        self.parse_tree_path = os.path.join(ASSETS_DIR, "Images", "parse_tree.png")
        self.symbol_table_path = os.path.join(ASSETS_DIR, "Images", "symbol_table.png")
        self.symbol_table = {}
        self.errors = []
        
        # Ensure Images directory exists
        images_dir = os.path.join(ASSETS_DIR, "Images")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
    
    def analyze(self, code_text):
        """
        Analyze the given code text using the ANTLR parser
        
        Args:
            code_text: Source code to analyze
            
        Returns:
            tuple: (success, errors, parse_tree_path, symbol_table_path)
        """
        # Reset state
        self.errors = []
        self.symbol_table = {}
        
        # Ensure the ANTLR parser files are generated
        if not self._ensure_parser_generated():
            self.errors.append({
                'message': "Failed to generate parser. Check console for details.",
                'line': 1,
                'column': 0,
                'length': 0
            })
            return False, self.errors, None, None
        
        try:
            # Import the generated lexer and parser
            sys.path.append(os.path.abspath(ASSETS_DIR))
            from VGraphLexer import VGraphLexer
            from VGraphParser import VGraphParser
            from VGraphListener import VGraphListener
            
            # Create a proper symbol table collector
            class SymbolTableCollector(VGraphListener):
                def __init__(self):
                    # Tabla de símbolos global: nombre → info
                    self.symbol_table = {}
                    # Pila de ámbitos; arrancamos en "global"
                    self.scope_stack = ["global"]

                def current_scope(self):
                    return self.scope_stack[-1]

                # ----- Scope management -----
                def enterProgram(self, ctx):
                    self.symbol_table.clear()
                    self.scope_stack = ["global"]

                def enterFunctionDeclStatement(self, ctx):
                    fname = ctx.ID().getText()
                    # registramos la función en el scope "global"
                    self.symbol_table[fname] = {
                        'type': 'function',
                        'scope': 'global',
                        'line': ctx.start.line
                    }
                    # entramos en el nuevo scope de la función
                    self.scope_stack.append(fname)
                    # parámetros quedan en el scope de la función
                    param_list = ctx.paramList()
                    if param_list:
                        for p in param_list.ID():
                            pname = p.getText()
                            self.symbol_table[pname] = {
                                'type': 'parameter',
                                'scope': fname,
                                'line': p.symbol.line
                            }

                def exitFunctionDeclStatement(self, ctx):
                    # salimos del scope de la función
                    self.scope_stack.pop()

                def enterFrameStatement(self, ctx):
                    # creamos un scope genérico "frame"
                    # si quieres distinguir varios frames, podrías usar ctx.start.line
                    self.scope_stack.append("frame")

                def exitFrameStatement(self, ctx):
                    self.scope_stack.pop()

                # ----- Declaraciones y asignaciones -----
                def enterDeclaration(self, ctx):
                    # puede ser single ID o lista
                    vartype = ctx.typeDeclaration().vartype().getText()
                    # caso ID único
                    if ctx.ID():
                        name = ctx.ID().getText()
                        self.symbol_table[name] = {
                            'type': vartype,
                            'scope': self.current_scope(),
                            'line': ctx.start.line
                        }
                    # caso lista
                    if ctx.idList():
                        for id_node in ctx.idList().ID():
                            name = id_node.getText()
                            self.symbol_table[name] = {
                                'type': vartype,
                                'scope': self.current_scope(),
                                'line': id_node.symbol.line
                            }

                def enterAssignmentStatement(self, ctx):
                    # el ID está dentro de assignmentExpression()
                    assignCtx = ctx.assignmentExpression()
                    name = assignCtx.ID().getText()
                    if name not in self.symbol_table:
                        self.symbol_table[name] = {
                            'type': 'unknown',
                            'scope': self.current_scope(),
                            'line': ctx.start.line
                        }

                # Métodos vacíos del listener
                def enterEveryRule(self, ctx): pass
                def exitEveryRule(self, ctx): pass
                def visitTerminal(self, node): pass
                def visitErrorNode(self, node): pass

            
            # Create input stream 
            input_stream = InputStream(code_text)
            
            # Create error listener to capture syntax errors
            error_listener = SyntaxErrorListener()
            
            # Create lexer
            lexer = VGraphLexer(input_stream)
            lexer.removeErrorListeners()
            lexer.addErrorListener(error_listener)
            
            # Create token stream
            token_stream = CommonTokenStream(lexer)
            
            # Create parser
            parser = VGraphParser(token_stream)
            parser.removeErrorListeners()
            parser.addErrorListener(error_listener)
            
            # Parse the input
            try:
                parse_tree = parser.program()  # Start rule
                
                # Check for syntax errors
                if error_listener.errors:
                    self.errors = error_listener.errors
                    return False, self.errors, None, None
                
                # Generate parse tree visualization
                self._visualize_parse_tree(parse_tree, parser)
                
                # Extract symbol table
                symbol_collector = SymbolTableCollector()
                walker = ParseTreeWalker()
                walker.walk(symbol_collector, parse_tree)
                self.symbol_table = symbol_collector.symbol_table
                
                # Generate symbol table visualization
                self._visualize_symbol_table()
                
                return True, [], self.parse_tree_path, self.symbol_table_path
                
            except Exception as e:
                print(f"Parser exception: {e}")
                import traceback
                traceback.print_exc()
                self.errors = error_listener.errors
                if not self.errors:
                    # If no specific errors were captured by the listener,
                    # add a generic one
                    self.errors.append({
                        'message': f"Syntax error: {str(e)}",
                        'line': 1,
                        'column': 0,
                        'length': 0
                    })
                return False, self.errors, None, None
            
        except Exception as e:
            print(f"Error in syntactic analysis: {e}")
            import traceback
            traceback.print_exc()
            self.errors.append({
                'message': f"Syntactic analysis error: {str(e)}",
                'line': 1,
                'column': 0,
                'length': 0
            })
            return False, self.errors, None, None
    
    def _ensure_parser_generated(self):
        """
        Ensure the ANTLR parser files are generated
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Get paths
        grammar_file = os.path.join(ASSETS_DIR, 'VGraph.g4')
        antlr_jar = '/tmp/antlr-4.9.2-complete.jar'
        
        # Check if grammar file exists
        if not os.path.exists(grammar_file):
            print(f"Error: Grammar file not found at {grammar_file}")
            return False
        
        # Check if ANTLR jar exists
        if not os.path.exists(antlr_jar):
            print(f"Error: ANTLR jar not found at {antlr_jar}")
            try:
                # Try to download ANTLR jar
                print("Downloading ANTLR jar...")
                subprocess.run(['wget', 'https://www.antlr.org/download/antlr-4.9.2-complete.jar', '-P', '/tmp/'], 
                              check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print("ANTLR jar downloaded successfully")
            except Exception as e:
                print(f"Failed to download ANTLR jar: {e}")
                return False
        
        # Always regenerate parser for consistency
        try:
            current_dir = os.getcwd()
            os.chdir(ASSETS_DIR)
            
            # Generate parser with visitor option
            cmd = ['java', '-jar', antlr_jar, '-Dlanguage=Python3', '-visitor', 'VGraph.g4']
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Check if command was successful
            if result.returncode != 0:
                error_message = result.stderr.decode('utf-8')
                print(f"Error generating parser: {error_message}")
                os.chdir(current_dir)
                return False
                
            print("Parser generated successfully")
            os.chdir(current_dir)
            return True
        except Exception as e:
            print(f"Error generating parser: {e}")
            if current_dir != os.getcwd():
                os.chdir(current_dir)
            return False
    
    def _visualize_parse_tree(self, parse_tree, parser):
        """
        Create a visualization of the parse tree using pydot
        
        Args:
            parse_tree: ANTLR parse tree
            parser: ANTLR parser
        """
        try:
            # Modificar la configuración del grafo para agregar más espacio
            graph = pydot.Dot(
                graph_type='graph', 
                rankdir='TB',      # Top to Bottom layout
                ranksep='1.2',     # Aumentar espacio vertical entre rangos (niveles)
                nodesep='1.0',     # Aumentar espacio horizontal entre nodos
                ratio='expand',  # Ajustar ratio para mejor uso del espacio
                splines='polyline'  # Segmentos de línea conectados
            )
            
            # Configuración adicional para mejorar la legibilidad
            graph.set_graph_defaults(fontname='Arial')
            graph.set_node_defaults(fontname='Arial', fontsize='12')
            graph.set_edge_defaults(fontname='Arial', fontsize='10')
            
            # Add nodes and edges for the parse tree
            self._build_parse_tree_graph(graph, parse_tree, parser, None, 0)
            
            # Save the graph
            graph.write_png(self.parse_tree_path)
            
        except Exception as e:
            print(f"Error visualizing parse tree: {e}")
            # Create a simple error image if visualization fails
            self._create_error_image(f"Error visualizing parse tree: {e}", self.parse_tree_path)
    
    def _build_parse_tree_graph(self, graph, tree, parser, parent_node, node_id):
        """
        Recursively build the parse tree graph
        
        Args:
            graph: pydot graph
            tree: ANTLR parse tree node
            parser: ANTLR parser
            parent_node: Parent node ID
            node_id: Current node ID
            
        Returns:
            int: Next available node ID
        """
        # Create node label
        if tree.getChildCount() == 0:
            # Terminal node (token)
            label = tree.getText()
            if label:
                # Escape special characters for the label
                label = label.replace('"', '\\"').replace('\\', '\\\\')
                node_label = f'"{label}"'
            else:
                node_label = "ε"  # Epsilon for empty text
            
            # Create the node with lighter color for terminals
            node = pydot.Node(str(node_id), label=node_label, shape="box", 
                             style="filled", fillcolor="lightblue")
        else:
            # Non-terminal node (rule)
            rule_name = parser.ruleNames[tree.getRuleIndex()]
            node = pydot.Node(str(node_id), label=rule_name, shape="ellipse",
                             style="filled", fillcolor="lightgreen")
        
        # Add the node to the graph
        graph.add_node(node)
        
        # Connect with parent if there is one
        if parent_node is not None:
            edge = pydot.Edge(str(parent_node), str(node_id))
            graph.add_edge(edge)
        
        # Recursively process child nodes
        next_id = node_id + 1
        for i in range(tree.getChildCount()):
            child = tree.getChild(i)
            next_id = self._build_parse_tree_graph(graph, child, parser, node_id, next_id)
        
        return next_id
    
    def _visualize_symbol_table(self):
        """
        Create a visualization of the symbol table using pydot with an HTML table label.
        """
        try:
            graph = pydot.Dot(graph_type='digraph', rankdir='TB')

            # Nodo título
            title_node = pydot.Node(
                "title",
                label="Symbol Table",
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
                '</TR>'
            ]

            # Una fila por cada símbolo
            for symbol, info in self.symbol_table.items():
                sym = symbol.replace("<", "&lt;").replace(">", "&gt;")
                typ = info.get('type', 'unknown').replace("<", "&lt;").replace(">", "&gt;")
                scp = info.get('scope', 'global').replace("<", "&lt;").replace(">", "&gt;")
                line = info.get('line', 0)

                html_parts.append(
                    f'<TR>'
                      f'<TD>{sym}</TD>'
                      f'<TD>{typ}</TD>'
                      f'<TD>{scp}</TD>'
                      f'<TD>{line}</TD>'
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
            graph.write_png(self.symbol_table_path)

        except Exception as e:
            print(f"Error visualizing symbol table: {e}")
            import traceback
            traceback.print_exc()
            # En caso de fallo, mostramos un mensaje de error
            self._create_error_image(f"Error visualizing symbol table: {e}", self.symbol_table_path)
    
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


class SyntaxErrorListener(ErrorListener):
    """
    Custom error listener to capture syntax errors
    """
    def __init__(self):
        super().__init__()
        self.errors = []
        
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        """
        Handle syntax error
        """
        error_info = {
            'message': f"Syntax error at line {line}:{column}: {msg}",
            'line': line,
            'column': column,
            'length': len(offendingSymbol.text) if offendingSymbol else 1
        }
        self.errors.append(error_info)
        
    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        """
        Handle ambiguity report (optional)
        """
        pass
    
    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        """
        Handle attempting full context report (optional)
        """
        pass
    
    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        """
        Handle context sensitivity report (optional)
        """
        pass