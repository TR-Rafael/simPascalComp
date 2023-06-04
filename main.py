from myLexer import my_lexer
from myLexer import my_parser


def define_tipo(node):
    aux = node.tipo
    if aux.find('integer') != -1 or aux.find('real') != -1:
        return node.folhas[0]
    elif aux.find('id') != -1:
        return node.filhos[0].folhas[0]
    elif aux.find('record') != -1:
        return node.folhas[0]
    elif aux.find('array') != -1:
        return f'array[{node.filhos[0].folhas[0]}] of {define_tipo(node.filhos[1])}'


def handle_list_id(node, escopo, tipo):
    if node.tipo == 'Vazio':
        return []

    simbolo = {}
    simbolo['nome'] = node.filhos[0].folhas[0]
    simbolo['classificacao'] = 'VARIAVEL'
    simbolo['tipo'] = tipo
    simbolo['escopo'] = escopo
    simbolo['qtd'] = '-'
    simbolo['ordem'] = '-'

    return [simbolo] + handle_list_id(node=node.filhos[1], escopo=escopo, tipo=tipo)

def aux_def_var(node, escopo):
    if node.tipo == 'Vazio':
        return []

    list_of_vars = []
    simbolo = {}
    if node.filhos[0].tipo == 'VARIAVEL':
        variavel = node.filhos[0]
        simbolo['nome'] = variavel.filhos[0].folhas[0]
        simbolo['classificacao'] = 'VARIAVEL'
        simbolo['tipo'] = define_tipo(variavel.filhos[2])
        simbolo['escopo'] = escopo
        simbolo['qtd'] = '-'
        simbolo['ordem'] = '-'
        list_of_vars.append(simbolo)
        if variavel.filhos[1].tipo == 'LISTA_ID':
            lista_id = variavel.filhos[1]
            list_of_vars = list_of_vars + handle_list_id(node=lista_id,escopo=escopo, tipo=define_tipo(variavel.filhos[2]))

    if node.filhos[1].tipo == 'DEF_VAR':
        list_of_vars = list_of_vars + aux_def_var(node=node.filhos[1], escopo=escopo)

    return list_of_vars

def aux_campos(node, escopo, index, classificacao):
    if node.tipo == 'Vazio':
        return []

    simbolo = {}
    simbolo['nome'] = node.filhos[0].folhas[0]
    simbolo['classificacao'] = classificacao
    simbolo['tipo'] = define_tipo(node.filhos[1])
    simbolo['escopo'] = escopo
    simbolo['qtd'] = '-'
    simbolo['ordem'] = index
    if node.filhos[2].tipo == 'LISTA_CAMPOS':
        return [simbolo] + aux_campos(node=node.filhos[2].filhos[0], escopo=escopo, index=index + 1, classificacao=classificacao)

    return [simbolo] + aux_campos(node=node.filhos[2], escopo=escopo, index=index + 1, classificacao=classificacao)


def creation_of_symbol_table(node, escopo='global'):
    if node.tipo == 'Vazio':
        return []

    part_of_symbol_table = []

    if node.tipo == 'DECLARACOES':
        if node.filhos[2].tipo == 'DEF_VAR':
            aux_vars = aux_def_var(node=node.filhos[2], escopo='global')
            part_of_symbol_table = part_of_symbol_table + aux_vars

    elif node.tipo == 'TIPO':
        simbolo = {}
        information_about_the_type = []
        simbolo['nome'] = node.filhos[0].folhas[0]
        simbolo['classificacao'] = 'TIPO'
        tipo = define_tipo(node.filhos[1])
        simbolo['tipo'] = tipo
        if tipo.find('record') != -1:
            if node.filhos[1].filhos[0].tipo == 'CAMPOS':
                campos = node.filhos[1].filhos[0]
                information_about_the_type = aux_campos(node=campos, index=0, escopo=node.filhos[0].folhas[0],
                                                        classificacao='CAMPOS DE RECORD')
                part_of_symbol_table = part_of_symbol_table + information_about_the_type

        simbolo['escopo'] = escopo
        simbolo['qtd'] = '-' if len(information_about_the_type) == 0 else len(information_about_the_type)
        simbolo['ordem'] = '-'
        part_of_symbol_table.append(simbolo)
    elif node.tipo == 'FUNCAO':
        simbolo = {}
        information_about_the_parameters = []
        if node.filhos[0].tipo == 'NOME_FUNCAO':
            nome_func = node.filhos[0]
            simbolo['nome'] = nome_func.filhos[0].folhas[0]
            if nome_func.filhos[1].tipo == 'PARAM_FUNC':
                param_func = nome_func.filhos[1]
                if param_func.filhos[0].tipo == 'CAMPOS':
                    campos = param_func.filhos[0]
                    information_about_the_parameters = aux_campos(node=campos, index=0, escopo=nome_func.filhos[0].folhas[0],
                                                                  classificacao='PARAMETROS DE FUNÇÃO')
                    part_of_symbol_table = part_of_symbol_table + information_about_the_parameters

        if node.filhos[1].tipo == 'BLOCO_FUNCAO':
            if node.filhos[1].filhos[0].tipo == 'DEF_VAR':
                aux_vars = aux_def_var(node=node.filhos[1].filhos[0], escopo=node.filhos[0].filhos[0].folhas[0])
                part_of_symbol_table = part_of_symbol_table + aux_vars
        simbolo['classificacao'] = 'FUNCAO'
        simbolo['tipo'] = define_tipo(node.filhos[0].filhos[2])
        simbolo['escopo'] = escopo
        simbolo['qtd'] = '-' if len(information_about_the_parameters) == 0 else len(information_about_the_parameters)
        simbolo['ordem'] = '-'
        part_of_symbol_table.append(simbolo)
    elif node.tipo == 'CONSTANTE':
        simbolo = {}
        simbolo['nome'] = node.filhos[0].folhas[0]
        simbolo['classificacao'] = 'CONSTANTE'
        simbolo['tipo'] = 'vou descobrir ainda'
        simbolo['escopo'] = escopo
        simbolo['qtd'] = '-'
        simbolo['ordem'] = '-'
        part_of_symbol_table.append(simbolo)

    for filho in node.filhos:
        part_of_symbol_table += creation_of_symbol_table(filho)
    return part_of_symbol_table


filename = 'exampleOfCode.simPascal'
print(filename)
with open(filename, 'r', encoding='utf-8') as arquivo:
    code = arquivo.read()
lexer = my_lexer()
parser = my_parser()
# lexer.input(code)
ast = parser.parse(code)
teste = creation_of_symbol_table(ast)
for elemento in teste:
    print(elemento)
