grammar VGraph;

// Parser rules
program: statement* EOF;
statement: ';'; // Placeholder para esta fase

// Palabras clave
DRAW: 'draw';
SETCOLOR: 'setcolor';
FRAME: 'frame';
LOOP: 'loop';
IF: 'if';
ELSE: 'else';
END: 'end';
WAIT: 'wait';
LINE: 'line';
CIRCLE: 'circle';
RECT: 'rect';
MOVE: 'move';
ANIMATE: 'animate';
COS: 'cos';
SIN: 'sin';
PIXEL: 'pixel';
FUNCTION: 'function';
RETURN: 'return';
CLEAR: 'clear';

// Tipos
INT_TYPE: 'int';
COLOR_TYPE: 'color';

// Paréntesis y corchetes
LPAREN: '(';
RPAREN: ')';
LBRACK: '[';
RBRACK: ']';

// Operadores
PLUS: '+';
MINUS: '-';
MULT: '*';
DIV: '/';
MOD: '%';
ASSIGN: '=';
EQ: '==';
LT: '<';
GT: '>';
LE: '<=';
GE: '>=';
NE: '!=';

// Delimitadores
LBRACE: '{';
RBRACE: '}';
SEMICOLON: ';';
COMMA: ',';

// Definir fragmentos para mejorar legibilidad
fragment MINUSCULA: 'a'..'z';
fragment MAYUSCULA: 'A'..'Z';
fragment DIGITO: '0'..'9';
fragment LETRA: MINUSCULA | MAYUSCULA;
fragment ALFANUMERICO: LETRA | DIGITO;

// Identificadores (inician con minúscula, sin límite de longitud)
ID: MINUSCULA ALFANUMERICO*;

// Números (enteros o decimales)
NUMBER: DIGITO+ ('.' DIGITO+)?;

// Colores (constantes predefinidas)
COLOR_CONST: 'rojo' | 'azul' | 'verde' | 'amarillo' | 'cyan' | 'magenta' | 'blanco' | 'negro' | 'marrón';

// Comentarios
COMMENT: '#' ~[\r\n]* -> skip;

// Espacios en blanco (este es el cambio principal)
WS: [ \t\r\n]+ -> skip;