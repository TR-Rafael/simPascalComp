from ply.lex import lex
from ply.yacc import yacc

reserved = {
    'begin': 'BEGIN',
    'end': 'END',
    'const': 'CONST',
    'var': 'VAR',
    'type': 'TYPE',
    'integer': 'INTEGER',
    'real': 'REAL',
    'array': 'ARRAY',
    'of': 'OF',
    'record': 'RECORD',
    'function': 'FUNCTION',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'then': 'THEN',
    'write': 'WRITE',
    'read': 'READ'
}

tokens = ['SEMICOLON', 'ASSIGMENT', 'COLON', 'DOT', 'COMMA', 'EQUAL', 'OPEN_BRACKET', 'CLOSE_BRACKET',
          'OPEN_PARENTHESIS',
          'CLOSE_PARENTHESIS', 'NEGATION', 'SMALLER_THAN', 'GREATER_THAN', 'PLUS', 'MINUS', 'MULTIPLICATION', 'DIVIDE',
          'IDENTIFIER', 'STRING', 'NUMBER'
          ] + list(reserved.values())

'''
tokens and simbols
( ) [ ] { } , ; + - * / == != > >= < <= || && ! = += -= *= /= %= ? :
'''
t_ignore = ' \t'

t_SEMICOLON = r';'
t_ASSIGMENT = r':\='
t_COLON = r':'
t_DOT = r'\.'
t_COMMA = r','
t_EQUAL = r'\='
t_OPEN_BRACKET = r'\['
t_CLOSE_BRACKET = r'\]'
t_OPEN_PARENTHESIS = r'\('
t_CLOSE_PARENTHESIS = r'\)'
t_NEGATION = r'!'
t_SMALLER_THAN = r'<'
t_GREATER_THAN = r'>'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLICATION = r'\*'
t_DIVIDE = r'/'


def t_IDENTIFIER(t):
    r"""[a-zA-Z_][a-zA-Z_0-9]*"""
    if t.value in reserved:  # Check for reserved words
        t.type = reserved[t.value]
    return t


def t_STRING(t):
    r"\"([^\"]*)\""
    return t


def t_NUMBER(t):
    r"[0-9]*\.?[0-9]+"
    return t


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_COMMENT_MONOLINE(t):
    r"""//.*"""
    pass
    # No return value. Token discarded


def my_lexer():
    return lex()


lexer = my_lexer()


#  testar coisas
# Build the lexer object


# --- Parser

# Write functions for each grammar rule which is
# specified in the docstring.
def p_empty(p):
    '''
    empty :
    '''
    pass
def p_programa(p):
    '''
    PROGRAMA : DECLARACOES PRINCIPAL
    '''
    p[0] = ('PROGRAMA', p[1], p[2])

def p_principal(p):
    '''
    PRINCIPAL : BEGIN COMANDO LISTA_COM END
    '''
    p[0] = ('PRINCIPAL', 'begin', p[2], p[3], 'end')

def p_declaracoes(p):
    '''
    DECLARACOES : DEF_CONST DEF_TIPOS DEF_VAR DEF_FUNC
    '''
    p[0] = ('DECLARACOES', p[1], p[2], p[3], p[4])

def p_def_const(p):
    '''
    DEF_CONST : CONSTANT DEF_CONST
              | empty
    '''
    if len(p) == 3:
        p[0] = ('DEF_CONST', p[1], p[2])
    else:
        p[0] = 'empty'

def p_def_tipos(p):
    '''
    DEF_TIPOS : TIPO DEF_TIPOS
              | empty
    '''
    if len(p) == 3:
        p[0] = ('DEF_TIPOS', p[1], p[2])
    else:
        p[0] = 'empty'

def p_def_func(p):
    '''
    DEF_FUNC : FUNCAO DEF_FUNC
              | empty
    '''
    if len(p) == 3:
        p[0] = ('DEF_FUNC', p[1], p[2])
    else:
        p[0] = 'empty'

def p_id(p):
    '''
    ID : IDENTIFIER
    '''
    p[0] = p[1]

def p_numero(p):
    '''
    NUMERO : NUMBER
    '''
    aux = float(p[1])
    if aux // 1 == aux:
        p[0] = int(aux)
    else:
        p[0] = float(aux)

def p_constante(p):
    '''
    CONSTANTE : CONST ID = CONST_VALOR ;
    '''
    p[0] = ('CONSTANTE', 'const', p[2], '=', p[4], ';')

def p_const_valor(p):
    '''
    CONST_VALOR : STRING
                | EXP_MAT
    '''
    print(p[1])
    # isinstance(4, str)
    #  È algo assim que tem que fazer aqui, mas preciso entender melhor o que tem dentro de p[1] para fazer a validação
    if isinstance(p[1], str):
        p[0] = ('CONST_VALOR', p[1])
    else:
        p[0] = ('CONST_VALOR', p[1])

def p_tipo(p):
    '''
    TIPO : type ID = TIPO_DADO ;
    '''
    p[0] = ('TIPO', 'type', p[2], '=', p[4], ';')

def p_variavel(p):
    '''
    VARIAVEL : var ID LISTA_ID : TIPO_DADO ;
    '''
    p[0] = ('VARIAVEL', 'var', p[2], p[3], ':', p[5], ';')

def p_lista_id(p):
    '''
    LISTA_ID : , ID LISTA_ID
             | empty
    '''
    if len(p) == 4:
        p[0] = ('LISTA_ID', ',', p[2], p[3])
    else:
        p[0] = 'empty'

def p_campos(p):
    '''
    CAMPOS : ID : TIPO_DADO LISTA_CAMPOS
    '''
    p[0] = ('CAMPOS', p[1], ':', p[3], p[4])

def p_lista_campos(p):
    '''
    LISTA_CAMPOS : ; CAMPOS LISTA_CAMPOS
                 | empty
    '''
    if len(p) == 4:
        p[0] = ('LISTA_CAMPOS', ';', p[2], p[3])
    else:
        p[0] = 'empty'

def p_tipo_dado(p):
    '''
    TIPO_DADO : integer
              | real
              | array [ NUMERO ] of TIPO_DADO
              | record CAMPOS end
              | ID
    '''
    if len(p) == 2:
        print(p)
        print(p[1])
        if p[1] == 'integer':
            p[0] = ('TIPO_DADO', 'integer')
        else:
            p[0] = ('TIPO_DADO', 'real')
        p[0] = 'algo'
    elif len(p) == 4:
        p[0] = ('TIPO_DADO', 'record', p[2], 'end')
    elif len(p) == 7:
        p[0] = ('TIPO_DADO', 'array', '[', p[3], ']', 'of', p[6])

def p_funcao(p):
    '''
    FUNCAO : function NOME_FUNCAO BLOCO_FUNCAO
    '''
    p[0] = ('FUNCAO', 'function', p[1], p[2])

def p_nome_funcao(p):
    '''
    NOME_FUNCAO : ID PARAM_FUNC : TIPO_DADO
    '''
    p[0] = ('NOME_FUNCAO', p[1], p[2], ':', p[4])

def p_param_func(p):
    '''
    PARAM_FUNC : ( CAMPOS )
               | empty
    '''
    if len(p) == 4:
        p[0] = ('PARAM_FUNC', '(', p[2], ')')
    else:
        p[0] = 'empty'

def p_bloco_funcao(p):
    '''
    BLOCO_FUNCAO : DEF_VAR begin COMANDO LISTA_COM end
    '''
    p[0] = ('BLOCO_FUNCAO', p[1], 'begin', p[3], p[4], 'end')

def p_lista_com(p):
    '''
    LISTA_COM : ; COMANDO LISTA_COM
              | empty
    '''
    if len(p) == 4:
        p[0] = ('LISTA_COM', ';', p[2], p[3])
    else:
        p[0] = 'empty'

def p_bloco(p):
    '''
    BLOCO : begin COMANDO LISTA_COM end
          | COMANDO
    '''
    if len(p) == 5:
        p[0] = ('BLOCO', 'begin', p[2], p[3], 'end')
    else:
        p[0] = ('BLOCO', p[2])

def p_comando(p):
    '''
    COMANDO : ID NOME ASSIGMENT EXP_MAT
            | while EXP_LOGICA BLOCO
            | if EXP_LOGICA then BLOCO ELSE
            | write CONST_VALOR
            | read ID NOME
    '''
    if p[1] == 'while':
        p[0] = ('WHILE', 'while', p[2], p[3])
    elif p[1] == 'if':
        p[0] = ('IF', 'if', p[2], 'then', p[4], p[5])
    elif p[1] == 'write':
        p[0] = ('WRITE', 'write', p[2])
    elif p[1] == 'read':
        p[0] = ('READ', 'read', p[2], p[3])
    else:
        p[0] = ('COMANDO', p[1], p[2], ':=', p[4])

def p_else(p):
    '''
    ELSE : else BLOCO
         | empty
    '''
    if len(p) == 3:
        p[0] = ('ELSE', 'else', p[2])
    else:
        p[0] = 'empty'

def p_lista_param(p):
    '''
    LISTA_PARAM : PARAMETRO , LISTA_PARAM
                | PARAMETRO
                | empty
    '''
    if len(p) == 4:
        p[0] = ('LISTA_PARAM com mais args', p[1], ',', p[3])
    elif len(p) == 2:
        p[0] = ('LISTA_PARAM pura', p[1])
    else:
        p[0] = 'empty'

def p_exp_logica(p):
    '''
    EXP_LOGICA : EXP_MAT OP_LOGICO EXP_LOGICA
               | EXP_MAT
    '''
    if len(p) == 4:
        p[0] = ('EXP_LOGICA maior', p[1], p[2], p[3])
    elif len(p) == 2:
        p[0] = ('EXP_LOGICA menor', p[1])

def p_exp_mat(p):
    '''
    EXP_MAT : PARAMETRO OP_MAT EXP_MAT
            | PARAMETRO
    '''
    print(p[1])
    if len(p) == 4:
        p[0] = ('EXP_MAT', 'PARAMETRO', 'OP_MAT', 'EXP_MAT')
    else:
        p[0] = ('EXP_MAT', 'PARAMETRO')

def p_parametro(p):
    '''
    PARAMETRO : ID NOME
              | NUMERO
    '''
    # Prints para entender melhor oque ocorre aqui depois
    print(p)
    print(p[0])
    if len(p) == 3:
        p[0] = ('PARAMETRO', p[1], p[2])
    else:
        p[0] = ('PARAMETRO', p[1])

def p_op_logico(p):
    '''
    OP_LOGICO : >
              | <
              | =
              | !
    '''
    if p[1] == '>':
        p[0] = p[1]
    elif p[1] == '<':
        p[0] = p[1]
    elif p[1] == '=':
        p[0] = p[1]
    elif p[1] == '!':
        p[0] = p[1]

def p_op_mat(p):
    '''
    OP_MAT : +
          | -
          | *
          | /
    '''
    if p[1] == '+':
        p[0] = p[1]
    elif p[1] == '-':
        p[0] = p[1]
    elif p[1] == '*':
        p[0] = p[1]
    elif p[1] == '/':
        p[0] = p[1]

def p_nome(p):
    '''
    NOME : . ID NOME
         | [ PARAMETRO ]
         | ( LISTA_PARAM )
         | empty
    '''
    if len(p) == 4:
        if p[1] == '[':
            p[0] = ('NOME', '[', p[2], ']')
        elif p[1] == '(':
            p[0] = ('NOME', '(', p[2], ')')
        else:
            p[0] = ('NOME', '.', p[2], p[3])
    else:
        p[0] = 'empty'
def p_error(p):
    print(f'Syntax error at {p.value!r}')


# Build the parser
parser = yacc()

# Parse an expression
ast = parser.parse('2 * 3 + 4')
print(ast)
