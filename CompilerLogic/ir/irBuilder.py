# -*- coding: utf-8 -*-
"""Generador de IR LLVM para VGraph (solo IR, sin optimizaciones)"""
from llvmlite import ir
from config import CompilerData   # Acceso a AST + symbol table
from antlr4.tree.Tree import TerminalNodeImpl

# Tipos básicos ----------------------------------------------------------
_f64  = ir.DoubleType()  # nuestros "int" (float64)
_i32  = ir.IntType(32)
_i1   = ir.IntType(1)
_void = ir.VoidType()

_COLOR = {
    'rojo':0x00FF0000,'verde':0x0000FF00,'azul':0x000000FF,
    'amarillo':0x00FFFF00,'cyan':0x0000FFFF,'magenta':0x00FF00FF,
    'blanco':0x00FFFFFF,'negro':0x00000000,'marrón':0x00503A17,
}

class IRGenerator:
    """Recorre el AST anotado y emite llvmlite Module."""

    # ------------------------------------------------------------------
    def __init__(self, ast, symtab):
        self.ast     = ast
        self.symtab  = symtab
        self.module  = ir.Module(name="vgraph")
        self.builder = None
        self.func    = None
        self.locals  = {}   # nombre→alloca
        self._decl_runtime()
        self._gen_program(ast)

    # ============  runtime externals  ==================================
    def _decl(self, name, ret, *args):
        fnty = ir.FunctionType(ret, list(args))
        return ir.Function(self.module, fnty, name=name)

    def _decl_runtime(self):
        self._rt_setcolor   = self._decl("vg_set_color",   _void, _i32)
        self._rt_draw_pixel = self._decl("vg_draw_pixel",  _void, _i32, _i32)
        self._rt_draw_line  = self._decl("vg_draw_line",   _void, _i32, _i32, _i32, _i32)
        self._rt_draw_circle= self._decl("vg_draw_circle", _void, _i32, _i32, _i32)
        self._rt_draw_rect  = self._decl("vg_draw_rect",   _void, _i32, _i32, _i32, _i32)
        self._rt_clear      = self._decl("vg_clear",       _void)
        self._rt_wait       = self._decl("vg_wait",        _void, _i32)

    # ============  programa global  ====================================
    def _gen_program(self, node):
        main_ty = ir.FunctionType(_i32, [])
        self.func = ir.Function(self.module, main_ty, name="main")
        entry = self.func.append_basic_block("entry")
        self.builder = ir.IRBuilder(entry)

        # TODO: recorrer declaraciones globales y hacer allocas
        for ch in self._children(node):
            self._gen_stmt(ch)

        self.builder.ret(ir.Constant(_i32, 0))

    # ============  helpers  ============================================
    @staticmethod
    def _children(ctx):
        """Sólo hijos que son reglas (descarta TerminalNodeImpl)."""
        return [ctx.getChild(i) for i in range(ctx.getChildCount())
                if not isinstance(ctx.getChild(i), TerminalNodeImpl)]


    def _as_i32(self, f64_val):
        return self.builder.fptosi(f64_val, _i32)

    # ============  statements  =========================================
    def _gen_stmt(self, ctx):
        if not _is_rule(ctx):
            return
        rule = ctx.parser.ruleNames[ctx.getRuleIndex()]
        if rule == "drawStatement":
            self._gen_draw(ctx.drawObject())
        elif rule == "setColorStatement":
            self._gen_setcolor(ctx)
        elif rule == "waitStatement":
            ms = self._as_i32(self._gen_expr(ctx.expr()))
            self.builder.call(self._rt_wait, [ms])
        elif rule == "clearStatement":
            self.builder.call(self._rt_clear, [])
        # TODO: if/loop/function/assignment

    # ---------------- draw ---------------------------------------------
    def _gen_draw(self, obj):
        kind = obj.start.text  # pixel|line|circle|rect
        if kind == "pixel":
            x = self._as_i32(self._gen_expr(obj.expr(0)))
            y = self._as_i32(self._gen_expr(obj.expr(1)))
            self.builder.call(self._rt_draw_pixel, [x, y])
        elif kind == "line":
            xs = [self._as_i32(self._gen_expr(e)) for e in obj.expr()]
            self.builder.call(self._rt_draw_line, xs)
        elif kind == "circle":
            cx = self._as_i32(self._gen_expr(obj.expr(0)))
            cy = self._as_i32(self._gen_expr(obj.expr(1)))
            r  = self._as_i32(self._gen_expr(obj.expr(2)))
            self.builder.call(self._rt_draw_circle, [cx, cy, r])
        elif kind == "rect":
            xs = [self._as_i32(self._gen_expr(e)) for e in obj.expr()]
            self.builder.call(self._rt_draw_rect, xs)

    # ---------------- setcolor -----------------------------------------
    def _gen_setcolor(self, ctx):
        arg = ctx.getChild(2)
        if arg.getChildCount() == 0 and arg.getText() in _COLOR:
            rgb = ir.Constant(_i32, _COLOR[arg.getText()])
            self.builder.call(self._rt_setcolor, [rgb])
        else:  # variable
            name = arg.getText()
            if name not in self.locals:
                raise RuntimeError(f"variable '{name}' usada antes de su alloca en IR gén.")
            rgb_val = self.builder.load(self.locals[name])
            self.builder.call(self._rt_setcolor, [rgb_val])

    # ============  expresiones  ========================================
    def _gen_expr(self, ctx):
        if isinstance(ctx, TerminalNodeImpl):
            raise ValueError("expr recibió un nodo terminal inesperado")
        alt = ctx.__class__.__name__.replace("Context", "")
        if alt == "NumberExpr":
            return ir.Constant(_f64, float(ctx.NUMBER().getText()))
        if alt == "ColorExpr":
            return ir.Constant(_i32, _COLOR[ctx.COLOR_CONST().getText()])
        if alt == "IdExpr":
            return self.builder.load(self.locals[ctx.ID().getText()])
        if alt == "AddSubExpr":
            a = self._gen_expr(ctx.expr(0)); b = self._gen_expr(ctx.expr(1))
            return self.builder.fadd(a, b) if ctx.PLUS() else self.builder.fsub(a, b)
        # … implementa MulDivExpr, NegExpr, cos/sin, etc.
        raise NotImplementedError(alt)

# helper compacto
def _is_rule(ctx):
    """Devuelve True si ctx es un nodo de regla (no terminal)."""
    return not isinstance(ctx, TerminalNodeImpl)