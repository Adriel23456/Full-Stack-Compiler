"""
Utilidades para trabajar con el AST de ANTLR
"""
from antlr4.tree.Trees import Trees

def get_node_text(node, parser):
    """Obtiene el texto de un nodo en el árbol sintáctico"""
    if node.getChildCount() == 0:
        return node.getText()
    return Trees.getNodeText(node, parser.ruleNames)

def print_ast(tree, parser, indent=0):
    """Imprime un árbol sintáctico con indentación para visualización"""
    if not tree:
        return "AST vacío"
    
    result = "  " * indent + get_node_text(tree, parser) + "\n"
    
    for i in range(tree.getChildCount()):
        result += print_ast(tree.getChild(i), parser, indent + 1)
    
    return result

def get_rule_name(node, parser):
    """Obtiene el nombre de la regla para un nodo"""
    if node.getChildCount() == 0:
        return None  # Terminal node
    return parser.ruleNames[node.getRuleIndex()]

def get_node_line(node):
    """Obtiene el número de línea de un nodo"""
    if hasattr(node, 'start') and node.start:
        return node.start.line
    return 0

def get_node_column(node):
    """Obtiene el número de columna de un nodo"""
    if hasattr(node, 'start') and node.start:
        return node.start.column
    return 0

def get_text(node):
    """Obtiene el texto de un nodo terminal"""
    return node.getText() if node else ""

def is_terminal(node):
    """Determina si un nodo es terminal"""
    return node.getChildCount() == 0

def find_node_by_rule(tree, parser, rule_name):
    """Encuentra todos los nodos que coinciden con un nombre de regla específico"""
    result = []
    
    if not is_terminal(tree) and get_rule_name(tree, parser) == rule_name:
        result.append(tree)
    
    for i in range(tree.getChildCount()):
        result.extend(find_node_by_rule(tree.getChild(i), parser, rule_name))
    
    return result