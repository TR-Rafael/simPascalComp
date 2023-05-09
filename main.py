from myLexer import my_lexer
from myLexer import my_parser

filename = 'exampleOfCode.simPascal'
with open(filename, 'r', encoding='utf-8') as arquivo:
    code = arquivo.read()
lexer = my_lexer()
parser = my_parser()
# lexer.input(code)
parser.parse(code)
print(filename)
# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    # print(tok)




