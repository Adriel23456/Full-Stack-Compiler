"""
AST ➜ LLVM IR generator using llvmlite

UPDATE #9
• Se implementa _visit_AssignmentExpressionContext → permite que la
  parte “inicialización” e “incremento” de un for-loop almacenen el
  valor en la variable.
• Resto idéntico a Update #8.
"""

from __future__ import annotations
from antlr4.tree.Tree import TerminalNodeImpl
from llvmlite import ir, binding as llvm

# ──────────────── host triple / datalayout ────────────────
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()
HOST_TRIPLE = llvm.get_default_triple()
HOST_DATALAYOUT = (
    llvm.Target.from_default_triple().create_target_machine().target_data
)

# ───────────────────── literal → RGB ──────────────────────
COLORS = {
    "rojo": 0x00FF0000,
    "verde": 0x0000FF00,
    "azul": 0x000000FF,
    "amarillo": 0x00FFFF00,
    "cyan": 0x0000FFFF,
    "magenta": 0x00FF00FF,
    "blanco": 0x00FFFFFF,
    "negro": 0x00000000,
    "marrón": 0x00800000,
}


def _dbg(msg: str) -> None:
    print(f"[IR-BUILDER] {msg}")


class IRGenerator:
    # ─────────────────────────────────────────────────────────
    def __init__(self, ast, symtab, parser):
        self.ast, self.symtab, self.parser = ast, symtab, parser

        self.module = ir.Module(name="vgraph")
        self.module.triple = HOST_TRIPLE
        self.module.data_layout = HOST_DATALAYOUT

        # tipos LLVM
        self.f64 = ir.DoubleType()
        self.i32 = ir.IntType(32)
        self.i1 = ir.IntType(1)
        self.void = ir.VoidType()

        self.builder: ir.IRBuilder | None = None
        self.value_ptr: dict[str, ir.Value] = {}

        self._declare_runtime()
        self._codegen_globals()

    # ─────────────── punto de entrada generate() ─────────────
    def generate(self) -> str:
        _dbg("starting IR generation pass")

        fn_main = ir.Function(
            self.module, ir.FunctionType(self.i32, ()), name="main"
        )
        self.builder = ir.IRBuilder(fn_main.append_basic_block("entry"))
        self._visit(self.ast)
        self.builder.ret(ir.Constant(self.i32, 0))

        # wrapper _main para lli
        fn_wrap = ir.Function(self.module, fn_main.function_type, name="_main")
        bw = ir.IRBuilder(fn_wrap.append_basic_block("entry"))
        bw.ret(bw.call(fn_main, []))

        _dbg("IR generation completed")
        return str(self.module)

    # ──────────────── runtime externals ──────────────────────
    def _declare_runtime(self):
        _dbg("declaring runtime externals")
        proto = {
            "vg_set_color": (self.void, (self.i32,)),
            "vg_draw_pixel": (self.void, (self.i32, self.i32)),
            "vg_draw_circle": (self.void, (self.i32,) * 3),
            "vg_draw_line": (self.void, (self.i32,) * 4),
            "vg_draw_rect": (self.void, (self.i32,) * 4),
            "vg_clear": (self.void, ()),
            "vg_wait": (self.void, (self.i32,)),
            "cos": (self.f64, (self.f64,)),
            "sin": (self.f64, (self.f64,)),
        }
        for n, (ret, params) in proto.items():
            if n not in self.module.globals:
                ir.Function(
                    self.module, ir.FunctionType(ret, params), name=n
                )

    # ──────────────── global vars (x,y,c,…) ──────────────────
    def _codegen_globals(self):
        _dbg("emitting global variables")
        g_scope = self.symtab.get_all_symbols().get("global", {})
        for ident, info in g_scope.items():
            typ = info.get("type", "int")
            if typ == "color":
                g = ir.GlobalVariable(self.module, self.i32, ident)
                g.initializer = ir.Constant(self.i32, 0x00FFFFFF)
            elif typ == "bool":
                g = ir.GlobalVariable(self.module, self.i1, ident)
                g.initializer = ir.Constant(self.i1, 0)
            else:
                g = ir.GlobalVariable(self.module, self.f64, ident)
                g.initializer = ir.Constant(self.f64, 0.0)
            self.value_ptr[ident] = g

    # ───────────────────────── visit gen ──────────────────────
    def _visit(self, node):
        h = getattr(self, f"_visit_{node.__class__.__name__}", None)
        if h:
            return h(node)
        res = None
        for i in range(node.getChildCount()):
            v = self._visit(node.getChild(i))
            res = res or v
        return res

    # ─────── terminales ───────
    def _visit_TerminalNodeImpl(self, tok):
        t = tok.getText()
        if t in ("true", "false"):
            return ir.Constant(self.i1, t == "true")
        if t in COLORS:
            return ir.Constant(self.i32, COLORS[t])
        if t.replace(".", "", 1).isdigit():
            return ir.Constant(self.f64, float(t))
        return None

    # ─────── literales + ID ───
    def _visit_NumberExprContext(self, ctx):
        return ir.Constant(self.f64, float(ctx.getText()))

    def _visit_ColorExprContext(self, ctx):
        return ir.Constant(self.i32, COLORS[ctx.getText()])

    def _visit_BoolConstExprContext(self, ctx):
        return ir.Constant(self.i1, ctx.getText() == "true")

    def _visit_IdExprContext(self, ctx):
        name = ctx.getText()
        if name in COLORS and name not in self.value_ptr:
            return ir.Constant(self.i32, COLORS[name])
        return self.builder.load(self._get_ptr(name))

    def _visit_ParenExprContext(self, ctx):
        return self._visit(ctx.expr())

    def _visit_CosExprContext(self, ctx):
        return self.builder.call(
            self.module.globals["cos"], [self._visit(ctx.expr())]
        )

    def _visit_SinExprContext(self, ctx):
        return self.builder.call(
            self.module.globals["sin"], [self._visit(ctx.expr())]
        )

    # ─────── aritmética / comparaciones / booleanos ───────────
    # helper binario
    def _binary(self, ctx):
        lhs = self._visit(ctx.getChild(0))
        rhs = self._visit(ctx.getChild(2))
        if lhs is None or rhs is None:
            _dbg(f"⚠️ binary op got None lhs={lhs} rhs={rhs}")
            lhs = lhs or self._const_zero(self.f64)
            rhs = rhs or self._const_zero(self.f64)
        return lhs, rhs

    def _visit_AddSubExprContext(self, ctx):
        lhs, rhs = self._binary(ctx)
        return (
            self.builder.fsub(lhs, rhs)
            if ctx.MINUS()
            else self.builder.fadd(lhs, rhs)
        )

    def _visit_MulDivExprContext(self, ctx):
        lhs, rhs = self._binary(ctx)
        return (
            self.builder.fdiv(lhs, rhs)
            if ctx.DIV()
            else self.builder.fmul(lhs, rhs)
        )

    def _visit_NegExprContext(self, ctx):
        return self.builder.fsub(
            ir.Constant(self.f64, 0.0), self._visit(ctx.getChild(1))
        )

    def _visit_ComparisonExprContext(self, ctx):
        lhs, rhs = self._binary(ctx)
        op = ctx.getChild(1).getText()
        cm = {
            "==": "oeq",
            "!=": "one",
            "<": "olt",
            "<=": "ole",
            ">": "ogt",
            ">=": "oge",
        }
        return self.builder.fcmp_ordered(cm[op], lhs, rhs)

    # booleanas
    def _visit_AndExprContext(self, ctx):
        lhs, rhs = self._binary(ctx)
        return self.builder.and_(lhs, rhs)

    def _visit_OrExprContext(self, ctx):
        lhs, rhs = self._binary(ctx)
        return self.builder.or_(lhs, rhs)

    def _visit_NotExprContext(self, ctx):
        return self.builder.xor(
            self._visit(ctx.boolExpr()), ir.Constant(self.i1, 1)
        )

    def _visit_ParenBoolExprContext(self, ctx):
        return self._visit(ctx.boolExpr())

    def _visit_BoolIdExprContext(self, ctx):
        return self.builder.load(self._get_ptr(ctx.getText()))

    # ────────────────── STATEMENTS ─────────────────────────────
    # asignación – statement (termina en ';')
    def _visit_AssignmentStatementContext(self, ctx):
        self._gen_assign(ctx.assignmentExpression())

    # asignación – expression (t = t+5 dentro del for)
    def _visit_AssignmentExpressionContext(self, ctx):
        return self._gen_assign(ctx)

    # helper común
    def _gen_assign(self, assign_ctx):
        name = assign_ctx.ID().getText()
        dest_ptr = self._get_ptr(name)
        dest_ty = dest_ptr.type.pointee

        rhs_node = assign_ctx.getChild(assign_ctx.getChildCount() - 1)
        rhs_val = self._visit(rhs_node)
        if rhs_val is None:
            _dbg(f"⚠️ RHS of '{name}' is None – injecting zero")
            rhs_val = self._const_zero(dest_ty)

        rhs_val = self._coerce(rhs_val, dest_ty)
        self.builder.store(rhs_val, dest_ptr)
        return rhs_val

    # setcolor
    def _visit_SetColorStatementContext(self, ctx):
        raw = ctx.getChild(2)  # ID o COLOR_CONST
        arg_val = self._visit(raw)
        if arg_val is None:  # variable color
            arg_val = self.builder.load(self._get_ptr(raw.getText()))
        arg_val = self._coerce(arg_val, self.i32)
        self.builder.call(self.module.globals["vg_set_color"], [arg_val])

    # clear
    def _visit_ClearStatementContext(self, _ctx):
        self.builder.call(self.module.globals["vg_clear"], [])

    # wait
    def _visit_WaitStatementContext(self, ctx):
        ms = self._round_to_i32(self._visit(ctx.expr()))
        self.builder.call(self.module.globals["vg_wait"], [ms])

    # draw pixel / circle / rect / line
    def _visit_DrawStatementContext(self, ctx):
        obj = ctx.drawObject()
        kind = obj.getChild(0).getText()
        fn = self.module.globals[f"vg_draw_{kind}"]

        expr_nodes = [
            ch
            for ch in obj.children
            if ch.__class__.__name__.endswith("ExprContext")
        ]
        args = [self._round_to_i32(self._visit(n)) for n in expr_nodes]
        self.builder.call(fn, args)

    # if / else
    def _visit_IfStatementContext(self, ctx):
        cond = self._coerce(self._visit(ctx.boolExpr()), self.i1)
        then_bb = self.builder.function.append_basic_block("then")
        merge_bb = self.builder.function.append_basic_block("endif")
        else_bb = (
            self.builder.function.append_basic_block("else")
            if ctx.ELSE()
            else merge_bb
        )
        self.builder.cbranch(cond, then_bb, else_bb)

        self.builder.position_at_start(then_bb)
        self._visit(ctx.block(0))
        self.builder.branch(merge_bb)

        if ctx.ELSE():
            self.builder.position_at_start(else_bb)
            self._visit(ctx.getChild(ctx.getChildCount() - 1))
            self.builder.branch(merge_bb)

        self.builder.position_at_start(merge_bb)

    # loop (for)
    def _visit_LoopStatementContext(self, ctx):
        self._visit(ctx.assignmentExpression(0))  # init
        f = self.builder.function
        cond_bb, body_bb, incr_bb, end_bb = [
            f.append_basic_block(n)
            for n in ("for.cond", "for.body", "for.incr", "for.end")
        ]
        self.builder.branch(cond_bb)

        # cond
        self.builder.position_at_start(cond_bb)
        cond_val = self._coerce(self._visit(ctx.boolExpr()), self.i1)
        self.builder.cbranch(cond_val, body_bb, end_bb)

        # body
        self.builder.position_at_start(body_bb)
        self._visit(ctx.block())
        self.builder.branch(incr_bb)

        # incr
        self.builder.position_at_start(incr_bb)
        self._visit(ctx.assignmentExpression(1))
        self.builder.branch(cond_bb)

        # end
        self.builder.position_at_start(end_bb)

    # ╰──────────────────────────────────────────────────────────╯
    # ────────────────── helpers ───────────────────────────────
    def _coerce(self, val: ir.Value | None, target_ty: ir.Type) -> ir.Value:
        if val is None:
            return self._const_zero(target_ty)
        if val.type == target_ty:
            return val
        if target_ty is self.i1:
            if val.type is self.f64:
                return self.builder.fcmp_ordered(
                    "one", val, ir.Constant(self.f64, 0.0)
                )
            if val.type is self.i32:
                return self.builder.icmp_unsigned(
                    "ne", val, ir.Constant(self.i32, 0)
                )
        if target_ty is self.i32:
            if val.type is self.f64:
                return self._round_to_i32(val)
            if val.type is self.i1:
                return self.builder.zext(val, self.i32)
        if target_ty is self.f64:
            if val.type is self.i32:
                return self.builder.sitofp(val, self.f64)
            if val.type is self.i1:
                return self.builder.uitofp(val, self.f64)
        _dbg(f"⚠️ cannot coerce {val.type} → {target_ty} – zero used")
        return self._const_zero(target_ty)

    def _round_to_i32(self, val: ir.Value) -> ir.Value:
        if val.type is self.i32:
            return val
        if val.type is self.f64:
            return self.builder.fptosi(
                self.builder.fadd(val, ir.Constant(self.f64, 0.5)), self.i32
            )
        if val.type is self.i1:
            return self.builder.zext(val, self.i32)
        return ir.Constant(self.i32, 0)

    def _const_zero(self, ty: ir.Type) -> ir.Constant:
        if ty is self.f64:
            return ir.Constant(self.f64, 0.0)
        if ty is self.i32:
            return ir.Constant(self.i32, 0)
        if ty is self.i1:
            return ir.Constant(self.i1, 0)
        return ir.Constant(ty, None)

    def _get_ptr(self, name: str) -> ir.Value:
        ptr = self.value_ptr.get(name)
        if ptr is None:
            _dbg(f"⚠️ '{name}' undeclared – creating implicit f64 global")
            g = ir.GlobalVariable(self.module, self.f64, name)
            g.initializer = ir.Constant(self.f64, 0.0)
            self.value_ptr[name] = g
            ptr = g
        return ptr