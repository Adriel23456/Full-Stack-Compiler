"""
Syntactic analyzer module for the Full Stack Compiler
Handles syntactic analysis of code and generates parse trees and symbol tables
Cross-platform compatible (Windows/Linux/MacOS)
"""
import os
import sys
import subprocess
import platform
import tempfile
import urllib.request
import urllib.error
from pathlib import Path

# Try to import required modules with fallbacks
try:
    from antlr4 import *
    from antlr4.tree.Trees import Trees
    from antlr4.error.ErrorListener import ErrorListener
    ANTLR4_AVAILABLE = True
except ImportError:
    ANTLR4_AVAILABLE = False
    print("Warning: antlr4 module not found. Install with: pip install antlr4-python3-runtime")

try:
    import pydot
    PYDOT_AVAILABLE = True
except ImportError:
    PYDOT_AVAILABLE = False
    print("Warning: pydot module not found. Install with: pip install pydot")

from config import BASE_DIR, ASSETS_DIR, CompilerData, States

class SyntacticAnalyzer:
    """
    Handles syntactic analysis of code - Cross-platform compatible
    """
    def __init__(self):
        """
        Initializes the syntactic analyzer
        """
        self.parse_tree_path = os.path.join(ASSETS_DIR, "Images", "parse_tree.png")
        self.symbol_table_path = os.path.join(ASSETS_DIR, "Images", "symbol_table.png")
        self.symbol_table = {}
        self.errors = []
        
        # Platform detection
        self.platform = platform.system().lower()
        self.is_windows = self.platform == 'windows'
        self.is_linux = self.platform == 'linux'
        self.is_mac = self.platform == 'darwin'
        
        # Set platform-specific paths and commands
        self._setup_platform_specifics()
        
        # Ensure Images directory exists
        images_dir = os.path.join(ASSETS_DIR, "Images")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
    
    def _setup_platform_specifics(self):
        """Setup platform-specific configurations"""
        if self.is_windows:
            # Use Windows temp directory
            self.temp_dir = tempfile.gettempdir()
            self.antlr_jar_path = os.path.join(self.temp_dir, 'antlr-4.9.2-complete.jar')
            self.java_cmd = 'java'
        else:
            # Linux/Mac - use /tmp as before
            self.temp_dir = '/tmp'
            self.antlr_jar_path = '/tmp/antlr-4.9.2-complete.jar'
            self.java_cmd = 'java'
    
    def _check_dependencies(self):
        """Check if required dependencies are available"""
        missing_deps = []
        
        if not ANTLR4_AVAILABLE:
            missing_deps.append('antlr4-python3-runtime')
        
        if not PYDOT_AVAILABLE:
            missing_deps.append('pydot')
        
        # Check if Java is available
        try:
            subprocess.run([self.java_cmd, '-version'], 
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                         check=True, timeout=10)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            missing_deps.append('java (JRE/JDK)')
        
        return missing_deps
    
    def _install_missing_dependencies(self):
        """Try to install missing Python dependencies automatically"""
        missing_deps = []
        
        if not ANTLR4_AVAILABLE:
            try:
                print("Installing antlr4-python3-runtime...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'antlr4-python3-runtime'], 
                             check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print("Successfully installed antlr4-python3-runtime")
            except subprocess.CalledProcessError:
                missing_deps.append('antlr4-python3-runtime')
        
        if not PYDOT_AVAILABLE:
            try:
                print("Installing pydot...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'pydot'], 
                             check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print("Successfully installed pydot")
            except subprocess.CalledProcessError:
                missing_deps.append('pydot')
        
        return missing_deps
    
    def _download_file(self, url, destination):
        """
        Cross-platform file download
        
        Args:
            url: URL to download from
            destination: Path to save the file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self.is_windows:
                # Use urllib for Windows (no wget)
                print(f"Downloading {url}...")
                urllib.request.urlretrieve(url, destination)
                print("Download completed successfully")
                return True
            else:
                # Use wget for Linux/Mac (if available)
                try:
                    subprocess.run(['wget', url, '-O', destination], 
                                 check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    print("Download completed successfully with wget")
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # Fallback to urllib if wget not available
                    print("wget not available, using urllib...")
                    urllib.request.urlretrieve(url, destination)
                    print("Download completed successfully with urllib")
                    return True
        except Exception as e:
            print(f"Failed to download file: {e}")
            return False
    
    def analyze(self, code_text):
        """
        Analyze the given code text using the ANTLR parser
        """
        # Reset state
        self.errors = []
        self.symbol_table = {}
        CompilerData.reset_syntactic()
        
        # Check dependencies first
        if not ANTLR4_AVAILABLE:
            missing_deps = self._install_missing_dependencies()
            if 'antlr4-python3-runtime' in missing_deps:
                self.errors.append({
                    'message': "ANTLR4 Python runtime not available. Please install with: pip install antlr4-python3-runtime",
                    'line': 1,
                    'column': 0,
                    'length': 0
                })
                return False, self.errors, None, None
        
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
        if not PYDOT_AVAILABLE:
            print("Warning: pydot not available, creating text visualization")
            self._create_text_parse_tree(parse_tree, parser)
            return
        
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

    def _create_text_parse_tree(self, parse_tree, parser):
        """
        Create a text-based parse tree when pydot is not available
        """
        try:
            tree_text = "PARSE TREE (Text Mode)\n"
            tree_text += "=" * 50 + "\n\n"
            
            def traverse_tree(node, depth=0):
                indent = "  " * depth
                if node.getChildCount() == 0:
                    # Terminal node
                    text = node.getText()
                    if hasattr(self, 'tree_renames') and id(node) in self.tree_renames:
                        rename_info = self.tree_renames[id(node)]
                        if rename_info['context'] == 'parameter':
                            text = f"{text} -> {rename_info['renamed']}"
                    return f"{indent}Terminal: '{text}'\n"
                else:
                    # Non-terminal node
                    rule_name = parser.ruleNames[node.getRuleIndex()]
                    result = f"{indent}Rule: {rule_name}\n"
                    for i in range(node.getChildCount()):
                        result += traverse_tree(node.getChild(i), depth + 1)
                    return result
            
            tree_text += traverse_tree(parse_tree)
            
            # Save as text file
            text_path = self.parse_tree_path.replace('.png', '.txt')
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(tree_text)
            
            print(f"Parse tree saved as text file: {text_path}")
            
        except Exception as e:
            print(f"Error creating text parse tree: {e}")

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
        Ensure the ANTLR parser files are generated - Cross-platform compatible
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Get paths
        grammar_file = os.path.join(ASSETS_DIR, 'VGraph.g4')
        
        # Check if grammar file exists
        if not os.path.exists(grammar_file):
            print(f"Error: Grammar file not found at {grammar_file}")
            return False
        
        # Check if ANTLR jar exists
        if not os.path.exists(self.antlr_jar_path):
            print(f"ANTLR jar not found at {self.antlr_jar_path}")
            
            # Ensure temp directory exists
            os.makedirs(os.path.dirname(self.antlr_jar_path), exist_ok=True)
            
            # Download ANTLR jar
            antlr_url = 'https://www.antlr.org/download/antlr-4.9.2-complete.jar'
            if not self._download_file(antlr_url, self.antlr_jar_path):
                return False
        
        # Always regenerate parser for consistency
        try:
            current_dir = os.getcwd()
            os.chdir(ASSETS_DIR)
            
            # Generate parser with visitor option - platform independent
            cmd = [self.java_cmd, '-jar', self.antlr_jar_path, '-Dlanguage=Python3', '-visitor', 'VGraph.g4']
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Check if command was successful
            if result.returncode != 0:
                error_message = result.stderr.decode('utf-8')
                print(f"Error generating parser: {error_message}")
                os.chdir(current_dir)
                return False
                
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
        if not PYDOT_AVAILABLE:
            print("Warning: pydot not available, creating text symbol table")
            self._create_text_symbol_table()
            return
        
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
    
    def _create_text_symbol_table(self):
        """
        Create a text-based symbol table when pydot is not available
        """
        try:
            table_text = "SYMBOL TABLE (Text Mode)\n"
            table_text += "=" * 50 + "\n\n"
            table_text += f"{'Renamed ID':<20} {'Original':<15} {'Type':<12} {'Scope':<15} {'Line':<5}\n"
            table_text += "-" * 67 + "\n"
            
            # Sort by scope and then by name
            sorted_symbols = sorted(self.symbol_table.items(), 
                                key=lambda x: (x[1].get('scope', 'global'), x[0]))

            for symbol, info in sorted_symbols:
                original_name = info.get('name', symbol)
                renamed_name = symbol
                typ = info.get('type', 'unknown')
                scope = info.get('scope', 'global')
                line = info.get('line', 0)
                
                table_text += f"{renamed_name:<20} {original_name:<15} {typ:<12} {scope:<15} {line:<5}\n"
            
            # Save as text file
            text_path = self.symbol_table_path.replace('.png', '.txt')
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(table_text)
            
            print(f"Symbol table saved as text file: {text_path}")
            
        except Exception as e:
            print(f"Error creating text symbol table: {e}")
    
    def _create_error_image(self, error_message, output_path):
        """
        Create a simple error image when visualization fails
        
        Args:
            error_message: Error message to display
            output_path: Path to save the error image
        """
        if not PYDOT_AVAILABLE:
            # Create text file instead
            try:
                error_text = f"ERROR IN VISUALIZATION\n{'=' * 40}\n\n{error_message}"
                text_path = output_path.replace('.png', '_error.txt')
                with open(text_path, 'w', encoding='utf-8') as f:
                    f.write(error_text)
                print(f"Error details saved to: {text_path}")
            except Exception as e:
                print(f"Error creating error file: {e}")
            return
        
        try:
            graph = pydot.Dot(graph_type='digraph')
            node = pydot.Node("error", label=error_message, shape="box", 
                             style="filled", fillcolor="red")
            graph.add_node(node)
            graph.write_png(output_path)
        except Exception as e:
            print(f"Error creating error image: {e}")

    def get_system_info(self):
        """
        Get system information for debugging
        
        Returns:
            dict: System information
        """
        return {
            'platform': self.platform,
            'is_windows': self.is_windows,
            'is_linux': self.is_linux,
            'is_mac': self.is_mac,
            'temp_dir': self.temp_dir,
            'antlr_jar_path': self.antlr_jar_path,
            'antlr4_available': ANTLR4_AVAILABLE,
            'pydot_available': PYDOT_AVAILABLE,
            'python_version': sys.version,
            'missing_dependencies': self._check_dependencies()
        }


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