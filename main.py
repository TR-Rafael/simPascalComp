from intermediateCodeGenerator import intermediateCodeGenerator
from myLexer import my_lexer
from myLexer import my_parser
import json
from mySemantic import creation_of_symbol_table


filename = 'exampleOfCode.simPascal'
print(filename)
with open(filename, 'r', encoding='utf-8') as arquivo:
    code = arquivo.read()
lexer = my_lexer()
parser = my_parser()
ast = parser.parse(code)

with open('intermediateCode.txt', 'w') as arquivo:
    arquivo.write(intermediateCodeGenerator(ast))

with open('Arvore.txt', 'w') as arquivo:
    arquivo.write(ast.printNode())


output = json.dumps(creation_of_symbol_table(ast, current_symbol_table=[]), indent=4, ensure_ascii=False)
with open("tabelaDeSimbolos.json", "w") as outfile:
    outfile.write(output)

