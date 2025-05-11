class SymbolTable:
    """
    Gestiona la tabla de símbolos con soporte para ámbitos
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
        
        # Inicialización desde una tabla existente si se proporciona
        if initial_table:
            self._initialize_from_table(initial_table)
    
    def _initialize_from_table(self, initial_table):
        """
        Inicializa la tabla de símbolos a partir de una tabla existente del análisis sintáctico
        """
        # Guardar la tabla original para referencia y evitar duplicados
        self.initial_symbols = initial_table.copy()
        
        # Primero, identificar todos los parámetros
        parameter_names_by_scope = {}
        for name, info in initial_table.items():
            if info.get('type') == 'parameter':
                scope_name = info.get('scope', 'global')
                if scope_name not in parameter_names_by_scope:
                    parameter_names_by_scope[scope_name] = set()
                parameter_names_by_scope[scope_name].add(name)
        
        # Inicializar información de símbolos con ámbitos correctos
        for name, info in initial_table.items():
            scope_name = info.get('scope', 'global')
            symbol_type = info.get('type', 'unknown')
            
            # SKIP si es una variable global que ya existe como parámetro
            if scope_name == 'global' and symbol_type != 'function':
                # Verificar si este nombre ya existe como parámetro en alguna función
                is_parameter_elsewhere = False
                for func_scope, params in parameter_names_by_scope.items():
                    if func_scope != 'global' and name in params:
                        # Verificar que sea la misma línea (es duplicado)
                        if info.get('line') == initial_table.get(name, {}).get('line'):
                            is_parameter_elsewhere = True
                            break
                
                if is_parameter_elsewhere:
                    print(f"DEBUG: Skipping duplicate global variable '{name}' - already exists as parameter")
                    continue
            
            # Obtener la línea, asegurándose de que existe
            line = info.get('line', 1)
            
            # Decidir si es una inicialización o uso
            is_initialized = info.get('type') in ['function', 'parameter']
            
            # Crear una clave única para cada símbolo en su ámbito
            scope_key = f"{scope_name}_{name}" if scope_name != 'global' else name
            
            symbol_info = {
                'type': symbol_type,
                'line': line,
                'initialized': is_initialized,
                'used': False,
                'scope': scope_name
            }
            
            # Guardar información del símbolo con su clave única
            self.symbol_info[scope_key] = symbol_info
            
            # También mantener una copia sin ámbito para compatibilidad
            if scope_name == 'global':
                self.symbol_info[name] = symbol_info
            
            # Si es una función, registrarla en la tabla de funciones
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
                            'name': param_name,
                            'type': 'int'  # Asumimos int por defecto
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
        
        # IMPORTANTE: Si el símbolo ya existe en la tabla inicial del análisis sintáctico,
        # usar su línea original para preservar la información correcta
        if hasattr(self, 'initial_symbols') and name in self.initial_symbols:
            initial_info = self.initial_symbols[name]
            # Conservar la línea del análisis sintáctico
            if 'line' in initial_info:
                full_symbol_info['line'] = initial_info['line']
            # También conservar el scope del análisis sintáctico
            if 'scope' in initial_info:
                full_symbol_info['scope'] = initial_info['scope']
        
        # Si no tenemos una línea definida, usar 1 como fallback en lugar de 0
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
        Busca un símbolo en todos los ámbitos, del más interno al más externo.
        Si current_scope_only es True, solo busca en el ámbito actual.
        """
        # Primero buscar en los ámbitos creados durante el análisis semántico
        if current_scope_only:
            # Buscar solo en el ámbito actual
            if name in self.scopes[-1]["symbols"]:
                return self.scopes[-1]["symbols"][name]
            return None
        
        # Buscar en todos los ámbitos actuales, del más interno al más externo
        for scope in reversed(self.scopes):
            if name in scope["symbols"]:
                result = scope["symbols"][name].copy()
                result["current_scope"] = scope["name"]  # Agregar información del ámbito
                return result
        
        # Si no se encuentra en los ámbitos actuales, buscar en la información inicial
        if hasattr(self, 'initial_symbols') and name in self.initial_symbols:
            info = self.initial_symbols[name]
            # Determinar si la variable es accesible desde el ámbito actual
            initial_scope = info.get('scope', 'global')
            current_scope = self.current_scope_name()
            
            # Si estamos en una función y la variable es de ámbito global, es accesible
            # Si estamos en el mismo ámbito que la variable, es accesible
            if (initial_scope == 'global' or 
                initial_scope == current_scope or
                current_scope == 'global'):
                result = {
                    'type': info.get('type', 'unknown'),
                    'line': info.get('line', 0),
                    'initialized': self.symbol_info.get(name, {}).get('initialized', False),
                    'used': self.symbol_info.get(name, {}).get('used', False),
                    'current_scope': initial_scope
                }
                return result
        
        return None
    
    def is_declared_in_current_scope(self, name):
        """
        Verifica si un símbolo ya está declarado en el ámbito actual,
        sin incluir símbolos de la tabla inicial
        """
        return name in self.scopes[-1]["symbols"]
    
    def is_function_declared(self, name):
        """
        Verifica si una función ya está declarada en la tabla actual
        (sin considerar la tabla inicial)
        """
        # Solo verificar en los ámbitos actuales, no en la tabla inicial
        for scope in self.scopes:
            if name in scope["symbols"] and scope["symbols"][name].get("type") == "function":
                return True
        return False
    
    def mark_initialized(self, name):
        """
        Marca un símbolo como inicializado en el ámbito correcto
        """
        # Buscar el símbolo en todos los ámbitos, del más interno al más externo
        for scope in reversed(self.scopes):
            if name in scope["symbols"]:
                scope["symbols"][name]["initialized"] = True
                # Actualizar la información global del símbolo
                scope_key = f"{scope['name']}_{name}"
                if scope_key not in self.symbol_info:
                    scope_key = name  # Fallback para ámbito global
                if scope_key in self.symbol_info:
                    self.symbol_info[scope_key]["initialized"] = True
                return True
        
        # Si no está en los ámbitos actuales pero está en la información global
        if name in self.symbol_info:
            self.symbol_info[name]["initialized"] = True
            return True
            
        return False
    
    def mark_used(self, name):
        """
        Marca un símbolo como usado en el ámbito correcto
        """
        # Buscar el símbolo en todos los ámbitos, del más interno al más externo
        for scope in reversed(self.scopes):
            if name in scope["symbols"]:
                scope["symbols"][name]["used"] = True
                # Actualizar la información global del símbolo
                scope_key = f"{scope['name']}_{name}"
                if scope_key not in self.symbol_info:
                    scope_key = name  # Fallback para ámbito global
                if scope_key in self.symbol_info:
                    self.symbol_info[scope_key]["used"] = True
                return True
        
        # Si no está en los ámbitos actuales pero está en la información global
        if name in self.symbol_info:
            self.symbol_info[name]["used"] = True
            return True
            
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
                if '_' in key and key.count('_') == 1:
                    scope_name, name = key.rsplit('_', 1)
                else:
                    scope_name = 'global'
                    name = key
                
                # Solo agregar si es un símbolo global o si no hay duplicado global
                if scope_name == 'global' or name not in self.symbol_info:
                    unused.append({
                        "name": name,
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
        # Buscar variables globales que tienen el mismo nombre y línea que parámetros
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
                                    print(f"DEBUG: Removing duplicate global variable '{global_name}' in favor of parameter")
                                    del result['global'][global_name]
                                    break
                            else:
                                continue
                            break
        
        return result
    
    def mark_initialized(self, name, current_scope=None):
        """
        Marca un símbolo como inicializado en el ámbito especificado
        """
        if current_scope is None:
            current_scope = self.current_scope_name()
        
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
        Marca un símbolo como usado en el ámbito especificado
        """
        if current_scope is None:
            current_scope = self.current_scope_name()
        
        # Buscar en el ámbito especificado primero
        if current_scope != "global":
            for scope in reversed(self.scopes):
                if scope["name"] == current_scope and name in scope["symbols"]:
                    scope["symbols"][name]["used"] = True
                    scope_key = f"{current_scope}_{name}"
                    if scope_key in self.symbol_info:
                        self.symbol_info[scope_key]["used"] = True
                    return True
        
        # Si no se encuentra en el ámbito especificado, buscar en todos los ámbitos
        for scope in reversed(self.scopes):
            if name in scope["symbols"]:
                scope["symbols"][name]["used"] = True
                if scope["name"] == "global":
                    scope_key = name
                else:
                    scope_key = f"{scope['name']}_{name}"
                if scope_key in self.symbol_info:
                    self.symbol_info[scope_key]["used"] = True
                return True
        
        return False