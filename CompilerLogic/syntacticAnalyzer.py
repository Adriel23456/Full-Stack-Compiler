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
from config import BASE_DIR, ASSETS_DIR, CompilerData, States

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
        """
        # Reset state
        self.errors = []
        self.symbol_table = {}
        CompilerData.reset_syntactic()
        
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
            
            # Create a proper symbol table collector with renaming
            class SymbolTableCollector(VGraphListener):
                def __init__(self):
                    self.symbol_table = {}
                    self.current_function = None
                    self.parser = None
                    self.variable_renames = {}  # Map original names to renamed names
                    self.tree_renames = {}      # Map node IDs to rename information

                def set_parser(self, parser):
                    self.parser = parser

                def enterFunctionDeclStatement(self, ctx):
                    fname = ctx.ID().getText()
                    line = ctx.ID().symbol.line
                    
                    # Add function to symbol table
                    self.symbol_table[fname] = {
                        'type': 'function',
                        'scope': 'global',
                        'line': line,
                        'name': fname
                    }
                    
                    # Set current function
                    self.current_function = fname
                    
                    # IMPORTANTE: Inicializar el diccionario para esta función
                    if fname not in self.variable_renames:
                        self.variable_renames[fname] = {}
                    
                    # Process parameters with renaming
                    param_list = ctx.paramList()
                    if param_list:
                        for p in param_list.ID():
                            pname = p.getText()
                            pline = p.symbol.line
                            
                            # Apply renaming rule: param_name_function_name
                            renamed_param = f"{pname}_{fname}"
                            
                            # Add to symbol table with renamed key
                            self.symbol_table[renamed_param] = {
                                'type': 'parameter',
                                'scope': fname,
                                'line': pline,
                                'name': pname,  # Original name
                                'renamed_to': renamed_param
                            }
                            
                            # Store rename mapping for tree traversal
                            # IMPORTANTE: Guardar en el diccionario de la función, no como string
                            self.variable_renames[fname][pname] = renamed_param
                            
                            # Store tree node renaming information
                            self.tree_renames[id(p)] = {
                                'original': pname,
                                'renamed': renamed_param,
                                'context': 'parameter'
                            }

                def exitFunctionDeclStatement(self, ctx):
                    # Clear current function context
                    self.current_function = None
                    # Note: We keep the renames active for the entire analysis

                def enterDeclaration(self, ctx):
                    vartype = ctx.typeDeclaration().vartype().getText()
                    
                    # Process single ID declarations
                    if ctx.ID():
                        name = ctx.ID().getText()
                        line = ctx.ID().symbol.line
                        scope = self.current_function or 'global'
                        
                        # Use original name as key for non-parameters
                        key = name
                        if vartype == 'parameter' and self.current_function:
                            key = f"{name}_{self.current_function}"
                        
                        self.symbol_table[key] = {
                            'type': vartype,
                            'scope': scope,
                            'line': line,
                            'name': name
                        }
                    
                    # Process ID lists
                    if ctx.idList():
                        for id_node in ctx.idList().ID():
                            name = id_node.getText()
                            line = id_node.symbol.line
                            scope = self.current_function or 'global'
                            
                            # Use original name as key for non-parameters
                            key = name
                            if vartype == 'parameter' and self.current_function:
                                key = f"{name}_{self.current_function}"
                            
                            self.symbol_table[key] = {
                                'type': vartype,
                                'scope': scope,
                                'line': line,
                                'name': name
                            }

                def get_symbol_table(self):
                    """Get the symbol table with proper naming"""
                    return self.symbol_table
                
                def get_rename_map(self):
                    """Get the variable rename mapping with correct format"""
                    # Asegurarse de que el formato sea correcto
                    result = {}
                    
                    # self.variable_renames ya debería tener el formato correcto desde enterFunctionDeclStatement
                    for func_name, renames in self.variable_renames.items():
                        if isinstance(renames, dict):
                            result[func_name] = renames.copy()
                        else:
                            # Si por alguna razón está mal formateado, intentar corregirlo
                            print(f"=== WARNING: Incorrect format for {func_name}: {renames} ===")
                    
                    return result
                
                def get_tree_renames(self):
                    """Get the tree node rename information"""
                    return self.tree_renames

            # Create input stream 
            input_stream = InputStream(code_text)
            
            # Create error listener
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
                parse_tree = parser.program()
                
                # Check for syntax errors
                if error_listener.errors:
                    self.errors = error_listener.errors
                    return False, self.errors, None, None
                
                # Extract symbol table with renaming
                symbol_collector = SymbolTableCollector()
                symbol_collector.set_parser(parser)
                walker = ParseTreeWalker()
                walker.walk(symbol_collector, parse_tree)

                # Get the symbol table and renaming maps
                self.symbol_table = symbol_collector.get_symbol_table()
                self.variable_renames = symbol_collector.get_rename_map()
                self.tree_renames = symbol_collector.get_tree_renames()
                
                # Generate parse tree visualization with renaming
                self._visualize_parse_tree(parse_tree, parser)
                
                # Generate symbol table visualization
                self._visualize_symbol_table()

                print(f"=== DEBUG SyntacticAnalyzer: Before saving to CompilerData ===")
                print(f"symbol_table type: {type(self.symbol_table)}")
                print(f"symbol_table content: {self.symbol_table}")

                # Verificar que la tabla sea un diccionario
                if not isinstance(self.symbol_table, dict):
                    print(f"=== ERROR: symbol_table is not a dict! Converting... ===")
                
                

                # Store in CompilerData with renaming information
                CompilerData.symbol_table = self.symbol_table
                CompilerData.parse_tree_path = self.parse_tree_path
                CompilerData.symbol_table_path = self.symbol_table_path
                CompilerData.parser = parser
                CompilerData.ast = parse_tree
                
                # Store renaming information in CompilerData
                CompilerData.variable_renames = self.variable_renames
                CompilerData.tree_renames = self.tree_renames

                return True, [], self.parse_tree_path, self.symbol_table_path
                
            except Exception as e:
                print(f"Parser exception: {e}")
                import traceback
                traceback.print_exc()
                self.errors = error_listener.errors
                if not self.errors:
                    self.errors.append({
                        'message': f"Syntax error: {str(e)}",
                        'line': 1,
                        'column': 0,
                        'length': 0
                    })
                CompilerData.syntactic_errors = self.errors
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
            CompilerData.syntactic_errors = self.errors
            return False, self.errors, None, None

    def _visualize_parse_tree(self, parse_tree, parser):
        """
        Create a visualization of the parse tree using pydot with parameter renaming
        """
        try:
            # Configure the graph with more spacing
            graph = pydot.Dot(
                graph_type='graph', 
                rankdir='TB',
                ranksep='1.2',
                nodesep='1.0',
                ratio='expand',
                splines='polyline'
            )
            
            # Set default styling
            graph.set_graph_defaults(fontname='Arial')
            graph.set_node_defaults(fontname='Arial', fontsize='12')
            graph.set_edge_defaults(fontname='Arial', fontsize='10')
            
            # Add nodes and edges for the parse tree with renaming
            self._build_parse_tree_graph(graph, parse_tree, parser, None, 0)
            
            # Save the graph
            graph.write_png(self.parse_tree_path)
            
        except Exception as e:
            print(f"Error visualizing parse tree: {e}")
            self._create_error_image(f"Error visualizing parse tree: {e}", self.parse_tree_path)

    def _build_parse_tree_graph(self, graph, tree, parser, parent_node, node_id):
        """
        Recursively build the parse tree graph with parameter renaming applied
        """
        # Create node label
        if tree.getChildCount() == 0:
            # Terminal node (token)
            label = tree.getText()
            if label:
                # Check if this node has a renaming mapping
                node_id_ref = id(tree)
                if hasattr(self, 'tree_renames') and node_id_ref in self.tree_renames:
                    rename_info = self.tree_renames[node_id_ref]
                    if rename_info['context'] == 'parameter':
                        # This is a renamed parameter
                        label = rename_info['renamed']
                
                # Escape special characters for the label
                label = label.replace('"', '\\"').replace('\\', '\\\\')
                node_label = f'"{label}"'
            else:
                node_label = "ε"  # Epsilon for empty text
            
            # Create the node with lighter color for terminals, 
            # different color for renamed parameters
            fill_color = "lightblue"
            if hasattr(self, 'tree_renames') and id(tree) in self.tree_renames:
                if self.tree_renames[id(tree)]['context'] == 'parameter':
                    fill_color = "lightcoral"  # Different color for renamed parameters
            
            node = pydot.Node(str(node_id), label=node_label, shape="box", 
                            style="filled", fillcolor=fill_color)
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
    
    def _visualize_symbol_table(self):
        """
        Create a visualization of the symbol table using the simplified renaming
        """
        try:
            graph = pydot.Dot(graph_type='digraph', rankdir='TB')

            # Title node
            title_node = pydot.Node(
                "title",
                label="Symbol Table (with parameter renaming)",
                shape="plaintext",
                fontsize="18",
                fontcolor="blue"
            )
            graph.add_node(title_node)

            # Build HTML table
            html_parts = [
                '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
                '<TR>'
                '<TD BGCOLOR="#d0e0ff"><B>Renamed ID</B></TD>'
                '<TD BGCOLOR="#d0e0ff"><B>Original Name</B></TD>'
                '<TD BGCOLOR="#d0e0ff"><B>Type</B></TD>'
                '<TD BGCOLOR="#d0e0ff"><B>Scope</B></TD>'
                '<TD BGCOLOR="#d0e0ff"><B>Line</B></TD>'
                '</TR>'
            ]

            # Sort by scope and then by name
            sorted_symbols = sorted(self.symbol_table.items(), 
                                key=lambda x: (x[1].get('scope', 'global'), x[0]))

            # One row per symbol
            for symbol, info in sorted_symbols:
                # Get the original name and renamed name
                original_name = info.get('name', symbol)
                renamed_name = symbol
                
                # Escape special characters
                orig = original_name.replace("<", "&lt;").replace(">", "&gt;")
                renamed = renamed_name.replace("<", "&lt;").replace(">", "&gt;")
                typ = info.get('type', 'unknown').replace("<", "&lt;").replace(">", "&gt;")
                scp = info.get('scope', 'global').replace("<", "&lt;").replace(">", "&gt;")
                line = info.get('line', 0)

                html_parts.append(
                    f'<TR>'
                    f'<TD>{renamed}</TD>'
                    f'<TD>{orig}</TD>'
                    f'<TD>{typ}</TD>'
                    f'<TD>{scp}</TD>'
                    f'<TD>{line}</TD>'
                    f'</TR>'
                )

            html_parts.append('</TABLE>>')
            table_label = "".join(html_parts)

            # Create table node
            table_node = pydot.Node(
                "symbol_table",
                label=table_label,
                shape="plaintext"
            )
            graph.add_node(table_node)

            # Connect title and table
            graph.add_edge(pydot.Edge("title", "symbol_table", style="invis"))

            # Save
            graph.write_png(self.symbol_table_path)

        except Exception as e:
            print(f"Error visualizing symbol table: {e}")
            import traceback
            traceback.print_exc()
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