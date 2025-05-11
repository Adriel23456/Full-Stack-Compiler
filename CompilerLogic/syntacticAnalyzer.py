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
        
        Args:
            code_text: Source code to analyze
            
        Returns:
            tuple: (success, errors, parse_tree_path, symbol_table_path)
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
            
            # Create a proper symbol table collector
            class SymbolTableCollector(VGraphListener):
                def __init__(self):
                    # Tabla de símbolos con clave compuesta: (nombre, scope) → info
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
                    line = ctx.ID().symbol.line
                    # Usamos clave compuesta (fname, 'global')
                    self.symbol_table[(fname, 'global')] = {
                        'type': 'function',
                        'scope': 'global',
                        'line': line,
                        'name': fname
                    }
                    # entramos en el nuevo scope de la función
                    self.scope_stack.append(fname)
                    # parámetros quedan en el scope de la función
                    param_list = ctx.paramList()
                    if param_list:
                        for p in param_list.ID():
                            pname = p.getText()
                            pline = p.symbol.line
                            # Usamos clave compuesta (pname, fname)
                            self.symbol_table[(pname, fname)] = {
                                'type': 'parameter',
                                'scope': fname,
                                'line': pline,
                                'name': pname
                            }

                def exitFunctionDeclStatement(self, ctx):
                    # salimos del scope de la función
                    self.scope_stack.pop()

                def enterFrameStatement(self, ctx):
                    # creamos un scope genérico "frame"
                    self.scope_stack.append("frame")

                def exitFrameStatement(self, ctx):
                    self.scope_stack.pop()

                # ----- Declaraciones y asignaciones -----
                def enterDeclaration(self, ctx):
                    # puede ser single ID o lista
                    vartype = ctx.typeDeclaration().vartype().getText()
                    current_scope = self.current_scope()
                    
                    # caso ID único
                    if ctx.ID():
                        name = ctx.ID().getText()
                        line = ctx.ID().symbol.line
                        # Usamos clave compuesta (name, current_scope)
                        self.symbol_table[(name, current_scope)] = {
                            'type': vartype,
                            'scope': current_scope,
                            'line': line,
                            'name': name
                        }
                    # caso lista
                    if ctx.idList():
                        for id_node in ctx.idList().ID():
                            name = id_node.getText()
                            line = id_node.symbol.line
                            # Usamos clave compuesta (name, current_scope)
                            self.symbol_table[(name, current_scope)] = {
                                'type': vartype,
                                'scope': current_scope,
                                'line': line,
                                'name': name
                            }

                def enterAssignmentStatement(self, ctx):
                    # el ID está dentro de assignmentExpression()
                    assignCtx = ctx.assignmentExpression()
                    name = assignCtx.ID().getText()
                    current_scope = self.current_scope()
                    
                    # Buscar si la variable ya existe en algún scope accesible
                    # Primero en el scope actual
                    if (name, current_scope) in self.symbol_table:
                        return  # Ya existe, no agregamos nada
                    
                    # Luego en scope de función si estamos en frame
                    if current_scope == 'frame' and len(self.scope_stack) > 1:
                        function_scope = self.scope_stack[-2]  # Scope de la función
                        if (name, function_scope) in self.symbol_table:
                            return  # Existe en el scope de la función
                    
                    # Finalmente en scope global
                    if (name, 'global') in self.symbol_table:
                        return  # Existe globalmente
                    
                    # Solo si no existe en ningún scope accesible, agregamos como unknown
                    self.symbol_table[(name, current_scope)] = {
                        'type': 'unknown',
                        'scope': current_scope,
                        'line': ctx.start.line,
                        'name': name
                    }

                # Métodos vacíos del listener
                def enterEveryRule(self, ctx): pass
                def exitEveryRule(self, ctx): pass
                def visitTerminal(self, node): pass
                def visitErrorNode(self, node): pass

                def get_flattened_symbol_table(self):
                    """
                    Convierte la tabla de símbolos de claves compuestas a claves simples
                    manteniendo solo una entrada por variable
                    """
                    flattened = {}
                    # Diccionario para rastrear variables por nombre
                    seen_names = {}
                    
                    # Ordenar por scope para dar prioridad a declaraciones globales
                    scopes_priority = {'global': 0, 'function': 1, 'frame': 2}
                    
                    sorted_entries = sorted(self.symbol_table.items(), 
                                        key=lambda x: (scopes_priority.get(x[1].get('scope', 'global'), 3), x[0]))
                    
                    for (name, scope), info in sorted_entries:
                        if name not in seen_names:
                            # Primera vez que vemos este nombre
                            flattened[name] = info
                            seen_names[name] = scope
                        else:
                            # Ya hemos visto este nombre
                            existing_scope = seen_names[name]
                            existing_type = flattened[name].get('type', 'unknown')
                            
                            # Si ya tenemos el tipo y el nuevo es 'unknown', no lo sobrescribimos
                            if existing_type != 'unknown' and info.get('type') == 'unknown':
                                continue
                            
                            # Si el nuevo es una función o parámetro, lo agregamos con un nombre único
                            if info.get('type') in ['function', 'parameter']:
                                unique_key = f"{name}_{scope}"
                                flattened[unique_key] = info
                            # Si el existente es 'unknown' y el nuevo tiene tipo, lo reemplazamos
                            elif existing_type == 'unknown' and info.get('type') != 'unknown':
                                flattened[name] = info
                                seen_names[name] = scope
                    
                    return flattened
                
                def clean_unknown_variables(self):
                    """
                    Elimina variables marcadas como 'unknown' que en realidad están declaradas
                    en un scope accesible
                    """
                    to_remove = []
                    
                    for (name, scope), info in self.symbol_table.items():
                        if info.get('type') == 'unknown':
                            # Verificar si existe en un scope accesible con tipo conocido
                            # Primero verificar en global
                            if (name, 'global') in self.symbol_table:
                                global_info = self.symbol_table[(name, 'global')]
                                if global_info.get('type') != 'unknown':
                                    to_remove.append((name, scope))
                                    continue
                            
                            # Si estamos en frame, verificar en la función
                            if scope == 'frame':
                                # Buscar en todas las funciones
                                for func_scope in [s for s in self.scope_stack if s not in ['global', 'frame']]:
                                    if (name, func_scope) in self.symbol_table:
                                        func_info = self.symbol_table[(name, func_scope)]
                                        if func_info.get('type') != 'unknown':
                                            to_remove.append((name, scope))
                                            break
                    
                    # Remover las variables unknown duplicadas
                    for key in to_remove:
                        del self.symbol_table[key]

                def get_symbol_table_list(self):
                    """
                    Retorna la tabla de símbolos como una lista de entradas
                    """
                    symbol_list = []
                    
                    for (name, scope), info in self.symbol_table.items():
                        symbol_list.append({
                            'name': name,
                            'type': info.get('type', 'unknown'),
                            'scope': scope,
                            'line': info.get('line', 0)
                        })
                    
                    return symbol_list
            
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

                # Limpiar variables unknown que están declaradas en otros scopes
                symbol_collector.clean_unknown_variables()

                # Obtener la tabla de símbolos aplanada para compatibilidad
                self.symbol_table = symbol_collector.get_flattened_symbol_table()

                # Para debugging, también podemos guardar la versión con claves compuestas
                symbol_collector.flattened_symbol_table = self.symbol_table

                # Generate symbol table visualization
                self._visualize_symbol_table()

                # Guardar la versión sin renombramiento para el análisis semántico
                CompilerData.symbol_table = self.symbol_table
                CompilerData.parse_tree_path = self.parse_tree_path
                CompilerData.symbol_table_path = self.symbol_table_path
                CompilerData.parser = parser
                CompilerData.ast = parse_tree

                # Para verificar que funciona correctamente, puedes agregar esto después de generar ambas tablas:
                print("\n=== DEBUG: Comparison of tables ===")
                print("Table with renaming (for visualization):")
                for name, info in self.symbol_table.items():
                    print(f"  {name}: {info}")
                
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

            # Ordenar por scope y luego por nombre para mejor visualización
            sorted_symbols = sorted(self.symbol_table.items(), 
                                key=lambda x: (x[1].get('scope', 'global'), x[0]))

            # Una fila por cada símbolo
            for symbol, info in sorted_symbols:
                # Extraer el nombre real del símbolo (puede incluir sufijo _in_scope)
                name = info.get('name', symbol)
                sym = name.replace("<", "&lt;").replace(">", "&gt;")
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