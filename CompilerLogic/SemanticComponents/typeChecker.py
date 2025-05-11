from CompilerLogic.SemanticComponents.astUtil import get_node_column, get_node_line

class TypeChecker:
    """
    Maneja la verificación de tipos para expresiones y declaraciones
    """
    def __init__(self, symbol_table, error_reporter):
        self.symbol_table = symbol_table
        self.error_reporter = error_reporter
        self.current_function = None  # Para verificación de return
    
    def get_type(self, node, parser):
        """
        Determina el tipo de una expresión considerando el renombramiento
        """
        from CompilerLogic.SemanticComponents.astUtil import get_rule_name, get_node_text, get_text, get_node_line, get_node_column
        
        rule_name = get_rule_name(node, parser)
        
        if not rule_name:  # Terminal node
            text = node.getText()
            
            # Verificar constantes booleanas PRIMERO
            if text in ["true", "false"]:
                return "bool"
            
            # Verificar constantes de color ANTES de verificar identificadores
            if text in ["rojo", "azul", "verde", "amarillo", "cyan", "magenta", "blanco", "negro", "marrón"]:
                return "color"
            
            # Verificar números
            if text.isdigit() or (text.replace('.', '', 1).isdigit() and text.count('.') <= 1):
                return "int"
            
            # Verificar funciones integradas
            if text == "cos" or text == "sin":
                return "builtin_function"
            
            # Verificar identificadores (considerando renombramiento)
            if text[0].islower() and text.isalnum():
                # Buscar usando lookup que maneja renombramiento automáticamente
                symbol = self.symbol_table.lookup(text)
                
                if symbol:
                    # Marcar como usado (también considera renombramiento)
                    self.symbol_table.mark_used(text)
                    return symbol.get("type", "unknown")
                
                # Variable no encontrada, reportar error
                # Usar la posición correcta del nodo terminal
                line = node.symbol.line if hasattr(node, 'symbol') else get_node_line(node)
                column = node.symbol.column if hasattr(node, 'symbol') else get_node_column(node)
                
                self.error_reporter.report_error(
                    line,
                    column,
                    f"Variable no declarada: {text}",
                    len(text)
                )
                return "unknown"
            
            return "unknown"
        
        # Para nodos no terminales
        text = node.getText()
        if text in ["true", "false"]:
            return "bool"
        if text in ["rojo", "azul", "verde", "amarillo", "cyan", "magenta", "blanco", "negro", "marrón"]:
            return "color"
        
        # Analizar tipos basados en el tipo de nodo
        if rule_name == "numberExpr":
            return "int"
        elif rule_name == "boolConstExpr":
            return "bool"
        elif rule_name == "boolExpr":
            return "bool"
        elif rule_name == "colorExpr":
            return "color"
        elif rule_name == "idExpr":
            var_name = get_text(node.getChild(0))
            # Verificar si es una función integrada
            if var_name == "cos" or var_name == "sin":
                return "builtin_function"
                
            symbol = self.symbol_table.lookup(var_name)
            if symbol:
                # Marcar como usado
                self.symbol_table.mark_used(var_name)
                return symbol.get("type", "unknown")
            
            # Variable no encontrada, reportar error
            self.error_reporter.report_error(
                get_node_line(node.getChild(0)),
                get_node_column(node.getChild(0)),
                f"Variable no declarada: {var_name}",
                len(var_name)
            )
            return "unknown"
        elif rule_name in ["addSubExpr", "mulDivExpr", "parenExpr", "negExpr"]:
            # Operaciones aritméticas siempre retornan int
            return "int"
        elif rule_name in ["cosExpr", "sinExpr"]:
            # Funciones trigonométricas retornan int
            # También verificamos el tipo del argumento, pero no fallamos si no es int
            arg_expr = node.getChild(2)  # cos(expr) o sin(expr) - expr es el índice 2
            self.check_expression(arg_expr, parser) # Solo verificar, no usar el resultado
            return "int" # Siempre retornar int para estas funciones
        elif rule_name == "comparisonExpr":
            # Comparaciones retornan bool
            return "bool"
        elif rule_name in ["andExpr", "orExpr", "notExpr", "parenBoolExpr"]:
            # Operaciones lógicas retornan bool
            return "bool"
        elif rule_name == "functionCallExpr":
            # Para llamadas a funciones, buscar en la tabla de símbolos
            func_node = node.getChild(0)  # Nodo functionCall
            func_name = get_text(func_node.getChild(0))  # Nombre de la función
            # Verificar si es una función integrada
            if func_name == "cos" or func_name == "sin":
                return "int"  # Las funciones trigonométricas retornan int
                
            # Marcar la función como usada
            self.symbol_table.mark_used(func_name)
            # En VGraph, asumimos que las funciones retornan int
            return "int"
        elif rule_name == "expr":
            # Para expresiones genéricas, necesitamos determinar mejor el tipo
            # Verificar si todos los hijos son literales booleanos
            if node.getChildCount() == 1:
                child = node.getChild(0)
                child_type = self.get_type(child, parser)
                if child_type == "bool":
                    return "bool"
            return "int"  # Fallback a int
        
        # Si no se pudo determinar el tipo, retornar int por defecto para evitar errores innecesarios
        return "int"
    
    def check_expression(self, node, parser, expected_type=None):
        """
        Verifica el tipo de una expresión y reporta errores si no coincide con el tipo esperado
        """
        from CompilerLogic.SemanticComponents.astUtil import get_rule_name, get_node_line, get_node_column, get_text
        
        actual_type = self.get_type(node, parser)
        rule_name = get_rule_name(node, parser)

        # AÑADIR ESTE CASO para functionCall dentro de expresiones
        if rule_name == "functionCall":
            print(f"=== DEBUG: Found functionCall in expression ===")
            self.check_function_call(node, parser)
        
        # Verificaciones específicas según el tipo de expresión
        if rule_name in ["addSubExpr", "mulDivExpr", "modExpr"]:
            # Verificar que las operaciones aritméticas se realicen entre valores numéricos
            left_expr = node.getChild(0)
            right_expr = node.getChild(2)
            
            left_type = self.get_type(left_expr, parser)
            right_type = self.get_type(right_expr, parser)
            
            if left_type != "int" and left_type != "unknown":
                self.error_reporter.report_error(
                    get_node_line(left_expr),
                    get_node_column(left_expr),
                    f"Operación aritmética requiere tipo numérico (int), pero se encontró {left_type}",
                    len(get_text(left_expr))
                )
            
            if right_type != "int" and right_type != "unknown":
                self.error_reporter.report_error(
                    get_node_line(right_expr),
                    get_node_column(right_expr),
                    f"Operación aritmética requiere tipo numérico (int), pero se encontró {right_type}",
                    len(get_text(right_expr))
                )
        
        elif rule_name in ["cosExpr", "sinExpr"]:
            # Verificar que los argumentos de las funciones trigonométricas sean numéricos
            arg_expr = node.getChild(2)  # cos(expr) o sin(expr) - expr es el índice 2
            arg_type = self.get_type(arg_expr, parser)
            
            if arg_type != "int" and arg_type != "unknown":
                self.error_reporter.report_error(
                    get_node_line(arg_expr),
                    get_node_column(arg_expr),
                    f"Función {rule_name[:-4]} requiere argumento numérico (int), pero se encontró {arg_type}",
                    len(get_text(arg_expr))
                )
        
        elif rule_name == "comparisonExpr":
            # Verificar que las comparaciones se realicen entre valores compatibles
            left_expr = node.getChild(0)
            right_expr = node.getChild(2)
            op = get_text(node.getChild(1))
            
            left_type = self.get_type(left_expr, parser)
            right_type = self.get_type(right_expr, parser)
            
            # Para == y !=, los tipos deben ser iguales
            if op in ["==", "!="]:
                if left_type != right_type and left_type != "unknown" and right_type != "unknown":
                    self.error_reporter.report_error(
                        get_node_line(node),
                        get_node_column(node),
                        f"Comparación {op} requiere tipos iguales, pero se encontró {left_type} y {right_type}",
                        len(get_text(node.getChild(1)))
                    )
            # Para <, >, <=, >=, los tipos deben ser numéricos
            elif op in ["<", ">", "<=", ">="]:
                if left_type != "int" and left_type != "unknown":
                    self.error_reporter.report_error(
                        get_node_line(left_expr),
                        get_node_column(left_expr),
                        f"Comparación {op} requiere tipo numérico (int), pero se encontró {left_type}",
                        len(get_text(left_expr))
                    )
                
                if right_type != "int" and right_type != "unknown":
                    self.error_reporter.report_error(
                        get_node_line(right_expr),
                        get_node_column(right_expr),
                        f"Comparación {op} requiere tipo numérico (int), pero se encontró {right_type}",
                        len(get_text(right_expr))
                    )
        
        elif rule_name in ["andExpr", "orExpr"]:
            # Verificar que las operaciones lógicas se realicen entre valores booleanos
            left_expr = node.getChild(0)
            right_expr = node.getChild(2)
            
            left_type = self.get_type(left_expr, parser)
            right_type = self.get_type(right_expr, parser)
            
            if left_type != "bool" and left_type != "unknown":
                self.error_reporter.report_error(
                    get_node_line(left_expr),
                    get_node_column(left_expr),
                    f"Operación lógica requiere tipo bool, pero se encontró {left_type}",
                    len(get_text(left_expr))
                )
            
            if right_type != "bool" and right_type != "unknown":
                self.error_reporter.report_error(
                    get_node_line(right_expr),
                    get_node_column(right_expr),
                    f"Operación lógica requiere tipo bool, pero se encontró {right_type}",
                    len(get_text(right_expr))
                )
        
        elif rule_name == "notExpr":
            # Verificar que la operación NOT se realice sobre un valor booleano
            expr = node.getChild(1)
            expr_type = self.get_type(expr, parser)
            
            if expr_type != "bool" and expr_type != "unknown":
                self.error_reporter.report_error(
                    get_node_line(expr),
                    get_node_column(expr),
                    f"Operación ! requiere tipo bool, pero se encontró {expr_type}",
                    len(get_text(expr))
                )
        
        # Verificar contra el tipo esperado, si se especificó
        if expected_type and actual_type != expected_type and actual_type != "unknown":
            self.error_reporter.report_error(
                get_node_line(node),
                get_node_column(node),
                f"Se esperaba tipo {expected_type}, pero se encontró {actual_type}",
                len(get_text(node))
            )
        
        # Revisar recursivamente todas las subexpresiones
        for i in range(node.getChildCount()):
            child = node.getChild(i)
            child_rule = get_rule_name(child, parser)
            
            if child_rule is not None:  # No es un nodo terminal
                self.check_expression(child, parser)
            elif child.getChildCount() == 0:  # Es un nodo terminal (posible ID)
                text = child.getText()
                
                # AÑADIR: Ignorar constantes de color
                if text in ["rojo", "azul", "verde", "amarillo", "cyan", "magenta", "blanco", "negro", "marrón"]:
                    continue  # No verificar constantes de color
                
                # AÑADIR: Ignorar funciones integradas y constantes booleanas
                if text in ["cos", "sin", "true", "false"]:
                    continue  # No verificar como variables
                
                if text[0].islower() and text.isalnum():  # Identificador
                    symbol = self.symbol_table.lookup(text)
                    if not symbol:
                        # Usar posición del token específico
                        line = child.symbol.line if hasattr(child, 'symbol') else get_node_line(child)
                        column = child.symbol.column if hasattr(child, 'symbol') else get_node_column(child)
                        
                        self.error_reporter.report_error(
                            line,
                            column,
                            f"Variable no declarada: {text}",
                            len(text)
                        )
                    else:
                        # Verificar si está inicializada
                        if not symbol.get('initialized', False) and symbol.get('type') not in ['function', 'parameter']:
                            # Usar posición del token específico
                            line = child.symbol.line if hasattr(child, 'symbol') else get_node_line(child)
                            column = child.symbol.column if hasattr(child, 'symbol') else get_node_column(child)
                            
                            self.error_reporter.report_error(
                                line,
                                column,
                                f"Variable '{text}' utilizada sin inicializar",
                                len(text)
                            )
                        
                        # Marcar como usado
                        self.symbol_table.mark_used(text)
        
        return actual_type
    
    def check_assignment(self, node, parser):
        """
        Verifica que una asignación sea válida
        """
        from CompilerLogic.SemanticComponents.astUtil import get_node_line, get_node_column, get_text
        
        # assignmentExpression: ID ASSIGN expr
        id_node = node.getChild(0)
        expr_node = node.getChild(2)
        
        var_name = get_text(id_node)
        
        # Buscar la variable en el ámbito actual primero
        var_info = self.symbol_table.lookup(var_name, current_scope_only=True)
        
        # Si no se encuentra en el ámbito actual, buscar en todos los ámbitos
        if not var_info:
            var_info = self.symbol_table.lookup(var_name)
        
        if not var_info:
            # Usar posición del ID específico
            line = id_node.symbol.line if hasattr(id_node, 'symbol') else get_node_line(id_node)
            column = id_node.symbol.column if hasattr(id_node, 'symbol') else get_node_column(id_node)
            
            self.error_reporter.report_error(
                line,
                column,
                f"Variable no declarada: {var_name}",
                len(var_name)
            )
            # IMPORTANTE: NO continuar con el análisis si la variable no está declarada
            return
        
        # Marcar como usada en el ámbito correcto
        self.symbol_table.mark_used(var_name, current_scope=var_info.get('current_scope', self.symbol_table.current_scope_name()))
        
        var_type = var_info.get("type", "unknown")
        
        # Caso especial para asignaciones de color
        expr_text = expr_node.getText()
        if var_type == "color" and expr_text in ["rojo", "azul", "verde", "amarillo", "cyan", "magenta", "blanco", "negro", "marrón"]:
            # IMPORTANTE: Marcar como inicializada inmediatamente
            self.symbol_table.mark_initialized(var_name, current_scope=var_info.get('current_scope', self.symbol_table.current_scope_name()))
            return  # Es una asignación válida de color
        
        # Verificación normal de tipo
        expr_type = self.check_expression(expr_node, parser)
        
        # IMPORTANTE: Marcar como inicializada en el ámbito correcto
        self.symbol_table.mark_initialized(var_name, current_scope=var_info.get('current_scope', self.symbol_table.current_scope_name()))
        
        # Verificar compatibilidad de tipos
        if var_type != expr_type and var_type != "unknown" and expr_type != "unknown":
            self.error_reporter.report_error(
                get_node_line(node),
                get_node_column(node),
                f"No se puede asignar {expr_type} a variable de tipo {var_type}",
                len(get_text(node))
            )
    
    def check_draw_statement(self, node, parser):
        """
        Verifica que los argumentos de una instrucción draw sean válidos
        """
        from CompilerLogic.SemanticComponents.astUtil import get_rule_name, get_node_line, get_node_column
        
        # drawStatement: DRAW drawObject SEMICOLON
        draw_object = node.getChild(1)
        object_type = get_rule_name(draw_object, parser)
        
        # Verificar cada expresión en los argumentos
        for i in range(draw_object.getChildCount()):
            child = draw_object.getChild(i)
            if get_rule_name(child, parser) == "expr":
                # Solo verificamos y marcamos como usado, pero no reportamos errores
                # para arreglar el problema con cos() y sin()
                expr_type = self.get_type(child, parser)
                
                # Solo reportar error si el tipo no es int y no es unknown
                # (unknown podría ser de una expresión compleja que ya sabemos es int)
                if expr_type != "int" and expr_type != "unknown":
                    self.error_reporter.report_error(
                        get_node_line(child),
                        get_node_column(child),
                        f"Las coordenadas y dimensiones deben ser numéricas (int), pero se encontró {expr_type}",
                        len(child.getText())
                    )
    
    def check_setcolor_statement(self, node, parser):
        """
        Verifica que el argumento de setcolor sea de tipo color
        """
        from CompilerLogic.SemanticComponents.astUtil import get_node_line, get_node_column, get_text
        
        # setColorStatement: SETCOLOR LPAREN (ID | COLOR_CONST) RPAREN SEMICOLON
        color_arg = node.getChild(2)
        color_text = get_text(color_arg)
        
        # Verificar primero si es una constante de color
        if color_text in ["rojo", "azul", "verde", "amarillo", "cyan", "magenta", "blanco", "negro", "marrón"]:
            return  # Es una constante de color válida
        
        if color_arg.getChildCount() == 0:  # Terminal node (ID)
            # Si es un identificador, verificar que sea de tipo color
            if color_text[0].islower() and color_text.isalnum():  # Es un ID
                var_info = self.symbol_table.lookup(color_text)
                
                if not var_info:
                    # CORRECCIÓN: Usar posición del token específico
                    line = color_arg.symbol.line if hasattr(color_arg, 'symbol') else get_node_line(color_arg)
                    column = color_arg.symbol.column if hasattr(color_arg, 'symbol') else get_node_column(color_arg)
                    
                    self.error_reporter.report_error(
                        line,
                        column,
                        f"Variable no declarada: {color_text}",
                        len(color_text)
                    )
                    return
                
                var_type = var_info.get("type", "unknown")
                self.symbol_table.mark_used(color_text)
                
                # Verificar si está inicializada
                if not var_info.get('initialized', False):
                    # CORRECCIÓN: Usar posición del token específico
                    line = color_arg.symbol.line if hasattr(color_arg, 'symbol') else get_node_line(color_arg)
                    column = color_arg.symbol.column if hasattr(color_arg, 'symbol') else get_node_column(color_arg)
                    
                    self.error_reporter.report_error(
                        line,
                        column,
                        f"Variable '{color_text}' utilizada sin inicializar",
                        len(color_text)
                    )
                
                if var_type != "color" and var_type != "unknown":
                    # CORRECCIÓN: Usar posición del token específico
                    line = color_arg.symbol.line if hasattr(color_arg, 'symbol') else get_node_line(color_arg)
                    column = color_arg.symbol.column if hasattr(color_arg, 'symbol') else get_node_column(color_arg)
                    
                    self.error_reporter.report_error(
                        line,
                        column,
                        f"La función setcolor requiere un argumento de tipo color, pero {color_text} es de tipo {var_type}",
                        len(color_text)
                    )
        else:
            # Si es una expresión, verificar que sea de tipo color
            expr_type = self.check_expression(color_arg, parser)
            
            if expr_type != "color" and expr_type != "unknown":
                self.error_reporter.report_error(
                    get_node_line(color_arg),
                    get_node_column(color_arg),
                    f"La función setcolor requiere un argumento de tipo color, pero se encontró {expr_type}",
                    len(get_text(color_arg))
                )
    
    def check_function_call(self, node, parser):
        """
        Verifica que una llamada a función sea válida
        """
        from CompilerLogic.SemanticComponents.astUtil import get_node_line, get_node_column, get_text, get_rule_name
        
        print(f"=== DEBUG TypeChecker: check_function_call called ===")
        print(f"Node children: {node.getChildCount()}")
        
        # Verificar si es un nodo de functionCall o functionCallStatement
        rule_name = get_rule_name(node, parser)
        print(f"=== DEBUG: Node rule name: {rule_name} ===")
        
        func_name = ""
        arg_list_index = -1
        
        if rule_name == "functionCall":
            # functionCall: ID LPAREN argumentList? RPAREN
            if node.getChildCount() >= 1:
                func_name = get_text(node.getChild(0))
                arg_list_index = 2 if node.getChildCount() > 3 else -1
        elif rule_name == "functionCallStatement":
            # functionCallStatement: ID LPAREN argumentList? RPAREN SEMICOLON
            if node.getChildCount() >= 1:
                func_name = get_text(node.getChild(0))
                arg_list_index = 2 if node.getChildCount() > 4 else -1
        else:
            print(f"=== DEBUG: Unknown node type for function call: {rule_name} ===")
            return
        
        print(f"=== DEBUG: Function name: {func_name} ===")
        
        if not func_name:
            print(f"=== DEBUG: Empty function name, skipping ===")
            return
        
        func_info = self.symbol_table.lookup(func_name)
        print(f"=== DEBUG: Function info: {func_info} ===")
        
        if not func_info:
            self.error_reporter.report_error(
                get_node_line(node),
                get_node_column(node),
                f"Función no declarada: {func_name}",
                len(func_name)
            )
            return
        
        # Marcar la función como usada
        self.symbol_table.mark_used(func_name)
        
        # Verificar tipo de función
        if func_info.get("type") != "function" and func_info.get("type") != "unknown":
            self.error_reporter.report_error(
                get_node_line(node),
                get_node_column(node),
                f"{func_name} no es una función",
                len(func_name)
            )
            return
        
        # Contar argumentos proporcionados
        arg_count = 0
        if arg_list_index >= 0 and arg_list_index < node.getChildCount():
            arg_list = node.getChild(arg_list_index)
            print(f"=== DEBUG: Argument list rule: {get_rule_name(arg_list, parser)} ===")
            if get_rule_name(arg_list, parser) == "argumentList":
                # argumentList: expr (COMMA expr)*
                arg_count = (arg_list.getChildCount() + 1) // 2
                print(f"=== DEBUG: Argument count calculated: {arg_count} ===")
        
        print(f"=== DEBUG: Final argument count: {arg_count} ===")
        
        # Obtener número de parámetros esperados
        expected_params = 0
        print(f"=== DEBUG: Checking in symbol_table.functions: {self.symbol_table.functions} ===")
        
        if func_name in self.symbol_table.functions:
            expected_params = len(self.symbol_table.functions[func_name]["params"])
            print(f"=== DEBUG: Expected params found: {expected_params} ===")
        else:
            print(f"=== DEBUG: Function {func_name} not found in functions table ===")
            # Podría ser una función pero sin información de parámetros, continuar
        
        # Comparar número de argumentos con parámetros esperados
        print(f"=== DEBUG: Comparing {expected_params} expected vs {arg_count} provided ===")
        
        if expected_params != arg_count:
            print(f"=== DEBUG: Error detected - reporting it ===")
            self.error_reporter.report_error(
                get_node_line(node),
                get_node_column(node),
                f"La función '{func_name}' espera {expected_params} argumentos, pero se proporcionaron {arg_count}",
                len(get_text(node))
            )
    
    def check_if_statement(self, node, parser):
        """
        Verifica que la condición de un if sea booleana
        """
        from CompilerLogic.SemanticComponents.astUtil import get_node_line, get_node_column, get_text
        
        # ifStatement: IF LPAREN boolExpr RPAREN block (ELSE (ifStatement | block))?
        condition = node.getChild(2)
        cond_type = self.check_expression(condition, parser)
        
        if cond_type != "bool" and cond_type != "unknown":
            self.error_reporter.report_error(
                get_node_line(condition),
                get_node_column(condition),
                f"La condición del if debe ser de tipo bool, pero se encontró {cond_type}",
                len(get_text(condition))
            )
    
    def check_loop_statement(self, node, parser):
        """
        Verifica que la condición de un loop sea booleana
        """
        from CompilerLogic.SemanticComponents.astUtil import get_node_line, get_node_column, get_text
        
        # loopStatement: LOOP LPAREN assignmentExpression SEMICOLON boolExpr SEMICOLON assignmentExpression RPAREN block
        condition = node.getChild(4)
        cond_type = self.check_expression(condition, parser)
        
        if cond_type != "bool" and cond_type != "unknown":
            self.error_reporter.report_error(
                get_node_line(condition),
                get_node_column(condition),
                f"La condición del loop debe ser de tipo bool, pero se encontró {cond_type}",
                len(get_text(condition))
            )
        
        # Verificar las asignaciones de inicialización y actualización
        init_assign = node.getChild(2)
        update_assign = node.getChild(6)
        
        self.check_assignment(init_assign, parser)
        self.check_assignment(update_assign, parser)
    
    def is_color_constant(self, text):
        """
        Verifica si un texto es una constante de color válida
        """
        return text in ["rojo", "azul", "verde", "amarillo", "cyan", "magenta", "blanco", "negro", "marrón"]