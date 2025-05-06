"""
Semantic analyzer module for the Full Stack Compiler
Handles semantic analysis of code, type checking, and semantic error detection
"""
import os
import re
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
        
        print(f"SemanticAnalyzer: Iniciando análisis con parse_tree={parse_tree is not None} y tabla de símbolos con {len(symbol_table)} entradas")
        
        # Verify if parse_tree is None
        if parse_tree is None:
            error_message = "Error de análisis semántico: Árbol sintáctico no disponible"
            print(f"SemanticAnalyzer: {error_message}")
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
            print("SemanticAnalyzer: Importando clases de ANTLR")
            sys.path.append(os.path.abspath(ASSETS_DIR))
            from VGraphVisitor import VGraphVisitor
            from VGraphParser import VGraphParser
            
            # Implementación de la fase 1: Visitor para enriquecer la tabla de símbolos
            class SemanticVisitor(VGraphVisitor):
                def __init__(self, analyzer):
                    VGraphVisitor.__init__(self) 
                    self.analyzer = analyzer
                    self.symbol_table = analyzer.enhanced_symbol_table
                    self.current_scope = ["global"]
                    self.errors = []
                    print(f"SemanticVisitor: Inicializado con tabla de símbolos: {len(self.symbol_table)} entradas")
                
                def visitProgram(self, ctx):
                    print("SemanticVisitor: Visitando programa")
                    # Visit all children
                    return self.visitChildren(ctx)
                
                def visitDeclaration(self, ctx):
                    print("SemanticVisitor: Visitando declaración")
                    type_node = ctx.typeDeclaration().vartype()
                    if type_node:
                        type_name = type_node.getText()
                        
                        # Case 1: Single variable with optional initialization
                        if ctx.ID():
                            var_name = ctx.ID().getText()
                            print(f"SemanticVisitor: Variable declarada: {var_name} de tipo {type_name}")
                            if var_name in self.symbol_table:
                                var_info = self.symbol_table[var_name]
                                if var_info.get('scope') == self.current_scope[-1]:
                                    self.add_error(f"Variable '{var_name}' ya declarada en este ámbito", 
                                                  ctx.ID().getSymbol().line, 
                                                  ctx.ID().getSymbol().column,
                                                  len(var_name))
                                
                            # Update or create symbol table entry
                            self.symbol_table[var_name] = {
                                'type': 'variable',
                                'data_type': type_name,
                                'scope': self.current_scope[-1],
                                'line': ctx.ID().getSymbol().line,
                                'is_initialized': ctx.expr() is not None,
                                'status': 'initialized' if ctx.expr() else 'declared'
                            }
                        
                        # Case 2: ID List
                        elif ctx.idList():
                            for id_node in ctx.idList().ID():
                                var_name = id_node.getText()
                                print(f"SemanticVisitor: Variable en lista declarada: {var_name} de tipo {type_name}")
                                if var_name in self.symbol_table:
                                    var_info = self.symbol_table[var_name]
                                    if var_info.get('scope') == self.current_scope[-1]:
                                        self.add_error(f"Variable '{var_name}' ya declarada en este ámbito", 
                                                      id_node.getSymbol().line, 
                                                      id_node.getSymbol().column,
                                                      len(var_name))
                                
                                # Update or create symbol table entry
                                self.symbol_table[var_name] = {
                                    'type': 'variable',
                                    'data_type': type_name,
                                    'scope': self.current_scope[-1],
                                    'line': id_node.getSymbol().line,
                                    'is_initialized': False,
                                    'status': 'declared'
                                }
                    return self.visitChildren(ctx)
                
                def visitAssignmentStatement(self, ctx):
                    print("SemanticVisitor: Visitando asignación")
                    var_name = ctx.assignmentExpression().ID().getText()
                    
                    # Check if variable exists
                    if var_name not in self.symbol_table:
                        self.add_error(f"Variable '{var_name}' usada sin declarar", 
                                      ctx.assignmentExpression().ID().getSymbol().line, 
                                      ctx.assignmentExpression().ID().getSymbol().column,
                                      len(var_name))
                    else:
                        # Check scope accessibility
                        var_info = self.symbol_table[var_name]
                        var_scope = var_info.get('scope', 'global')
                        if var_scope != 'global' and var_scope not in self.current_scope:
                            self.add_error(f"Variable '{var_name}' no accesible en este ámbito", 
                                          ctx.assignmentExpression().ID().getSymbol().line, 
                                          ctx.assignmentExpression().ID().getSymbol().column,
                                          len(var_name))
                        else:
                            # Update variable status to initialized
                            var_info['is_initialized'] = True
                            var_info['status'] = 'initialized'
                            self.symbol_table[var_name] = var_info
                    
                    return self.visitChildren(ctx)
                
                def visitIdExpr(self, ctx):
                    print(f"SemanticVisitor: Visitando referencia a variable: {ctx.ID().getText()}")
                    var_name = ctx.ID().getText()
                    
                    # Check if variable exists
                    if var_name not in self.symbol_table:
                        self.add_error(f"Variable '{var_name}' usada sin declarar", 
                                      ctx.ID().getSymbol().line, 
                                      ctx.ID().getSymbol().column,
                                      len(var_name))
                    else:
                        # Check initialization status
                        var_info = self.symbol_table[var_name]
                        if not var_info.get('is_initialized', False):
                            self.add_error(f"Variable '{var_name}' usada sin inicializar", 
                                          ctx.ID().getSymbol().line, 
                                          ctx.ID().getSymbol().column,
                                          len(var_name))
                        
                        # Check scope accessibility
                        var_scope = var_info.get('scope', 'global')
                        if var_scope != 'global' and var_scope not in self.current_scope:
                            self.add_error(f"Variable '{var_name}' no accesible en este ámbito", 
                                          ctx.ID().getSymbol().line, 
                                          ctx.ID().getSymbol().column,
                                          len(var_name))
                    
                    return self.visitChildren(ctx)
                
                def visitFrameStatement(self, ctx):
                    print("SemanticVisitor: Entrando en ámbito de frame")
                    # Enter frame scope
                    self.current_scope.append("frame")
                    
                    # Visit children
                    result = self.visitChildren(ctx)
                    
                    # Exit frame scope
                    self.current_scope.pop()
                    print("SemanticVisitor: Saliendo de ámbito de frame")
                    
                    return result
                
                def visitFunctionDeclStatement(self, ctx):
                    print("SemanticVisitor: Visitando declaración de función")
                    func_name = ctx.ID().getText()
                    
                    # Check if function already exists
                    if func_name in self.symbol_table:
                        func_info = self.symbol_table[func_name]
                        if func_info.get('type') == 'function':
                            self.add_error(f"Función '{func_name}' ya definida", 
                                          ctx.ID().getSymbol().line, 
                                          ctx.ID().getSymbol().column,
                                          len(func_name))
                            return self.visitChildren(ctx)
                    
                    # Add function to symbol table
                    self.symbol_table[func_name] = {
                        'type': 'function',
                        'scope': 'global',  # Functions are always global in VGraph
                        'line': ctx.ID().getSymbol().line,
                        'parameters': [],
                        'return_type': 'void',  # Default in VGraph
                        'status': 'defined'
                    }
                    
                    # Enter function scope
                    self.current_scope.append(func_name)
                    print(f"SemanticVisitor: Entrando en ámbito de función {func_name}")
                    
                    # Process parameters
                    param_list = ctx.paramList()
                    if param_list:
                        for param_node in param_list.ID():
                            param_name = param_node.getText()
                            print(f"SemanticVisitor: Procesando parámetro {param_name}")
                            # Add parameter to function's parameter list
                            self.symbol_table[func_name]['parameters'].append(param_name)
                            
                            # Add parameter to symbol table
                            self.symbol_table[param_name] = {
                                'type': 'parameter',
                                'data_type': 'unknown',  # Parameters don't have explicit types in VGraph
                                'scope': func_name,
                                'line': param_node.getSymbol().line,
                                'is_initialized': True,  # Parameters are always initialized
                                'status': 'initialized'
                            }
                    
                    # Visit children (function body)
                    result = self.visitChildren(ctx)
                    
                    # Exit function scope
                    self.current_scope.pop()
                    print(f"SemanticVisitor: Saliendo de ámbito de función {func_name}")
                    
                    return result
                
                def add_error(self, message, line, column, length):
                    error = {
                        'message': message,
                        'line': line,
                        'column': column,
                        'length': length
                    }
                    print(f"SemanticVisitor: Error detectado: {message} en línea {line}")
                    self.errors.append(error)
                    self.analyzer.errors.append(error)
            
            # Create visitor and visit parse tree
            print("SemanticAnalyzer: Creando visitor")
            visitor = SemanticVisitor(self)
            
            # Visit the parse tree
            print("SemanticAnalyzer: Iniciando visita del árbol")
            try:
                result = visitor.visit(parse_tree)
                print(f"SemanticAnalyzer: Visita completada, resultado: {result}")
            except Exception as e:
                print(f"SemanticAnalyzer: Error durante la visita: {e}")
                import traceback
                traceback.print_exc()
                raise
            
            # Check if we have any errors
            if self.errors:
                print(f"SemanticAnalyzer: Se encontraron {len(self.errors)} errores")
                # Create visualizations to show the errors
                self._create_semantic_analysis_graph()
                self._create_enhanced_symbol_table_visualization(self.enhanced_symbol_table)
                return False, self.errors, self.semantic_analysis_path, self.enhanced_symbol_table_path
            
            # If no errors, update the enhanced symbol table with visitor results
            self.enhanced_symbol_table = visitor.symbol_table
            
            # Create visualizations for successful analysis
            print("SemanticAnalyzer: Análisis exitoso, creando visualizaciones")
            self._create_semantic_analysis_graph()
            self._create_enhanced_symbol_table_visualization(self.enhanced_symbol_table)
            
            return True, [], self.semantic_analysis_path, self.enhanced_symbol_table_path
            
        except Exception as e:
            print(f"Error durante el análisis semántico: {e}")
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
    
    def _fallback_analysis(self, code_text, symbol_table):
        """
        Perform a basic semantic analysis directly on code text when parse tree is not available
        This is a simplified analysis for demonstration purposes
        """
        print("SemanticAnalyzer._fallback_analysis - Using fallback analysis")
        
        # Asegurarse de que la tabla de símbolos esté inicializada
        if not symbol_table:
            symbol_table = {}
            
        # Ejemplo: Como fallback simple, detectar si hay variables utilizadas sin declarar
        # Este es un análisis muy simplificado y sólo se usa como demostracion mientras
        # arreglamos el acceso al parse_tree
        
        # Buscar todas las declaraciones de variables
        declarations = {}
        # Patrón para declaraciones: (int) x; o (int) x, y, z;
        decl_pattern = r'\((\w+)\)\s+(\w+(?:\s*,\s*\w+)*)\s*;'
        
        for match in re.finditer(decl_pattern, code_text):
            line_number = code_text[:match.start()].count('\n') + 1
            type_name = match.group(1)
            vars_list = match.group(2).split(',')
            
            for var_name in vars_list:
                var_name = var_name.strip()
                declarations[var_name] = {
                    'type': 'variable',
                    'data_type': type_name,
                    'line': line_number,
                    'scope': 'global',
                    'is_initialized': False,
                    'status': 'declared'
                }
                
                # Actualizar la tabla de símbolos mejorada
                self.enhanced_symbol_table[var_name] = declarations[var_name]
        
        # Buscar todas las asignaciones
        # Ejemplo: x = 10;
        assign_pattern = r'(\w+)\s*=\s*([^;]+);'
        
        for match in re.finditer(assign_pattern, code_text):
            line_number = code_text[:match.start()].count('\n') + 1
            var_name = match.group(1)
            
            # Comprobar si la variable fue declarada
            if var_name not in declarations and var_name not in symbol_table:
                self.errors.append({
                    'message': f"Variable '{var_name}' utilizada sin declarar",
                    'line': line_number,
                    'column': match.start() - code_text.rfind('\n', 0, match.start()),
                    'length': len(var_name)
                })
            elif var_name in self.enhanced_symbol_table:
                # Marcar como inicializada
                self.enhanced_symbol_table[var_name]['is_initialized'] = True
                self.enhanced_symbol_table[var_name]['status'] = 'initialized'
        
        # Buscar usos de variables en expresiones
        # Este análisis es muy simplificado
        var_usage_pattern = r'[^a-zA-Z0-9_](\w+)[^a-zA-Z0-9_]'
        
        lines = code_text.split('\n')
        for i, line in enumerate(lines):
            line_number = i + 1
            
            for match in re.finditer(var_usage_pattern, ' ' + line + ' '):
                var_name = match.group(1)
                
                # Ignorar palabras clave y nombres de función
                keywords = ['if', 'else', 'loop', 'frame', 'draw', 'setcolor', 'wait', 
                           'function', 'return', 'clear', 'int', 'color', 'bool']
                
                if var_name not in keywords and var_name.isalpha():
                    if var_name not in declarations and var_name not in symbol_table:
                        # Posible variable no declarada, pero tenemos que verificar si es un literal
                        if var_name not in ['true', 'false'] and not var_name.isdigit():
                            # Verificar si es un color predefinido
                            colors = ['rojo', 'azul', 'verde', 'amarillo', 'cyan', 'magenta', 'blanco', 'negro', 'marrón']
                            if var_name not in colors:
                                self.errors.append({
                                    'message': f"Variable '{var_name}' posiblemente utilizada sin declarar",
                                    'line': line_number,
                                    'column': match.start() - 1,  # Ajustamos por el espacio añadido
                                    'length': len(var_name)
                                })
    
    def _analyze_symbol_types(self, parse_tree, symbol_table):
        """
        Fase 1: Mejora de la Tabla de Símbolos
        
        Aunque no podemos usar directamente el Visitor de ANTLR debido a problemas
        con el parse_tree, podemos enriquecer la tabla de símbolos con la información
        que ya tenemos.
        """
        print("SemanticAnalyzer._analyze_symbol_types - Analyzing symbol types")
        
        # Si no tenemos tabla de símbolos, no podemos hacer mucho
        if not symbol_table:
            print("SemanticAnalyzer._analyze_symbol_types - No symbol table available")
            self.errors.append({
                'message': "No hay tabla de símbolos disponible para realizar el análisis semántico",
                'line': 1,
                'column': 0,
                'length': 10
            })
            return
        
        print(f"Symbol table entries: {len(symbol_table)}")
        
        # Como ejemplo, creamos una simulación de enriquecimiento de la tabla
        for symbol, info in symbol_table.items():
            print(f"Processing symbol: {symbol}")
            # Determinar tipo de dato básico si no está especificado
            if 'data_type' not in info:
                # Intentar deducir tipo por nombre de la variable (muy simplificado)
                if symbol.startswith('i') or symbol.startswith('n') or symbol in ['x', 'y', 'z', 'w', 'h']:
                    info['data_type'] = 'int'
                elif symbol.startswith('c') or symbol.startswith('color'):
                    info['data_type'] = 'color'
                elif symbol.startswith('b') or symbol in ['flag', 'is', 'has']:
                    info['data_type'] = 'bool'
                else:
                    info['data_type'] = 'unknown'
            
            # Añadir estado de inicialización si no está especificado
            if 'is_initialized' not in info:
                info['is_initialized'] = False
            
            # Añadir estado si no está especificado
            if 'status' not in info:
                info['status'] = 'declared'
                
            # Verificar si el tipo es válido
            if info.get('data_type') not in ['int', 'color', 'bool', 'unknown', 'function', 'parameter']:
                self.errors.append({
                    'message': f"Tipo de dato no válido '{info.get('data_type')}' para la variable '{symbol}'",
                    'line': info.get('line', 1),
                    'column': 0,
                    'length': len(symbol)
                })
            
            # Actualizar la tabla de símbolos mejorada
            self.enhanced_symbol_table[symbol] = info
            
        # Como ejemplo, añadimos una comprobación de variables
        print("Checking for variables used without initialization")
        for symbol, info in self.enhanced_symbol_table.items():
            if info.get('type') == 'variable' and not info.get('is_initialized'):
                # Simular un problema con una variable específica para demostración
                if symbol == 'x' or symbol == 'y':
                    self.errors.append({
                        'message': f"Variable '{symbol}' utilizada pero no ha sido inicializada",
                        'line': info.get('line', 5),
                        'column': 1,
                        'length': len(symbol)
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