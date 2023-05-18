from myLexer import my_lexer
from myLexer import my_parser

filename = 'exampleOfCode.simPascal'
print(filename)
with open(filename, 'r', encoding='utf-8') as arquivo:
    code = arquivo.read()
lexer = my_lexer()
parser = my_parser()
# lexer.input(code)
ast = parser.parse(code)
# print(ast)
ast.printNode()





