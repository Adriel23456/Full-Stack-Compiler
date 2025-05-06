# CompilerLogic/SemanticComponents/errorReporter.py
class ErrorReporter:
    """
    Recopila y reporta errores semánticos
    """
    def __init__(self):
        self.errors = []
    
    def report_error(self, line, column, message, length=1):
        """
        Reporta un error semántico
        
        Args:
            line: Línea donde ocurrió el error
            column: Columna donde ocurrió el error
            message: Mensaje descriptivo del error
            length: Longitud del texto con error (para resaltado)
        """
        # Normalizar línea y columna (para evitar valores negativos)
        line = max(1, line)
        column = max(0, column)
        
        error = {
            'message': f"Error semántico: {message}",
            'line': line,
            'column': column,
            'length': length
        }
        
        # Evitar duplicados
        if error not in self.errors:
            self.errors.append(error)
    
    def report_warning(self, line, column, message, length=1):
        """
        Reporta una advertencia semántica
        
        Args:
            line: Línea donde ocurrió la advertencia
            column: Columna donde ocurrió la advertencia
            message: Mensaje descriptivo de la advertencia
            length: Longitud del texto con advertencia (para resaltado)
        """
        # Normalizar línea y columna (para evitar valores negativos)
        line = max(1, line)
        column = max(0, column)
        
        warning = {
            'message': f"Advertencia semántica: {message}",
            'line': line,
            'column': column,
            'length': length,
            'is_warning': True
        }
        
        # Evitar duplicados
        if warning not in self.errors:
            self.errors.append(warning)
    
    def has_errors(self):
        """
        Indica si hay errores (no incluye advertencias)
        """
        return any(not error.get('is_warning', False) for error in self.errors)
    
    def get_errors(self):
        """
        Retorna todos los errores y advertencias
        """
        return self.errors
    
    def get_error_count(self):
        """
        Retorna el número de errores (no incluye advertencias)
        """
        return sum(1 for error in self.errors if not error.get('is_warning', False))
    
    def get_warning_count(self):
        """
        Retorna el número de advertencias
        """
        return sum(1 for error in self.errors if error.get('is_warning', False))
    
    def clear(self):
        """
        Limpia todos los errores y advertencias
        """
        self.errors = []