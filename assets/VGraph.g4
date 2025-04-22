grammar VGraph;

// Parser rules
program : declaration* statement* EOF;

declaration 
    : typeDeclaration ID ('=' expr)? ';'
    | typeDeclaration idList ';'
    ;

typeDeclaration : '(' vartype ')';

vartype 
    : INT_TYPE
    | COLOR_TYPE
    ;

idList : ID (',' ID)*;

statement
    : drawStatement
    | setColorStatement
    | frameStatement
    | loopStatement
    | ifStatement
    | waitStatement
    | functionDeclStatement
    | functionCallStatement
    | assignmentStatement
    | returnStatement
    | clearStatement
    ;

assignmentStatement : ID '=' expr ';';

drawStatement 
    : DRAW drawObject ';'
    ;

drawObject
    : LINE '(' expr ',' expr ',' expr ',' expr ')'
    | CIRCLE '(' expr ',' expr ',' expr ')'
    | RECT '(' expr ',' expr ',' expr ',' expr ')'
    | PIXEL '(' expr ',' expr ')'
    ;

setColorStatement : SETCOLOR '(' (ID | COLOR_CONST) ')' ';';

frameStatement : FRAME '{' statement* '}';

loopStatement : LOOP '(' assignmentStatement expr ';' expr ')' '{' statement* '}';

ifStatement 
    : IF '(' expr ')' '{' statement* '}' 
      (ELSE '{' statement* '}')?
    ;

waitStatement : WAIT '(' expr ')' ';';

functionDeclStatement : FUNCTION ID '(' paramList? ')' '{' statement* '}';

paramList : ID (',' ID)*;

functionCallStatement : ID '(' argumentList? ')' ';';

argumentList : expr (',' expr)*;

returnStatement : RETURN expr? ';';

clearStatement : CLEAR '(' ')' ';';

expr
    : '(' expr ')'                               # ParenExpr
    | COS '(' expr ')'                           # CosExpr
    | SIN '(' expr ')'                           # SinExpr
    | expr op=(MULT|DIV|MOD) expr                # MulDivExpr
    | expr op=(PLUS|MINUS) expr                  # AddSubExpr
    | expr op=(EQ|NE|LT|LE|GT|GE) expr           # CompExpr
    | NUMBER                                     # NumberExpr
    | ID                                         # IdExpr
    | COLOR_CONST                                # ColorExpr
    | functionCall                               # FunctionCallExpr
    ;

functionCall : ID '(' argumentList? ')';

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

// Espacios en blanco
WS: [ \t\r\n]+ -> skip;