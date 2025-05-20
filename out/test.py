from llvmlite import binding as llvm
import ctypes, math

# 1) Carga el IR que acabas de escribir
with open("out/vGraph.ll") as f:
    ir_text = f.read()

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

mod = llvm.parse_assembly(ir_text)
mod.verify()

# 2) Crea un EE MCJIT e invoca _main
target = llvm.Target.from_default_triple()
tm      = target.create_target_machine()
backing = llvm.create_mcjit_compiler(mod, tm)
backing.finalize_object()

_main = backing.get_function_address("_main")
ctypes.CFUNCTYPE(None)(_main)()        # ← ejecuta

# 3) Lee los globals para ver si quedó todo bien
def load_double(name):
    addr = backing.get_global_value_address(name)
    return ctypes.c_double.from_address(addr).value

def load_i1(name):
    addr = backing.get_global_value_address(name)
    return bool(ctypes.c_uint8.from_address(addr).value)

print("a1 =", load_i1("a1"))           # True
print("b1 =", load_i1("b1"))           # True
print("c1 =", load_i1("c1"))           # False
print("c  =", hex(ctypes.c_uint32.from_address(
        backing.get_global_value_address("c")).value))  # 0x00ff0000
print("x  =", load_double("x"))        # 8.0