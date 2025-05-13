# ────────────────────────────────────────────────────────────────
# File: CompilerLogic/SemanticComponents/scopeChecker.py
# ────────────────────────────────────────────────────────────────
from CompilerLogic.SemanticComponents.astUtil import (
    get_node_line,
    get_node_column,
    get_text,
    get_rule_name,
)


class ScopeChecker:
    """
    Verifica reglas de ámbito; todas las posiciones enviadas al
    ErrorReporter se obtienen con `_pos(node)` para precisión.
    """

    # ------------------------------------------------------------------
    def __init__(self, symbol_table, error_reporter):
        self.symbol_table = symbol_table
        self.error_reporter = error_reporter
        self.in_function = False
        self.current_function = None

    # ------------------------------------------------------------------
    @staticmethod
    def _pos(node):
        if hasattr(node, "symbol") and node.symbol:
            return node.symbol.line, node.symbol.column
        return get_node_line(node), get_node_column(node)

    # ------------------------------------------------------------------
    def enter_function(self, function_name):
        self.in_function = True
        self.current_function = function_name

    def exit_function(self):
        self.in_function = False
        self.current_function = None

    # ------------------------------------------------------------------
    def check_variable_declaration(self, node, parser):
        current_scope = self.symbol_table.current_scope_name()
        if current_scope == "frame":
            line, col = self._pos(node)
            self.error_reporter.report_error(
                line,
                col,
                "Error: NO SE PUEDEN DECLARAR VARIABLES DENTRO DE FRAME",
                len(get_text(node)),
            )
            return

        type_node = node.getChild(0)
        var_type = type_node.getChild(1).getText()

        # DECLARACIÓN SIMPLE -----------------------------------------
        if get_rule_name(node.getChild(1), parser) is None:
            tok = node.getChild(1)
            line, col = self._pos(tok)
            var_name = get_text(tok)

            if self.symbol_table.is_declared_in_current_scope(var_name):
                self.error_reporter.report_error(
                    line,
                    col,
                    f"Variable {var_name} ya declarada en este ámbito",
                    len(var_name),
                )
                return

            if not self._check_identifier_rules(var_name, tok):
                return

            self.symbol_table.insert(
                var_name,
                {
                    "type": var_type,
                    "line": line,
                    "initialized": False,
                    "used": False,
                },
            )

            if node.getChildCount() > 3:
                self.symbol_table.mark_initialized(var_name)

        # DECLARACIÓN CON idList -------------------------------------
        elif get_rule_name(node.getChild(1), parser) == "idList":
            id_list = node.getChild(1)
            for i in range(0, id_list.getChildCount(), 2):
                tok = id_list.getChild(i)
                var_name = get_text(tok)
                line_curr, col_curr = self._pos(tok)

                if self.symbol_table.is_declared_in_current_scope(var_name):
                    self.error_reporter.report_error(
                        line_curr,
                        col_curr,
                        f"Variable {var_name} ya declarada en este ámbito",
                        len(var_name),
                    )
                    continue

                line_store = (
                    self.symbol_table.initial_symbols[var_name]["line"]
                    if hasattr(self.symbol_table, "initial_symbols")
                    and var_name in self.symbol_table.initial_symbols
                    else line_curr
                )

                if not self._check_identifier_rules(var_name, tok):
                    continue

                self.symbol_table.insert(
                    var_name,
                    {
                        "type": var_type,
                        "line": line_store,
                        "initialized": False,
                        "used": False,
                        "scope": self.symbol_table.current_scope_name(),
                    },
                )

    # ------------------------------------------------------------------
    def check_function_declaration(self, node, parser):
        tok = node.getChild(1)
        func_name = get_text(tok)
        line_tok, col_tok = self._pos(tok)

        if self.symbol_table.is_function_declared(func_name):
            self.error_reporter.report_error(
                line_tok,
                col_tok,
                f"Función {func_name} ya declarada",
                len(func_name),
            )
            return

        if not self._check_identifier_rules(func_name, tok):
            return

        if self.symbol_table.current_scope_name() != "global":
            self.error_reporter.report_error(
                line_tok,
                col_tok,
                "Las funciones solo pueden declararse en el ámbito global",
                len(func_name),
            )
            return

        self.symbol_table.insert(
            func_name,
            {
                "type": "function",
                "line": line_tok,
                "initialized": True,
                "used": False,
            },
        )

        self.symbol_table.functions[func_name] = {
            "params": [],
            "line": line_tok,
            "return_type": "void",
        }

        if node.getChildCount() > 5:
            param_list = node.getChild(3)
            for i in range(0, param_list.getChildCount(), 2):
                param_name = get_text(param_list.getChild(i))
                self.symbol_table.add_function_param(func_name, param_name)

    # ------------------------------------------------------------------
    def check_return_statement(self, node, parser):
        if not self.in_function:
            line, col = self._pos(node)
            self.error_reporter.report_error(
                line,
                col,
                "La sentencia return solo puede aparecer dentro de funciones",
                6,
            )

    # ------------------------------------------------------------------
    def _check_identifier_rules(self, identifier, node):
        line, col = self._pos(node)

        if not identifier[0].islower():
            self.error_reporter.report_error(
                line,
                col,
                "Los identificadores deben comenzar con minúscula",
                len(identifier),
            )
            return False

        if not identifier.isalnum():
            self.error_reporter.report_error(
                line,
                col,
                "Los identificadores deben ser alfanuméricos",
                len(identifier),
            )
            return False

        if len(identifier) > 15:
            self.error_reporter.report_error(
                line,
                col,
                "Los identificadores deben tener 15 caracteres o menos",
                len(identifier),
            )
            return False

        return True