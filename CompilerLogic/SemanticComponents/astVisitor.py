# CompilerLogic/SemanticComponents/astVisitor.py
from CompilerLogic.SemanticComponents.astUtil import get_rule_name, get_text


class ASTVisitor:
    """
    Visitador para recorrer el AST y realizar análisis semántico
    """
    def __init__(self, symbol_table, type_checker, scope_checker, error_reporter):
        self.symbol_table = symbol_table
        self.type_checker = type_checker
        self.scope_checker = scope_checker
        self.error_reporter = error_reporter
    
    def visit(self, node, parser):
        """
        Visita un nodo del AST y realiza análisis semántico
        """
        from CompilerLogic.SemanticComponents.astUtil import get_rule_name, get_text
        
        # Si es nodo terminal, no hay nada que analizar
        if node.getChildCount() == 0:
            return
        
        rule_name = get_rule_name(node, parser)
        
        # Según el tipo de nodo, realizar el análisis correspondiente
        if rule_name == "program":
            self.visit_program(node, parser)
        elif rule_name == "declaration":
            self.scope_checker.check_variable_declaration(node, parser)
        elif rule_name == "assignmentStatement":
            self.visit_assignment_statement(node, parser)
        elif rule_name == "functionDeclStatement":
            self.visit_function_declaration(node, parser)
        # SOLO llamar check_function_call para nodos válidos
        elif rule_name == "functionCall":
            # Verificar que el nodo tenga hijos antes de procesarlo
            if node.getChildCount() >= 3:  # ID LPAREN RPAREN mínimo
                self.type_checker.check_function_call(node, parser)
        elif rule_name == "functionCallStatement":
            # Este ya se maneja en visit_function_call_statement
            self.visit_function_call_statement(node, parser)
        elif rule_name == "returnStatement":
            self.scope_checker.check_return_statement(node, parser)
        elif rule_name == "drawStatement":
            self.type_checker.check_draw_statement(node, parser)
        elif rule_name == "setColorStatement":
            self.type_checker.check_setcolor_statement(node, parser)
        elif rule_name == "ifStatement":
            self.visit_if_statement(node, parser)
        elif rule_name == "loopStatement":
            self.visit_loop_statement(node, parser)
        elif rule_name == "frameStatement":
            self.visit_frame_statement(node, parser)
        elif rule_name == "expr" or rule_name.endswith("Expr"):
            # Verificar expresiones directamente
            self.type_checker.check_expression(node, parser)
        else:
            # Para otros tipos de nodos, visitar recursivamente los hijos
            for i in range(node.getChildCount()):
                self.visit(node.getChild(i), parser)
    
    def visit_program(self, node, parser):
        """
        Visita el nodo programa (raíz del AST)
        """
        # Visitar todos los hijos (statements)
        for i in range(node.getChildCount()):
            self.visit(node.getChild(i), parser)
        
        # Después de analizar todo el programa, verificar si hay variables no usadas
        unused_symbols = self.symbol_table.get_unused_symbols()
        for symbol in unused_symbols:
            self.error_reporter.report_warning(
                symbol["line"],
                0,  # No tenemos la columna exacta
                f"Variable '{symbol['name']}' declarada pero no utilizada",
                len(symbol["name"])
            )
        
        # Verificar si hay variables utilizadas pero no inicializadas
        uninitialized = self.symbol_table.get_uninitialized_used_symbols()
        for symbol in uninitialized:
            self.error_reporter.report_error(
                symbol["line"],
                0,  # No tenemos la columna exacta
                f"Variable '{symbol['name']}' utilizada sin inicializar",
                len(symbol["name"])
            )
    
    def visit_assignment_statement(self, node, parser):
        """
        Visita un nodo de asignación
        """
        from CompilerLogic.SemanticComponents.astUtil import get_rule_name
        
        # assignmentStatement: assignmentExpression SEMICOLON
        assignment_expr = node.getChild(0)
        
        # Verificar si es una asignación de expresión o booleana
        if assignment_expr.getChildCount() >= 3:  # ID ASSIGN expr o ID ASSIGN boolExpr
            # Procesar la asignación
            self.type_checker.check_assignment(assignment_expr, parser)
            
            # También visitar la expresión para verificar subexpresiones
            right_side = assignment_expr.getChild(2)
            self.visit(right_side, parser)
    
    def visit_function_declaration(self, node, parser):
        """
        Visita un nodo de declaración de función
        """
        from CompilerLogic.SemanticComponents.astUtil import get_text
        
        # functionDeclStatement: FUNCTION ID LPAREN paramList? RPAREN block
        func_name = get_text(node.getChild(1))
        
        print(f"=== DEBUG: Entering function '{func_name}' ===")
        
        # Verificar la declaración de la función
        self.scope_checker.check_function_declaration(node, parser)
        
        # Entrar en el ámbito de la función
        self.symbol_table.enter_scope(func_name)
        self.scope_checker.enter_function(func_name)
        
        # Si hay parámetros, agregarlos al ámbito de la función con renombramiento
        if node.getChildCount() > 5:  # FUNCTION ID LPAREN paramList RPAREN block
            param_list = node.getChild(3)
            
            # Recorrer parámetros
            for i in range(0, param_list.getChildCount(), 2):  # Saltar comas
                param_name = get_text(param_list.getChild(i))
                print(f"=== DEBUG: Processing parameter '{param_name}' ===")
                
                # IMPORTANTE: No agregar el parámetro aquí, ya está en la tabla inicial
                # pero sí asegurarse de que se marque como inicializado
                self.symbol_table.mark_initialized(param_name)
        
        # Visitar el bloque de la función
        block = node.getChild(node.getChildCount() - 1)
        self.visit(block, parser)
        
        # Salir del ámbito de la función
        self.symbol_table.exit_scope()
        self.scope_checker.exit_function()
        
        print(f"=== DEBUG: Exiting function '{func_name}' ===")
    
    def visit_function_call_statement(self, node, parser):
        """
        Visita un nodo de llamada a función
        """
        print(f"=== DEBUG ASTVisitor: visit_function_call_statement called ===")
        print(f"=== DEBUG: Node children count: {node.getChildCount()} ===")
        
        # functionCallStatement: ID LPAREN argumentList? RPAREN SEMICOLON
        if node.getChildCount() >= 4:  # Debe tener al menos ID, LPAREN, RPAREN, SEMICOLON
            # El nodo completo de la llamada es desde ID hasta RPAREN
            # Crear un nodo artificial que solo contenga la llamada
            print(f"=== DEBUG: Calling type_checker.check_function_call with full node ===")
            self.type_checker.check_function_call(node, parser)
            
            # También verificar los argumentos recursivamente
            if node.getChildCount() > 4:  # ID LPAREN argumentList RPAREN SEMICOLON
                arg_list = node.getChild(2)
                if get_rule_name(arg_list, parser) == "argumentList":
                    # Visitar cada argumento
                    for i in range(0, arg_list.getChildCount(), 2):  # Saltar comas
                        arg = arg_list.getChild(i)
                        self.visit(arg, parser)
    
    def visit_if_statement(self, node, parser):
        """
        Visita un nodo if
        """
        # ifStatement: IF LPAREN boolExpr RPAREN block (ELSE (ifStatement | block))?
        
        # Verificar la condición
        self.type_checker.check_if_statement(node, parser)
        
        # Visitar la condición
        condition = node.getChild(2)
        self.visit(condition, parser)
        
        # Visitar el bloque then
        then_block = node.getChild(4)
        self.visit(then_block, parser)
        
        # Visitar el bloque else si existe
        if node.getChildCount() > 5:  # IF LPAREN boolExpr RPAREN block ELSE ...
            else_part = node.getChild(6)  # ifStatement o block
            self.visit(else_part, parser)
    
    def visit_loop_statement(self, node, parser):
        """
        Visita un nodo loop
        """
        from CompilerLogic.SemanticComponents.astUtil import get_rule_name, get_text
        
        # loopStatement: LOOP LPAREN assignmentExpression SEMICOLON boolExpr SEMICOLON assignmentExpression RPAREN block
        
        # PRIMERO: Procesar la inicialización y asegurarnos de que se marca como inicializada
        init = node.getChild(2)
        if get_rule_name(init, parser) == "assignmentExpression":
            # Obtener el nombre de la variable
            var_name = get_text(init.getChild(0))
            
            # Procesar la asignación
            self.type_checker.check_assignment(init, parser)
            
            # CRÍTICO: Asegurarnos de que se marca como inicializada INMEDIATAMENTE
            # Esto debe hacerse después de check_assignment pero antes de visitar la condición
            var_info = self.symbol_table.lookup(var_name)
            if var_info:
                current_scope = var_info.get('current_scope', self.symbol_table.current_scope_name())
                self.symbol_table.mark_initialized(var_name, current_scope=current_scope)
                print(f"=== DEBUG: Marked {var_name} as initialized in loop init ===")
            
            # También visitar la expresión de inicialización para cualquier subexpresión
            expr = init.getChild(2)
            self.visit(expr, parser)
        
        # SEGUNDO: Verificar la condición (ahora que la variable está inicializada)
        condition = node.getChild(4)
        
        # Primero, verificar con type_checker
        print(f"=== DEBUG: About to check loop condition ===")
        self.type_checker.check_loop_statement(node, parser)
        
        # Luego visitar la condición
        self.visit(condition, parser)
        
        # TERCERO: Visitar el bloque del loop
        block = node.getChild(8)
        self.visit(block, parser)
        
        # CUARTO: Visitar la actualización (increment/decrement)
        update = node.getChild(6)
        if get_rule_name(update, parser) == "assignmentExpression":
            self.type_checker.check_assignment(update, parser)
            # Visitar cualquier expresión en la actualización
            update_expr = update.getChild(2)
            self.visit(update_expr, parser)
    
    def visit_frame_statement(self, node, parser):
        """
        Visita un nodo frame
        """
        # frameStatement: FRAME block
        
        # Entrar en el ámbito del frame
        self.symbol_table.enter_scope("frame")
        
        # Visitar el bloque
        block = node.getChild(1)
        self.visit(block, parser)
        
        # Salir del ámbito del frame
        self.symbol_table.exit_scope()