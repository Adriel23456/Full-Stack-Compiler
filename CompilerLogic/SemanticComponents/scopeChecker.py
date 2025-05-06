class ScopeChecker:
    """
    Maneja la verificación de ámbitos para variables y funciones
    """
    def __init__(self, symbol_table, error_reporter):
        self.symbol_table = symbol_table
        self.error_reporter = error_reporter
        self.in_function = False
        self.current_function = None
    
    def enter_function(self, function_name):
        """
        Indica que se está entrando en una función
        """
        self.in_function = True
        self.current_function = function_name
    
    def exit_function(self):
        """
        Indica que se está saliendo de una función
        """
        self.in_function = False
        self.current_function = None
    
    def check_variable_declaration(self, node, parser):
        """
        Verifica que una declaración de variable sea válida
        """
        from CompilerLogic.SemanticComponents.astUtil import get_node_line, get_node_column, get_text, get_rule_name
        
        # declaration: typeDeclaration ID (ASSIGN expr)? SEMICOLON | typeDeclaration idList SEMICOLON
        type_node = node.getChild(0)
        var_type = type_node.getChild(1).getText()
        
        # Caso 1: declaración con ID único
        if get_rule_name(node.getChild(1), parser) is None:  # Es un token terminal (ID)
            var_name = get_text(node.getChild(1))
            
            # Verificar si ya existe en el ámbito actual
            if self.symbol_table.is_declared_in_current_scope(var_name):
                self.error_reporter.report_error(
                    get_node_line(node.getChild(1)),
                    get_node_column(node.getChild(1)),
                    f"Variable {var_name} ya declarada en este ámbito",
                    len(var_name)
                )
                return
            
            # Verificar que el identificador cumpla con las reglas
            if not self._check_identifier_rules(var_name, node.getChild(1)):
                return
            
            # Agregar a la tabla de símbolos
            self.symbol_table.insert(var_name, {
                "type": var_type,
                "line": get_node_line(node.getChild(1)),
                "initialized": False,
                "used": False
            })
            
            # Si hay una asignación en la declaración, marcar como inicializada
            if node.getChildCount() > 3:  # typeDeclaration ID ASSIGN expr SEMICOLON
                self.symbol_table.mark_initialized(var_name)
        
        # Caso 2: declaración con lista de IDs
        elif get_rule_name(node.getChild(1), parser) == "idList":
            id_list = node.getChild(1)
            
            # Procesar cada ID en la lista
            for i in range(0, id_list.getChildCount(), 2):  # Saltar comas
                var_name = get_text(id_list.getChild(i))
                
                # Verificar si ya existe en el ámbito actual
                if self.symbol_table.is_declared_in_current_scope(var_name):
                    self.error_reporter.report_error(
                        get_node_line(id_list.getChild(i)),
                        get_node_column(id_list.getChild(i)),
                        f"Variable {var_name} ya declarada en este ámbito",
                        len(var_name)
                    )
                    continue
                
                # Verificar que el identificador cumpla con las reglas
                if not self._check_identifier_rules(var_name, id_list.getChild(i)):
                    continue
                
                # Agregar a la tabla de símbolos
                self.symbol_table.insert(var_name, {
                    "type": var_type,
                    "line": get_node_line(id_list.getChild(i)),
                    "initialized": False,
                    "used": False
                })
    
    def check_function_declaration(self, node, parser):
        """
        Verifica que una declaración de función sea válida
        """
        from CompilerLogic.SemanticComponents.astUtil import get_node_line, get_node_column, get_text
        
        # functionDeclStatement: FUNCTION ID LPAREN paramList? RPAREN block
        func_name = get_text(node.getChild(1))
        
        # Verificar si ya existe en el ámbito global SOLO en la tabla actual
        if self.symbol_table.is_function_declared(func_name):
            self.error_reporter.report_error(
                get_node_line(node.getChild(1)),
                get_node_column(node.getChild(1)),
                f"Función {func_name} ya declarada",
                len(func_name)
            )
            return
        
        # Verificar que el identificador cumpla con las reglas
        if not self._check_identifier_rules(func_name, node.getChild(1)):
            return
        
        # Verificar que la función se declare en el ámbito global
        if self.symbol_table.current_scope_name() != "global":
            self.error_reporter.report_error(
                get_node_line(node.getChild(1)),
                get_node_column(node.getChild(1)),
                "Las funciones solo pueden declararse en el ámbito global",
                len(func_name)
            )
            return
        
        # Agregar a la tabla de símbolos
        self.symbol_table.insert(func_name, {
            "type": "function",
            "line": get_node_line(node.getChild(1)),
            "initialized": True,  # Las funciones se consideran inicializadas
            "used": False
        })
        
        # Registrar en la tabla de funciones
        self.symbol_table.functions[func_name] = {
            "params": [],
            "line": get_node_line(node.getChild(1)),
            "return_type": "void"  # Por defecto, void
        }
        
        # Procesar parámetros si existen
        if node.getChildCount() > 5:  # FUNCTION ID LPAREN paramList RPAREN block
            param_list = node.getChild(3)
            
            # Recorrer parámetros
            for i in range(0, param_list.getChildCount(), 2):  # Saltar comas
                param_name = get_text(param_list.getChild(i))
                
                # Agregar a la lista de parámetros de la función
                self.symbol_table.add_function_param(func_name, param_name)
    
    def check_return_statement(self, node, parser):
        """
        Verifica que una sentencia return sea válida
        """
        from CompilerLogic.SemanticComponents.astUtil import get_node_line, get_node_column
        
        # returnStatement: RETURN expr? SEMICOLON
        
        # Verificar que estemos dentro de una función
        if not self.in_function:
            self.error_reporter.report_error(
                get_node_line(node),
                get_node_column(node),
                "La sentencia return solo puede aparecer dentro de funciones",
                6  # Longitud de "return"
            )
    
    def _check_identifier_rules(self, identifier, node):
        """
        Verifica que un identificador cumpla con las reglas de VGraph
        """
        from CompilerLogic.SemanticComponents.astUtil import get_node_line, get_node_column
        
        # Los identificadores deben empezar con minúscula
        if not identifier[0].islower():
            self.error_reporter.report_error(
                get_node_line(node),
                get_node_column(node),
                "Los identificadores deben comenzar con minúscula",
                len(identifier)
            )
            return False
        
        # Los identificadores deben ser alfanuméricos
        if not identifier.isalnum():
            self.error_reporter.report_error(
                get_node_line(node),
                get_node_column(node),
                "Los identificadores deben ser alfanuméricos",
                len(identifier)
            )
            return False
        
        # Los identificadores deben tener 15 caracteres o menos
        if len(identifier) > 15:
            self.error_reporter.report_error(
                get_node_line(node),
                get_node_column(node),
                "Los identificadores deben tener 15 caracteres o menos",
                len(identifier)
            )
            return False
        
        return True