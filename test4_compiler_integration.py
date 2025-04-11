"""
Implementación del compilador optimizada para Windows.
Este compilador genera un archivo objeto directamente, evitando problemas con la sintaxis del ensamblador.
"""

import sys
import ply.lex as lex
import ply.yacc as yacc
from test3_llvm_code_gen import LLVMCodeGenerator, compile_to_executable

# -------------------------- ANALIZADOR LÉXICO --------------------------

# Lista de tokens
tokens = (
    'ID',
    'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN',
    'EQUALS',
    'SEMICOLON',
    'LBRACE', 'RBRACE',
    'LT', 'GT', 'LE', 'GE', 'EQ', 'NE',
)

# Palabras reservadas
reserved = {
    'if': 'IF',
    'elif': 'ELIF',
    'else': 'ELSE',
    'for': 'FOR',
    'in': 'IN',
    'range': 'RANGE',
    'print': 'PRINT',
}

# Agregar palabras reservadas a la lista de tokens
tokens = tokens + tuple(reserved.values())

# Reglas para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_SEMICOLON = r';'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

# Ignorar espacios en blanco y tabulaciones
t_ignore = ' \t'

# Identificar números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Identificar identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Seguimiento de números de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores léxicos
def t_error(t):
    print(f"Error léxico: Carácter ilegal '{t.value[0]}' en línea {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# -------------------------- ANALIZADOR SINTÁCTICO --------------------------

# Reglas de precedencia para operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'LT', 'GT', 'LE', 'GE', 'EQ', 'NE'),  # Operadores relacionales
)

# Regla inicial: programa
def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])

# Lista de declaraciones
def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

# Tipos de declaraciones
def p_statement(p):
    '''statement : assignment
                 | if_statement
                 | for_statement
                 | print_statement'''
    p[0] = p[1]

# Asignación de variable
def p_assignment(p):
    '''assignment : ID EQUALS expression SEMICOLON'''
    # Solo construir el AST, sin análisis semántico
    p[0] = ('assign', p[1], p[3], p.lineno(1))  # Guardar número de línea para análisis semántico

# Declaración print
def p_print_statement(p):
    '''print_statement : PRINT LPAREN expression RPAREN SEMICOLON'''
    p[0] = ('print', p[3], p.lineno(1))

# Expresiones aritméticas
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = ('binop', p[2], p[1], p[3], p.lineno(2))

# Paréntesis en expresiones
def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

# Expresión de número
def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = ('number', p[1], p.lineno(1))

# Expresión de variable
def p_expression_id(p):
    '''expression : ID'''
    # Solo construir el AST, sin análisis semántico
    p[0] = ('id', p[1], p.lineno(1))

# Expresiones relacionales
def p_expression_relop(p):
    '''expression : expression LT expression
                  | expression GT expression
                  | expression LE expression
                  | expression GE expression
                  | expression EQ expression
                  | expression NE expression'''
    p[0] = ('relop', p[2], p[1], p[3], p.lineno(2))

# Estructura if-elif-else
def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE
                    | IF LPAREN expression RPAREN LBRACE statement_list RBRACE ELIF LPAREN expression RPAREN LBRACE statement_list RBRACE
                    | IF LPAREN expression RPAREN LBRACE statement_list RBRACE ELIF LPAREN expression RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE
                    | IF LPAREN expression RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE'''
    if len(p) == 8:  # solo if
        p[0] = ('if', p[3], p[6], None, None, p.lineno(1))
    elif len(p) == 15:  # if-elif
        p[0] = ('if', p[3], p[6], ('elif', p[10], p[13], p.lineno(8)), None, p.lineno(1))
    elif len(p) == 19:  # if-elif-else
        p[0] = ('if', p[3], p[6], ('elif', p[10], p[13], p.lineno(8)), p[17], p.lineno(1))
    elif len(p) == 12:  # if-else
        p[0] = ('if', p[3], p[6], None, p[10], p.lineno(1))

# Bucle for con range
def p_for_statement(p):
    '''for_statement : FOR LPAREN ID IN RANGE LPAREN expression RPAREN RPAREN LBRACE statement_list RBRACE'''
    # Solo construir el AST, sin análisis semántico
    p[0] = ('for', p[3], p[7], p[11], p.lineno(1))

# Manejo de errores sintácticos
def p_error(p):
    if p:
        print(f"Error sintáctico: Token inesperado '{p.value}' en línea {p.lineno}")
    else:
        print("Error sintáctico: Fin de archivo inesperado")

# Construir el parser
parser = yacc.yacc()

# -------------------------- ANALIZADOR SEMÁNTICO --------------------------

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.errors = []
        
    def analyze(self, ast):
        """Realiza el análisis semántico completo del AST"""
        if not ast:
            return False
            
        # Primera pasada: declaraciones (recolectar todas las variables)
        self._collect_declarations(ast)
        
        # Segunda pasada: verificación de tipos y referencias
        self._check_references(ast)
        
        # Reportar errores
        if self.errors:
            for error in self.errors:
                print(error)
            return False
        
        return True
    
    def _collect_declarations(self, node):
        """Primera pasada: recolecta todas las declaraciones de variables"""
        if node is None:
            return
            
        if isinstance(node, tuple):
            if node[0] == 'program':
                for stmt in node[1]:
                    self._collect_declarations(stmt)
                    
            elif node[0] == 'assign':
                # Registrar variable en asignación
                var_name = node[1]
                self.symbol_table[var_name] = {
                    'declared': True,
                    'initialized': True,
                    'line': node[3]  # Línea donde se declaró
                }
                
            elif node[0] == 'for':
                # Registrar variable de iteración
                var_name = node[1]
                self.symbol_table[var_name] = {
                    'declared': True,
                    'initialized': True,
                    'line': node[4]  # Línea donde se declaró
                }
                # Analizar cuerpo del bucle
                for stmt in node[3]:
                    self._collect_declarations(stmt)
                    
            elif node[0] == 'if':
                # Analizar bloque if
                for stmt in node[2]:
                    self._collect_declarations(stmt)
                
                # Analizar bloque elif si existe
                if node[3]:
                    for stmt in node[3][2]:
                        self._collect_declarations(stmt)
                
                # Analizar bloque else si existe
                if node[4]:
                    for stmt in node[4]:
                        self._collect_declarations(stmt)
        
        elif isinstance(node, list):
            for item in node:
                self._collect_declarations(item)
    
    def _check_references(self, node):
        """Segunda pasada: verifica referencias a variables y otros errores semánticos"""
        if node is None:
            return
            
        if isinstance(node, tuple):
            if node[0] == 'program':
                for stmt in node[1]:
                    self._check_references(stmt)
                    
            elif node[0] == 'id':
                # Verificar uso de variable
                var_name = node[1]
                if var_name not in self.symbol_table:
                    self.errors.append(f"Error semántico: Variable '{var_name}' no definida en línea {node[2]}")
                    
            elif node[0] == 'binop':
                # Verificar operandos
                self._check_references(node[2])
                self._check_references(node[3])
                
                # Verificación adicional para división por cero si es posible
                if node[1] == '/' and isinstance(node[3], tuple) and node[3][0] == 'number' and node[3][1] == 0:
                    self.errors.append(f"Error semántico: División por cero en línea {node[4]}")
                    
            elif node[0] == 'relop':
                # Verificar operandos de comparación
                self._check_references(node[2])
                self._check_references(node[3])
                
            elif node[0] == 'assign':
                # Verificar expresión de la derecha
                self._check_references(node[2])
                
            elif node[0] == 'print':
                # Verificar expresión a imprimir
                self._check_references(node[1])
                
            elif node[0] == 'if':
                # Verificar condición if
                self._check_references(node[1])
                
                # Verificar bloque if
                for stmt in node[2]:
                    self._check_references(stmt)
                
                # Verificar bloque elif si existe
                if node[3]:
                    self._check_references(node[3][1])  # Condición elif
                    for stmt in node[3][2]:
                        self._check_references(stmt)
                
                # Verificar bloque else si existe
                if node[4]:
                    for stmt in node[4]:
                        self._check_references(stmt)
                        
            elif node[0] == 'for':
                # Verificar expresión de rango
                self._check_references(node[2])
                
                # Verificar que el rango sea un número entero positivo (si es constante)
                if isinstance(node[2], tuple) and node[2][0] == 'number' and node[2][1] < 0:
                    self.errors.append(f"Error semántico: El valor del rango debe ser no negativo en línea {node[4]}")
                
                # Verificar cuerpo del bucle
                for stmt in node[3]:
                    self._check_references(stmt)
                    
        elif isinstance(node, list):
            for item in node:
                self._check_references(item)

# -------------------------- COMPILADOR PRINCIPAL --------------------------

def compile_file(source_file, output_file):
    """
    Compila un archivo fuente y genera un ejecutable directamente.
    
    Args:
        source_file: Archivo fuente a compilar
        output_file: Archivo ejecutable de salida
    
    Returns:
        bool: True si la compilación fue exitosa, False en caso contrario
    """
    try:
        # Leer archivo fuente
        with open(source_file, 'r') as f:
            source_code = f.read()
            
        # Fase 1: Análisis sintáctico
        lexer.input(source_code)
        ast = parser.parse(source_code, lexer=lexer)
        
        if not ast:
            print("Error: No se pudo construir el AST")
            return False
            
        # Fase 2: Análisis semántico
        semantic_analyzer = SemanticAnalyzer()
        if not semantic_analyzer.analyze(ast):
            print("Error: El análisis semántico ha fallado")
            return False
            
        # Fase 3: Generación de código y compilación a ejecutable
        success = compile_to_executable(ast, output_file, source_file)
        
        if success:
            print(f"Compilación exitosa. Ejecutable generado: {output_file}")
            return True
        else:
            print("Error durante la compilación a ejecutable")
            return False
            
    except Exception as e:
        print(f"Error en la compilación: {str(e)}")
        return False
        
def main():
    """Función principal del compilador"""
    if len(sys.argv) < 2:
        print("Uso: python compiler_windows.py <archivo_fuente> [<archivo_salida>]")
        return
    
    source_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else source_file.rsplit('.', 1)[0] + ".exe"
    
    success = compile_file(source_file, output_file)
    
    if success:
        print(f"Para ejecutar el programa: {output_file}")
        
if __name__ == "__main__":
    main()