import sys

import options as options

from myLexer import my_lexer
from myLexer import my_parser

filename = 'exampleOfCode4.simPascal'
print(filename)
with open(filename, 'r', encoding='utf-8') as arquivo:
    code = arquivo.read()
lexer = my_lexer()
parser = my_parser()
# lexer.input(code)
#  OLHA o passo a passo das regras e veja se bate
ast = parser.parse(code, debug=0)
print(ast)





# algo = ('1',2)
# print(','.join(algo))
# print(type(parser.parse(code)))
# teste = ''.join()
# print(teste)

# print(parser.parse(code))
# print(type(parser.parse(code)))
# with open('output_parser.txt', 'w+') as arquivo:
#     arquivo.write('teste')
# Tokenize
# while True:
#     tok = lexer.token()
#     if not tok:
#         break      # No more input
    # print(tok)




