# ────────────────────────────────────────────────────────────────
# File: CompilerLogic/SemanticComponents/typeChecker.py
# ────────────────────────────────────────────────────────────────
from CompilerLogic.SemanticComponents.astUtil import (
    get_node_line,
    get_node_column,
    get_rule_name,
    get_text,
)

# ────────────────────────────────────────────────────────────────
#  UTILIDADES AUXILIARES
# ────────────────────────────────────────────────────────────────
def _ctx_alt(ctx):
    """Nombre de la alternativa etiquetada (sin «Context»)."""
    return ctx.__class__.__name__.replace("Context", "")


# ── comodines de tipo: los parámetros sirven para TODO ───────────
def _is_numeric(t):
    return t in ("int", "parameter", "unknown")


def _is_bool(t):
    return t in ("bool", "parameter", "unknown")


def _is_color(t):
    return t in ("color", "parameter", "unknown")


_COLOR_LITERALS = {
    "rojo",
    "azul",
    "verde",
    "amarillo",
    "cyan",
    "magenta",
    "blanco",
    "negro",
    "marrón",
}

_BUILTINS = {"cos", "sin"}
_BOOL_LITERALS = {"true", "false"}


# ────────────────────────────────────────────────────────────────
#  TYPE-CHECKER
# ────────────────────────────────────────────────────────────────
class TypeChecker:
    """
    Verifica TODAS las reglas de tipo del lenguaje VGraph y además
    detecta: variables no declaradas y uso sin inicializar.
    Los parámetros de función («parameter») se aceptan como int/bool/color.
    """

    # ------------------------------------------------------------
    def __init__(self, symbol_table, error_reporter):
        self.symbol_table = symbol_table
        self.error_reporter = error_reporter

    # ------------------------------------------------------------
    @staticmethod
    def _pos(node):
        if hasattr(node, "symbol") and node.symbol:
            return node.symbol.line, node.symbol.column
        return get_node_line(node), get_node_column(node)

    # ------------------------------------------------------------
    #  INFERENCIA DE TIPO (sin errores)
    # ------------------------------------------------------------
    def get_type(self, node, parser):
        alt = _ctx_alt(node)

        # ─── terminal ───────────────────────────────────────────
        if node.getChildCount() == 0:
            txt = node.getText()

            if txt in _BOOL_LITERALS:
                return "bool"
            if txt in _COLOR_LITERALS:
                return "color"
            if txt.replace(".", "", 1).isdigit():
                return "int"

            # identificador
            if txt[0].islower() and txt.isalnum():
                info = self.symbol_table.lookup(txt)
                if info:
                    self.symbol_table.mark_used(txt)
                    return info.get("type", "unknown")
                return "unknown"

            return "unknown"

        # ─── no-terminal (por alt-label) ────────────────────────
        if alt in ("NumberExpr",):
            return "int"
        if alt in ("BoolConstExpr", "BoolLiteralExpr"):
            return "bool"
        if alt == "ColorExpr":
            return "color"
        if alt == "IdExpr":
            var = get_text(node.getChild(0))
            info = self.symbol_table.lookup(var)
            if info:
                self.symbol_table.mark_used(var)
                return info.get("type", "unknown")
            return "unknown"

        if alt in ("AddSubExpr", "MulDivExpr", "ModExpr", "NegExpr", "ParenExpr"):
            return "int"
        if alt in ("CosExpr", "SinExpr"):
            return "int"
        if alt == "FunctionCallExpr":
            return "int"
        if alt == "ComparisonExpr":
            return "bool"
        if alt in ("AndExpr", "OrExpr", "NotExpr", "ParenBoolExpr"):
            return "bool"
        # ------------------------------------------------------------------
        #  IDENTIFICADOR USADO EN EXPRESIÓN BOOL  ( !  &&  ||  )
        # ------------------------------------------------------------------
        if alt == "BoolIdExpr":                 #  <<––  NUEVO  ──┐
            var = get_text(node)                #                 │
            info = self.symbol_table.lookup(var)                # │
            if info:                                                # │
                self.symbol_table.mark_used(var)                    # │
                return info.get("type", "unknown")                  # │
            return "unknown"                                        # │
        # ------------------------------------------------------------------  ┘

        return "unknown"

    # ------------------------------------------------------------
    #  CHECK EXPRESSION  (recursivo)
    # ------------------------------------------------------------
    def check_expression(self, node, parser, expected_type=None):
        alt = _ctx_alt(node)

        # — verificación específica —
        if alt in ("AddSubExpr", "MulDivExpr", "ModExpr"):
            self._check_arithmetic(node, parser)
        elif alt == "ComparisonExpr":
            self._check_comparison(node, parser)
        elif alt in ("AndExpr", "OrExpr", "NotExpr"):
            self._check_logical(node, parser)
        elif alt in ("CosExpr", "SinExpr"):
            self._check_trig(node, parser)
        elif alt == "FunctionCallExpr":
            self.check_function_call(node.getChild(0), parser)

        # — tipo esperado —
        actual_type = self.get_type(node, parser)
        if (
            expected_type
            and actual_type != expected_type
            and "unknown" not in (actual_type, expected_type)
            and "parameter" not in (actual_type, expected_type)
        ):
            line, col = self._pos(node)
            self.error_reporter.report_error(
                line,
                col,
                f"Se esperaba tipo {expected_type} pero se obtuvo {actual_type}",
                len(node.getText()),
            )

        # — recorrer hijos —
        for i in range(node.getChildCount()):
            child = node.getChild(i)

            # no-terminal
            if child.getChildCount() > 0:
                self.check_expression(child, parser)
                continue

            # terminal: ¿identificador ?
            txt = child.getText()
            if (
                txt in _COLOR_LITERALS
                or txt in _BOOL_LITERALS
                or txt in _BUILTINS
                or txt.replace(".", "", 1).isdigit()
            ):
                continue

            if txt[0].islower() and txt.isalnum():
                info = self.symbol_table.lookup(txt)
                if not info:
                    line, col = self._pos(child)
                    self.error_reporter.report_error(
                        line, col, f"Variable no declarada: {txt}", len(txt)
                    )
                else:
                    self.symbol_table.mark_used(txt)
                    if (
                        not info.get("initialized", False)
                        and info.get("type") not in ("function", "parameter")
                    ):
                        line, col = self._pos(child)
                        self.error_reporter.report_error(
                            line,
                            col,
                            f"Variable '{txt}' utilizada sin inicializar",
                            len(txt),
                        )
        return actual_type

    # ------------------------------------------------------------
    #  SUB-VERIFICACIONES
    # ------------------------------------------------------------
    def _check_arithmetic(self, node, parser):
        l, _, r = node.getChild(0), node.getChild(1), node.getChild(2)
        if not _is_numeric(self.get_type(l, parser)):
            line, col = self._pos(l)
            self.error_reporter.report_error(
                line,
                col,
                "Las operaciones aritméticas sólo admiten operandos int",
                len(l.getText()),
            )
        if not _is_numeric(self.get_type(r, parser)):
            line, col = self._pos(r)
            self.error_reporter.report_error(
                line,
                col,
                "Las operaciones aritméticas sólo admiten operandos int",
                len(r.getText()),
            )

    def _check_comparison(self, node, parser):
        l, op_tok, r = node.getChild(0), node.getChild(1), node.getChild(2)
        lt, rt = self.get_type(l, parser), self.get_type(r, parser)
        op = op_tok.getText()

        if op in ("==", "!="):
            if (
                lt != rt
                and "unknown" not in (lt, rt)
                and "parameter" not in (lt, rt)
            ):
                line, col = self._pos(op_tok)
                self.error_reporter.report_error(
                    line,
                    col,
                    f"Comparación {op}: ambos operandos deben ser del mismo tipo "
                    f"(se encontró {lt} y {rt})",
                    len(op),
                )
        else:  # <, >, <=, >=
            for expr, typ in ((l, lt), (r, rt)):
                if not _is_numeric(typ):
                    line, col = self._pos(expr)
                    self.error_reporter.report_error(
                        line,
                        col,
                        f"Comparación {op} sólo admite operandos int",
                        len(expr.getText()),
                    )

    def _check_logical(self, node, parser):
        alt = _ctx_alt(node)
        if alt in ("AndExpr", "OrExpr"):
            l, r = node.getChild(0), node.getChild(2)
            for expr in (l, r):
                if not _is_bool(self.get_type(expr, parser)):
                    line, col = self._pos(expr)
                    self.error_reporter.report_error(
                        line,
                        col,
                        "Las operaciones lógicas sólo admiten operandos bool",
                        len(expr.getText()),
                    )
        else:  # NotExpr
            expr = node.getChild(1)
            if not _is_bool(self.get_type(expr, parser)):
                line, col = self._pos(expr)
                self.error_reporter.report_error(
                    line,
                    col,
                    "El operador ! sólo admite operandos bool",
                    len(expr.getText()),
                )

    def _check_trig(self, node, parser):
        arg = node.getChild(2)
        if not _is_numeric(self.get_type(arg, parser)):
            line, col = self._pos(arg)
            self.error_reporter.report_error(
                line,
                col,
                "Las funciones cos/sin sólo aceptan argumentos int",
                len(arg.getText()),
            )

    # ------------------------------------------------------------
    #  drawStatement
    # ------------------------------------------------------------
    def check_draw_statement(self, node, parser):
        draw_obj = node.getChild(1)
        for i in range(draw_obj.getChildCount()):
            ch = draw_obj.getChild(i)
            if get_rule_name(ch, parser) == "expr":
                if not _is_numeric(self.get_type(ch, parser)):
                    line, col = self._pos(ch)
                    self.error_reporter.report_error(
                        line,
                        col,
                        "Las coordenadas y dimensiones deben ser int",
                        len(ch.getText()),
                    )

    # ------------------------------------------------------------
    #  setcolor
    # ------------------------------------------------------------
    def check_setcolor_statement(self, node, parser):
        color_arg = node.getChild(2)
        txt = get_text(color_arg)

        # literal ✔
        if txt in _COLOR_LITERALS:
            return

        # variable simple
        if color_arg.getChildCount() == 0 and txt[0].islower() and txt.isalnum():
            info = self.symbol_table.lookup(txt)
            if not info:
                line, col = self._pos(color_arg)
                self.error_reporter.report_error(
                    line, col, f"Variable no declarada: {txt}", len(txt)
                )
                return

            self.symbol_table.mark_used(txt)

            if not info.get("initialized", False):
                line, col = self._pos(color_arg)
                self.error_reporter.report_error(
                    line,
                    col,
                    f"Variable '{txt}' utilizada sin inicializar",
                    len(txt),
                )

            if not _is_color(info.get("type", "unknown")):
                line, col = self._pos(color_arg)
                self.error_reporter.report_error(
                    line,
                    col,
                    f"setcolor requiere argumento color, pero {txt} es {info.get('type')}",
                    len(txt),
                )
            return

        # expresión compleja
        expr_type = self.check_expression(color_arg, parser)
        if not _is_color(expr_type):
            line, col = self._pos(color_arg)
            self.error_reporter.report_error(
                line,
                col,
                f"setcolor requiere argumento color, pero se encontró {expr_type}",
                len(color_arg.getText()),
            )

    # ------------------------------------------------------------
    #  ASSIGNMENT  (necesario para ASTVisitor)
    # ------------------------------------------------------------
    def check_assignment(self, node, parser):
        id_node = node.getChild(0)
        expr_node = node.getChild(2)
        var_name = get_text(id_node)

        info = (
            self.symbol_table.lookup(var_name, current_scope_only=True)
            or self.symbol_table.lookup(var_name)
        )

        if not info:
            line, col = self._pos(id_node)
            self.error_reporter.report_error(
                line, col, f"Variable no declarada: {var_name}", len(var_name)
            )
            return

        self.symbol_table.mark_used(
            var_name,
            current_scope=info.get("current_scope", self.symbol_table.current_scope_name()),
        )

        var_type = info.get("type", "unknown")
        expr_type = self.check_expression(expr_node, parser)

        self.symbol_table.mark_initialized(
            var_name,
            current_scope=info.get("current_scope", self.symbol_table.current_scope_name()),
        )

        if "parameter" in (var_type, expr_type):
            return

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
                len(node.getText()),
            )

    # ------------------------------------------------------------
    #  functionCall  (usada por ASTVisitor y check_expression)
    # ------------------------------------------------------------
    def check_function_call(self, node, parser):
        rule_name = get_rule_name(node, parser)
        func_name = ""
        arg_list_idx = -1

        if rule_name == "functionCall":
            func_name = get_text(node.getChild(0))
            arg_list_idx = 2 if node.getChildCount() > 3 else -1
        elif rule_name == "functionCallStatement":
            func_name = get_text(node.getChild(0))
            arg_list_idx = 2 if node.getChildCount() > 4 else -1
        else:
            return

        if not func_name:
            return

        info = self.symbol_table.lookup(func_name)
        if not info:
            line, col = self._pos(node)
            self.error_reporter.report_error(
                line, col, f"Función no declarada: {func_name}", len(func_name)
            )
            return

        self.symbol_table.mark_used(func_name)

        if info.get("type") not in ("function", "unknown"):
            line, col = self._pos(node)
            self.error_reporter.report_error(
                line, col, f"{func_name} no es una función", len(func_name)
            )
            return

        # número de argumentos
        arg_count = 0
        if arg_list_idx >= 0 and arg_list_idx < node.getChildCount():
            arg_list = node.getChild(arg_list_idx)
            if get_rule_name(arg_list, parser) == "argumentList":
                arg_count = (arg_list.getChildCount() + 1) // 2

        expected = len(self.symbol_table.functions.get(func_name, {}).get("params", []))
        if expected != arg_count:
            line, col = self._pos(node)
            self.error_reporter.report_error(
                line,
                col,
                f"La función '{func_name}' espera {expected} argumentos, pero se proporcionaron {arg_count}",
                len(node.getText()),
            )

    # ------------------------------------------------------------
    #  if / loop  (llamados por ASTVisitor)
    # ------------------------------------------------------------
    def check_if_statement(self, node, parser):
        cond = node.getChild(2)
        typ = self.check_expression(cond, parser)
        if typ not in ("bool", "unknown"):
            line, col = self._pos(cond)
            self.error_reporter.report_error(
                line,
                col,
                f"La condición del if debe ser bool, pero se encontró {typ}",
                len(cond.getText()),
            )

    def check_loop_statement(self, node, parser):
        cond = node.getChild(4)
        typ = self.check_expression(cond, parser)
        if typ not in ("bool", "unknown"):
            line, col = self._pos(cond)
            self.error_reporter.report_error(
                line,
                col,
                f"La condición del loop debe ser bool, pero se encontró {typ}",
                len(cond.getText()),
            )

        # init y update son assignmentExpression
        self.check_assignment(node.getChild(2), parser)
        self.check_assignment(node.getChild(6), parser)