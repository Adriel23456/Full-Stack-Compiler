# ────────────────────────────────────────────────────────────────
# File: CompilerLogic/SemanticComponents/typeChecker.py
# ────────────────────────────────────────────────────────────────
from CompilerLogic.SemanticComponents.astUtil import (
    get_node_line,
    get_node_column,
    get_rule_name,
    get_text,
)


class TypeChecker:
    """
    Verifica tipos y otras reglas semánticas de las expresiones.
    Toda la lógica se conserva; solo se unifica la obtención de la
    línea y la columna exactas con `_pos(node)`.
    """

    # ────────────────────────────────────────────────────────────
    def __init__(self, symbol_table, error_reporter):
        self.symbol_table = symbol_table
        self.error_reporter = error_reporter
        self.current_function = None  # para verificación de return

    # ------------------------------------------------------------------
    # POSICIÓN EXACTA ---------------------------------------------------
    # ------------------------------------------------------------------
    @staticmethod
    def _pos(node):
        """
        Devuelve (línea, columna) exactas basadas en el token.
        Si no hay token usa utilidades previas.
        """
        if hasattr(node, "symbol") and node.symbol:
            return node.symbol.line, node.symbol.column
        return get_node_line(node), get_node_column(node)

    # ------------------------------------------------------------------
    #  GET-TYPE ---------------------------------------------------------
    # ------------------------------------------------------------------
    def get_type(self, node, parser):
        """Determina el tipo de la expresión `node`."""
        rule_name = get_rule_name(node, parser)

        # ── NODO TERMINAL ─────────────────────────────────────────────
        if not rule_name:
            text = node.getText()

            # constantes
            if text in ("true", "false"):
                return "bool"
            if text in (
                "rojo",
                "azul",
                "verde",
                "amarillo",
                "cyan",
                "magenta",
                "blanco",
                "negro",
                "marrón",
            ):
                return "color"
            if text.isdigit() or (
                text.replace(".", "", 1).isdigit() and text.count(".") <= 1
            ):
                return "int"
            if text in ("cos", "sin"):
                return "builtin_function"

            # identificador
            if text[0].islower() and text.isalnum():
                symbol = self.symbol_table.lookup(text)
                if symbol:
                    self.symbol_table.mark_used(text)
                    return symbol.get("type", "unknown")

                # no declarado
                line, col = self._pos(node)
                self.error_reporter.report_error(
                    line, col, f"Variable no declarada: {text}", len(text)
                )
                return "unknown"
            return "unknown"

        # ── NODO NO TERMINAL ──────────────────────────────────────────
        text = node.getText()
        if text in ("true", "false"):
            return "bool"
        if text in (
            "rojo",
            "azul",
            "verde",
            "amarillo",
            "cyan",
            "magenta",
            "blanco",
            "negro",
            "marrón",
        ):
            return "color"

        # clasificación
        if rule_name == "numberExpr":
            return "int"
        if rule_name in ("boolConstExpr", "boolExpr"):
            return "bool"
        if rule_name == "colorExpr":
            return "color"
        if rule_name == "idExpr":
            var_name = get_text(node.getChild(0))
            if var_name in ("cos", "sin"):
                return "builtin_function"
            symbol = self.symbol_table.lookup(var_name)
            if symbol:
                self.symbol_table.mark_used(var_name)
                return symbol.get("type", "unknown")

            line, col = self._pos(node.getChild(0))
            self.error_reporter.report_error(
                line, col, f"Variable no declarada: {var_name}", len(var_name)
            )
            return "unknown"

        if rule_name in ("addSubExpr", "mulDivExpr", "parenExpr", "negExpr"):
            return "int"
        if rule_name in ("cosExpr", "sinExpr"):
            self.check_expression(node.getChild(2), parser)
            return "int"
        if rule_name == "comparisonExpr":
            return "bool"
        if rule_name in ("andExpr", "orExpr", "notExpr", "parenBoolExpr"):
            return "bool"
        if rule_name == "functionCallExpr":
            func_name = get_text(node.getChild(0).getChild(0))
            if func_name in ("cos", "sin"):
                return "int"
            self.symbol_table.mark_used(func_name)
            return "int"
        if rule_name == "expr":
            if node.getChildCount() == 1:
                if self.get_type(node.getChild(0), parser) == "bool":
                    return "bool"
            return "int"

        return "int"

    # ------------------------------------------------------------------
    # CHECK-EXPRESSION --------------------------------------------------
    # ------------------------------------------------------------------
    def check_expression(self, node, parser, expected_type=None):
        actual_type = self.get_type(node, parser)
        rule_name = get_rule_name(node, parser)

        # función dentro de expresión
        if rule_name == "functionCall":
            self.check_function_call(node, parser)

        # OPERACIONES ARITMÉTICAS -------------------------------------
        if rule_name in ("addSubExpr", "mulDivExpr", "modExpr"):
            left_expr = node.getChild(0)
            right_expr = node.getChild(2)

            left_type = self.get_type(left_expr, parser)
            right_type = self.get_type(right_expr, parser)

            if left_type not in ("int", "unknown"):
                line, col = self._pos(left_expr)
                self.error_reporter.report_error(
                    line,
                    col,
                    f"Operación aritmética requiere tipo numérico (int), pero se encontró {left_type}",
                    len(get_text(left_expr)),
                )

            if right_type not in ("int", "unknown"):
                line, col = self._pos(right_expr)
                self.error_reporter.report_error(
                    line,
                    col,
                    f"Operación aritmética requiere tipo numérico (int), pero se encontró {right_type}",
                    len(get_text(right_expr)),
                )

        # FUNCIONES trigonométricas -----------------------------------
        elif rule_name in ("cosExpr", "sinExpr"):
            arg_expr = node.getChild(2)
            arg_type = self.get_type(arg_expr, parser)
            if arg_type not in ("int", "unknown"):
                line, col = self._pos(arg_expr)
                self.error_reporter.report_error(
                    line,
                    col,
                    f"Función {rule_name[:-4]} requiere argumento int, pero se encontró {arg_type}",
                    len(get_text(arg_expr)),
                )

        # COMPARACIONES ------------------------------------------------
        elif rule_name == "comparisonExpr":
            left_expr = node.getChild(0)
            right_expr = node.getChild(2)
            op = get_text(node.getChild(1))

            left_type = self.get_type(left_expr, parser)
            right_type = self.get_type(right_expr, parser)

            if op in ("==", "!="):
                if (
                    left_type != right_type
                    and left_type != "unknown"
                    and right_type != "unknown"
                ):
                    line, col = self._pos(node)
                    self.error_reporter.report_error(
                        line,
                        col,
                        f"Comparación {op} requiere tipos iguales, pero se encontró {left_type} y {right_type}",
                        len(get_text(node.getChild(1))),
                    )
            else:  # <, >, <=, >=
                if left_type not in ("int", "unknown"):
                    line, col = self._pos(left_expr)
                    self.error_reporter.report_error(
                        line,
                        col,
                        f"Comparación {op} requiere tipo int, pero se encontró {left_type}",
                        len(get_text(left_expr)),
                    )
                if right_type not in ("int", "unknown"):
                    line, col = self._pos(right_expr)
                    self.error_reporter.report_error(
                        line,
                        col,
                        f"Comparación {op} requiere tipo int, pero se encontró {right_type}",
                        len(get_text(right_expr)),
                    )

        # OPERACIONES lógicas -----------------------------------------
        elif rule_name in ("andExpr", "orExpr"):
            left_expr = node.getChild(0)
            right_expr = node.getChild(2)

            left_type = self.get_type(left_expr, parser)
            right_type = self.get_type(right_expr, parser)

            if left_type not in ("bool", "unknown"):
                line, col = self._pos(left_expr)
                self.error_reporter.report_error(
                    line,
                    col,
                    f"Operación lógica requiere tipo bool, pero se encontró {left_type}",
                    len(get_text(left_expr)),
                )
            if right_type not in ("bool", "unknown"):
                line, col = self._pos(right_expr)
                self.error_reporter.report_error(
                    line,
                    col,
                    f"Operación lógica requiere tipo bool, pero se encontró {right_type}",
                    len(get_text(right_expr)),
                )

        elif rule_name == "notExpr":
            expr = node.getChild(1)
            expr_type = self.get_type(expr, parser)
            if expr_type not in ("bool", "unknown"):
                line, col = self._pos(expr)
                self.error_reporter.report_error(
                    line,
                    col,
                    f"Operación ! requiere tipo bool, pero se encontró {expr_type}",
                    len(get_text(expr)),
                )

        # EXPECTED TYPE ------------------------------------------------
        if (
            expected_type
            and actual_type != expected_type
            and actual_type != "unknown"
        ):
            line, col = self._pos(node)
            self.error_reporter.report_error(
                line,
                col,
                f"Se esperaba tipo {expected_type}, pero se encontró {actual_type}",
                len(get_text(node)),
            )

        # RECORRIDO RECURSIVO DE SUBEXPRESIONES -----------------------
        for i in range(node.getChildCount()):
            child = node.getChild(i)
            child_rule = get_rule_name(child, parser)

            if child_rule is not None:
                self.check_expression(child, parser)
            elif child.getChildCount() == 0:
                text = child.getText()
                if text in (
                    "rojo",
                    "azul",
                    "verde",
                    "amarillo",
                    "cyan",
                    "magenta",
                    "blanco",
                    "negro",
                    "marrón",
                    "cos",
                    "sin",
                    "true",
                    "false",
                ):
                    continue  # ignorar literales y built-ins

                if text[0].islower() and text.isalnum():
                    symbol = self.symbol_table.lookup(text)
                    if not symbol:
                        line, col = self._pos(child)
                        self.error_reporter.report_error(
                            line,
                            col,
                            f"Variable no declarada: {text}",
                            len(text),
                        )
                    else:
                        if (
                            not symbol.get("initialized", False)
                            and symbol.get("type") not in ("function", "parameter")
                        ):
                            line, col = self._pos(child)
                            self.error_reporter.report_error(
                                line,
                                col,
                                f"Variable '{text}' utilizada sin inicializar",
                                len(text),
                            )
                        self.symbol_table.mark_used(text)

        return actual_type

    # ------------------------------------------------------------------
    # CHECK-ASSIGNMENT --------------------------------------------------
    # ------------------------------------------------------------------
    def check_assignment(self, node, parser):
        id_node = node.getChild(0)
        expr_node = node.getChild(2)
        var_name = get_text(id_node)

        var_info = self.symbol_table.lookup(var_name, current_scope_only=True) or self.symbol_table.lookup(var_name)

        if not var_info:
            line, col = self._pos(id_node)
            self.error_reporter.report_error(
                line, col, f"Variable no declarada: {var_name}", len(var_name)
            )
            return

        self.symbol_table.mark_used(
            var_name,
            current_scope=var_info.get(
                "current_scope", self.symbol_table.current_scope_name()
            ),
        )

        var_type = var_info.get("type", "unknown")
        expr_text = expr_node.getText()

        if var_type == "color" and expr_text in (
            "rojo",
            "azul",
            "verde",
            "amarillo",
            "cyan",
            "magenta",
            "blanco",
            "negro",
            "marrón",
        ):
            self.symbol_table.mark_initialized(
                var_name,
                current_scope=var_info.get(
                    "current_scope", self.symbol_table.current_scope_name()
                ),
            )
            return

        expr_type = self.check_expression(expr_node, parser)
        self.symbol_table.mark_initialized(
            var_name,
            current_scope=var_info.get(
                "current_scope", self.symbol_table.current_scope_name()
            ),
        )

        if (
            var_type != expr_type
            and var_type != "unknown"
            and expr_type != "unknown"
        ):
            line, col = self._pos(node)
            self.error_reporter.report_error(
                line,
                col,
                f"No se puede asignar {expr_type} a variable de tipo {var_type}",
                len(get_text(node)),
            )

    # ------------------------------------------------------------------
    def check_draw_statement(self, node, parser):
        draw_object = node.getChild(1)
        for i in range(draw_object.getChildCount()):
            child = draw_object.getChild(i)
            if get_rule_name(child, parser) == "expr":
                expr_type = self.get_type(child, parser)
                if expr_type not in ("int", "unknown"):
                    line, col = self._pos(child)
                    self.error_reporter.report_error(
                        line,
                        col,
                        f"Las coordenadas y dimensiones deben ser int, pero se encontró {expr_type}",
                        len(child.getText()),
                    )

    # ------------------------------------------------------------------
    def check_setcolor_statement(self, node, parser):
        color_arg = node.getChild(2)
        color_text = get_text(color_arg)

        if color_text in (
            "rojo",
            "azul",
            "verde",
            "amarillo",
            "cyan",
            "magenta",
            "blanco",
            "negro",
            "marrón",
        ):
            return

        if color_arg.getChildCount() == 0:
            if color_text[0].islower() and color_text.isalnum():
                var_info = self.symbol_table.lookup(color_text)
                if not var_info:
                    line, col = self._pos(color_arg)
                    self.error_reporter.report_error(
                        line, col, f"Variable no declarada: {color_text}", len(color_text)
                    )
                    return

                var_type = var_info.get("type", "unknown")
                self.symbol_table.mark_used(color_text)

                if not var_info.get("initialized", False):
                    line, col = self._pos(color_arg)
                    self.error_reporter.report_error(
                        line,
                        col,
                        f"Variable '{color_text}' utilizada sin inicializar",
                        len(color_text),
                    )

                if var_type not in ("color", "unknown"):
                    line, col = self._pos(color_arg)
                    self.error_reporter.report_error(
                        line,
                        col,
                        f"setcolor requiere argumento color, pero {color_text} es {var_type}",
                        len(color_text),
                    )
        else:
            expr_type = self.check_expression(color_arg, parser)
            if expr_type not in ("color", "unknown"):
                line, col = self._pos(color_arg)
                self.error_reporter.report_error(
                    line,
                    col,
                    f"setcolor requiere argumento color, pero se encontró {expr_type}",
                    len(get_text(color_arg)),
                )

    # ------------------------------------------------------------------
    def check_function_call(self, node, parser):
        rule_name = get_rule_name(node, parser)
        func_name = ""
        arg_list_index = -1

        if rule_name == "functionCall":
            func_name = get_text(node.getChild(0))
            arg_list_index = 2 if node.getChildCount() > 3 else -1
        elif rule_name == "functionCallStatement":
            func_name = get_text(node.getChild(0))
            arg_list_index = 2 if node.getChildCount() > 4 else -1
        else:
            return

        if not func_name:
            return

        func_info = self.symbol_table.lookup(func_name)
        if not func_info:
            line, col = self._pos(node)
            self.error_reporter.report_error(
                line, col, f"Función no declarada: {func_name}", len(func_name)
            )
            return

        self.symbol_table.mark_used(func_name)

        if func_info.get("type") not in ("function", "unknown"):
            line, col = self._pos(node)
            self.error_reporter.report_error(
                line, col, f"{func_name} no es una función", len(func_name)
            )
            return

        arg_count = 0
        if arg_list_index >= 0 and arg_list_index < node.getChildCount():
            arg_list = node.getChild(arg_list_index)
            if get_rule_name(arg_list, parser) == "argumentList":
                arg_count = (arg_list.getChildCount() + 1) // 2

        expected_params = 0
        if func_name in self.symbol_table.functions:
            expected_params = len(self.symbol_table.functions[func_name]["params"])

        if expected_params != arg_count:
            line, col = self._pos(node)
            self.error_reporter.report_error(
                line,
                col,
                f"La función '{func_name}' espera {expected_params} argumentos, pero se proporcionaron {arg_count}",
                len(get_text(node)),
            )

    # ------------------------------------------------------------------
    def check_if_statement(self, node, parser):
        condition = node.getChild(2)
        cond_type = self.check_expression(condition, parser)
        if cond_type not in ("bool", "unknown"):
            line, col = self._pos(condition)
            self.error_reporter.report_error(
                line,
                col,
                f"La condición del if debe ser bool, pero se encontró {cond_type}",
                len(get_text(condition)),
            )

    # ------------------------------------------------------------------
    def check_loop_statement(self, node, parser):
        condition = node.getChild(4)
        cond_type = self.check_expression(condition, parser)
        if cond_type not in ("bool", "unknown"):
            line, col = self._pos(condition)
            self.error_reporter.report_error(
                line,
                col,
                f"La condición del loop debe ser bool, pero se encontró {cond_type}",
                len(get_text(condition)),
            )

        init_assign = node.getChild(2)
        update_assign = node.getChild(6)
        self.check_assignment(init_assign, parser)
        self.check_assignment(update_assign, parser)

    # ------------------------------------------------------------------
    def is_color_constant(self, text):
        return text in (
            "rojo",
            "azul",
            "verde",
            "amarillo",
            "cyan",
            "magenta",
            "blanco",
            "negro",
            "marrón",
        )