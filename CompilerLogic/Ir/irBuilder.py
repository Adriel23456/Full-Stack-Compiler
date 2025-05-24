"""
AST ➜ LLVM IR generator using llvmlite

UPDATE #15  – Hot-fix llamadas de función
─────────────────────────────────────────
• _visit_FunctionCallStatementContext y _visit_FunctionCallExprContext
  detectan si el nodo contiene el token ID() directamente
  **o** si viene envuelto en functionCall().  
  Con esto vuelven a funcionar los ejemplos simples (p.ej. calcularArea).

El resto del archivo es idéntico al UPDATE #13:  
– soporte de ‘%’, asignaciones en encabezados loop, recursión, etc.
"""

from __future__ import annotations
from antlr4.tree.Tree import TerminalNodeImpl
from llvmlite import ir, binding as llvm

# ─────────────  host triple / datalayout  ─────────────
llvm.initialize(); llvm.initialize_native_target(); llvm.initialize_native_asmprinter()
HOST_TRIPLE     = llvm.get_default_triple()
HOST_DATALAYOUT = llvm.Target.from_default_triple().create_target_machine().target_data

# ─────────────  literal → RGB  ─────────────
COLORS = {
    "rojo": 0x00FF0000,  "verde": 0x0000FF00,  "azul": 0x000000FF,
    "amarillo": 0x00FFFF00, "cyan": 0x0000FFFF, "magenta": 0x00FF00FF,
    "blanco": 0x00FFFFFF,  "negro": 0x00000000, "marrón": 0x00800000,
}


# ╭────────────────────────────────────────────╮
# │                IRGenerator                 │
# ╰────────────────────────────────────────────╯
class IRGenerator:
    # ─────────────────────────────────────────
    def __init__(self, ast, symtab, parser):
        self.ast, self.symtab, self.parser = ast, symtab, parser

        # 1)  recolectar nombres de funciones
        self.fn_names: set[str] = set()
        self._collect_function_names(self.ast)

        # 2)  módulo LLVM
        self.module = ir.Module(name="vgraph")
        self.module.triple, self.module.data_layout = HOST_TRIPLE, HOST_DATALAYOUT

        # 3)  tipos básicos
        self.f64  = ir.DoubleType()
        self.i32  = ir.IntType(32)
        self.i1   = ir.IntType(1)
        self.void = ir.VoidType()

        # 4)  estado de construcción
        self.builder: ir.IRBuilder | None = None
        self.value_ptr: dict[str, ir.Value] = {}
        self._builder_stack: list[ir.IRBuilder] = []
        self._scope_stack:   list[dict[str, ir.Value]] = []

        # 5)  declaraciones y globales
        self._declare_runtime()
        self._codegen_globals()

    # ──────────── paso previo: nombres de funciones ────────────
    def _collect_function_names(self, node):
        if node.__class__.__name__ == "FunctionDeclStatementContext":
            self.fn_names.add(node.ID().getText())
        for i in range(getattr(node, "getChildCount", lambda: 0)()):
            self._collect_function_names(node.getChild(i))

    # ───────────── generate() ─────────────
    def generate(self) -> str:

        fn_main = ir.Function(self.module, ir.FunctionType(self.i32, ()), name="main")
        self.builder = ir.IRBuilder(fn_main.append_basic_block("entry"))
        self._visit(self.ast)
        self.builder.ret(ir.Constant(self.i32, 0))

        fn_wrap = ir.Function(self.module, fn_main.function_type, name="_main")
        bw = ir.IRBuilder(fn_wrap.append_basic_block("entry"))
        bw.ret(bw.call(fn_main, []))

        return str(self.module)

    # ───────────── runtime externals ─────────────
    def _declare_runtime(self):
        proto = {
            "vg_set_color":  (self.void, (self.i32,)),
            "vg_draw_pixel": (self.void, (self.i32, self.i32)),
            "vg_draw_circle":(self.void, (self.i32,)*3),
            "vg_draw_line":  (self.void, (self.i32,)*4),
            "vg_draw_rect":  (self.void, (self.i32,)*4),
            "vg_clear":      (self.void, ()),
            "vg_wait":       (self.void, (self.i32,)),
            "cos":           (self.f64,  (self.f64,)),
            "sin":           (self.f64,  (self.f64,)),
        }
        for n, (ret, params) in proto.items():
            if n not in self.module.globals:
                ir.Function(self.module, ir.FunctionType(ret, params), name=n)

    # ───────────── global vars ─────────────
    def _codegen_globals(self):
        for ident, info in self.symtab.get_all_symbols().get("global", {}).items():
            if ident in self.fn_names:          # ¡evitar colisión con funciones!
                continue
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

    # ───────────── visitor genérico ─────────────
    def _visit(self, node):
        h = getattr(self, f"_visit_{node.__class__.__name__}", None)
        if h:
            return h(node)
        res = None
        for i in range(getattr(node, "getChildCount", lambda: 0)()):
            res = res or self._visit(node.getChild(i))
        return res

    # ───────────── TERMINALES y expresiones básicas ─────────────
    def _visit_TerminalNodeImpl(self, tok):
        t = tok.getText()
        if t in ("true", "false"):
            return ir.Constant(self.i1, t == "true")
        if t in COLORS:
            return ir.Constant(self.i32, COLORS[t])
        if t.replace(".", "", 1).isdigit():
            return ir.Constant(self.f64, float(t))
        return None

    def _visit_NumberExprContext(self, ctx):    return ir.Constant(self.f64, float(ctx.getText()))
    def _visit_ColorExprContext (self, ctx):    return ir.Constant(self.i32, COLORS[ctx.getText()])
    def _visit_BoolConstExprContext(self, ctx): return ir.Constant(self.i1,  ctx.getText() == "true")

    def _visit_IdExprContext(self, ctx):
        name = ctx.getText()
        if name in COLORS and name not in self.value_ptr:
            return ir.Constant(self.i32, COLORS[name])
        return self.builder.load(self._get_ptr(name))

    def _visit_ParenExprContext(self, ctx): return self._visit(ctx.expr())
    def _visit_CosExprContext  (self, ctx): return self.builder.call(self.module.globals["cos"], [self._visit(ctx.expr())])
    def _visit_SinExprContext  (self, ctx): return self.builder.call(self.module.globals["sin"], [self._visit(ctx.expr())])

    # ───────────── operaciones aritméticas ─────────────
    def _binary(self, ctx):
        lhs = self._visit(ctx.getChild(0))
        rhs = self._visit(ctx.getChild(2))
        if lhs is None or rhs is None:
            lhs = lhs or self._const_zero(self.f64)
            rhs = rhs or self._const_zero(self.f64)
        return lhs, rhs

    def _visit_AddSubExprContext(self, ctx):
        lhs, rhs = self._binary(ctx)
        return self.builder.fsub(lhs, rhs) if ctx.MINUS() else self.builder.fadd(lhs, rhs)

    def _visit_MulDivExprContext(self, ctx):
        lhs, rhs = self._binary(ctx)
        op = ctx.getChild(1).getText()
        if op == "/":
            return self.builder.fdiv(lhs, rhs)
        if op == "%":                                 # soporte módulo
            lhs_i = self._round_to_i32(lhs)
            rhs_i = self._round_to_i32(rhs)
            rem_i = self.builder.srem(lhs_i, rhs_i)
            return self.builder.sitofp(rem_i, self.f64)
        return self.builder.fmul(lhs, rhs)

    def _visit_NegExprContext(self, ctx): return self.builder.fsub(ir.Constant(self.f64, 0.0), self._visit(ctx.getChild(1)))

    # comparaciones
    def _visit_ComparisonExprContext(self, ctx):
        lhs, rhs = self._binary(ctx)
        op = ctx.getChild(1).getText()
        cmap = {"==": "oeq", "!=": "one", "<": "olt", "<=": "ole", ">": "ogt", ">=": "oge"}
        return self.builder.fcmp_ordered(cmap[op], lhs, rhs)

    # booleanas
    def _visit_AndExprContext(self, ctx): lhs, rhs = self._binary(ctx); return self.builder.and_(lhs, rhs)
    def _visit_OrExprContext (self, ctx): lhs, rhs = self._binary(ctx); return self.builder.or_(lhs, rhs)
    def _visit_NotExprContext(self, ctx): return self.builder.xor(self._visit(ctx.boolExpr()), ir.Constant(self.i1, 1))
    def _visit_ParenBoolExprContext(self, ctx): return self._visit(ctx.boolExpr())
    def _visit_BoolIdExprContext  (self, ctx): return self.builder.load(self._get_ptr(ctx.getText()))

    # ───────────── asignaciones ─────────────
    def _handle_assignment(self, assign_ctx):
        name = assign_ctx.ID().getText()
        ptr  = self._get_ptr(name)
        dest_ty = ptr.type.pointee
        rhs_node = assign_ctx.getChild(assign_ctx.getChildCount() - 1)
        rhs_val  = self._visit(rhs_node) or self._const_zero(dest_ty)
        rhs_val  = self._coerce(rhs_val, dest_ty)
        self.builder.store(rhs_val, ptr)
        return rhs_val

    def _visit_AssignmentStatementContext(self, ctx): self._handle_assignment(ctx.assignmentExpression())
    def _visit_AssignmentExpressionContext(self, ctx): return self._handle_assignment(ctx)

    # ───────────── STATEMENTS NUEVOS ─────────────
    def _visit_ReturnStatementContext(self, ctx):
        """
        • Si la función es 'void' y no hay expresión → ret void
        • De momento todas las funciones de usuario son void.
          (Si el usuario escribe 'return expr;' simplemente lo ignoramos
           para no romper el IR; opcional: evalúa la expr para efectos
           colaterales.)
        """
        if ctx.expr():          # por ahora descartamos el valor
            self._visit(ctx.expr())          # -- side-effects
        if not self.builder.block.is_terminated:
            self.builder.ret_void()

    # ───────────── draw / clear / setcolor / wait ─────────────
    def _visit_SetColorStatementContext(self, ctx):
        raw = ctx.getChild(2)
        val = self._visit(raw) or self.builder.load(self._get_ptr(raw.getText()))
        self.builder.call(self.module.globals["vg_set_color"], [self._coerce(val, self.i32)])

    def _visit_ClearStatementContext(self, _ctx): self.builder.call(self.module.globals["vg_clear"], [])
    def _visit_WaitStatementContext (self, ctx):  self.builder.call(self.module.globals["vg_wait"],
                                                                    [self._round_to_i32(self._visit(ctx.expr()))])

    def _visit_DrawStatementContext(self, ctx):
        kind = ctx.drawObject().getChild(0).getText()
        fn = self.module.globals[f"vg_draw_{kind}"]
        args = [self._round_to_i32(self._visit(ch))
                for ch in ctx.drawObject().children
                if ch.__class__.__name__.endswith("ExprContext")]
        self.builder.call(fn, args)

    # ───────────── control: IF ─────────────
    def _visit_IfStatementContext(self, ctx):
        cond = self._coerce(self._visit(ctx.boolExpr()), self.i1)

        then_bb  = self.builder.function.append_basic_block("then")
        merge_bb = self.builder.function.append_basic_block("endif")
        else_bb  = self.builder.function.append_basic_block("else") if ctx.ELSE() else merge_bb

        self.builder.cbranch(cond, then_bb, else_bb)

        # THEN
        self.builder.position_at_start(then_bb)
        self._visit(ctx.block(0))
        if not self.builder.block.is_terminated:
            self.builder.branch(merge_bb)

        # ELSE (puede ser otro if en cascada)
        if ctx.ELSE():
            self.builder.position_at_start(else_bb)
            self._visit(ctx.getChild(ctx.getChildCount() - 1))
            if not self.builder.block.is_terminated:
                self.builder.branch(merge_bb)

        # MERGE
        if not merge_bb.is_terminated:
            self.builder.position_at_start(merge_bb)

    # ───────────── control: LOOP ─────────────
    def _visit_LoopStatementContext(self, ctx):
        self._visit(ctx.assignmentExpression(0))   # init
        f = self.builder.function
        cond_bb, body_bb, incr_bb, end_bb = [f.append_basic_block(n) for n in
                                             ("for.cond", "for.body", "for.incr", "for.end")]
        self.builder.branch(cond_bb)

        # cond
        self.builder.position_at_start(cond_bb)
        self.builder.cbranch(self._coerce(self._visit(ctx.boolExpr()), self.i1), body_bb, end_bb)

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

    # ───────────── funciones de usuario (void) ─────────────
    def _visit_FunctionDeclStatementContext(self, ctx):
        name = ctx.ID().getText()

        # eliminar global “basura” si se llamaba igual que la función
        g = self.module.globals.get(name)
        if g and not isinstance(g, ir.Function):
            del self.module.globals[name]
            self.value_ptr.pop(name, None)

        # parámetros
        params = [tok.getText() for tok in (ctx.paramList().ID() if ctx.paramList() else [])]
        fn_ty  = ir.FunctionType(self.void, (self.f64,) * len(params))
        fn     = ir.Function(self.module, fn_ty, name=name)

        # crear nuevo scope (stacks)
        entry = fn.append_basic_block("entry")
        self._builder_stack.append(self.builder)
        self.builder = ir.IRBuilder(entry)
        self._scope_stack.append(self.value_ptr)
        self.value_ptr = self.value_ptr.copy()

        # alocar slots para parámetros
        for i, p in enumerate(params):
            slot = self.builder.alloca(self.f64, name=p)
            self.builder.store(fn.args[i], slot)
            self.value_ptr[p] = slot

        # generar cuerpo
        self._visit(ctx.block())

        # si el cuerpo no terminó con return explícito → ret void implícito
        if not self.builder.block.is_terminated:
            self.builder.ret_void()

        # restaurar scopes
        self.value_ptr = self._scope_stack.pop()
        self.builder   = self._builder_stack.pop()

    # ───────────── llamadas de función ─────────────
    def _visit_FunctionCallStatementContext(self, ctx):
        # puede venir como ID(…) o functionCall() según la gramática usada
        if hasattr(ctx, "ID") and ctx.ID():                # gramática antigua
            name = ctx.ID().getText()
            args_ctx = ctx.argumentList()
        else:                                              # gramática nueva: functionCall()
            fc = ctx.functionCall()
            name = fc.ID().getText()
            args_ctx = fc.argumentList()

        fn = self.module.globals.get(name)
        if not isinstance(fn, ir.Function):
            return
        args = [self._visit(e) for e in (args_ctx.expr() if args_ctx else [])]
        self.builder.call(fn, args)

    def _visit_FunctionCallExprContext(self, ctx):
        if hasattr(ctx, "ID") and ctx.ID():
            name = ctx.ID().getText()
            args_ctx = ctx.argumentList()
        else:
            fc = ctx.functionCall()
            name = fc.ID().getText()
            args_ctx = fc.argumentList()

        fn = self.module.globals.get(name)
        if not isinstance(fn, ir.Function):
            return ir.Constant(self.f64, 0.0)
        args = [self._visit(e) for e in (args_ctx.expr() if args_ctx else [])]
        self.builder.call(fn, args)
        return None  # funciones usuario → void

    # ───────────── helpers ─────────────
    def _coerce(self, val: ir.Value | None, target_ty: ir.Type) -> ir.Value:
        if val is None:
            return self._const_zero(target_ty)
        if val.type == target_ty:
            return val

        # → i1
        if target_ty is self.i1:
            if val.type is self.f64:
                return self.builder.fcmp_ordered("one", val, ir.Constant(self.f64, 0.0))
            if val.type is self.i32:
                return self.builder.icmp_unsigned("ne", val, ir.Constant(self.i32, 0))

        # → i32
        if target_ty is self.i32:
            if val.type is self.f64:
                return self._round_to_i32(val)
            if val.type is self.i1:
                return self.builder.zext(val, self.i32)

        # → f64
        if target_ty is self.f64:
            if val.type is self.i32:
                return self.builder.sitofp(val, self.f64)
            if val.type is self.i1:
                return self.builder.uitofp(val, self.f64)

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
        if ptr:
            return ptr

        if name in self.fn_names:          # no crear variable homónima a función
            return ir.Undef(self.f64)      # valor “vacío”

        # local dentro de función
        if (
            self.builder
            and self.builder.block
            and self.builder.function.name != "main"
        ):
            entry = self.builder.function.entry_basic_block
            with self.builder.goto_block(entry):
                slot = self.builder.alloca(self.f64, name=name)
                slot.initializer = ir.Constant(self.f64, 0.0)
            self.value_ptr[name] = slot
            return slot

        # global implícito
        g = ir.GlobalVariable(self.module, self.f64, name)
        g.initializer = ir.Constant(self.f64, 0.0)
        self.value_ptr[name] = g
        return g