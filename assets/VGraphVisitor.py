# Generated from VGraph.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .VGraphParser import VGraphParser
else:
    from VGraphParser import VGraphParser

# This class defines a complete generic visitor for a parse tree produced by VGraphParser.

class VGraphVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by VGraphParser#program.
    def visitProgram(self, ctx:VGraphParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#declaration.
    def visitDeclaration(self, ctx:VGraphParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx:VGraphParser.TypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#vartype.
    def visitVartype(self, ctx:VGraphParser.VartypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#idList.
    def visitIdList(self, ctx:VGraphParser.IdListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#statement.
    def visitStatement(self, ctx:VGraphParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#block.
    def visitBlock(self, ctx:VGraphParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#assignmentExpression.
    def visitAssignmentExpression(self, ctx:VGraphParser.AssignmentExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#assignmentStatement.
    def visitAssignmentStatement(self, ctx:VGraphParser.AssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#drawStatement.
    def visitDrawStatement(self, ctx:VGraphParser.DrawStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#drawObject.
    def visitDrawObject(self, ctx:VGraphParser.DrawObjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#setColorStatement.
    def visitSetColorStatement(self, ctx:VGraphParser.SetColorStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#frameStatement.
    def visitFrameStatement(self, ctx:VGraphParser.FrameStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#loopStatement.
    def visitLoopStatement(self, ctx:VGraphParser.LoopStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#ifStatement.
    def visitIfStatement(self, ctx:VGraphParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#waitStatement.
    def visitWaitStatement(self, ctx:VGraphParser.WaitStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#functionDeclStatement.
    def visitFunctionDeclStatement(self, ctx:VGraphParser.FunctionDeclStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#paramList.
    def visitParamList(self, ctx:VGraphParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#functionCallStatement.
    def visitFunctionCallStatement(self, ctx:VGraphParser.FunctionCallStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#argumentList.
    def visitArgumentList(self, ctx:VGraphParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#returnStatement.
    def visitReturnStatement(self, ctx:VGraphParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#clearStatement.
    def visitClearStatement(self, ctx:VGraphParser.ClearStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#AndExpr.
    def visitAndExpr(self, ctx:VGraphParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#ParenBoolExpr.
    def visitParenBoolExpr(self, ctx:VGraphParser.ParenBoolExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#BoolConstExpr.
    def visitBoolConstExpr(self, ctx:VGraphParser.BoolConstExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#ComparisonExpr.
    def visitComparisonExpr(self, ctx:VGraphParser.ComparisonExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#BoolIdExpr.
    def visitBoolIdExpr(self, ctx:VGraphParser.BoolIdExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#NotExpr.
    def visitNotExpr(self, ctx:VGraphParser.NotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#OrExpr.
    def visitOrExpr(self, ctx:VGraphParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#BoolLiteralExpr.
    def visitBoolLiteralExpr(self, ctx:VGraphParser.BoolLiteralExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#FunctionCallExpr.
    def visitFunctionCallExpr(self, ctx:VGraphParser.FunctionCallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#MulDivExpr.
    def visitMulDivExpr(self, ctx:VGraphParser.MulDivExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#IdExpr.
    def visitIdExpr(self, ctx:VGraphParser.IdExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#NumberExpr.
    def visitNumberExpr(self, ctx:VGraphParser.NumberExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#ColorExpr.
    def visitColorExpr(self, ctx:VGraphParser.ColorExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#NegExpr.
    def visitNegExpr(self, ctx:VGraphParser.NegExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#ParenExpr.
    def visitParenExpr(self, ctx:VGraphParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#SinExpr.
    def visitSinExpr(self, ctx:VGraphParser.SinExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#CosExpr.
    def visitCosExpr(self, ctx:VGraphParser.CosExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#AddSubExpr.
    def visitAddSubExpr(self, ctx:VGraphParser.AddSubExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VGraphParser#functionCall.
    def visitFunctionCall(self, ctx:VGraphParser.FunctionCallContext):
        return self.visitChildren(ctx)



del VGraphParser