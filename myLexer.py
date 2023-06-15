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


# Build the lexer object

def auxPrint(espacos):
    return '---' * espacos * 2
# --- Parser
class Node:
    def __init__(self, tipo, filhos=None, folhas=None):
        self.tipo = tipo
        if filhos:
            self.filhos = filhos
        else:
            self.filhos = []
        if folhas:
            self.folhas = folhas
        else:
            self.folhas = []

        # def __str__(self):
        #     return f' Esse é meu objeto: [{self.numero}, {self.titular}, {self.saldo}, {self.limite}

    def printNode(self, profundidade=0):
        if self.tipo == 'Vazio':
            return

        print(f'{auxPrint(profundidade)} Nó {self.tipo}')
        # if len(self.filhos) != 0:
        #     print(list(map(lambda x: print(x) if isinstance(x, str) else x.printNode(), self.filhos)))
        # if len(self.folhas) != 0:
        #     print(list(map(lambda x: print(x) if isinstance(x, str) else x.printNode(), self.folhas)))
        for filho in self.filhos:
            filho.printNode(profundidade + 1)
        for folha in self.folhas:
            print(f'{auxPrint(profundidade+1)} Folha: \'{folha}\'')

        print(f'{auxPrint(profundidade)} fim do bloco de {self.tipo}')

# Write functions for each grammar rule which is
# specified in the docstring.
def p_programa(p):
    '''
    PROGRAMA : DECLARACOES PRINCIPAL
    '''
    #  Ta ok
    # p[0] = ('PROGRAMA', p[1], p[2])
    p[0] = Node('PROGRAMA', filhos=[p[1], p[2]])


def p_principal(p):
    '''
    PRINCIPAL : BEGIN COMANDO LISTA_COM END
    '''
    # Ta ok
    # p[0] = ('PRINCIPAL', 'begin', p[2], p[3], 'end')
    p[0] = Node('PRINCIPAL', filhos=[p[2], p[3]], folhas=[p[1], p[4]])


def p_declaracoes(p):
    '''
    DECLARACOES : DEF_CONST DEF_TIPOS DEF_VAR DEF_FUNC
    '''
    # p[0] = ('DECLARACOES', p[1], p[2], p[3], p[4])
    p[0] = Node('DECLARACOES', filhos=[p[1], p[2], p[3], p[4]])


def p_empty(p):
    '''
    empty :
    '''
    p[0] = Node('Vazio')


def p_def_const(p):
    '''
    DEF_CONST : CONSTANTE DEF_CONST
              | empty
    '''
    if len(p) == 3:
        # p[0] = ('DEF_CONST', p[1], p[2])
        p[0] = Node('DEF_CONST', filhos=[p[1], p[2]])
    else:
        p[0] = Node('Vazio')


def p_def_tipos(p):
    '''
    DEF_TIPOS : TIPO DEF_TIPOS
              | empty
    '''
    if len(p) == 3:
        # p[0] = ('DEF_TIPOS', p[1], p[2])
        p[0] = Node('DEF_TIPOS', filhos=[p[1], p[2]])
    else:
        p[0] = Node('Vazio')


def p_def_var(p):
    '''
    DEF_VAR : VARIAVEL DEF_VAR
              | empty
    '''
    if len(p) == 3:
        # p[0] = ('DEF_VAR', p[1], p[2])
        p[0] = Node('DEF_VAR', filhos=[p[1], p[2]])
    else:
        p[0] = Node('Vazio')


def p_def_func(p):
    '''
    DEF_FUNC : FUNCAO DEF_FUNC
              | empty
    '''
    if len(p) == 3:
        # p[0] = ('DEF_FUNC', p[1], p[2])
        p[0] = Node('DEF_FUNC', filhos=[p[1], p[2]])
    else:
        p[0] = Node('Vazio')


def p_id(p):
    '''
    ID : IDENTIFIER
    '''
    # p[0] = p[1]
    p[0] = Node('IDENTIFIER', folhas=[p[1]])


def p_numero(p):
    '''
    NUMERO : NUMBER
    '''
    aux = float(p[1])
    if aux // 1 == aux:
        # p[0] = int(aux)
        p[0] = Node('NUMERO inteiro', folhas=[int(p[1])])
    else:
        # p[0] = float(aux)
        p[0] = Node('NUMERO flutuante', folhas=[float(p[1])])


def p_constante(p):
    '''
    CONSTANTE : CONST ID EQUAL CONST_VALOR SEMICOLON
    '''
    # p[0] = ('CONSTANTE', 'const', p[2], '=', p[4], ';')
    p[0] = Node('CONSTANTE', filhos=[p[2], p[4]], folhas=[p[1], p[3], p[5]])


def p_const_valor(p):
    '''
    CONST_VALOR : STRING
                | EXP_MAT
    '''
    if isinstance(p[1], str):
        # p[0] = ('CONST_VALOR', p[1])
        p[0] = Node('CONST_VALOR', folhas=[p[1]])
    else:
        # p[0] = ('CONST_VALOR', p[1])
        p[0] = Node('CONST_VALOR', filhos=[p[1]])


def p_tipo(p):
    '''
    TIPO : TYPE ID EQUAL TIPO_DADO SEMICOLON
    '''
    # p[0] = ('TIPO', 'type', p[2], '=', p[4], ';')
    p[0] = Node('TIPO', filhos=[p[2], p[4]], folhas=[p[1], p[3], p[5]])


def p_variavel(p):
    '''
    VARIAVEL : VAR ID LISTA_ID COLON TIPO_DADO SEMICOLON
    '''
    # p[0] = ('VARIAVEL', 'var', p[2], p[3], ':', p[5], ';')
    p[0] = Node('VARIAVEL', filhos=[p[2], p[3], p[5]], folhas=[p[1], p[4], p[6]])


def p_lista_id(p):
    '''
    LISTA_ID : COMMA ID LISTA_ID
             | empty
    '''
    if len(p) == 4:
        # p[0] = ('LISTA_ID', ',', p[2], p[3])
        p[0] = Node('LISTA_ID', filhos=[p[2], p[3]], folhas=[p[1]])
    else:
        # p[0] = 'empty'
        p[0] = Node('Vazio')


def p_campos(p):
    '''
    CAMPOS : ID COLON TIPO_DADO LISTA_CAMPOS
    '''
    # p[0] = ('CAMPOS', p[1], ':', p[3], p[4])
    p[0] = Node('CAMPOS', filhos=[p[1], p[3], p[4]], folhas=[p[2]])


def p_lista_campos(p):
    '''
    LISTA_CAMPOS : SEMICOLON CAMPOS LISTA_CAMPOS
                 | empty
    '''
    if len(p) == 4:
        # p[0] = ('LISTA_CAMPOS', ';', p[2], p[3])
        p[0] = Node('LISTA_CAMPOS', filhos=[p[2], p[3]], folhas=[p[1]])
    else:
        # p[0] = 'empty'
        p[0] = Node('Vazio')


def p_tipo_dado(p):
    '''
    TIPO_DADO : INTEGER
              | REAL
              | ARRAY OPEN_BRACKET NUMERO CLOSE_BRACKET OF TIPO_DADO
              | RECORD CAMPOS END
              | ID
    '''
    if len(p) == 2:
        if p[1] == 'integer':
            # p[0] = ('TIPO_DADO integer', 'integer')
            p[0] = Node('TIPO_DADO integer', folhas=[p[1]])
        elif p[1] == 'real':
            # p[0] = ('TIPO_DADO real', 'real')
            p[0] = Node('TIPO_DADO real', folhas=[p[1]])
        else:
            # p[0] = ('TIPO_DADO id', p[1])
            p[0] = Node('TIPO_DADO id', filhos=[p[1]])
    elif len(p) == 4:
        # p[0] = ('TIPO_DADO record', 'record', p[2], 'end')
        p[0] = Node('TIPO_DADO record', filhos=[p[2]], folhas=[p[1], p[3]])
    elif len(p) == 7:
        # p[0] = ('TIPO_DADO array', 'array', '[', p[3], ']', 'of', p[6])
        p[0] = Node('TIPO_DADO array', filhos=[p[3], p[6]], folhas=[p[1], p[2], p[4], p[5]])


def p_funcao(p):
    '''
    FUNCAO : FUNCTION NOME_FUNCAO BLOCO_FUNCAO
    '''
    # p[0] = ('FUNCAO', 'function', p[2], p[3])
    p[0] = Node('FUNCAO', filhos=[p[2], p[3]], folhas=[p[1]])


def p_nome_funcao(p):
    '''
    NOME_FUNCAO : ID PARAM_FUNC COLON TIPO_DADO
    '''
    # p[0] = ('NOME_FUNCAO', p[1], p[2], ':', p[4])
    p[0] = Node('NOME_FUNCAO', filhos=[p[1], p[2], p[4]], folhas=[p[3]])


def p_param_func(p):
    '''
    PARAM_FUNC : OPEN_PARENTHESIS CAMPOS CLOSE_PARENTHESIS
               | empty
    '''
    if len(p) == 4:
        # p[0] = ('PARAM_FUNC', '(', p[2], ')')
        p[0] = Node('PARAM_FUNC', filhos=[p[2]], folhas=[p[1], p[3]])
    else:
        # p[0] = 'empty'
        p[0] = Node('Vazio')


def p_bloco_funcao(p):
    '''
    BLOCO_FUNCAO : DEF_VAR BEGIN COMANDO LISTA_COM END
    '''
    # p[0] = ('BLOCO_FUNCAO', p[1], 'begin', p[3], p[4], 'end')
    p[0] = Node('BLOCO_FUNCAO', filhos=[p[1], p[3], p[4]], folhas=[p[2], p[5]])


def p_lista_com(p):
    '''
    LISTA_COM : SEMICOLON COMANDO LISTA_COM
              | empty
    '''
    if len(p) == 4:
        # p[0] = ('LISTA_COM', ';', p[2], p[3])
        p[0] = Node('LISTA_COM', filhos=[p[2], p[3]], folhas=[p[1]])
    else:
        # p[0] = 'empty'
        p[0] = Node('Vazio')


def p_bloco(p):
    '''
    BLOCO : BEGIN COMANDO LISTA_COM END
          | COMANDO
    '''
    if len(p) == 5:
        # p[0] = ('BLOCO', 'begin', p[2], p[3], 'end')
        p[0] = Node('BLOCO', filhos=[p[2], p[3]], folhas=[p[1], p[4]])
    else:
        # p[0] = ('BLOCO', p[1])
        p[0] = Node('BLOCO', filhos=[p[1]])


def p_comando(p):
    '''
    COMANDO : ID NOME ASSIGMENT EXP_MAT
            | WHILE EXP_LOGICA BLOCO
            | IF EXP_LOGICA THEN BLOCO ELSE_BLOCO
            | WRITE CONST_VALOR
            | READ ID NOME
    '''
    if p[1] == 'while':
        # p[0] = ('WHILE', 'while', p[2], p[3])
        p[0] = Node('COMANDO WHILE', filhos=[p[2], p[3]], folhas=[p[1]])
    elif p[1] == 'if':
        # p[0] = ('IF', 'if', p[2], 'then', p[4], p[5])
        p[0] = Node('COMANDO IF', filhos=[p[2], p[4], p[5]], folhas=[p[1], p[3]])
    elif p[1] == 'write':
        # p[0] = ('WRITE', 'write', p[2])
        p[0] = Node('COMANDO WRITE', filhos=[p[2]], folhas=[p[1]])
    elif p[1] == 'read':
        # p[0] = ('READ', 'read', p[2], p[3])
        p[0] = Node('COMANDO READ', filhos=[p[2], p[3]], folhas=[p[1]])
    else:
        # p[0] = ('COMANDO', p[1], p[2], ':=', p[4])
        p[0] = Node('COMANDO puro', filhos=[p[1], p[2], p[4]], folhas=[p[3]])


def p_else(p):
    '''
    ELSE_BLOCO : ELSE BLOCO
         | empty
    '''
    if len(p) == 3:
        # p[0] = ('ELSE_BLOCO', 'else', p[2])
        p[0] = Node('ELSE_BLOCO', filhos=[p[2]], folhas=[p[1]])
    else:
        # p[0] = 'empty'
        p[0] = Node('Vazio')


def p_lista_param(p):
    '''
    LISTA_PARAM : PARAMETRO COMMA LISTA_PARAM
                | PARAMETRO
                | empty
    '''
    if len(p) == 4:
        # p[0] = ('LISTA_PARAM', p[1], ',', p[3])
        p[0] = Node('LISTA_PARAM', filhos=[p[1], p[3]], folhas=[p[2]])
    elif len(p) == 2:
        # p[0] = ('LISTA_PARAM', p[1])
        p[0] = Node('LISTA_PARAM', filhos=[p[1]])
    else:
        # p[0] = 'empty'
        p[0] = Node('Vazio')


def p_exp_logica(p):
    '''
    EXP_LOGICA : EXP_MAT OP_LOGICO EXP_LOGICA
               | EXP_MAT
    '''
    if len(p) == 4:
        # p[0] = ('EXP_LOGICA', p[1], p[2], p[3])
        p[0] = Node('EXP_LOGICA longa', filhos=[p[1], p[2], p[3]])
    elif len(p) == 2:
        # p[0] = ('EXP_LOGICA', p[1])
        p[0] = Node('EXP_LOGICA curta', filhos=[p[1]])


def p_exp_mat(p):
    '''
    EXP_MAT : PARAMETRO OP_MAT EXP_MAT
            | PARAMETRO
    '''
    if len(p) == 4:
        # p[0] = ('EXP_MAT', p[1], p[2], p[3])
        p[0] = Node('EXP_MAT longa', filhos=[p[1], p[2], p[3]])
    else:
        # p[0] = ('EXP_MAT', p[1])
        p[0] = Node('EXP_MAT curta', filhos=[p[1]])


def p_PARAMETRO(p):
    '''
    PARAMETRO : ID NOME
              | NUMERO
    '''
    if len(p) == 3:
        # p[0] = ('PARAMETRO', p[1], p[2])
        p[0] = Node('PARAMETRO id', filhos=[p[1], p[2]])
    else:
        # p[0] = ('PARAMETRO', p[1])
        p[0] = Node('PARAMETRO numero', filhos=[p[1]])


def p_op_logico(p):
    '''
    OP_LOGICO : GREATER_THAN
              | SMALLER_THAN
              | EQUAL
              | NEGATION
    '''
    if p[1] == '>':
        # p[0] = p[1]
        p[0] = Node('GREATER_THAN', folhas=[p[1]])
    elif p[1] == '<':
        # p[0] = p[1]
        p[0] = Node('SMALLER_THAN', folhas=[p[1]])
    elif p[1] == '=':
        # p[0] = p[1]
        p[0] = Node('EQUAL', folhas=[p[1]])
    elif p[1] == '!':
        # p[0] = p[1]
        p[0] = Node('NEGATION', folhas=[p[1]])


def p_op_mat(p):
    '''
    OP_MAT : PLUS
          | MINUS
          | MULTIPLICATION
          | DIVIDE
    '''
    if p[1] == '+':
        # p[0] = p[1]
        p[0] = Node('PLUS', folhas=[p[1]])
    elif p[1] == '-':
        # p[0] = p[1]
        p[0] = Node('MINUS', folhas=[p[1]])
    elif p[1] == '*':
        # p[0] = p[1]
        p[0] = Node('MULTIPLICATION', folhas=[p[1]])
    elif p[1] == '/':
        # p[0] = p[1]
        p[0] = Node('DIVIDE', folhas=[p[1]])


def p_nome(p):
    '''
    NOME : DOT ID NOME
         | OPEN_BRACKET PARAMETRO CLOSE_BRACKET
         | OPEN_PARENTHESIS LISTA_PARAM CLOSE_PARENTHESIS
         | empty
    '''
    if len(p) == 4:
        if p[1] == '[':
            # p[0] = ('NOME', '[', p[2], ']')
            p[0] = Node('NOME', filhos=[p[2]], folhas=[p[1], p[3]])
        elif p[1] == '(':
            # p[0] = ('NOME', '(', p[2], ')')
            p[0] = Node('NOME', filhos=[p[2]], folhas=[p[1], p[3]])
        elif p[1] == '.':
            # p[0] = ('NOME', '.', p[2], p[3])
            p[0] = Node('NOME', filhos=[p[2], p[3]], folhas=[p[1]])
    else:
        # p[0] = 'empty'
        p[0] = Node('Vazio')


def p_error(p):
    print(f'Syntax error at {p.value!r} in line {p.lineno!r} and position {p.lexpos!r}')
    exit()


# Build the parser
def my_parser():
    #  for debug use this
    # return yacc(start='PROGRAMA', debug=1)
    return yacc(start='PROGRAMA')
# Parse an expression
# ast = parser.parse('2 * 3 + 4')
# print(ast)
