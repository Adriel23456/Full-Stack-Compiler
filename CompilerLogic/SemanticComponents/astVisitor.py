# ────────────────────────────────────────────────────────────────
# File: CompilerLogic/SemanticComponents/astVisitor.py
# ────────────────────────────────────────────────────────────────
from CompilerLogic.SemanticComponents.astUtil import (
    get_rule_name,
    get_text,
    get_node_line,
    get_node_column,
)

class ASTVisitor:
    """
    Recorre el AST y delega en los *checkers* la verificación semántica.
    Todas las posiciones de error/‐warning se obtienen con `_pos(node)`
    para garantizar que el subrayado se alinee exactamente con el token.
    """

    # ------------------------------------------------------------------
    def __init__(self, symbol_table, type_checker, scope_checker, error_reporter):
        self.symbol_table = symbol_table
        self.type_checker = type_checker
        self.scope_checker = scope_checker
        self.error_reporter = error_reporter

    # ------------------------------------------------------------------
    # POSICIÓN EXACTA ---------------------------------------------------
    # ------------------------------------------------------------------
    @staticmethod
    def _pos(node):
        """
        Devuelve (línea, columna) exactas basadas en el token `node`.
        Si no hay token (por ser nodo sintético), usa utilidades auxiliares.
        """
        if hasattr(node, "symbol") and node.symbol:
            return node.symbol.line, node.symbol.column
        return get_node_line(node), get_node_column(node)

    # ------------------------------------------------------------------
    def visit(self, node, parser):
        """
        Visita un nodo del AST y aplica la verificación semántica necesaria.
        """
        # Mantener la línea actual para mensajes de símbolos
        if hasattr(node, "start") and node.start:
            self.symbol_table.set_current_line(node.start.line)

        # Nodo terminal ⇒ nada que hacer
        if node.getChildCount() == 0:
            return

        rule_name = get_rule_name(node, parser)

        # Despacho según la regla del nodo
        if rule_name == "program":
            self.visit_program(node, parser)
        elif rule_name == "declaration":
            self.scope_checker.check_variable_declaration(node, parser)
        elif rule_name == "assignmentStatement":
            self.visit_assignment_statement(node, parser)
        elif rule_name == "functionDeclStatement":
            self.visit_function_declaration(node, parser)
        elif rule_name == "functionCall":
            # Llamada a función usada como expresión
            if node.getChildCount() >= 3:  # ID LPAREN RPAREN (mínimo)
                self.type_checker.check_function_call(node, parser)
        elif rule_name == "functionCallStatement":
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
            # Resto de nodos: recorrido recursivo
            for i in range(node.getChildCount()):
                self.visit(node.getChild(i), parser)

    # ------------------------------------------------------------------
    def visit_program(self, node, parser):
        """
        Visita el nodo raíz `program`.
        """
        # Visitar declaraciones / sentencias
        for i in range(node.getChildCount()):
            self.visit(node.getChild(i), parser)

        # ── POST‐ANÁLISIS: símbolos sin usar / sin inicializar ─────────
        unused_symbols = self.symbol_table.get_unused_symbols()
        for symbol in unused_symbols:
            col = symbol.get("column", 0)
            self.error_reporter.report_warning(
                symbol["line"],
                col,
                f"Variable '{symbol['name']}' declarada pero no utilizada",
                len(symbol["name"]),
            )

        uninitialized = self.symbol_table.get_uninitialized_used_symbols()
        for symbol in uninitialized:
            col = symbol.get("column", 0)
            self.error_reporter.report_error(
                symbol["line"],
                col,
                f"Variable '{symbol['name']}' utilizada sin inicializar",
                len(symbol["name"]),
            )

    # ------------------------------------------------------------------
    def visit_assignment_statement(self, node, parser):
        """
        Procesa: `assignmentStatement : assignmentExpression SEMICOLON`
        """
        assignment_expr = node.getChild(0)

        # Verificar la asignación completa
        if assignment_expr.getChildCount() >= 3:  # ID ASSIGN expr
            self.type_checker.check_assignment(assignment_expr, parser)

            # Visitar la expresión del RHS
            rhs_expr = assignment_expr.getChild(2)
            self.visit(rhs_expr, parser)

    # ------------------------------------------------------------------
    def visit_function_declaration(self, node, parser):
        """
        Procesa la declaración de función y su bloque.
        """
        func_name = get_text(node.getChild(1))

        # Declaración (scopeChecker maneja errores de posición)
        self.scope_checker.check_function_declaration(node, parser)

        # Nuevo ámbito
        self.symbol_table.enter_scope(func_name)
        self.scope_checker.enter_function(func_name)

        # Parámetros
        if node.getChildCount() > 5:  # hay paramList
            param_list = node.getChild(3)
            for i in range(0, param_list.getChildCount(), 2):  # saltar comas
                param_name = get_text(param_list.getChild(i))
                self.symbol_table.mark_initialized(param_name)

        # Bloque de la función
        block = node.getChild(node.getChildCount() - 1)
        self.visit(block, parser)

        # Salir del ámbito
        self.symbol_table.exit_scope()
        self.scope_checker.exit_function()

    # ------------------------------------------------------------------
    def visit_function_call_statement(self, node, parser):
        """
        Procesa: `functionCallStatement : ID LPAREN argumentList? RPAREN SEMICOLON`
        """

        # Llamada a función (typeChecker verifica tipos y argumentos)
        self.type_checker.check_function_call(node, parser)

        # Recorrer argumentos (si existen) para detección adicional
        if node.getChildCount() > 4:  # con argumentList
            arg_list = node.getChild(2)
            if get_rule_name(arg_list, parser) == "argumentList":
                for i in range(0, arg_list.getChildCount(), 2):  # saltar comas
                    self.visit(arg_list.getChild(i), parser)

    # ------------------------------------------------------------------
    def visit_if_statement(self, node, parser):
        """
        Procesa: `ifStatement : IF LPAREN boolExpr RPAREN block (ELSE (ifStatement | block))?`
        """
        self.type_checker.check_if_statement(node, parser)

        # Condición
        self.visit(node.getChild(2), parser)
        # Bloque then
        self.visit(node.getChild(4), parser)
        # Bloque else (opcional)
        if node.getChildCount() > 5:
            self.visit(node.getChild(6), parser)

    # ------------------------------------------------------------------
    def visit_loop_statement(self, node, parser):
        """
        Procesa: `loopStatement : LOOP LPAREN assignmentExpression ; boolExpr ; assignmentExpression RPAREN block`
        """
        # Inicialización
        init = node.getChild(2)
        if get_rule_name(init, parser) == "assignmentExpression":
            var_name = get_text(init.getChild(0))
            self.type_checker.check_assignment(init, parser)
            var_info = self.symbol_table.lookup(var_name)
            if var_info:
                current_scope = var_info.get(
                    "current_scope", self.symbol_table.current_scope_name()
                )
                self.symbol_table.mark_initialized(var_name, current_scope=current_scope)

            # subexpresiones
            self.visit(init.getChild(2), parser)

        # Condición + verificación completa del loop
        self.type_checker.check_loop_statement(node, parser)
        self.visit(node.getChild(4), parser)

        # Bloque del loop
        self.visit(node.getChild(8), parser)

        # Actualización
        update = node.getChild(6)
        if get_rule_name(update, parser) == "assignmentExpression":
            self.type_checker.check_assignment(update, parser)
            self.visit(update.getChild(2), parser)

    # ------------------------------------------------------------------
    def visit_frame_statement(self, node, parser):
        """
        Procesa: `frameStatement : FRAME block`
        """
        self.symbol_table.enter_scope("frame")
        self.visit(node.getChild(1), parser)  # block
        self.symbol_table.exit_scope()