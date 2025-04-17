import os
import sys
import subprocess
from antlr4 import *
import pydot  # Librería para visualizar gráficos

# Ejecutar ANTLR para generar el lexer
def generate_lexer():
    # Verificar que existe el archivo de gramática
    grammar_file = os.path.join('assets', 'VGraph.g4')
    if not os.path.exists(grammar_file):
        print(f"Error: No se encontró el archivo de gramática en {grammar_file}")
        print("Por favor, asegúrate de que el archivo existe antes de ejecutar este script.")
        return False
    
    # Ruta al JAR de ANTLR4
    antlr_jar = '/tmp/antlr-4.9.2-complete.jar'
    
    # Si el archivo no existe, informar al usuario
    if not os.path.exists(antlr_jar):
        print(f"Error: No se encontró el archivo JAR de ANTLR4 en {antlr_jar}")
        print("Por favor, descárgalo con el siguiente comando:")
        print("wget https://www.antlr.org/download/antlr-4.9.2-complete.jar -P /tmp/")
        return False
    
    # Guardar directorio actual
    current_dir = os.getcwd()
    
    try:
        # Cambiar al directorio de la gramática
        os.chdir('assets')
        
        # Generar el lexer usando el JAR de ANTLR4
        cmd = ['java', '-jar', antlr_jar, '-Dlanguage=Python3', 'VGraph.g4']
        subprocess.run(cmd, check=True)
        print(f"Lexer generado correctamente en assets/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al generar el lexer: {e}")
        return False
    finally:
        # Volver al directorio original
        os.chdir(current_dir)

# Crear un visualizador de tokens usando pydot
def visualize_tokens(tokens, output_file='token_graph.png'):
    graph = pydot.Dot(graph_type='digraph', rankdir='LR')
    
    # Nodos para cada token
    for i, (token_type, text, line, col) in enumerate(tokens):
        node_label = f"{token_type}\\n\"{text}\""
        node = pydot.Node(f"token_{i}", label=node_label, shape="box", style="filled", fillcolor="lightblue")
        graph.add_node(node)
        
        # Conectar con el token anterior
        if i > 0:
            edge = pydot.Edge(f"token_{i-1}", f"token_{i}")
            graph.add_edge(edge)
    
    # Guardar el gráfico
    graph.write_png(output_file)
    print(f"Gráfico de tokens guardado como {output_file}")

# Función para analizar un texto con el lexer
def analyze_text(text):
    # Importar el lexer generado
    sys.path.append(os.path.abspath('assets'))
    
    try:
        from VGraphLexer import VGraphLexer
    except ImportError:
        print("Error: No se pudo importar VGraphLexer. Asegúrate de que se haya generado correctamente.")
        return []
    
    input_stream = InputStream(text)
    lexer = VGraphLexer(input_stream)
    
    # Obtener todos los tokens y organizarlos
    all_tokens = []
    token = lexer.nextToken()
    while token.type != Token.EOF:
        token_name = lexer.symbolicNames[token.type] if token.type > 0 else 'EOF'
        all_tokens.append((token_name, token.text, token.line, token.column))
        token = lexer.nextToken()
    
    # Imprimir tokens en una tabla formateada
    print("\nAnálisis Léxico del código de ejemplo:")
    print("─" * 80)
    print(f"{'TIPO DE TOKEN':<20} {'TEXTO':<30} {'LÍNEA':<10} {'COLUMNA':<10}")
    print("─" * 80)
    for token_type, text, line, column in all_tokens:
        # Truncar texto si es demasiado largo
        display_text = text[:27] + "..." if len(text) > 30 else text
        print(f"{token_type:<20} {display_text:<30} {line:<10} {column:<10}")
    print("─" * 80)
    print(f"Total de tokens: {len(all_tokens)}")
    
    # Visualizar los tokens
    visualize_tokens(all_tokens)
    
    return all_tokens

def main():
    # Código de ejemplo VGraph como string raw
    example_code = r"""
    # Definir variables para la espiral
    (int) x, y, t;
    (color) c;

    frame {
        loop (t = 0; t < 360; t = t + 5) {
            # Calcular coordenadas de la espiral usando trigonometría
            x = 320 + t * cos(t * 3.1416 / 180);  # Centro en X=320
            y = 240 + t * sin(t * 3.1416 / 180);  # Centro en Y=240

            # Cambiar color en cada iteración
            if (t % 3 == 0) { c = rojo; }
            else if (t % 3 == 1) { c = azul; }
            else { c = verde; }

            setcolor(c);
            draw pixel(x, y);

            wait(1);  # Pequeño retraso para animación suave
        }
    }
    """
    
    print("Generando lexer con ANTLR4...")
    
    if generate_lexer():
        print("Analizando código de ejemplo...")
        analyze_text(example_code)
    else:
        print("No se pudo continuar debido a errores en la generación del lexer.")

if __name__ == "__main__":
    main()