class SymbolTable:
    """
    Gestiona la tabla de símbolos con soporte para ámbitos y renombramiento
    """
    def __init__(self, initial_table=None):
        """
        Inicializa la tabla de símbolos, opcionalmente con una tabla existente
        """
        # Cada ámbito es un diccionario con nombre y símbolos
        self.scopes = [{"name": "global", "symbols": {}}]
        # Para llevar un registro de las funciones declaradas
        self.functions = {}
        # Información de inicialización y uso de símbolos
        self.symbol_info = {}
        
        # Mapa de renombramientos para variables de funciones
        self.variable_renames = {}
        self.inverse_renames = {}  # Para mapear de renombrado a original
        
        # Inicialización desde una tabla existente si se proporciona
        if initial_table:
            self._initialize_from_table(initial_table)
    
    def _initialize_from_table(self, initial_table):
        """
        Inicializa la tabla de símbolos con soporte para renombramientos
        """
        print(f"=== DEBUG SymbolTable: _initialize_from_table called ===")
        
        # Guardar la tabla original
        self.initial_symbols = initial_table.copy()
        
        # Construir mapas de renombramiento
        for name, info in initial_table.items():
            if info.get('type') == 'parameter':
                original_name = info.get('name', name)
                if name != original_name:  # Es un parámetro renombrado
                    scope_name = info.get('scope', 'global')
                    if scope_name not in self.variable_renames:
                        self.variable_renames[scope_name] = {}
                    self.variable_renames[scope_name][original_name] = name
                    self.inverse_renames[name] = original_name
        
        # Continuar con la inicialización normal
        for name, info in initial_table.items():
            scope_name = info.get('scope', 'global')
            symbol_type = info.get('type', 'unknown')
            line = info.get('line', 1)
            
            # Determinar si es una inicialización
            is_initialized = info.get('type') in ['function', 'parameter']
            
            # Crear información del símbolo
            symbol_info = {
                'type': symbol_type,
                'line': line,
                'initialized': is_initialized,
                'used': False,
                'scope': scope_name,
                'original_name': info.get('name', name)
            }
            
            # Guardar información del símbolo
            if scope_name == 'global':
                self.symbol_info[name] = symbol_info
            else:
                # Para símbolos en ámbitos de función
                scope_key = f"{scope_name}_{name}"
                self.symbol_info[scope_key] = symbol_info
                # También mantener una referencia simple para búsquedas
                self.symbol_info[name] = symbol_info
            
            # Si es una función, registrarla
            if info.get('type') == 'function':
                self.functions[name] = {
                    'params': [],
                    'line': line,
                    'return_type': 'void'
                }
                
                # Buscar parámetros asociados
                for param_name, param_info in initial_table.items():
                    if param_info.get('scope') == name and param_info.get('type') == 'parameter':
                        self.functions[name]['params'].append({
                            'name': param_info.get('name', param_name),
                            'renamed': param_name if param_name != param_info.get('name', param_name) else None,
                            'type': 'int'
                        })
    
    def enter_scope(self, scope_name):
        """
        Entra en un nuevo ámbito
        """
        self.scopes.append({"name": scope_name, "symbols": {}})
    
    def exit_scope(self):
        """
        Sale del ámbito actual y retorna al anterior
        """
        if len(self.scopes) > 1:
            return self.scopes.pop()
        return None
    
    def current_scope_name(self):
        """
        Retorna el nombre del ámbito actual
        """
        return self.scopes[-1]["name"]
    
    def insert(self, name, symbol_info):
        """
        Inserta un símbolo en el ámbito actual
        """
        current_scope = self.scopes[-1]
        
        # Crear una copia completa de la información del símbolo
        full_symbol_info = symbol_info.copy()
        
        # Si el símbolo ya existe en la tabla inicial, usar su línea original
        if hasattr(self, 'initial_symbols') and name in self.initial_symbols:
            initial_info = self.initial_symbols[name]
            if 'line' in initial_info:
                full_symbol_info['line'] = initial_info['line']
            if 'scope' in initial_info:
                full_symbol_info['scope'] = initial_info['scope']
        
        # Si no tenemos una línea definida, usar 1 como fallback
        if 'line' not in full_symbol_info or full_symbol_info['line'] == 0:
            full_symbol_info['line'] = 1
        
        # Agregar al scope actual
        current_scope["symbols"][name] = full_symbol_info
        
        # Actualizar información global del símbolo
        scope_name = current_scope["name"]
        scope_key = f"{scope_name}_{name}" if scope_name != 'global' else name
        
        # Asegurarnos de que toda la información esté completa
        full_symbol_info['scope'] = scope_name
        
        self.symbol_info[scope_key] = full_symbol_info
        
        # También mantener una copia sin ámbito para compatibilidad si es global
        if scope_name == 'global':
            self.symbol_info[name] = full_symbol_info
    
    def lookup(self, name, current_scope_only=False):
        """
        Busca un símbolo considerando el renombramiento automático en funciones
        """
        current_scope = self.current_scope_name()
        
        # Si estamos en una función y el nombre podría ser un parámetro renombrado
        if current_scope != 'global' and current_scope in self.variable_renames:
            if name in self.variable_renames[current_scope]:
                # El nombre tiene un renombramiento, usamos la versión renombrada
                renamed_name = self.variable_renames[current_scope][name]
                # Buscar el símbolo renombrado
                result = self._lookup_symbol(renamed_name, current_scope_only)
                if result:
                    # Agregar información de renombramiento al resultado
                    result['original_name'] = name
                    result['renamed_from'] = renamed_name
                    return result
        
        # Búsqueda normal
        return self._lookup_symbol(name, current_scope_only)
    
    def _lookup_symbol(self, name, current_scope_only=False):
        """
        Búsqueda interna de símbolos (sin renombramiento)
        """
        # Buscar en los ámbitos creados durante el análisis semántico
        if current_scope_only:
            if name in self.scopes[-1]["symbols"]:
                return self.scopes[-1]["symbols"][name]
            return None
        
        # Buscar en todos los ámbitos actuales, del más interno al más externo
        for scope in reversed(self.scopes):
            if name in scope["symbols"]:
                result = scope["symbols"][name].copy()
                result["current_scope"] = scope["name"]
                return result
        
        # Si no se encuentra, buscar en la información inicial
        if hasattr(self, 'initial_symbols') and name in self.initial_symbols:
            info = self.initial_symbols[name]
            initial_scope = info.get('scope', 'global')
            current_scope = self.current_scope_name()
            
            # Determinar si la variable es accesible
            if (initial_scope == 'global' or 
                initial_scope == current_scope or
                current_scope == 'global'):
                result = {
                    'type': info.get('type', 'unknown'),
                    'line': info.get('line', 0),
                    'initialized': self.symbol_info.get(name, {}).get('initialized', False),
                    'used': self.symbol_info.get(name, {}).get('used', False),
                    'current_scope': initial_scope,
                    'original_name': info.get('name', name)
                }
                return result
        
        return None
    
    def is_declared_in_current_scope(self, name):
        """
        Verifica si un símbolo ya está declarado en el ámbito actual
        """
        return name in self.scopes[-1]["symbols"]
    
    def is_function_declared(self, name):
        """
        Verifica si una función ya está declarada
        """
        for scope in self.scopes:
            if name in scope["symbols"] and scope["symbols"][name].get("type") == "function":
                return True
        return False
    
    def mark_initialized(self, name, current_scope=None):
        """
        Marca un símbolo como inicializado considerando el renombramiento
        """
        if current_scope is None:
            current_scope = self.current_scope_name()
        
        # Si estamos en una función y el nombre podría ser un parámetro
        if current_scope != 'global' and current_scope in self.variable_renames:
            if name in self.variable_renames[current_scope]:
                # Marcar la versión renombrada como inicializada
                renamed_name = self.variable_renames[current_scope][name]
                return self._mark_symbol_initialized(renamed_name, current_scope)
        
        # Marcar el símbolo normal
        return self._mark_symbol_initialized(name, current_scope)
    
    def _mark_symbol_initialized(self, name, current_scope):
        """
        Marca un símbolo específico como inicializado (sin renombramiento)
        """
        # Buscar en el ámbito especificado primero
        if current_scope != "global":
            for scope in reversed(self.scopes):
                if scope["name"] == current_scope and name in scope["symbols"]:
                    scope["symbols"][name]["initialized"] = True
                    scope_key = f"{current_scope}_{name}"
                    if scope_key in self.symbol_info:
                        self.symbol_info[scope_key]["initialized"] = True
                    return True
        
        # Si no se encuentra en el ámbito especificado, buscar en todos los ámbitos
        for scope in reversed(self.scopes):
            if name in scope["symbols"]:
                scope["symbols"][name]["initialized"] = True
                if scope["name"] == "global":
                    scope_key = name
                else:
                    scope_key = f"{scope['name']}_{name}"
                if scope_key in self.symbol_info:
                    self.symbol_info[scope_key]["initialized"] = True
                return True
        
        return False
    
    def mark_used(self, name, current_scope=None):
        """
        Marca un símbolo como usado considerando el renombramiento
        """
        if current_scope is None:
            current_scope = self.current_scope_name()
        
        print(f"=== DEBUG: mark_used called with name='{name}', current_scope='{current_scope}' ===")
        
        # Si estamos en una función y el nombre podría ser un parámetro
        if current_scope != 'global' and current_scope in self.variable_renames:
            if name in self.variable_renames[current_scope]:
                # Marcar la versión renombrada como usada
                renamed_name = self.variable_renames[current_scope][name]
                print(f"=== DEBUG: Using renamed version '{renamed_name}' ===")
                return self._mark_symbol_used(renamed_name, current_scope)
        
        print(f"=== DEBUG: Using original name '{name}' ===")
        # Marcar el símbolo normal
        return self._mark_symbol_used(name, current_scope)
    
    def _mark_symbol_used(self, name, current_scope):
        """
        Marca un símbolo específico como usado (sin renombramiento)
        """
        print(f"=== DEBUG: _mark_symbol_used called with name='{name}', current_scope='{current_scope}' ===")
        
        # Buscar en los ámbitos actuales
        for scope in reversed(self.scopes):
            if name in scope["symbols"]:
                scope["symbols"][name]["used"] = True
                print(f"=== DEBUG: Marked '{name}' as used in scope '{scope['name']}' ===")
                
                # Actualizar información global
                if scope["name"] == "global":
                    scope_key = name
                else:
                    scope_key = name  # No agregar prefijo para mantener compatibilidad
                
                if scope_key in self.symbol_info:
                    self.symbol_info[scope_key]["used"] = True
                    print(f"=== DEBUG: Updated symbol_info for '{scope_key}' ===")
                return True
        
        # Si no se encuentra en ámbitos actuales, buscar en información global
        if name in self.symbol_info:
            self.symbol_info[name]["used"] = True
            print(f"=== DEBUG: Marked '{name}' as used in symbol_info ===")
            return True
        
        print(f"=== DEBUG: Symbol '{name}' not found in any scope ===")
        return False
    
    def get_unused_symbols(self):
        """
        Retorna una lista de símbolos declarados pero no usados
        """
        unused = []
        
        # Revisar símbolos en la información global
        for key, info in self.symbol_info.items():
            if not info.get("used", False):
                # Determinar el nombre real del símbolo
                original_name = info.get('original_name', key)
                scope_name = info.get('scope', 'global')
                
                # Si es un parámetro renombrado, usar el nombre original en el reporte
                if info.get('type') == 'parameter':
                    # Buscar en inverse_renames si existe la versión renombrada
                    if key in self.inverse_renames:
                        original_name = self.inverse_renames[key]
                
                # Solo agregar si no hay duplicado
                add_to_unused = True
                for existing in unused:
                    if (existing['name'] == original_name and 
                        existing['scope'] == scope_name and 
                        existing['line'] == info.get('line', 0)):
                        add_to_unused = False
                        break
                
                if add_to_unused:
                    unused.append({
                        "name": original_name,  # Usar nombre original, no renombrado
                        "type": info.get("type", "unknown"),
                        "scope": scope_name,
                        "line": info.get("line", 0)
                    })
        
        return unused
    
    def get_uninitialized_used_symbols(self):
        """
        Retorna una lista de símbolos usados pero no inicializados
        """
        uninitialized = []
        
        # Revisar símbolos en la información global
        for name, info in self.symbol_info.items():
            if info.get("used", False) and not info.get("initialized", False):
                # Las funciones y parámetros se consideran inicializados
                if info.get("type") not in ["function", "parameter"]:
                    # Obtener el ámbito del símbolo
                    scope_name = "global"
                    if hasattr(self, 'initial_symbols') and name in self.initial_symbols:
                        scope_name = self.initial_symbols[name].get("scope", "global")
                    
                    uninitialized.append({
                        "name": name,
                        "type": info.get("type", "unknown"),
                        "scope": scope_name,
                        "line": info.get("line", 0)
                    })
        
        return uninitialized
    
    def add_function_param(self, function_name, param_name, param_type="int"):
        """
        Agrega un parámetro a una función en la tabla de funciones
        """
        if function_name in self.functions:
            self.functions[function_name]["params"].append({
                "name": param_name,
                "type": param_type
            })
            return True
        return False
    
    def get_all_symbols(self):
        """
        Retorna todos los símbolos de la tabla, organizados por ámbito
        """
        result = {}
        
        # Incluir símbolos de ámbitos actuales
        for scope in self.scopes:
            scope_name = scope["name"]
            if scope_name not in result:
                result[scope_name] = {}
            
            for name, info in scope["symbols"].items():
                result[scope_name][name] = {
                    'type': info.get('type', 'unknown'),
                    'line': info.get('line', 1),
                    'initialized': info.get('initialized', False),
                    'used': info.get('used', False)
                }
        
        # Incluir símbolos de la información inicial que no se hayan incluido ya
        if hasattr(self, 'initial_symbols'):
            for name, info in self.initial_symbols.items():
                scope_name = info.get('scope', 'global')
                
                # Solo agregar si no existe ya un símbolo con el mismo nombre en ese ámbito
                if scope_name not in result:
                    result[scope_name] = {}
                    
                if name not in result[scope_name]:
                    # Buscar información actualizada del símbolo
                    scope_key = f"{scope_name}_{name}" if scope_name != 'global' else name
                    symbol_info = self.symbol_info.get(scope_key) or self.symbol_info.get(name)
                    
                    if symbol_info:
                        result[scope_name][name] = {
                            'type': symbol_info.get('type', 'unknown'),
                            'line': symbol_info.get('line', 1),
                            'initialized': symbol_info.get('initialized', False),
                            'used': symbol_info.get('used', False)
                        }
                    else:
                        result[scope_name][name] = {
                            'type': info.get('type', 'unknown'),
                            'line': info.get('line', 1),
                            'initialized': info.get('type') in ['function', 'parameter'],
                            'used': False
                        }
        
        # POST-PROCESAMIENTO: Eliminar duplicados dando prioridad a los parámetros
        if 'global' in result:
            global_symbols = result['global'].copy()
            for global_name, global_info in global_symbols.items():
                if global_info.get('type') not in ['function']:  # No filtrar funciones
                    # Buscar si existe como parámetro en alguna función
                    for scope_name, scope_symbols in result.items():
                        if scope_name != 'global':
                            for param_name, param_info in scope_symbols.items():
                                if (param_name == global_name and 
                                    param_info.get('type') == 'parameter' and
                                    param_info.get('line') == global_info.get('line')):
                                    # Es un duplicado - remover el global
                                    del result['global'][global_name]
                                    break
                            else:
                                continue
                            break
        
        return result