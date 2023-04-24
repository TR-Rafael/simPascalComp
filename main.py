#!/usr/bin/python
# import grammar
# import sys
#!/usr/bin/python
# import ply

from ply import lex

filename = 'exampleOfCode2.simPascal'
with open(filename, 'r', encoding='utf-8') as arquivo:
    code = arquivo.read()


'''
palavras reservadas
bool break for false if int return string true void while
'''
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

tokens = ['SEMICOLON', 'ASSIGMENT', 'COLON', 'DOT', 'COMMA', 'EQUAL', 'OPEN_BRACKET', 'CLOSE_BRACKET', 'OPEN_PARENTHESIS',
          'CLOSE_PARENTHESIS', 'NEGATION', 'SMALLER_THAN', 'GREATER_THAN', 'PLUS', 'MINUS', 'MULTIPLICATION', 'DIVIDE',
          'IDENTIFIER', 'STRING', 'NUMBER'
          ] + list(reserved.values())

'''
tokens e simbolos
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


# t_ASPAS			= r'\"'


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
    t.value = float(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_COMMENT_MONOLINE(t):
    r"""//.*"""
    pass
    # No return value. Token discarded


lexer = lex.lex()
lexer.input(code)
# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
print(filename)
# print(code)

