grammar VGraph;

// Parser rules

program
    : statement* EOF
    ;

declaration
    : typeDeclaration ID (ASSIGN expr)? SEMICOLON
    | typeDeclaration idList SEMICOLON
    ;

typeDeclaration
    : LPAREN vartype RPAREN
    ;

vartype
    : INT_TYPE
    | COLOR_TYPE
    ;

idList
    : ID (COMMA ID)*
    ;

statement
    : declaration               
    | drawStatement
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

block
    : LBRACE statement* RBRACE
    ;

assignmentExpression
    : ID ASSIGN expr
    ;

assignmentStatement
    : assignmentExpression SEMICOLON
    ;

drawStatement
    : DRAW drawObject SEMICOLON
    ;

drawObject
    : LINE   LPAREN expr COMMA expr COMMA expr COMMA expr RPAREN
    | CIRCLE LPAREN expr COMMA expr COMMA expr RPAREN
    | RECT   LPAREN expr COMMA expr COMMA expr COMMA expr RPAREN
    | PIXEL  LPAREN expr COMMA expr RPAREN
    ;

setColorStatement
    : SETCOLOR LPAREN (ID | COLOR_CONST) RPAREN SEMICOLON
    ;

frameStatement
    : FRAME block
    ;

loopStatement
    : LOOP LPAREN
        assignmentExpression SEMICOLON
        expr                  SEMICOLON
        assignmentExpression
      RPAREN
      block
    ;

ifStatement
    : IF LPAREN expr RPAREN block
      ( ELSE ( ifStatement | block ) )?
    ;

waitStatement
    : WAIT LPAREN expr RPAREN SEMICOLON
    ;

functionDeclStatement
    : FUNCTION ID LPAREN paramList? RPAREN block
    ;

paramList
    : ID (COMMA ID)*
    ;

functionCallStatement
    : ID LPAREN argumentList? RPAREN SEMICOLON
    ;

argumentList
    : expr (COMMA expr)*
    ;

returnStatement
    : RETURN expr? SEMICOLON
    ;

clearStatement
    : CLEAR LPAREN RPAREN SEMICOLON
    ;

expr
    : LPAREN expr RPAREN                             # ParenExpr
    | COS LPAREN expr RPAREN                         # CosExpr
    | SIN LPAREN expr RPAREN                         # SinExpr
    | expr op=(MULT | DIV | MOD) expr                # MulDivExpr
    | expr op=(PLUS | MINUS) expr                    # AddSubExpr
    | expr op=(EQ | NE | LT | LE | GT | GE) expr     # CompExpr
    | NUMBER                                         # NumberExpr
    | ID                                             # IdExpr
    | COLOR_CONST                                    # ColorExpr
    | functionCall                                   # FunctionCallExpr
    ;

functionCall
    : ID LPAREN argumentList? RPAREN
    ;

// Lexer rules

DRAW       : 'draw';
SETCOLOR   : 'setcolor';
FRAME      : 'frame';
LOOP       : 'loop';
IF         : 'if';
ELSE       : 'else';
END        : 'end';
WAIT       : 'wait';
LINE       : 'line';
CIRCLE     : 'circle';
RECT       : 'rect';
MOVE       : 'move';
ANIMATE    : 'animate';
COS        : 'cos';
SIN        : 'sin';
PIXEL      : 'pixel';
FUNCTION   : 'function';
RETURN     : 'return';
CLEAR      : 'clear';

INT_TYPE   : 'int';
COLOR_TYPE : 'color';

LPAREN     : '(';
RPAREN     : ')';
LBRACE     : '{';
RBRACE     : '}';
LBRACK     : '[';
RBRACK     : ']';

PLUS       : '+';
MINUS      : '-';
MULT       : '*';
DIV        : '/';
MOD        : '%';
ASSIGN     : '=';
EQ         : '==';
LT         : '<';
GT         : '>';
LE         : '<=';
GE         : '>=';
NE         : '!=';

SEMICOLON  : ';';
COMMA      : ',';

fragment MINUSCULA    : [a-z];
fragment MAYUSCULA    : [A-Z];
fragment DIGITO       : [0-9];
fragment LETRA        : MINUSCULA | MAYUSCULA;
fragment ALFANUMERICO : LETRA | DIGITO;

ID          : MINUSCULA ALFANUMERICO*;
NUMBER      : DIGITO+ ('.' DIGITO+)?;
COLOR_CONST : 'rojo' | 'azul' | 'verde' | 'amarillo' | 'cyan' | 'magenta' | 'blanco' | 'negro' | 'marrón';

COMMENT     : '#' ~[\r\n]* -> skip;
WS          : [ \t\r\n]+ -> skip;