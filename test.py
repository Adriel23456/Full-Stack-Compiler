from lark import Lark, Tree
from lark.lexer import Token
import os
# -*- coding: utf-8 -*-

# Define the complex grammar in Lark format
grammar = r'''
start: program
program: "program" ID "{" sentence* "}"
sentence: println | conditional | var_decl | var_assign
    
println: "println" expression ";"
conditional: "if" "(" expression ")" "{" sentence* "}" "else" "{" sentence* "}"
    
var_decl: "var" ID ";"
var_assign: ID "=" expression ";"
    
expression: factor (op factor)* | "mutGen" "(" binary_array "," expression "," expression ")"
    
op: "+" | "-" | "&&" | "||"
    
factor: comp (factor_op comp)*
factor_op: "*" | "/"
    
comp: "|-" term | "|-" "(" expression ")" | term
    
term: NUMBER | BOOLEAN | ID | "(" expression ")"
    
binary_array: "[" binary_term ("," binary_term)* "]"
binary_term: BINARY

// Terminals
BOOLEAN: "true" | "false"
BINARY: /0b[0-1]+/
ID: /[a-zA-Z_][a-zA-Z0-9_]*/
NUMBER: /[0-9]+((\.|,)[0-9]+)?/

// Skip whitespace
%import common.WS
%ignore WS
'''

# Sample program in this language
input_text = '''
program myProgram {
    var x;
    x = 10;
    if (x) {
        println x;
    } else {
        println 20;
    }
    println |-5;
    println mutGen([0b101, 0b110], 0.5, 3);
}
'''

# Create parser with explicit lexer to access tokens
parser = Lark(grammar, parser='earley')

# Function to get tokens
def get_tokens(text, grammar_def):
    lexer_parser = Lark(grammar_def, parser='earley')
    tokens = list(lexer_parser.lex(text))
    return tokens

try:
    # Get and display token stream
    tokens = get_tokens(input_text, grammar)
    print("--- TOKEN STREAM ---")
    for i, token in enumerate(tokens):
        print(f"Token {i}: Type={token.type}, Value='{token.value}'")
    print("-------------------\n")

    # Parse the tree
    tree = parser.parse(input_text)
    
    # Simple text visualization
    print("--- PARSE TREE ---")
    print(tree.pretty())
    print("-----------------\n")
    
    # For graphical visualization, use pydot and graphviz
    import pydot
    
    def find_node_by_path(tree, path):
        """Find a node by following a path of indices from the root."""
        current = tree
        for idx in path:
            if hasattr(current, 'children') and idx < len(current.children):
                current = current.children[idx]
            else:
                return None
        return current
    
    def find_nodes_by_type(tree, node_type):
        """Find all nodes of a specific type in the tree."""
        result = []
        
        def search(node, path):
            if isinstance(node, Tree) and node.data == node_type:
                result.append((path[:], node))
            
            if hasattr(node, 'children'):
                for i, child in enumerate(node.children):
                    path.append(i)
                    search(child, path)
                    path.pop()
        
        search(tree, [])
        return result
    
    def visualize_tree(tree, filename="parse_tree.png", highlight_paths=None, highlight_types=None, max_depth=None):
        graph = pydot.Dot(graph_type='graph', rankdir='TB')
        
        # Node tracking for highlighting
        all_nodes = {}
        
        # Add root node
        root_node = pydot.Node("root", shape="ellipse", label=str(tree.data))
        graph.add_node(root_node)
        all_nodes[()] = root_node
        
        # Recursively add children
        def add_children(parent_node, node_name, children, path, depth=0):
            if max_depth is not None and depth >= max_depth:
                # Add ellipsis node if we hit max depth
                ellipsis_id = f"{node_name}_ellipsis"
                ellipsis_node = pydot.Node(ellipsis_id, shape="plaintext", label="...")
                graph.add_node(ellipsis_node)
                graph.add_edge(pydot.Edge(parent_node, ellipsis_node))
                return
                
            for i, child in enumerate(children):
                current_path = path + [i]
                
                if isinstance(child, Tree):  # Tree node
                    child_id = f"{node_name}_{i}"
                    # Check if this node should be highlighted
                    highlight = False
                    if highlight_paths and current_path in highlight_paths:
                        highlight = True
                    if highlight_types and child.data in highlight_types:
                        highlight = True
                    
                    # Set node attributes
                    node_attrs = {
                        'shape': 'ellipse',
                        'label': str(child.data),
                    }
                    
                    # Add highlighting if needed
                    if highlight:
                        node_attrs['style'] = 'filled'
                        node_attrs['fillcolor'] = 'lightblue'
                        node_attrs['penwidth'] = '2.0'
                    
                    child_node = pydot.Node(child_id, **node_attrs)
                    graph.add_node(child_node)
                    graph.add_edge(pydot.Edge(parent_node, child_node))
                    all_nodes[tuple(current_path)] = child_node
                    
                    # Process this node's children
                    add_children(child_node, child_id, child.children, current_path, depth+1)
                else:  # Token
                    child_id = f"{node_name}_token_{i}"
                    
                    # Check if this token should be highlighted
                    highlight = False
                    if highlight_paths and current_path in highlight_paths:
                        highlight = True
                    
                    # Set node attributes
                    node_attrs = {
                        'shape': 'box',
                        'label': f"{child.type}: '{child.value}'",
                    }
                    
                    # Add highlighting if needed
                    if highlight:
                        node_attrs['style'] = 'filled'
                        node_attrs['fillcolor'] = 'lightyellow'
                        node_attrs['penwidth'] = '2.0'
                    
                    child_node = pydot.Node(child_id, **node_attrs)
                    graph.add_node(child_node)
                    graph.add_edge(pydot.Edge(parent_node, child_node))
                    all_nodes[tuple(current_path)] = child_node
        
        add_children(root_node, "root", tree.children, [], 0)
        
        # Save the graph
        graph.write_png(filename)
        print(f"Visualization saved to {os.path.abspath(filename)}")
        
        return all_nodes
    
    # Find interesting nodes for highlighting
    expression_nodes = find_nodes_by_type(tree, 'expression')
    var_nodes = find_nodes_by_type(tree, 'var_decl')
    println_nodes = find_nodes_by_type(tree, 'println')
    
    print(f"Found {len(expression_nodes)} expression nodes in the tree")
    print(f"Found {len(var_nodes)} var_decl nodes in the tree")
    print(f"Found {len(println_nodes)} println nodes in the tree")
    
    # Generate visualization of the entire tree (with depth limit for clarity)
    visualize_tree(tree, "full_parse_tree.png", max_depth=10)
    
    # Highlight specific parts of the tree
    paths_to_highlight = []
    if var_nodes:
        paths_to_highlight.append(var_nodes[0][0])  # First var_decl
    if println_nodes:
        paths_to_highlight.append(println_nodes[0][0])  # First println
    
    # Example: Highlight specific node types
    types_to_highlight = ['expression', 'term']
    
    # Generate visualization with highlighted nodes
    visualize_tree(tree, "highlighted_parse_tree.png", 
                  highlight_paths=paths_to_highlight,
                  highlight_types=types_to_highlight,
                  max_depth=10)
    
    # Visualize token stream as a graph
    def visualize_tokens(tokens, filename="token_stream.png"):
        graph = pydot.Dot(graph_type='digraph', rankdir='LR')
        
        prev_node = None
        for i, token in enumerate(tokens):
            # Skip whitespace tokens
            if token.type == 'WS':
                continue
                
            # Create a node for this token
            node_id = f"token_{i}"
            node_label = f"{token.type}\n'{token.value}'"
            
            # Coloring by token type
            color = "#FFFFFF"  # Default white
            if token.type in ['PROGRAM', 'VAR', 'PRINTLN', 'IF', 'ELSE', 'MUTGEN']:
                color = "#FFD580"  # Light orange for keywords
            elif token.value in ['+', '-', '*', '/', '&&', '||', '=']:
                color = "#ADD8E6"  # Light blue for operators
            elif token.type in ['NUMBER', 'BOOLEAN', 'BINARY']:
                color = "#90EE90"  # Light green for literals
            elif token.type == 'ID':
                color = "#FFC0CB"  # Light pink for identifiers
            
            token_node = pydot.Node(node_id, 
                                   shape="box", 
                                   label=node_label,
                                   style="filled",
                                   fillcolor=color)
            graph.add_node(token_node)
            
            # Connect to previous token
            if prev_node:
                graph.add_edge(pydot.Edge(prev_node, token_node))
            
            prev_node = token_node
        
        # Save the graph
        graph.write_png(filename)
        print(f"Token stream visualization saved to {os.path.abspath(filename)}")
    
    # Generate token stream visualization
    visualize_tokens(tokens)
    
    # Generate detailed view of specific subtrees
    if expression_nodes:
        # Get the first expression node
        first_expr_path, first_expr = expression_nodes[0]
        
        # Create a detailed visualization of just this subtree
        expr_graph = pydot.Dot(graph_type='graph')
        
        # Create root node for this subtree
        expr_root = pydot.Node("expr_root", shape="ellipse", label="expression", style="filled", fillcolor="lightblue")
        expr_graph.add_node(expr_root)
        
        # Helper function to add this specific subtree
        def add_expr_children(parent_node, node_name, node):
            if isinstance(node, Tree):
                for i, child in enumerate(node.children):
                    child_id = f"{node_name}_{i}"
                    
                    if isinstance(child, Tree):
                        child_node = pydot.Node(child_id, shape="ellipse", label=str(child.data))
                        expr_graph.add_node(child_node)
                        expr_graph.add_edge(pydot.Edge(parent_node, child_node))
                        add_expr_children(child_node, child_id, child)
                    else:  # Token
                        child_node = pydot.Node(child_id, shape="box", label=f"{child.type}: '{child.value}'")
                        expr_graph.add_node(child_node)
                        expr_graph.add_edge(pydot.Edge(parent_node, child_node))
        
        # Add children of the expression node
        add_expr_children(expr_root, "expr", first_expr)
        
        # Save the expression subtree visualization
        expr_graph.write_png("expression_subtree.png")
        print(f"Expression subtree visualization saved to {os.path.abspath('expression_subtree.png')}")
        
    # Sección para visualizar tabla de parseo, FIRST y FOLLOW sets
    def compute_first_follow_sets(grammar_text):
        """Calcula los conjuntos FIRST y FOLLOW para la gramática dada"""
        from collections import defaultdict
        import re
        
        # Extraer reglas de producción de la gramática
        lines = grammar_text.strip().split('\n')
        productions = {}
        non_terminals = set()
        terminals = set()
        
        # Paso 1: Extraer producciones y símbolos
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//') or line.startswith('%'):
                continue
                
            # Extraer reglas de producción
            if ':' in line:
                lhs, rhs = line.split(':', 1)
                lhs = lhs.strip()
                if lhs not in productions:
                    productions[lhs] = []
                
                # Manejar múltiples alternativas
                alternatives = rhs.split('|')
                for alt in alternatives:
                    alt = alt.strip()
                    if alt:
                        # Extraer símbolos de la producción
                        symbols = []
                        tokens = re.findall(r'("[^"]*"|\S+)', alt)
                        for token in tokens:
                            if token.startswith('"') and token.endswith('"'):
                                # Terminal literal
                                terminal = token.strip('"')
                                terminals.add(terminal)
                                symbols.append(terminal)
                            elif token not in ['(', ')', '*', '+', '?', '{', '}']:
                                # No-terminal o terminal nombrado
                                symbols.append(token)
                                if token[0].islower() or token == 'start':
                                    non_terminals.add(token)
                                else:
                                    terminals.add(token)
                        
                        productions[lhs].append(symbols)
                
                non_terminals.add(lhs)
        
        # Inicializar conjuntos FIRST y FOLLOW
        first = defaultdict(set)
        follow = defaultdict(set)
        
        # Inicializar FIRST para terminales
        for terminal in terminals:
            first[terminal] = {terminal}
        
        # Calcular conjuntos FIRST
        changed = True
        while changed:
            changed = False
            for lhs, rhs_list in productions.items():
                for rhs in rhs_list:
                    if not rhs:  # Producción vacía
                        if '' not in first[lhs]:
                            first[lhs].add('')
                            changed = True
                        continue
                    
                    # Manejar el primer símbolo
                    symbol = rhs[0]
                    # Si es un terminal, añadirlo a FIRST
                    if symbol in terminals:
                        if symbol not in first[lhs]:
                            first[lhs].add(symbol)
                            changed = True
                    else:  # No-terminal
                        # Añadir todos los elementos de FIRST[symbol] excepto ε a FIRST[lhs]
                        for item in first[symbol] - {''}:
                            if item not in first[lhs]:
                                first[lhs].add(item)
                                changed = True
                        
                        # Manejar cadenas de no-terminales que pueden derivar ε
                        all_nullable = '' in first[symbol]
                        i = 1
                        while all_nullable and i < len(rhs):
                            symbol = rhs[i]
                            if symbol in terminals:
                                if symbol not in first[lhs]:
                                    first[lhs].add(symbol)
                                    changed = True
                                all_nullable = False
                            else:
                                for item in first[symbol] - {''}:
                                    if item not in first[lhs]:
                                        first[lhs].add(item)
                                        changed = True
                                all_nullable = all_nullable and '' in first[symbol]
                            i += 1
                        
                        # Si todos los símbolos son anulables, añadir ε a FIRST[lhs]
                        if all_nullable and '' not in first[lhs]:
                            first[lhs].add('')
                            changed = True
        
        # Inicializar FOLLOW para el símbolo inicial
        follow['start'].add('$')  # $ representa el fin de entrada
        
        # Calcular conjuntos FOLLOW
        changed = True
        while changed:
            changed = False
            for lhs, rhs_list in productions.items():
                for rhs in rhs_list:
                    for i, symbol in enumerate(rhs):
                        # Solo nos interesan los no-terminales
                        if symbol not in non_terminals:
                            continue
                        
                        # Si es el último símbolo o los siguientes pueden derivar ε
                        if i == len(rhs) - 1:
                            # FOLLOW[A] ⊆ FOLLOW[lhs]
                            for item in follow[lhs]:
                                if item not in follow[symbol]:
                                    follow[symbol].add(item)
                                    changed = True
                        else:
                            # Próximo símbolo
                            next_symbol = rhs[i + 1]
                            
                            # FIRST[next_symbol] - {ε} ⊆ FOLLOW[symbol]
                            if next_symbol in terminals:
                                if next_symbol not in follow[symbol]:
                                    follow[symbol].add(next_symbol)
                                    changed = True
                            else:
                                for item in first[next_symbol] - {''}:
                                    if item not in follow[symbol]:
                                        follow[symbol].add(item)
                                        changed = True
                                
                                # Si next_symbol puede derivar ε
                                if '' in first[next_symbol]:
                                    # FOLLOW[lhs] ⊆ FOLLOW[symbol]
                                    for item in follow[lhs]:
                                        if item not in follow[symbol]:
                                            follow[symbol].add(item)
                                            changed = True
        
        # Importante: devolver también el diccionario de producciones
        return first, follow, non_terminals, terminals, productions

    def visualize_parsing_table(grammar_text, parser, input_text, filename="parsing_table.png"):
        """Visualiza una tabla de parseo predictivo LL(1) para la gramática dada"""
        import pydot
        import re
        
        # Obtener conjuntos FIRST, FOLLOW y producciones
        first, follow, non_terminals, terminals, productions = compute_first_follow_sets(grammar_text)
        
        # Visualizamos FIRST y FOLLOW
        print("\n--- FIRST SETS ---")
        for nt in sorted(non_terminals):
            print(f"FIRST({nt}) = {{{', '.join(sorted(first[nt]))}}}")
        
        print("\n--- FOLLOW SETS ---")
        for nt in sorted(non_terminals):
            print(f"FOLLOW({nt}) = {{{', '.join(sorted(follow[nt]))}}}")
        
        # Filtramos los terminales para obtener solo los símbolos reales
        real_terminals = set()
        for term in terminals:
            if not term.startswith('/') and term not in ['', ' ']:
                real_terminals.add(term)
        
        # Añadimos $ como terminal para fin de entrada
        real_terminals.add('$')
        
        # Crear la tabla LL(1) con las producciones
        # Esta es la tabla M en el formato que mostraste
        from PIL import Image, ImageDraw, ImageFont
        import os
        
        def create_table_image(filename, title, non_terminals, terminals, table_data, cell_width=120, cell_height=50):
            # Calcular dimensiones de la tabla
            num_cols = len(terminals) + 1  # +1 para la columna de no-terminales
            num_rows = len(non_terminals) + 1  # +1 para la fila de encabezado
            width = cell_width * num_cols
            height = cell_height * num_rows + 50  # Espacio para título
            
            # Crear imagen con fondo blanco
            img = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(img)
            
            # Intentar cargar una fuente
            try:
                font_path = 'C:\\Windows\\Fonts\\Arial.ttf'
                title_font = ImageFont.truetype(font_path, 16)
                header_font = ImageFont.truetype(font_path, 12)
                cell_font = ImageFont.truetype(font_path, 10)
            except:
                title_font = ImageFont.load_default()
                header_font = ImageFont.load_default()
                cell_font = ImageFont.load_default()
            
            # Dibujar título
            draw.rectangle([(0, 0), (width, 50)], fill='#4B6082')
            draw.text((width//2, 25), title, fill='white', font=title_font, anchor='mm')
            
            # Dibujar encabezado especial para la esquina superior izquierda
            x1, y1 = 0, 50
            x2, y2 = cell_width, 50 + cell_height
            draw.rectangle([(x1, y1), (x2, y2)], fill='#D0D0D0', outline='black')
            draw.line([(x1, y1), (x2, y2)], fill='black', width=1)  # Diagonal line
            draw.text((x1 + 20, y1 + 15), "N", fill='black', font=header_font)
            draw.text((x2 - 20, y2 - 15), "T", fill='black', font=header_font)
            
            # Dibujar encabezados de columnas (terminales)
            for i, terminal in enumerate(terminals):
                x1 = (i+1) * cell_width
                y1 = 50
                x2 = (i+2) * cell_width
                y2 = 50 + cell_height
                draw.rectangle([(x1, y1), (x2, y2)], fill='#E5E5E5', outline='black')
                draw.text((x1 + cell_width//2, y1 + cell_height//2), terminal, fill='black', font=header_font, anchor='mm')
            
            # Dibujar filas de no-terminales
            for i, nt in enumerate(non_terminals):
                # Dibujar etiqueta de fila (no-terminal)
                x1 = 0
                y1 = 50 + (i+1) * cell_height
                x2 = cell_width
                y2 = 50 + (i+2) * cell_height
                draw.rectangle([(x1, y1), (x2, y2)], fill='#E5E5E5', outline='black')
                draw.text((x1 + cell_width//2, y1 + cell_height//2), nt, fill='black', font=header_font, anchor='mm')
                
                # Dibujar celdas de la tabla
                for j, terminal in enumerate(terminals):
                    x1 = (j+1) * cell_width
                    y1 = 50 + (i+1) * cell_height
                    x2 = (j+2) * cell_width
                    y2 = 50 + (i+2) * cell_height
                    
                    cell_content = table_data.get((nt, terminal), "")
                    bg_color = '#FFFFFF'
                    
                    # Si hay una producción, colorear la celda
                    if cell_content:
                        bg_color = '#E0F0FF'  # Azul claro
                    
                    draw.rectangle([(x1, y1), (x2, y2)], fill=bg_color, outline='black')
                    
                    # Ajustar texto si es demasiado largo
                    text = str(cell_content)
                    text_width = draw.textlength(text, font=cell_font)
                    if text_width > cell_width - 10:
                        text = text[:12] + "..."
                    
                    draw.text((x1 + cell_width//2, y1 + cell_height//2), text, fill='black', font=cell_font, anchor='mm')
            
            # Guardar imagen
            img.save(filename)
            return os.path.abspath(filename)
        
        # Construir tabla LL(1) - tabla M
        table_data = {}
        
        # Para cada no-terminal
        for nt in non_terminals:
            # Para cada producción de ese no-terminal
            for lhs, rhs_list in productions.items():
                if lhs == nt:
                    for rhs in rhs_list:
                        # Calcular los terminales para los que esta producción se aplica
                        if not rhs:  # Producción epsilon
                            # Para epsilon, usamos FOLLOW
                            for terminal in follow[nt]:
                                prod_text = "ε"  # Epsilon
                                table_data[(nt, terminal)] = prod_text
                        else:
                            # Para otros, usamos FIRST del primer símbolo
                            first_sym = rhs[0]
                            if first_sym in terminals:
                                # Si el primer símbolo es un terminal
                                prod_text = " ".join(rhs)
                                table_data[(nt, first_sym)] = prod_text
                            else:
                                # Si el primer símbolo es un no-terminal
                                for terminal in first[first_sym]:
                                    if terminal != '':  # Ignorar epsilon
                                        prod_text = " ".join(rhs)
                                        table_data[(nt, terminal)] = prod_text
                                
                                # Si el primer símbolo puede derivar epsilon, añadir FOLLOW
                                if '' in first[first_sym]:
                                    for terminal in follow[nt]:
                                        prod_text = " ".join(rhs)
                                        table_data[(nt, terminal)] = prod_text
        
        # Filtrar solo los no-terminales y terminales clave para la tabla
        key_non_terminals = ['start', 'program', 'sentence', 'expression', 'factor', 'term']
        key_terminals = ['program', 'if', 'var', 'println', 'ID', '{', '}', '$']
        
        display_non_terminals = [nt for nt in key_non_terminals if nt in non_terminals]
        display_terminals = [t for t in key_terminals if t in real_terminals]
        
        # Crear la tabla de parseo LL(1)
        ll1_table_path = create_table_image(filename, "TABLA DE PARSEO LL(1) - TABLA M", 
                                        display_non_terminals, display_terminals, table_data)
        print(f"\nVisualizacion de la tabla de parseo LL(1) guardada en {ll1_table_path}")
        
        # Crear simulación del proceso de parsing
        def create_parsing_simulation(filename, input_text):
            # Tokens para la simulación
            tokens = [t.value for t in list(parser.lex(input_text)) if t.type != 'WS'][:10]  # Limitamos a 10 tokens
            tokens.append('$')  # Añadir fin de entrada
            
            # Simulación del proceso de parsing
            parsing_steps = []
            stack = ['$', 'start']  # Pila inicial con símbolo de fin y símbolo de inicio
            remaining_input = tokens.copy()
            
            # Añadir el estado inicial
            parsing_steps.append({
                'stack': stack.copy(),
                'input': remaining_input.copy(),
                'action': 'Inicio del parseo'
            })
            
            # Simular pasos básicos del parsing
            for _ in range(min(8, len(tokens))):  # Limitar a 8 pasos para claridad
                if not stack or not remaining_input:
                    break
                    
                top = stack[-1]
                current_input = remaining_input[0] if remaining_input else '$'
                
                # Si el tope de la pila es un terminal
                if top in terminals or top == '$':
                    if top == current_input:
                        # Match
                        stack.pop()
                        remaining_input.pop(0)
                        parsing_steps.append({
                            'stack': stack.copy(),
                            'input': remaining_input.copy(),
                            'action': f'Match: {top}'
                        })
                    else:
                        # Error
                        parsing_steps.append({
                            'stack': stack.copy(),
                            'input': remaining_input.copy(),
                            'action': f'Error: se esperaba {top}'
                        })
                        break
                # Si el tope es un no-terminal
                elif top in non_terminals:
                    if (top, current_input) in table_data:
                        # Aplicar producción
                        production = table_data[(top, current_input)]
                        stack.pop()
                        
                        # Si no es epsilon, añadir símbolos a la pila en orden inverso
                        if production != "ε":
                            prod_symbols = production.split()
                            for symbol in reversed(prod_symbols):
                                stack.append(symbol)
                                
                        parsing_steps.append({
                            'stack': stack.copy(),
                            'input': remaining_input.copy(),
                            'action': f'Aplicar: {top} -> {production}'
                        })
                    else:
                        # Error - no hay producción aplicable
                        parsing_steps.append({
                            'stack': stack.copy(),
                            'input': remaining_input.copy(),
                            'action': f'Error: no hay producción para ({top}, {current_input})'
                        })
                        break
                else:
                    # Caso inesperado
                    parsing_steps.append({
                        'stack': stack.copy(),
                        'input': remaining_input.copy(),
                        'action': f'Símbolo desconocido: {top}'
                    })
                    break
            
            # Crear tabla para la simulación
            headers = ["Paso", "Pila", "Entrada", "Acción"]
            rows = []
            
            for i, step in enumerate(parsing_steps):
                stack_str = " ".join(reversed(step['stack']))  # La pila se lee de derecha a izquierda
                input_str = " ".join(step['input'])
                rows.append([str(i), stack_str, input_str, step['action']])
            
            # Crear imagen de la tabla
            from PIL import Image, ImageDraw, ImageFont
            
            # Calcular dimensiones de la tabla
            cell_width = 200
            cell_height = 40
            width = cell_width * len(headers)
            height = cell_height * (len(rows) + 1) + 50  # +1 para encabezados, +50 para título
            
            img = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(img)
            
            # Intentar cargar una fuente
            try:
                font_path = 'C:\\Windows\\Fonts\\Arial.ttf'
                title_font = ImageFont.truetype(font_path, 16)
                header_font = ImageFont.truetype(font_path, 12)
                cell_font = ImageFont.truetype(font_path, 10)
            except:
                title_font = ImageFont.load_default()
                header_font = ImageFont.load_default()
                cell_font = ImageFont.load_default()
            
            # Dibujar título
            draw.rectangle([(0, 0), (width, 50)], fill='#4B6082')
            draw.text((width//2, 25), "SIMULACIÓN DEL PROCESO DE PARSING LL(1)", fill='white', font=title_font, anchor='mm')
            
            # Dibujar encabezados de columnas
            for i, header in enumerate(headers):
                x1 = i * cell_width
                y1 = 50
                x2 = (i+1) * cell_width
                y2 = 50 + cell_height
                draw.rectangle([(x1, y1), (x2, y2)], fill='#7B96B6', outline='black')
                draw.text((x1 + cell_width//2, y1 + cell_height//2), header, fill='white', font=header_font, anchor='mm')
            
            # Dibujar filas de datos
            for row_idx, row in enumerate(rows):
                for col_idx, cell in enumerate(row):
                    x1 = col_idx * cell_width
                    y1 = 50 + (row_idx + 1) * cell_height
                    x2 = (col_idx + 1) * cell_width
                    y2 = 50 + (row_idx + 2) * cell_height
                    
                    # Alternar colores de filas
                    bg_color = '#E9F0F7' if row_idx % 2 == 0 else '#FFFFFF'
                    draw.rectangle([(x1, y1), (x2, y2)], fill=bg_color, outline='black')
                    
                    # Ajustar texto si es demasiado largo
                    text = str(cell)
                    text_width = draw.textlength(text, font=cell_font)
                    if text_width > cell_width - 10:
                        text = text[:25] + "..."
                    
                    draw.text((x1 + cell_width//2, y1 + cell_height//2), text, fill='black', font=cell_font, anchor='mm')
            
            # Guardar imagen
            img.save(filename)
            return os.path.abspath(filename)
        
        # Crear simulación del proceso de parsing
        simulation_path = create_parsing_simulation("parsing_simulation.png", input_text)
        print(f"Simulacion del proceso de parsing guardada en {simulation_path}")
        
        # Crear tabla con las reglas de producción
        def create_grammar_rules_image(filename):
            headers = ["No-Terminal", "Producción"]
            rows = []
            
            # Recopilar reglas para la visualización
            for lhs, rhs_list in productions.items():
                for rhs in rhs_list:
                    prod_str = " ".join(rhs) if rhs else "ε"
                    rows.append([lhs, f"{lhs} -> {prod_str}"])
            
            # Limitar a un número razonable de reglas para la visualización
            if len(rows) > 20:
                rows = rows[:20]
                rows.append(["...", "..."])
            
            # Parámetros de la tabla
            cell_width = 250
            cell_height = 30
            width = cell_width * len(headers)
            height = cell_height * (len(rows) + 1) + 50
            
            img = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(img)
            
            # Intentar cargar una fuente
            try:
                font_path = 'C:\\Windows\\Fonts\\Arial.ttf'
                title_font = ImageFont.truetype(font_path, 16)
                header_font = ImageFont.truetype(font_path, 12)
                cell_font = ImageFont.truetype(font_path, 10)
            except:
                title_font = ImageFont.load_default()
                header_font = ImageFont.load_default()
                cell_font = ImageFont.load_default()
            
            # Dibujar título
            draw.rectangle([(0, 0), (width, 50)], fill='#4B6082')
            draw.text((width//2, 25), "REGLAS DE LA GRAMÁTICA", fill='white', font=title_font, anchor='mm')
            
            # Dibujar encabezados
            for i, header in enumerate(headers):
                x1 = i * cell_width
                y1 = 50
                x2 = (i+1) * cell_width
                y2 = 50 + cell_height
                draw.rectangle([(x1, y1), (x2, y2)], fill='#7B96B6', outline='black')
                draw.text((x1 + cell_width//2, y1 + cell_height//2), header, fill='white', font=header_font, anchor='mm')
            
            # Dibujar filas
            for row_idx, row in enumerate(rows):
                for col_idx, cell in enumerate(row):
                    x1 = col_idx * cell_width
                    y1 = 50 + (row_idx + 1) * cell_height
                    x2 = (col_idx + 1) * cell_width
                    y2 = 50 + (row_idx + 2) * cell_height
                    
                    bg_color = '#E9F0F7' if row_idx % 2 == 0 else '#FFFFFF'
                    draw.rectangle([(x1, y1), (x2, y2)], fill=bg_color, outline='black')
                    
                    text = str(cell)
                    text_width = draw.textlength(text, font=cell_font)
                    if text_width > cell_width - 10:
                        text = text[:30] + "..."
                    
                    draw.text((x1 + cell_width//2, y1 + cell_height//2), text, fill='black', font=cell_font, anchor='mm')
            
            img.save(filename)
            return os.path.abspath(filename)
        
        # Crear tabla de reglas
        rules_path = create_grammar_rules_image("grammar_rules.png")
        print(f"Tabla de reglas de gramatica guardada en {rules_path}")
        
        return first, follow, real_terminals

    # Modificación aquí: recibir también real_terminals
    first, follow, real_terminals = visualize_parsing_table(grammar, parser, input_text)

    # Visualizar la tabla de parseo en formato de texto
    print("\n--- TABLA DE PARSEO (REPRESENTACIÓN TEXTUAL) ---")
    print("Esta es una aproximación de la tabla de parseo Earley para la gramática dada.")
    print("\nReglas de producción utilizadas:")

    # Obtener producciones para esta sección
    _, _, _, _, productions = compute_first_follow_sets(grammar)

    for i, (lhs, rhs_list) in enumerate(productions.items()):
        for j, rhs in enumerate(rhs_list):
            print(f"R{i+1}.{j+1}: {lhs} -> {' '.join(rhs) if rhs else 'ε'}")

    # Ahora real_terminals está disponible aquí
    print("\nTabla de parseo (Formato de Matriz):")
    print(" " * 15, end="")
    for term in sorted(real_terminals):
        print(f"{term:^10}", end="")
    print()
    print("-" * (15 + 10 * len(real_terminals)))

    # También necesitamos non_terminals aquí
    _, _, non_terminals, _, _ = compute_first_follow_sets(grammar)

    for nt in sorted(non_terminals):
        print(f"{nt:15}", end="")
        for term in sorted(real_terminals):
            action = ""
            if term in first[nt]:
                action = "S"  # Shift
            if term in follow[nt]:
                action += "R"  # Reduce
            if not action:
                action = " "
            print(f"{action:^10}", end="")
        print()
    
except Exception as e:
    print(f"Error parsing or visualizing: {e}")
    import traceback
    traceback.print_exc()
    
