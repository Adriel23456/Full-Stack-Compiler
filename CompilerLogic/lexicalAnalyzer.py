"""
Lexical analyzer module for the Full Stack Compiler
Handles lexical analysis of code and generates token graphs
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

from config import BASE_DIR, ASSETS_DIR, CompilerData

class LexicalAnalyzer:
    """
    Handles lexical analysis of code - Cross-platform compatible
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
        
        # Platform detection
        self.platform = platform.system().lower()
        self.is_windows = self.platform == 'windows'
        self.is_linux = self.platform == 'linux'
        self.is_mac = self.platform == 'darwin'
        
        # Set platform-specific paths and commands
        self._setup_platform_specifics()
    
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
                # Note: We can't reimport in the same session, but it will work next time
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
        CompilerData.reset_all()  # Resetear todos los datos cuando inicia un nuevo análisis
        
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
                return False, self.errors, None
        
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
                CompilerData.tokens = all_tokens
                CompilerData.token_graph_path = self.token_graph_path
                return True, [], self.token_graph_path
            else:
                # Return errors
                self.errors = lexical_errors
                CompilerData.lexical_errors = lexical_errors
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
    
    def _ensure_lexer_generated(self):
        """
        Ensure the ANTLR lexer files are generated - Cross-platform compatible
        
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
        
        # Always regenerate lexer to ensure consistency
        try:
            current_dir = os.getcwd()
            os.chdir(ASSETS_DIR)
            
            # Generate lexer - platform independent
            cmd = [self.java_cmd, '-jar', self.antlr_jar_path, '-Dlanguage=Python3', 'VGraph.g4']
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Check if command was successful
            if result.returncode != 0:
                error_message = result.stderr.decode('utf-8')
                print(f"Error generating lexer: {error_message}")
                os.chdir(current_dir)
                return False
                
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
        if not PYDOT_AVAILABLE:
            print("Warning: pydot not available, skipping token visualization")
            self._create_text_visualization(tokens)
            return
        
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
    
    def _create_text_visualization(self, tokens):
        """
        Create a text-based visualization when pydot is not available
        
        Args:
            tokens: List of tokens to visualize
        """
        try:
            # Create a simple text representation
            visualization_text = "TOKEN VISUALIZATION (Text Mode)\n"
            visualization_text += "=" * 50 + "\n\n"
            
            for i, (token_type, text, line, col) in enumerate(tokens):
                visualization_text += f"Token {i+1}: {token_type}\n"
                visualization_text += f"  Text: '{text}'\n"
                visualization_text += f"  Position: Line {line}, Column {col}\n"
                visualization_text += "-" * 30 + "\n"
            
            # Save as text file instead of image
            text_path = self.token_graph_path.replace('.png', '.txt')
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(visualization_text)
            
            print(f"Token visualization saved as text file: {text_path}")
            
        except Exception as e:
            print(f"Error creating text visualization: {e}")
    
    def _create_error_image(self, error_message):
        """
        Create a simple error image when token visualization fails
        
        Args:
            error_message: Error message to display
        """
        if not PYDOT_AVAILABLE:
            # Create text file instead
            try:
                error_text = f"ERROR IN TOKEN VISUALIZATION\n{'=' * 40}\n\n{error_message}"
                text_path = self.token_graph_path.replace('.png', '_error.txt')
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
            graph.write_png(self.token_graph_path)
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