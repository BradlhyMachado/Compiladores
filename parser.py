# Importación de librerías y métodos necesarias
from lexer import lexer
import pandas as pd
import sys
import graphviz

# Variables globales que serán útiles para el desarrollo del código
counter = 0
cont = 0
tokens = {}

syntax_table = pd.read_csv("syntax_table.csv", index_col=0)
tree = graphviz.Graph(comment='Árbol Generado')

# Imprime stack #################
def print_stack():            ###
  print("\nStack:")           ###
  for e in stack:             ###
    print(e.symbol, end=" ")  ###
  print()                     ###
#################################

# Imprime input #################
def print_input():            ###
  print("\nInput:")           ###
  for t in tokens:            ###
    print(t['type'], end=" ") ###
  print()                     ###
#################################

# Actualización de stack y función que albergará la lógica del problema
def update_stack(stack, token_type):  
  production = syntax_table.loc[stack[0].symbol][token_type]
  # Procesar production E -> T E'  =>  T E' 
  # Production=production[production.index(">")+1:]
  #print(production)

  # Imprime accion ######
  print("\nAction:") ###
  print(production)  ###
  print()            ###
  ######################
  
  # Cuando no hay producción de la tabla
  if(pd.isna(production)):
    print("ERROR sintáctico")
    sys.exit()

  elementos = production.split(" ")
  
  #Asignamos el origen o raiz para el gráfico
  sourc = elementos[0]

  # Iniciando el grafo con un nodo origen
  if(elementos[0] in tree.source):  
    pos = tree.source.rfind(elementos[0])
    aux = tree.source[pos]
    i = 1
    while(True):
      if(tree.source[pos+i] == '"' or tree.source[pos+i] == ' ' or tree.source[pos+i] == '\n' or tree.source[pos+i] == '\t'):
        break
      else:
        aux = aux + tree.source[pos+i]
        i = i+1
    aux = aux.strip()
    sourc = aux

  elementos.pop(0)
  elementos.pop(0)

  # Eliminar el ultimo elemento de la pila
  stack.pop(0)
  
  if elementos[0] == "''": # Nulo
    for f in range(len(elementos)):
      nodo = elementos[f]
      if(nodo in tree.source):             #Si el nodo pertenede a su padre o raiz
        key=str(len(tree.source))
        tree.node(nodo+key, "ɛ")           # Nodo del arbol
        tree.edge(sourc, nodo+key)         # Conección de nodo
      else:    #Si el nodo no pertenede a su padre o raiz
        tree.node(nodo, "ɛ")               # Nodo del arbol
        tree.edge(sourc, nodo)             # Conección de nodo
    return
  
  # Insertar production a la stack: primero E' y luego T
  for i in range(len(elementos)-1, -1, -1):      
    symbol = node_stack(elementos[i], not elementos[i].isupper())
    stack.insert(0, symbol)

  # Se generan los nodos y relacionan
  for f in range(0, len(elementos)):
    nodo = elementos[f]
    if(nodo in tree.source):             #Si el nodo pertenede a su padre o raiz
      key=str(len(tree.source))
      tree.node(nodo+key, nodo)          # Nodo del arbol
      tree.edge(sourc, nodo+key)         # Conección de nodo
    else:   #Si el nodo no pertenede a su padre o raiz
      tree.node(nodo, nodo)              # Nodo del arbol
      tree.edge(sourc, nodo)             # Conección de nodo
  
  # Dando color a los nodos
  tree.node_attr.update(color='red')
  tree.edge_attr.update(color='red')

# Clase Stack Nodo
class node_stack:
  def __init__(self, symbol, terminal):
    global counter
    self.id = counter
    self.symbol = symbol        # Símbolo de la gramatica
    self.is_terminal = terminal # Para saber si es terminal
    counter += 1

class node_parser:
  def __init__(self, node_st, lexeme = None, children =[], father = None, line=None):
    self.node_st = node_st
    self.lexeme = lexeme
    self.line = line
    self.children = children
    self.father = father

# Creación y agregación de elementos iniciales a Stack
stack = []
symbol_1 = node_stack('$', True)
symbol_2 = node_stack('PROGRAM', False)
stack.insert(0, symbol_1)
stack.insert(0, symbol_2)

# Tokens o input a evaluar
'''tokens = [   
            {'type':'id', 'lexeme':'x', 'line':1}, 
            {'type':'*', 'lexeme':'+', 'line':1},
            {'type':'id', 'lexeme':'y', 'line':1},
            {'type':'$', 'lexeme':'$', 'line':1}
        ]'''
#######tokens = lexer(ruta)

# Main del programa
def parser():
    #Si el $ es igual q $
  while True:
    global cont
    cont = cont + 1
    print("--------- ITERATION ", cont, " ---------")
    print_stack()
    print_input()
    if stack[0].symbol == '$' and tokens[0]['type'] == '$':
      print("\nTodo bien! \n")
      break
  
    # cuando son terminales
    if stack[0].is_terminal:
      print("\nterminales ... \n")
      if stack[0].symbol == tokens[0]['type']:
        stack.pop(0)
        tokens.pop(0)
      else:
        print("ERROR sintáctico")
        break
    # cuando reemplazar en la pila, según tabla sintáctica
    else:
      update_stack(stack, tokens[0]['type'])

def graficar(ruta):
    global tokens
    tokens = lexer(ruta)
    parser()
    # Generando el arbol en formato ".png"
    tree.render(filename="Arbol_obtenido_"+ruta, format="png")