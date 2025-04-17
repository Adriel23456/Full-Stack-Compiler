# Generated from VGraph.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\60")
        buf.write("\21\4\2\t\2\4\3\t\3\3\2\7\2\b\n\2\f\2\16\2\13\13\2\3\2")
        buf.write("\3\2\3\3\3\3\3\3\2\2\4\2\4\2\2\2\17\2\t\3\2\2\2\4\16\3")
        buf.write("\2\2\2\6\b\5\4\3\2\7\6\3\2\2\2\b\13\3\2\2\2\t\7\3\2\2")
        buf.write("\2\t\n\3\2\2\2\n\f\3\2\2\2\13\t\3\2\2\2\f\r\7\2\2\3\r")
        buf.write("\3\3\2\2\2\16\17\7*\2\2\17\5\3\2\2\2\3\t")
        return buf.getvalue()


class VGraphParser ( Parser ):

    grammarFileName = "VGraph.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'draw'", "'setcolor'", "'frame'", "'loop'", 
                     "'if'", "'else'", "'end'", "'wait'", "'line'", "'circle'", 
                     "'rect'", "'move'", "'animate'", "'cos'", "'sin'", 
                     "'pixel'", "'function'", "'return'", "'clear'", "'int'", 
                     "'color'", "'('", "')'", "'['", "']'", "'+'", "'-'", 
                     "'*'", "'/'", "'%'", "'='", "'=='", "'<'", "'>'", "'<='", 
                     "'>='", "'!='", "'{'", "'}'", "';'", "','" ]

    symbolicNames = [ "<INVALID>", "DRAW", "SETCOLOR", "FRAME", "LOOP", 
                      "IF", "ELSE", "END", "WAIT", "LINE", "CIRCLE", "RECT", 
                      "MOVE", "ANIMATE", "COS", "SIN", "PIXEL", "FUNCTION", 
                      "RETURN", "CLEAR", "INT_TYPE", "COLOR_TYPE", "LPAREN", 
                      "RPAREN", "LBRACK", "RBRACK", "PLUS", "MINUS", "MULT", 
                      "DIV", "MOD", "ASSIGN", "EQ", "LT", "GT", "LE", "GE", 
                      "NE", "LBRACE", "RBRACE", "SEMICOLON", "COMMA", "ID", 
                      "NUMBER", "COLOR_CONST", "COMMENT", "WS" ]

    RULE_program = 0
    RULE_statement = 1

    ruleNames =  [ "program", "statement" ]

    EOF = Token.EOF
    DRAW=1
    SETCOLOR=2
    FRAME=3
    LOOP=4
    IF=5
    ELSE=6
    END=7
    WAIT=8
    LINE=9
    CIRCLE=10
    RECT=11
    MOVE=12
    ANIMATE=13
    COS=14
    SIN=15
    PIXEL=16
    FUNCTION=17
    RETURN=18
    CLEAR=19
    INT_TYPE=20
    COLOR_TYPE=21
    LPAREN=22
    RPAREN=23
    LBRACK=24
    RBRACK=25
    PLUS=26
    MINUS=27
    MULT=28
    DIV=29
    MOD=30
    ASSIGN=31
    EQ=32
    LT=33
    GT=34
    LE=35
    GE=36
    NE=37
    LBRACE=38
    RBRACE=39
    SEMICOLON=40
    COMMA=41
    ID=42
    NUMBER=43
    COLOR_CONST=44
    COMMENT=45
    WS=46

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(VGraphParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VGraphParser.StatementContext)
            else:
                return self.getTypedRuleContext(VGraphParser.StatementContext,i)


        def getRuleIndex(self):
            return VGraphParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)




    def program(self):

        localctx = VGraphParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 7
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==VGraphParser.SEMICOLON:
                self.state = 4
                self.statement()
                self.state = 9
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 10
            self.match(VGraphParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SEMICOLON(self):
            return self.getToken(VGraphParser.SEMICOLON, 0)

        def getRuleIndex(self):
            return VGraphParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)




    def statement(self):

        localctx = VGraphParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 12
            self.match(VGraphParser.SEMICOLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





