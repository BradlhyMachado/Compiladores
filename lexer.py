import ply.lex as lex

resultado_analisis = []

reserved = {
  'funcion': 'funcion', 
  'imprimir': 'imprimir',
  'leer':'leer',
  'retornar':'retornar',
  'si':'si',
  'sino':'sino',
  'mientras':'mientras',
  'llamafun':'llamafun'
}

tokens = [
  # Tipos
  'numerico',
  'boolean',
  
  # Operadores Aritmeticas
  'suma',
  'resta',
  'multiplicacion',
  'division',
  
  # Operadores lógicos
  'y',
  'o',
  'igual',
  'mayor_que',
  'menor_que',
  'mayor_igual',
  'menor_igual',
  'igualdad',
  'diferente',

  #Signos
  'iz_paren',
  'der_paren',
  'iz_llave',
  'der_llave',
  'pt_coma',
  'coma',
  'hash',

  # Otros
  'id'
] + list(reserved.values())

 # Regular expression rules for simple tokens
t_suma    = r'\+'
t_resta   = r'-'
t_multiplicacion   = r'\*'
t_division  = r'/'
t_y     = r'&&'
t_o      = r'\|{2}'
t_igual  = r'='
t_iz_paren  = r'\('
t_der_paren  = r'\)'
t_iz_llave    = r'\{'
t_der_llave    = r'\}'
t_pt_coma = r'\;'
t_coma = r'\,'
t_hash = r'\#'
t_mayor_que = r'\>'
t_menor_que = r'\<'
t_mayor_igual = r'\>='
t_menor_igual = r'\<='
t_igualdad = r'\=='
t_diferente=r'\!='
 # A regular expression rule with some action code
def t_numerico(t):
  r'([0-9]*[.])?[0-9]+'
  #t.value = int(t.value)
  return t
  
def t_boolean(t):
  r'true | false'
  return t
 
 # A regular expression rule with some action code
def t_id(t):
  r'[a-zA-Z]+ ( [a-zA-Z0-9]* )'    
  t.type = reserved.get(t.value,'id')    # Check for reserved words
  return t

 # Define a rule so we can track line numbers
def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)
 
 # A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
 
 # Error handling rule
def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

# Prueba de ingreso
def prueba(data):
  global resultado_analisis
  analizador = lex.lex()
  analizador.input(data)
  
  resultado_analisis.clear()
  while True:
    tok = analizador.token()
    if not tok:
      break
    resultado_analisis.append({'type':str(tok.type), 'lexeme':str(tok.value), 'line':str(tok.lineno)})
  resultado_analisis.append({'type': '$', 'lexeme': '$', 'line': -1})
  return resultado_analisis

# instanciamos el analizador lexico
analizador = lex.lex()

def lexer(ruta):
  
  archivo = open(ruta, "r")
  
  data = archivo.read() #Se ingresa para leer la data obtenida del archivo txt
  return (prueba(data))