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


    # Enter a parse tree produced by VGraphParser#declaration.
    def enterDeclaration(self, ctx:VGraphParser.DeclarationContext):
        pass

    # Exit a parse tree produced by VGraphParser#declaration.
    def exitDeclaration(self, ctx:VGraphParser.DeclarationContext):
        pass


    # Enter a parse tree produced by VGraphParser#typeDeclaration.
    def enterTypeDeclaration(self, ctx:VGraphParser.TypeDeclarationContext):
        pass

    # Exit a parse tree produced by VGraphParser#typeDeclaration.
    def exitTypeDeclaration(self, ctx:VGraphParser.TypeDeclarationContext):
        pass


    # Enter a parse tree produced by VGraphParser#vartype.
    def enterVartype(self, ctx:VGraphParser.VartypeContext):
        pass

    # Exit a parse tree produced by VGraphParser#vartype.
    def exitVartype(self, ctx:VGraphParser.VartypeContext):
        pass


    # Enter a parse tree produced by VGraphParser#idList.
    def enterIdList(self, ctx:VGraphParser.IdListContext):
        pass

    # Exit a parse tree produced by VGraphParser#idList.
    def exitIdList(self, ctx:VGraphParser.IdListContext):
        pass


    # Enter a parse tree produced by VGraphParser#statement.
    def enterStatement(self, ctx:VGraphParser.StatementContext):
        pass

    # Exit a parse tree produced by VGraphParser#statement.
    def exitStatement(self, ctx:VGraphParser.StatementContext):
        pass


    # Enter a parse tree produced by VGraphParser#block.
    def enterBlock(self, ctx:VGraphParser.BlockContext):
        pass

    # Exit a parse tree produced by VGraphParser#block.
    def exitBlock(self, ctx:VGraphParser.BlockContext):
        pass


    # Enter a parse tree produced by VGraphParser#assignmentExpression.
    def enterAssignmentExpression(self, ctx:VGraphParser.AssignmentExpressionContext):
        pass

    # Exit a parse tree produced by VGraphParser#assignmentExpression.
    def exitAssignmentExpression(self, ctx:VGraphParser.AssignmentExpressionContext):
        pass


    # Enter a parse tree produced by VGraphParser#assignmentStatement.
    def enterAssignmentStatement(self, ctx:VGraphParser.AssignmentStatementContext):
        pass

    # Exit a parse tree produced by VGraphParser#assignmentStatement.
    def exitAssignmentStatement(self, ctx:VGraphParser.AssignmentStatementContext):
        pass


    # Enter a parse tree produced by VGraphParser#drawStatement.
    def enterDrawStatement(self, ctx:VGraphParser.DrawStatementContext):
        pass

    # Exit a parse tree produced by VGraphParser#drawStatement.
    def exitDrawStatement(self, ctx:VGraphParser.DrawStatementContext):
        pass


    # Enter a parse tree produced by VGraphParser#drawObject.
    def enterDrawObject(self, ctx:VGraphParser.DrawObjectContext):
        pass

    # Exit a parse tree produced by VGraphParser#drawObject.
    def exitDrawObject(self, ctx:VGraphParser.DrawObjectContext):
        pass


    # Enter a parse tree produced by VGraphParser#setColorStatement.
    def enterSetColorStatement(self, ctx:VGraphParser.SetColorStatementContext):
        pass

    # Exit a parse tree produced by VGraphParser#setColorStatement.
    def exitSetColorStatement(self, ctx:VGraphParser.SetColorStatementContext):
        pass


    # Enter a parse tree produced by VGraphParser#frameStatement.
    def enterFrameStatement(self, ctx:VGraphParser.FrameStatementContext):
        pass

    # Exit a parse tree produced by VGraphParser#frameStatement.
    def exitFrameStatement(self, ctx:VGraphParser.FrameStatementContext):
        pass


    # Enter a parse tree produced by VGraphParser#loopStatement.
    def enterLoopStatement(self, ctx:VGraphParser.LoopStatementContext):
        pass

    # Exit a parse tree produced by VGraphParser#loopStatement.
    def exitLoopStatement(self, ctx:VGraphParser.LoopStatementContext):
        pass


    # Enter a parse tree produced by VGraphParser#ifStatement.
    def enterIfStatement(self, ctx:VGraphParser.IfStatementContext):
        pass

    # Exit a parse tree produced by VGraphParser#ifStatement.
    def exitIfStatement(self, ctx:VGraphParser.IfStatementContext):
        pass


    # Enter a parse tree produced by VGraphParser#waitStatement.
    def enterWaitStatement(self, ctx:VGraphParser.WaitStatementContext):
        pass

    # Exit a parse tree produced by VGraphParser#waitStatement.
    def exitWaitStatement(self, ctx:VGraphParser.WaitStatementContext):
        pass


    # Enter a parse tree produced by VGraphParser#functionDeclStatement.
    def enterFunctionDeclStatement(self, ctx:VGraphParser.FunctionDeclStatementContext):
        pass

    # Exit a parse tree produced by VGraphParser#functionDeclStatement.
    def exitFunctionDeclStatement(self, ctx:VGraphParser.FunctionDeclStatementContext):
        pass


    # Enter a parse tree produced by VGraphParser#paramList.
    def enterParamList(self, ctx:VGraphParser.ParamListContext):
        pass

    # Exit a parse tree produced by VGraphParser#paramList.
    def exitParamList(self, ctx:VGraphParser.ParamListContext):
        pass


    # Enter a parse tree produced by VGraphParser#functionCallStatement.
    def enterFunctionCallStatement(self, ctx:VGraphParser.FunctionCallStatementContext):
        pass

    # Exit a parse tree produced by VGraphParser#functionCallStatement.
    def exitFunctionCallStatement(self, ctx:VGraphParser.FunctionCallStatementContext):
        pass


    # Enter a parse tree produced by VGraphParser#argumentList.
    def enterArgumentList(self, ctx:VGraphParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by VGraphParser#argumentList.
    def exitArgumentList(self, ctx:VGraphParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by VGraphParser#returnStatement.
    def enterReturnStatement(self, ctx:VGraphParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by VGraphParser#returnStatement.
    def exitReturnStatement(self, ctx:VGraphParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by VGraphParser#clearStatement.
    def enterClearStatement(self, ctx:VGraphParser.ClearStatementContext):
        pass

    # Exit a parse tree produced by VGraphParser#clearStatement.
    def exitClearStatement(self, ctx:VGraphParser.ClearStatementContext):
        pass


    # Enter a parse tree produced by VGraphParser#AndExpr.
    def enterAndExpr(self, ctx:VGraphParser.AndExprContext):
        pass

    # Exit a parse tree produced by VGraphParser#AndExpr.
    def exitAndExpr(self, ctx:VGraphParser.AndExprContext):
        pass


    # Enter a parse tree produced by VGraphParser#ParenBoolExpr.
    def enterParenBoolExpr(self, ctx:VGraphParser.ParenBoolExprContext):
        pass

    # Exit a parse tree produced by VGraphParser#ParenBoolExpr.
    def exitParenBoolExpr(self, ctx:VGraphParser.ParenBoolExprContext):
        pass


    # Enter a parse tree produced by VGraphParser#BoolConstExpr.
    def enterBoolConstExpr(self, ctx:VGraphParser.BoolConstExprContext):
        pass

    # Exit a parse tree produced by VGraphParser#BoolConstExpr.
    def exitBoolConstExpr(self, ctx:VGraphParser.BoolConstExprContext):
        pass


    # Enter a parse tree produced by VGraphParser#ComparisonExpr.
    def enterComparisonExpr(self, ctx:VGraphParser.ComparisonExprContext):
        pass

    # Exit a parse tree produced by VGraphParser#ComparisonExpr.
    def exitComparisonExpr(self, ctx:VGraphParser.ComparisonExprContext):
        pass


    # Enter a parse tree produced by VGraphParser#BoolIdExpr.
    def enterBoolIdExpr(self, ctx:VGraphParser.BoolIdExprContext):
        pass

    # Exit a parse tree produced by VGraphParser#BoolIdExpr.
    def exitBoolIdExpr(self, ctx:VGraphParser.BoolIdExprContext):
        pass


    # Enter a parse tree produced by VGraphParser#NotExpr.
    def enterNotExpr(self, ctx:VGraphParser.NotExprContext):
        pass

    # Exit a parse tree produced by VGraphParser#NotExpr.
    def exitNotExpr(self, ctx:VGraphParser.NotExprContext):
        pass


    # Enter a parse tree produced by VGraphParser#OrExpr.
    def enterOrExpr(self, ctx:VGraphParser.OrExprContext):
        pass

    # Exit a parse tree produced by VGraphParser#OrExpr.
    def exitOrExpr(self, ctx:VGraphParser.OrExprContext):
        pass


    # Enter a parse tree produced by VGraphParser#BoolLiteralExpr.
    def enterBoolLiteralExpr(self, ctx:VGraphParser.BoolLiteralExprContext):
        pass

    # Exit a parse tree produced by VGraphParser#BoolLiteralExpr.
    def exitBoolLiteralExpr(self, ctx:VGraphParser.BoolLiteralExprContext):
        pass


    # Enter a parse tree produced by VGraphParser#FunctionCallExpr.
    def enterFunctionCallExpr(self, ctx:VGraphParser.FunctionCallExprContext):
        pass

    # Exit a parse tree produced by VGraphParser#FunctionCallExpr.
    def exitFunctionCallExpr(self, ctx:VGraphParser.FunctionCallExprContext):
        pass


    # Enter a parse tree produced by VGraphParser#MulDivExpr.
    def enterMulDivExpr(self, ctx:VGraphParser.MulDivExprContext):
        pass

    # Exit a parse tree produced by VGraphParser#MulDivExpr.
    def exitMulDivExpr(self, ctx:VGraphParser.MulDivExprContext):
        pass


    # Enter a parse tree produced by VGraphParser#IdExpr.
    def enterIdExpr(self, ctx:VGraphParser.IdExprContext):
        pass

    # Exit a parse tree produced by VGraphParser#IdExpr.
    def exitIdExpr(self, ctx:VGraphParser.IdExprContext):
        pass


    # Enter a parse tree produced by VGraphParser#NumberExpr.
    def enterNumberExpr(self, ctx:VGraphParser.NumberExprContext):
        pass

    # Exit a parse tree produced by VGraphParser#NumberExpr.
    def exitNumberExpr(self, ctx:VGraphParser.NumberExprContext):
        pass


    # Enter a parse tree produced by VGraphParser#ColorExpr.
    def enterColorExpr(self, ctx:VGraphParser.ColorExprContext):
        pass

    # Exit a parse tree produced by VGraphParser#ColorExpr.
    def exitColorExpr(self, ctx:VGraphParser.ColorExprContext):
        pass


    # Enter a parse tree produced by VGraphParser#NegExpr.
    def enterNegExpr(self, ctx:VGraphParser.NegExprContext):
        pass

    # Exit a parse tree produced by VGraphParser#NegExpr.
    def exitNegExpr(self, ctx:VGraphParser.NegExprContext):
        pass


    # Enter a parse tree produced by VGraphParser#ParenExpr.
    def enterParenExpr(self, ctx:VGraphParser.ParenExprContext):
        pass

    # Exit a parse tree produced by VGraphParser#ParenExpr.
    def exitParenExpr(self, ctx:VGraphParser.ParenExprContext):
        pass


    # Enter a parse tree produced by VGraphParser#SinExpr.
    def enterSinExpr(self, ctx:VGraphParser.SinExprContext):
        pass

    # Exit a parse tree produced by VGraphParser#SinExpr.
    def exitSinExpr(self, ctx:VGraphParser.SinExprContext):
        pass


    # Enter a parse tree produced by VGraphParser#CosExpr.
    def enterCosExpr(self, ctx:VGraphParser.CosExprContext):
        pass

    # Exit a parse tree produced by VGraphParser#CosExpr.
    def exitCosExpr(self, ctx:VGraphParser.CosExprContext):
        pass


    # Enter a parse tree produced by VGraphParser#AddSubExpr.
    def enterAddSubExpr(self, ctx:VGraphParser.AddSubExprContext):
        pass

    # Exit a parse tree produced by VGraphParser#AddSubExpr.
    def exitAddSubExpr(self, ctx:VGraphParser.AddSubExprContext):
        pass


    # Enter a parse tree produced by VGraphParser#functionCall.
    def enterFunctionCall(self, ctx:VGraphParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by VGraphParser#functionCall.
    def exitFunctionCall(self, ctx:VGraphParser.FunctionCallContext):
        pass



del VGraphParser