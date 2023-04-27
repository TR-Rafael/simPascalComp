from myLexer import my_lexer

filename = 'exampleOfCode.simPascal'
with open(filename, 'r', encoding='utf-8') as arquivo:
    code = arquivo.read()

lexer = my_lexer()
lexer.input(code)

print(filename)
# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)


