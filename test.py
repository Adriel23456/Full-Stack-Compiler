from lark import Lark, Tree
from lark.lexer import Token
import os

# Define the complex grammar in Lark format
grammar = r'''
    start: program

    program: "program" ID "{" sentence* "}"
    sentence: println | conditional | var_decl | var_assign
    
    println: "println" expression ";"
    conditional: "if" "(" expression ")" "{" sentence* "}" "else" "{" sentence* "}"
    
    var_decl: "var" ID ";"
    var_assign: ID "=" expression ";"
    
    expression: factor (op factor)*
              | "mutGen" "(" binary_array "," expression "," expression ")"
    
    op: "+" | "-" | "&&" | "||"
    
    factor: comp (factor_op comp)*
    factor_op: "*" | "/"
    
    comp: "|-" term
        | "|-" "(" expression ")"
        | term
    
    term: NUMBER
        | BOOLEAN
        | ID
        | "(" expression ")"
    
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
    
except Exception as e:
    print(f"Error parsing or visualizing: {e}")
    import traceback
    traceback.print_exc()