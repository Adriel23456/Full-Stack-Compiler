# ─────────────────────────────────────────────────────────────────────
# File: CompilerLogic/SemanticComponents/symbolTable.py
# (versión completa con manejo **preciso** de línea y COLUMNA)
# ─────────────────────────────────────────────────────────────────────
class SymbolTable:
    """
    Gestiona la tabla de símbolos con soporte para ámbitos, renombramiento
    y almacenamiento exacto de (línea, columna) para un subrayado preciso.
    """

    # ------------------------------------------------------------------
    def __init__(self, initial_table=None):
        """
        Crea la tabla de símbolos.  
        `initial_table` es la tabla semilla que proviene del pre-análisis
        (parámetros, funciones integradas, etc.).
        """
        # Pila de ámbitos: cada elemento → {"name": str, "symbols": {…}}
        self.scopes = [{"name": "global", "symbols": {}}]

        # Registro de funciones:  {func_name: {"params":[…], "line":…, …}}
        self.functions = {}

        # Información “flat” de todos los símbolos (útil para reportes)
        self.symbol_info = {}

        # Mapas de renombramiento para parámetros/variables de funciones
        #   variable_renames  : {scope: {original → renamed}}
        #   inverse_renames   : {renamed → original}
        self.variable_renames = {}
        self.inverse_renames = {}

        # Línea actual del análisis (la actualiza ASTVisitor)
        self.current_analysis_line = 0

        # Inicializar con tabla externa (si existe)
        if initial_table:
            self._initialize_from_table(initial_table)

    # ------------------------------------------------------------------
    #  INICIALIZACIÓN DESDE TABLA EXTERNA
    # ------------------------------------------------------------------
    def _initialize_from_table(self, initial_table):
        """
        Copia `initial_table` dentro de la tabla de símbolos preservando
        **línea** y **columna** y construyendo los mapas de renombramiento.
        """
        # Guardar referencia para accesos posteriores
        self.initial_symbols = initial_table.copy()

        # 1) Construir mapas de renombramiento para parámetros
        for name, info in initial_table.items():
            if info.get("type") == "parameter":
                original_name = info.get("name", name)
                if name != original_name:  # parámetro renombrado
                    scope_name = info.get("scope", "global")
                    self.variable_renames.setdefault(scope_name, {})
                    self.variable_renames[scope_name][original_name] = name
                    self.inverse_renames[name] = original_name

        # 2) Cargar cada símbolo a `symbol_info`
        for name, info in initial_table.items():
            scope_name = info.get("scope", "global")
            symbol_type = info.get("type", "unknown")
            line = info.get("line", 1)
            column = info.get("column", 0)

            # Las funciones y parámetros se consideran inicializados
            is_initialized = symbol_type in ("function", "parameter")

            symbol_record = {
                "type": symbol_type,
                "line": line,
                "column": column,
                "initialized": is_initialized,
                "used": False,
                "scope": scope_name,
                "original_name": info.get("name", name),
            }

            # Clave de almacenamiento
            if scope_name == "global":
                key = name
            else:
                key = f"{scope_name}_{name}"
                # Copia extra sin prefijo (para búsquedas rápidas)
                self.symbol_info[name] = symbol_record

            self.symbol_info[key] = symbol_record

            # Registrar funciones
            if symbol_type == "function":
                self.functions[name] = {
                    "params": [],
                    "line": line,
                    "column": column,
                    "return_type": "void",
                }

        # 3) Vincular parámetros a sus funciones
        for param_name, param_info in initial_table.items():
            if param_info.get("type") == "parameter":
                func_scope = param_info.get("scope", "")
                if func_scope in self.functions:
                    self.functions[func_scope]["params"].append(
                        {
                            "name": param_info.get("name", param_name),
                            "renamed": (
                                param_name
                                if param_name != param_info.get("name", param_name)
                                else None
                            ),
                            "type": "int",
                            "line": param_info.get("line", 1),
                            "column": param_info.get("column", 0),
                        }
                    )

    # ------------------------------------------------------------------
    #  ÁMBITOS
    # ------------------------------------------------------------------
    def enter_scope(self, scope_name):
        """Ingresa a un nuevo ámbito (pila)."""
        self.scopes.append({"name": scope_name, "symbols": {}})

    def exit_scope(self):
        """Sale del ámbito actual y devuelve su contenido."""
        if len(self.scopes) > 1:
            return self.scopes.pop()
        return None

    def current_scope_name(self):
        """Nombre del ámbito actual."""
        return self.scopes[-1]["name"]

    # ------------------------------------------------------------------
    #  INSERCIÓN
    # ------------------------------------------------------------------
    def insert(self, name, symbol_info):
        """
        Inserta un símbolo en el ámbito actual preservando línea y columna.
        `symbol_info` **puede** traer 'line' y 'column'; si no, se usa 1/0.
        """
        current_scope = self.scopes[-1]
        scope_name = current_scope["name"]

        # Combinar información
        full_info = symbol_info.copy()
        full_info.setdefault("line", 1)
        full_info.setdefault("column", 0)
        full_info.setdefault("scope", scope_name)
        full_info.setdefault("initialized", False)
        full_info.setdefault("used", False)

        # Si ya se conocía en initial_symbols se respeta su (línea, columna)
        if hasattr(self, "initial_symbols") and name in self.initial_symbols:
            init = self.initial_symbols[name]
            full_info["line"] = init.get("line", full_info["line"])
            full_info["column"] = init.get("column", full_info["column"])
            full_info["scope"] = init.get("scope", full_info["scope"])

        # Almacenar en el ámbito y en `symbol_info`
        current_scope["symbols"][name] = full_info
        key = name if scope_name == "global" else f"{scope_name}_{name}"
        self.symbol_info[key] = full_info

        # Copia adicional sin prefijo cuando es global (compatibilidad)
        if scope_name == "global":
            self.symbol_info[name] = full_info

    # ------------------------------------------------------------------
    #  BÚSQUEDA
    # ------------------------------------------------------------------
    def lookup(self, name, current_scope_only=False):
        """
        Busca un símbolo respetando renombramiento automático de parámetros.
        No crea símbolos nuevos bajo ninguna circunstancia.
        """
        curr_scope = self.current_scope_name()

        # 1) Intentar resolución de renombramiento (parámetros)
        if curr_scope != "global" and curr_scope in self.variable_renames:
            if name in self.variable_renames[curr_scope]:
                renamed = self.variable_renames[curr_scope][name]
                result = self._lookup_symbol(renamed, current_scope_only)
                if result:
                    result = result.copy()
                    result["original_name"] = name
                    result["renamed_from"] = renamed
                    return result

        # 2) Búsqueda normal
        return self._lookup_symbol(name, current_scope_only)

    def _lookup_symbol(self, name, current_scope_only=False):
        """Implementación interna de búsqueda (sin renombramiento)."""
        # a) Ámbito actual (si se solicita explícito)
        if current_scope_only:
            sym = self.scopes[-1]["symbols"].get(name)
            if sym:
                return sym.copy()
            return None

        # b) En la pila de ámbitos, del más interno al externo
        for scope in reversed(self.scopes):
            if name in scope["symbols"]:
                res = scope["symbols"][name].copy()
                res["current_scope"] = scope["name"]
                return res

        # c) En símbolos iniciales (siempre que sea visible por línea)
        if hasattr(self, "initial_symbols") and name in self.initial_symbols:
            info = self.initial_symbols[name]
            if info:  # visibilidad por línea
                decl_line = info.get("line", 0)
                if self.current_analysis_line and decl_line > self.current_analysis_line:
                    return None  # declarada *después* del uso
                res = {
                    "type": info.get("type", "unknown"),
                    "line": decl_line,
                    "column": info.get("column", 0),
                    "initialized": self.symbol_info.get(name, {}).get(
                        "initialized", False
                    ),
                    "used": self.symbol_info.get(name, {}).get("used", False),
                    "current_scope": info.get("scope", "global"),
                    "original_name": info.get("name", name),
                }
                return res
        return None

    # ------------------------------------------------------------------
    #  CONTEXTO (línea/columna actuales)
    # ------------------------------------------------------------------
    def set_current_line(self, line):
        """Registra la línea del token que se está procesando."""
        self.current_analysis_line = line

    def _get_current_line(self):
        """Devuelve la línea de análisis actual (0 si desconocida)."""
        return getattr(self, "current_analysis_line", 0)

    # ------------------------------------------------------------------
    #  CONSULTAS RÁPIDAS
    # ------------------------------------------------------------------
    def is_declared_in_current_scope(self, name):
        return name in self.scopes[-1]["symbols"]

    def is_function_declared(self, name):
        for scope in self.scopes:
            if (
                name in scope["symbols"]
                and scope["symbols"][name].get("type") == "function"
            ):
                return True
        return False

    # ------------------------------------------------------------------
    #  MARCADO DE ESTADO  (initialized / used)
    # ------------------------------------------------------------------
    def mark_initialized(self, name, current_scope=None):
        if current_scope is None:
            current_scope = self.current_scope_name()

        # Renombramiento de parámetros
        if current_scope != "global" and current_scope in self.variable_renames:
            if name in self.variable_renames[current_scope]:
                renamed = self.variable_renames[current_scope][name]
                return self._mark_symbol_initialized(renamed, current_scope)
        return self._mark_symbol_initialized(name, current_scope)

    def _mark_symbol_initialized(self, name, current_scope):
        # 1) En el ámbito indicado
        if current_scope != "global":
            for scope in reversed(self.scopes):
                if scope["name"] == current_scope and name in scope["symbols"]:
                    scope["symbols"][name]["initialized"] = True
                    key = f"{current_scope}_{name}"
                    if key in self.symbol_info:
                        self.symbol_info[key]["initialized"] = True
                    return True

        # 2) En cualquier ámbito (fallback)
        for scope in reversed(self.scopes):
            if name in scope["symbols"]:
                scope["symbols"][name]["initialized"] = True
                key = name if scope["name"] == "global" else f"{scope['name']}_{name}"
                if key in self.symbol_info:
                    self.symbol_info[key]["initialized"] = True
                return True
        return False

    def mark_used(self, name, current_scope=None):
        if current_scope is None:
            current_scope = self.current_scope_name()

        if current_scope != "global" and current_scope in self.variable_renames:
            if name in self.variable_renames[current_scope]:
                renamed = self.variable_renames[current_scope][name]
                return self._mark_symbol_used(renamed, current_scope)
        return self._mark_symbol_used(name, current_scope)

    def _mark_symbol_used(self, name, current_scope):
        for scope in reversed(self.scopes):
            if name in scope["symbols"]:
                scope["symbols"][name]["used"] = True
                key = name if scope["name"] == "global" else name
                if key in self.symbol_info:
                    self.symbol_info[key]["used"] = True
                return True
        if name in self.symbol_info:
            self.symbol_info[name]["used"] = True
            return True
        return False

    # ------------------------------------------------------------------
    #  REPORTES
    # ------------------------------------------------------------------
    def get_unused_symbols(self):
        """
        Devuelve símbolos declarados pero nunca usados,
        con (línea, columna) exactas para subrayado.
        """
        unused = []
        for key, info in self.symbol_info.items():
            if not info.get("used", False):
                original = info.get("original_name", key)
                scope_name = info.get("scope", "global")

                # Evitar duplicados
                if not any(
                    u["name"] == original
                    and u["scope"] == scope_name
                    and u["line"] == info.get("line", 0)
                    for u in unused
                ):
                    unused.append(
                        {
                            "name": original,
                            "type": info.get("type", "unknown"),
                            "scope": scope_name,
                            "line": info.get("line", 0),
                            "column": info.get("column", 0),
                        }
                    )
        return unused

    def get_uninitialized_used_symbols(self):
        """
        Devuelve símbolos utilizados sin inicializar (línea/columna precisas).
        """
        uninit = []
        for name, info in self.symbol_info.items():
            if info.get("used") and not info.get("initialized"):
                if info.get("type") not in ("function", "parameter"):
                    scope_name = info.get("scope", "global")
                    uninit.append(
                        {
                            "name": name,
                            "type": info.get("type", "unknown"),
                            "scope": scope_name,
                            "line": info.get("line", 0),
                            "column": info.get("column", 0),
                        }
                    )
        return uninit

    # ------------------------------------------------------------------
    #  UTILIDADES PARA FUNCIONES
    # ------------------------------------------------------------------
    def add_function_param(self, function_name, param_name, param_type="int"):
        """
        Añade un parámetro a `functions[function_name]['params']`.
        """
        if function_name in self.functions:
            self.functions[function_name]["params"].append(
                {"name": param_name, "type": param_type}
            )
            return True
        return False

    # ------------------------------------------------------------------
    #  DEBUG / EXPORTACIÓN
    # ------------------------------------------------------------------
    def get_all_symbols(self):
        """
        Devuelve todos los símbolos agrupados por ámbito, con línea y columna.
        """
        result = {}
        # 1) Ámbitos creados durante el análisis
        for scope in self.scopes:
            sn = scope["name"]
            result.setdefault(sn, {})
            for n, inf in scope["symbols"].items():
                result[sn][n] = {
                    "type": inf.get("type", "unknown"),
                    "line": inf.get("line", 1),
                    "column": inf.get("column", 0),
                    "initialized": inf.get("initialized", False),
                    "used": inf.get("used", False),
                }

        # 2) Símbolos de la tabla inicial que no estén ya incluidos
        if hasattr(self, "initial_symbols"):
            for n, inf in self.initial_symbols.items():
                sn = inf.get("scope", "global")
                result.setdefault(sn, {})
                if n not in result[sn]:
                    # Preferir información actualizada
                    key = n if sn == "global" else f"{sn}_{n}"
                    stored = self.symbol_info.get(key, {})
                    result[sn][n] = {
                        "type": stored.get("type", inf.get("type", "unknown")),
                        "line": stored.get("line", inf.get("line", 1)),
                        "column": stored.get("column", inf.get("column", 0)),
                        "initialized": stored.get(
                            "initialized",
                            inf.get("type") in ("function", "parameter"),
                        ),
                        "used": stored.get("used", False),
                    }

        # 3) Eliminar duplicados preferenciando parámetros sobre globales
        if "global" in result:
            globals_copy = result["global"].copy()
            for g_name, g_info in globals_copy.items():
                for sn, sym_dict in result.items():
                    if sn != "global" and g_name in sym_dict:
                        if sym_dict[g_name]["type"] == "parameter":
                            del result["global"][g_name]
                            break
        return result