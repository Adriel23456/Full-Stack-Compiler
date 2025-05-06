# CompilerLogic/SemanticComponents/symbolTable.py
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
        # Solo guardar la información de la tabla inicial, sin insertar en los ámbitos
        # Esto evita que se detecten como redeclaraciones durante el análisis semántico
        self.initial_symbols = initial_table.copy()
        
        # Crear mapa de símbolos por ámbito para referencia
        for name, info in initial_table.items():
            scope_name = info.get('scope', 'global')
            symbol_info = {
                'type': info.get('type', 'unknown'),
                'line': info.get('line', 0),
                'initialized': False,
                'used': False,
            }
            
            # Guardar la información para su uso posterior
            self.symbol_info[name] = symbol_info
            
            # Si es una función, registrarla
            if info.get('type') == 'function':
                self.functions[name] = {
                    'params': [],
                    'line': info.get('line', 0),
                    'return_type': 'void'
                }
    
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
        current_scope["symbols"][name] = symbol_info
        # Actualizar información global del símbolo
        self.symbol_info[name] = symbol_info
    
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
        
        # Buscar en todos los ámbitos actuales
        for scope in reversed(self.scopes):
            if name in scope["symbols"]:
                return scope["symbols"][name]
        
        # Si no se encuentra, buscar en la información inicial
        if hasattr(self, 'initial_symbols') and name in self.initial_symbols:
            # Convertir la información de la tabla inicial al formato que esperamos
            info = self.initial_symbols[name]
            return {
                'type': info.get('type', 'unknown'),
                'line': info.get('line', 0),
                'initialized': False,
                'used': False
            }
        
        return None
    
    def is_declared_in_current_scope(self, name):
        """
        Verifica si un símbolo ya está declarado en el ámbito actual,
        sin incluir símbolos de la tabla inicial
        """
        return name in self.scopes[-1]["symbols"]
    
    def mark_initialized(self, name):
        """
        Marca un símbolo como inicializado
        """
        # Buscar el símbolo en todos los ámbitos
        for scope in reversed(self.scopes):
            if name in scope["symbols"]:
                scope["symbols"][name]["initialized"] = True
                if name in self.symbol_info:
                    self.symbol_info[name]["initialized"] = True
                return True
                
        # Si no está en los ámbitos actuales pero está en la información global
        if name in self.symbol_info:
            self.symbol_info[name]["initialized"] = True
            return True
            
        return False
    
    def mark_used(self, name):
        """
        Marca un símbolo como usado
        """
        # Buscar el símbolo en todos los ámbitos
        for scope in reversed(self.scopes):
            if name in scope["symbols"]:
                scope["symbols"][name]["used"] = True
                if name in self.symbol_info:
                    self.symbol_info[name]["used"] = True
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
        
        # Revisar símbolos en ámbitos actuales
        for scope in self.scopes:
            scope_name = scope["name"]
            for name, info in scope["symbols"].items():
                if not info.get("used", False):
                    unused.append({
                        "name": name,
                        "type": info.get("type", "unknown"),
                        "scope": scope_name,
                        "line": info.get("line", 0)
                    })
        
        # Revisar símbolos en la información global
        for name, info in self.symbol_info.items():
            if not info.get("used", False):
                # Evitar duplicados
                if not any(item["name"] == name for item in unused):
                    unused.append({
                        "name": name,
                        "type": info.get("type", "unknown"),
                        "scope": "global",  # Asumimos global por defecto
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
                    uninitialized.append({
                        "name": name,
                        "type": info.get("type", "unknown"),
                        "scope": "global",  # Por defecto
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
                result[scope_name][name] = info
        
        # Incluir símbolos de la información inicial que no se hayan incluido ya
        if hasattr(self, 'initial_symbols'):
            for name, info in self.initial_symbols.items():
                scope_name = info.get('scope', 'global')
                
                # Evitar duplicados
                if scope_name not in result:
                    result[scope_name] = {}
                    
                if name not in result[scope_name]:
                    # Convertir al formato de los símbolos actuales
                    result[scope_name][name] = {
                        'type': info.get('type', 'unknown'),
                        'line': info.get('line', 0),
                        'initialized': self.symbol_info.get(name, {}).get('initialized', False),
                        'used': self.symbol_info.get(name, {}).get('used', False)
                    }
        
        return result