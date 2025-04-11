"""
Versión modificada del generador de código LLVM para compatibilidad con Windows.
Esta versión genera un archivo objeto directamente en lugar de código ensamblador.
"""

import llvmlite.ir as ir
import llvmlite.binding as llvm
import os
import platform
import ctypes
from collections import defaultdict

# Inicializar LLVM
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

class LLVMCodeGenerator:
    def __init__(self):
        # Crear un módulo LLVM
        self.module = ir.Module(name="programa")
        
        # Detectar sistema operativo para configurar target triple
        if platform.system() == "Windows":
            # Target triple para Windows con MinGW
            self.module.triple = "x86_64-pc-windows-gnu"
        else:
            # Target triple para Linux/macOS
            self.module.triple = llvm.get_default_triple()
        
        # Crear el tipo para enteros y valores booleanos
        self.int_type = ir.IntType(32)  # Enteros de 32 bits
        self.double_type = ir.DoubleType()  # Punto flotante
        self.void_type = ir.VoidType()  # Tipo void para funciones sin retorno
        self.bool_type = ir.IntType(1)  # Booleanos como enteros de 1 bit
        
        # Inicializar el constructor de funciones
        self.func_count = 0  # Contador para funciones anónimas
        
        # Tabla de símbolos para seguimiento de variables
        self.symbol_table = {}
        
        # Tabla para almacenar bloques de salida en bucles y condicionales
        self.exit_blocks = {}
        
        # Preparar la función printf para imprimir valores
        self._declare_printf_function()
        
        # Crear la función principal
        self._create_main_function()
    
    def _declare_printf_function(self):
        """Declara la función printf del sistema para poder usarla en el código generado"""
        # Crear el tipo de printf (retorna int, recibe un puntero a char y argumentos variables)
        printf_ty = ir.FunctionType(self.int_type, [ir.IntType(8).as_pointer()], var_arg=True)
        # Declarar la función printf en el módulo
        self.printf = ir.Function(self.module, printf_ty, name="printf")
    
    def _create_main_function(self):
        """Crea la función main del programa"""
        # Tipo de la función main (retorna int, sin argumentos)
        main_ty = ir.FunctionType(self.int_type, [])
        # Crear la función main en el módulo
        self.main_func = ir.Function(self.module, main_ty, name="main")
        # Crear el bloque de entrada de la función main
        self.entry_block = self.main_func.append_basic_block(name="entry")
        # Crear el constructor de IR para este bloque
        self.builder = ir.IRBuilder(self.entry_block)
        # Bloque actual donde se está insertando código
        self.current_block = self.entry_block
    
    def generate(self, ast):
        """Genera código LLVM IR a partir del AST"""
        # Generar código a partir del AST
        self._codegen(ast)
        
        # Añadir return 0 al final de main
        self.builder.ret(ir.Constant(self.int_type, 0))
        
        # Verificar que el módulo LLVM sea válido
        return str(self.module)
    
    def compile_to_object(self, output_file):
        """
        Compila el código LLVM directamente a un archivo objeto (.obj o .o)
        sin pasar por un archivo de ensamblador intermedio.
        """
        # Crear un motor de ejecución LLVM
        llvm_ir = str(self.module)
        mod = llvm.parse_assembly(llvm_ir)
        mod.verify()
        
        # Configurar target para el sistema actual
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        
        # Optimizar el módulo
        pmb = llvm.create_pass_manager_builder()
        pmb.opt_level = 2  # Nivel de optimización (0-3)
        pass_manager = llvm.create_module_pass_manager()
        pmb.populate(pass_manager)
        pass_manager.run(mod)
        
        # Generar código objeto directamente
        with open(output_file, 'wb') as f:
            f.write(target_machine.emit_object(mod))
        
        return True
    
    def _codegen(self, node):
        """Genera código LLVM IR para un nodo del AST"""
        if node is None:
            return None
        
        # Determinar tipo de nodo y llamar al método correspondiente
        if isinstance(node, tuple):
            node_type = node[0]
            
            if node_type == 'program':
                return self._codegen_program(node)
            elif node_type == 'assign':
                return self._codegen_assign(node)
            elif node_type == 'binop':
                return self._codegen_binop(node)
            elif node_type == 'relop':
                return self._codegen_relop(node)
            elif node_type == 'number':
                return self._codegen_number(node)
            elif node_type == 'id':
                return self._codegen_id(node)
            elif node_type == 'print':
                return self._codegen_print(node)
            elif node_type == 'if':
                return self._codegen_if(node)
            elif node_type == 'for':
                return self._codegen_for(node)
        
        elif isinstance(node, list):
            # Generar código para cada elemento de la lista
            last_val = None
            for item in node:
                last_val = self._codegen(item)
            return last_val
        
        # Si no se reconoce el tipo de nodo, devolver None
        return None
    
    def _codegen_program(self, node):
        """Genera código para el nodo raíz del programa"""
        # El programa es una lista de declaraciones, generamos código para cada una
        return self._codegen(node[1])
    
    def _codegen_assign(self, node):
        """Genera código para una asignación"""
        var_name = node[1]
        expr_val = self._codegen(node[2])
        
        # Si la variable no existe, crearla
        if var_name not in self.symbol_table:
            # Crear una variable en el stack
            var_ptr = self.builder.alloca(self.int_type, name=var_name)
            self.symbol_table[var_name] = var_ptr
        
        # Almacenar el valor en la variable
        self.builder.store(expr_val, self.symbol_table[var_name])
        return expr_val
    
    def _codegen_binop(self, node):
        """Genera código para una operación binaria"""
        op = node[1]
        left = self._codegen(node[2])
        right = self._codegen(node[3])
        
        if op == '+':
            return self.builder.add(left, right, name="addtmp")
        elif op == '-':
            return self.builder.sub(left, right, name="subtmp")
        elif op == '*':
            return self.builder.mul(left, right, name="multmp")
        elif op == '/':
            # Asumimos división entera
            return self.builder.sdiv(left, right, name="divtmp")
    
    def _codegen_relop(self, node):
        """Genera código para una operación relacional"""
        op = node[1]
        left = self._codegen(node[2])
        right = self._codegen(node[3])
        
        if op == '<':
            return self.builder.icmp_signed('<', left, right, name="cmptmp")
        elif op == '>':
            return self.builder.icmp_signed('>', left, right, name="cmptmp")
        elif op == '<=':
            return self.builder.icmp_signed('<=', left, right, name="cmptmp")
        elif op == '>=':
            return self.builder.icmp_signed('>=', left, right, name="cmptmp")
        elif op == '==':
            return self.builder.icmp_signed('==', left, right, name="cmptmp")
        elif op == '!=':
            return self.builder.icmp_signed('!=', left, right, name="cmptmp")
    
    def _codegen_number(self, node):
        """Genera código para un número literal"""
        return ir.Constant(self.int_type, node[1])
    
    def _codegen_id(self, node):
        """Genera código para acceder a una variable"""
        var_name = node[1]
        if var_name not in self.symbol_table:
            # Error: variable no definida
            raise ValueError(f"Variable '{var_name}' no definida")
        
        # Cargar el valor de la variable
        return self.builder.load(self.symbol_table[var_name], name=var_name)
    
    def _codegen_print(self, node):
        """Genera código para imprimir un valor"""
        # Obtener el valor a imprimir
        expr_val = self._codegen(node[1])
        
        # Crear un formato para printf ("%d\n")
        fmt = "%d\n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), 
                          bytearray(fmt.encode("utf8")))
        fmt_ptr = self.builder.alloca(c_fmt.type)
        self.builder.store(c_fmt, fmt_ptr)
        
        # Convertir el puntero de array a puntero de char
        void_ptr = self.builder.gep(fmt_ptr, [
            ir.Constant(ir.IntType(32), 0),
            ir.Constant(ir.IntType(32), 0)
        ], name="fmt_ptr")
        
        # Llamar a printf
        return self.builder.call(self.printf, [void_ptr, expr_val], name="printf_call")
    
    def _codegen_if(self, node):
        """Genera código para una estructura if-elif-else"""
        cond_val = self._codegen(node[1])
        
        # Crear bloques para if, else y continuación
        if_then_block = self.builder.append_basic_block(f"if.then.{self.func_count}")
        merge_block = self.builder.append_basic_block(f"if.end.{self.func_count}")
        
        if node[4]:  # Hay un bloque else
            if_else_block = self.builder.append_basic_block(f"if.else.{self.func_count}")
            self.builder.cbranch(cond_val, if_then_block, if_else_block)
        elif node[3]:  # Hay un bloque elif
            if_elif_block = self.builder.append_basic_block(f"if.elif.{self.func_count}")
            self.builder.cbranch(cond_val, if_then_block, if_elif_block)
        else:  # Solo hay un bloque if
            self.builder.cbranch(cond_val, if_then_block, merge_block)
        
        # Generar código para el bloque if
        self.builder.position_at_end(if_then_block)
        self._codegen(node[2])  # Cuerpo del if
        self.builder.branch(merge_block)
        
        # Generar código para el bloque elif si existe
        if node[3]:
            self.builder.position_at_end(if_elif_block)
            elif_cond = self._codegen(node[3][1])  # Condición del elif
            
            if node[4]:  # Hay un bloque else después del elif
                self.builder.cbranch(elif_cond, if_else_block, merge_block)
                
                # Generar código para el bloque elif
                if_else_block = self.builder.append_basic_block(f"if.elif.then.{self.func_count}")
                self.builder.position_at_end(if_else_block)
                self._codegen(node[3][2])  # Cuerpo del elif
                self.builder.branch(merge_block)
                
                # Generar código para el bloque else
                self.builder.position_at_end(if_else_block)
                self._codegen(node[4])  # Cuerpo del else
                self.builder.branch(merge_block)
            else:
                # No hay else, solo elif
                elif_then_block = self.builder.append_basic_block(f"if.elif.then.{self.func_count}")
                self.builder.cbranch(elif_cond, elif_then_block, merge_block)
                
                # Generar código para el bloque elif
                self.builder.position_at_end(elif_then_block)
                self._codegen(node[3][2])  # Cuerpo del elif
                self.builder.branch(merge_block)
        
        # Generar código para el bloque else si existe y no hay elif
        elif node[4]:
            self.builder.position_at_end(if_else_block)
            self._codegen(node[4])  # Cuerpo del else
            self.builder.branch(merge_block)
        
        # Continuar desde el bloque de merge
        self.builder.position_at_end(merge_block)
        self.func_count += 1
        return None
    
    def _codegen_for(self, node):
        """Genera código para un bucle for"""
        var_name = node[1]
        range_end = self._codegen(node[2])
        
        # Crear variable de iteración si no existe
        if var_name not in self.symbol_table:
            var_ptr = self.builder.alloca(self.int_type, name=var_name)
            self.symbol_table[var_name] = var_ptr
        
        # Inicializar variable de iteración a 0
        init_val = ir.Constant(self.int_type, 0)
        self.builder.store(init_val, self.symbol_table[var_name])
        
        # Crear bloques para el bucle
        loop_cond_block = self.builder.append_basic_block(f"for.cond.{self.func_count}")
        loop_body_block = self.builder.append_basic_block(f"for.body.{self.func_count}")
        loop_inc_block = self.builder.append_basic_block(f"for.inc.{self.func_count}")
        loop_end_block = self.builder.append_basic_block(f"for.end.{self.func_count}")
        
        # Saltar al bloque de condición
        self.builder.branch(loop_cond_block)
        
        # Generar código para la condición del bucle
        self.builder.position_at_end(loop_cond_block)
        var_val = self.builder.load(self.symbol_table[var_name], name=var_name)
        cond_val = self.builder.icmp_signed('<', var_val, range_end, name="for.cond")
        self.builder.cbranch(cond_val, loop_body_block, loop_end_block)
        
        # Generar código para el cuerpo del bucle
        self.builder.position_at_end(loop_body_block)
        self._codegen(node[3])  # Cuerpo del for
        self.builder.branch(loop_inc_block)
        
        # Generar código para incrementar la variable de iteración
        self.builder.position_at_end(loop_inc_block)
        var_val = self.builder.load(self.symbol_table[var_name], name=var_name)
        inc_val = self.builder.add(var_val, ir.Constant(self.int_type, 1), name="inc")
        self.builder.store(inc_val, self.symbol_table[var_name])
        self.builder.branch(loop_cond_block)
        
        # Continuar desde el bloque de fin del bucle
        self.builder.position_at_end(loop_end_block)
        self.func_count += 1
        return None


# Función para compilar directamente a un ejecutable
def compile_to_executable(ast, output_file, input_file=None):
    """
    Compila el AST directamente a un ejecutable para Windows.
    
    Args:
        ast: El árbol de sintaxis abstracta del programa
        output_file: Archivo ejecutable de salida
        input_file: Archivo fuente original (opcional, para referencia)
    
    Returns:
        bool: True si la compilación fue exitosa, False en caso contrario
    """
    import subprocess
    import tempfile
    import os
    
    try:
        # Crear un archivo objeto temporal
        obj_file = f"{output_file}.obj" if output_file else "temp.obj"
        
        # Generar el código objeto directamente
        code_gen = LLVMCodeGenerator()
        code_gen.generate(ast)
        code_gen.compile_to_object(obj_file)
        
        # Enlazar para crear un ejecutable
        linker_cmd = ['gcc', obj_file, '-o', output_file]
        
        print(f"Ejecutando: {' '.join(linker_cmd)}")
        result = subprocess.run(linker_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error al enlazar: {result.stderr}")
            return False
        
        # Limpieza de archivos temporales
        if os.path.exists(obj_file):
            os.remove(obj_file)
            
        return True
        
    except Exception as e:
        print(f"Error en la compilación: {e}")
        return False