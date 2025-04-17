# Generated from VGraph.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .VGraphParser import VGraphParser
else:
    from VGraphParser import VGraphParser

# This class defines a complete listener for a parse tree produced by VGraphParser.
class VGraphListener(ParseTreeListener):

    # Enter a parse tree produced by VGraphParser#program.
    def enterProgram(self, ctx:VGraphParser.ProgramContext):
        pass

    # Exit a parse tree produced by VGraphParser#program.
    def exitProgram(self, ctx:VGraphParser.ProgramContext):
        pass


    # Enter a parse tree produced by VGraphParser#statement.
    def enterStatement(self, ctx:VGraphParser.StatementContext):
        pass

    # Exit a parse tree produced by VGraphParser#statement.
    def exitStatement(self, ctx:VGraphParser.StatementContext):
        pass



del VGraphParser