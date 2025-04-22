"""
Lexical analyzer module for the Full Stack Compiler
Handles lexical analysis of code and generates token graphs
"""
import os
import sys
import subprocess
from antlr4 import *
import pydot
from config import BASE_DIR, ASSETS_DIR

class LexicalAnalyzer:
    """
    Handles lexical analysis of code
    """
    def __init__(self):
        """
        Initializes the lexical analyzer
        """
        self.tokens = []
        self.errors = []
        self.token_graph_path = os.path.join(ASSETS_DIR, "Images", "token_graph.png")
        
        # Ensure Images directory exists
        images_dir = os.path.join(ASSETS_DIR, "Images")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
    
    def analyze(self, code_text):
        """
        Analyze the given code text using the ANTLR lexer
        
        Args:
            code_text: Source code to analyze
            
        Returns:
            tuple: (success, errors, token_graph_path)
        """
        # Reset state
        self.tokens = []
        self.errors = []
        
        # Ensure the ANTLR lexer files are generated
        if not self._ensure_lexer_generated():
            self.errors.append({
                'message': "Failed to generate lexer. Check console for details.",
                'line': 1,
                'column': 0,
                'length': 0
            })
            return False, self.errors, None
        
        try:
            # Import the generated lexer
            sys.path.append(os.path.abspath(ASSETS_DIR))
            from VGraphLexer import VGraphLexer
            
            # Create input stream 
            input_stream = InputStream(code_text)
            
            # Store original stderr to capture lexical errors
            original_stderr = sys.stderr
            from io import StringIO
            error_output = StringIO()
            sys.stderr = error_output
            
            # Create lexer
            lexer = VGraphLexer(input_stream)
            
            # Get all tokens
            all_tokens = []
            token = lexer.nextToken()
            while token.type != Token.EOF:
                token_name = lexer.symbolicNames[token.type] if token.type > 0 and token.type < len(lexer.symbolicNames) else 'UNKNOWN'
                all_tokens.append((token_name, token.text, token.line, token.column))
                token = lexer.nextToken()
            
            # Restore stderr
            sys.stderr = original_stderr
            
            # Check for lexical errors in captured output
            error_output_str = error_output.getvalue()
            lexical_errors = []
            
            if error_output_str:
                for line in error_output_str.splitlines():
                    if "token recognition error at:" in line:
                        # Parse error line like: "line 4:7 token recognition error at: 'ñ'"
                        try:
                            # Extract line and column
                            parts = line.split(':')
                            error_line = int(parts[0].replace('line', '').strip())
                            error_col = int(parts[1].split()[0].strip())
                            
                            # Extract invalid token
                            error_text = line.split("'")[1] if "'" in line else "?"
                            
                            lexical_errors.append({
                                'message': f"Lexical error: Invalid token '{error_text}'",
                                'line': error_line,
                                'column': error_col,
                                'length': len(error_text),
                                'text': error_text
                            })
                        except (IndexError, ValueError) as e:
                            # Fallback if parsing fails
                            lexical_errors.append({
                                'message': f"Lexical error: {line}",
                                'line': 1,
                                'column': 0,
                                'length': 1
                            })
            
            self.tokens = all_tokens
            
            # Generate token graph if no errors
            if not lexical_errors:
                self._visualize_tokens(all_tokens)
                return True, [], self.token_graph_path
            else:
                # Return errors
                self.errors = lexical_errors
                return False, lexical_errors, None
            
        except Exception as e:
            print(f"Error in lexical analysis: {e}")
            self.errors.append({
                'message': f"Lexical analysis error: {str(e)}",
                'line': 1,
                'column': 0,
                'length': 0
            })
            return False, self.errors, None
    
    def _ensure_lexer_generated(self):
        """
        Ensure the ANTLR lexer files are generated
        
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
        
        # Always regenerate lexer to ensure consistency
        try:
            current_dir = os.getcwd()
            os.chdir(ASSETS_DIR)
            
            # Generate lexer
            cmd = ['java', '-jar', antlr_jar, '-Dlanguage=Python3', 'VGraph.g4']
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Check if command was successful
            if result.returncode != 0:
                error_message = result.stderr.decode('utf-8')
                print(f"Error generating lexer: {error_message}")
                os.chdir(current_dir)
                return False
                
            print("Lexer generated successfully")
            os.chdir(current_dir)
            return True
        except Exception as e:
            print(f"Error generating lexer: {e}")
            if current_dir != os.getcwd():
                os.chdir(current_dir)
            return False
    
    def _visualize_tokens(self, tokens):
        """
        Create a visualization of tokens using pydot
        
        Args:
            tokens: List of tokens to visualize
        """
        try:
            graph = pydot.Dot(graph_type='digraph', rankdir='LR')
            
            # Add nodes for each token
            for i, (token_type, text, line, col) in enumerate(tokens):
                # Escape special characters in text for label
                escaped_text = text.replace('"', '\\"').replace('\\', '\\\\')
                node_label = f"{token_type}\\n\"{escaped_text}\""
                
                node = pydot.Node(f"token_{i}", label=node_label, shape="box", 
                                 style="filled", fillcolor="lightblue")
                graph.add_node(node)
                
                # Connect with previous token
                if i > 0:
                    edge = pydot.Edge(f"token_{i-1}", f"token_{i}")
                    graph.add_edge(edge)
            
            # Save the graph
            graph.write_png(self.token_graph_path)
            
        except Exception as e:
            print(f"Error visualizing tokens: {e}")
            # Create a simple error image if visualization fails
            self._create_error_image(f"Error visualizing tokens: {e}")
    
    def _create_error_image(self, error_message):
        """
        Create a simple error image when token visualization fails
        
        Args:
            error_message: Error message to display
        """
        try:
            graph = pydot.Dot(graph_type='digraph')
            node = pydot.Node("error", label=error_message, shape="box", 
                             style="filled", fillcolor="red")
            graph.add_node(node)
            graph.write_png(self.token_graph_path)
        except Exception as e:
            print(f"Error creating error image: {e}")