from myLexer import my_lexer
from myLexer import my_parser
import json

def search (lista, valor):
    return [(lista.index(x), x.index(valor)) for x in lista if valor in x]
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
            list_of_vars = list_of_vars + handle_list_id(node=lista_id, escopo=escopo, tipo=define_tipo(variavel.filhos[2]))

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


def handle_comando(node, current_symbol_table, escopo):
    tipo_of_node = lambda x: node.tipo.find(x) != -1
    # print('dentro do handle comando, a seguir o tipo de node que entrou')
    # print(current_symbol_table)
    # print('depois')
    if tipo_of_node('WHILE'):
        print('teste WHILE')
    elif tipo_of_node('IF'):
        print('teste IF')
    elif tipo_of_node('WRITE'):
        print('teste WRITE')
    elif tipo_of_node('READ'):
        print('teste READ')
    elif tipo_of_node('puro'):
        id_exist = False
        id = node.filhos[0].folhas[0]
        for node_in_list in current_symbol_table:
            if node_in_list['nome'] == id:
                id_exist = True
        # if not id_exist:
        #     # TODO adicionar linha que ocorreu o problema
        #     print(f'Semantic error the variable {id!r} was not declared before use.')
        #     exit(1)

        # mat_exp = node.filhos[2]
        # if mat_exp.tipo.find('EXP_MAT') != -1:
        #     if mat_exp.tipo.find('longa') != -1:
        #         print('longa')
        #     else:
        #         print('curta')
    return []


def handle_lista_comando(node, current_symbol_table, escopo):
    aux = []

    if node.tipo == 'Vazio':
        return aux

    if node.filhos[0].tipo.find('COMANDO') != -1:
        aux += handle_comando(node=node.filhos[0], current_symbol_table=current_symbol_table, escopo=escopo)

    if node.filhos[1].tipo == 'LISTA_COM':
        aux += handle_lista_comando(node=node.filhos[1], current_symbol_table=current_symbol_table, escopo=escopo)

    return aux

def aux_def_tipos(node, escopo, current_symbol_table):
    if node.tipo == 'Vazio':
        return []

    if node.filhos[0].tipo == 'TIPO':
        node_tipo = node.filhos[0]
        simbolo = {}
        information_about_the_type = []
        simbolo['nome'] = node_tipo.filhos[0].folhas[0]
        simbolo['classificacao'] = 'TIPO'
        tipo = define_tipo(node_tipo.filhos[1])
        simbolo['tipo'] = tipo
        if tipo.find('record') != -1:
            if node_tipo.filhos[1].filhos[0].tipo == 'CAMPOS':
                campos = node_tipo.filhos[1].filhos[0]
                information_about_the_type = aux_campos(node=campos, index=0, escopo=node_tipo.filhos[0].folhas[0],
                                                        classificacao='CAMPOS DE RECORD')
                current_symbol_table = current_symbol_table + information_about_the_type

        simbolo['escopo'] = escopo
        simbolo['qtd'] = '-' if len(information_about_the_type) == 0 else len(information_about_the_type)
        simbolo['ordem'] = '-'
        current_symbol_table.append(simbolo)

    if node.filhos[1].tipo == 'DEF_TIPOS':
        current_symbol_table = current_symbol_table + aux_def_tipos(node=node.filhos[1], escopo=escopo,
                                                                    current_symbol_table=current_symbol_table)

    return current_symbol_table


def creation_of_symbol_table(node, escopo='global', current_symbol_table=[]):
    part_of_symbol_table = current_symbol_table

    if node.tipo == 'Vazio':
        return []
    elif node.tipo == 'DECLARACOES':
        if node.filhos[1].tipo == 'DEF_TIPOS':
            def_tipos = node.filhos[1]
            aux_tipos = aux_def_tipos(node=def_tipos, escopo='global', current_symbol_table=part_of_symbol_table)
            part_of_symbol_table = part_of_symbol_table + aux_tipos

        if node.filhos[2].tipo == 'DEF_VAR':
            aux_vars = aux_def_var(node=node.filhos[2], escopo='global')
            part_of_symbol_table = part_of_symbol_table + aux_vars

    elif node.tipo == 'PRINCIPAL':
        if node.filhos[0].tipo.find('COMANDO') != -1:
            handle_comando(node=node.filhos[0], current_symbol_table=part_of_symbol_table, escopo='global')
        if node.filhos[1].tipo == 'LISTA_COM':
            handle_lista_comando(node=node.filhos[1], current_symbol_table=part_of_symbol_table, escopo='global')


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
        if node.filhos[1].tipo == 'BLOCO_FUNCAO':
            bloco_funcao = node.filhos[1]
            # print('BLOCO função Comando')
            # print(bloco_funcao.filhos[1].tipo)
            # print(bloco_funcao.filhos[1].folhas[0])
            if bloco_funcao.filhos[1].tipo.find('COMANDO') != -1:
                handle_comando(node=bloco_funcao.filhos[1], current_symbol_table=part_of_symbol_table,
                               escopo=node.filhos[0].filhos[0].folhas[0])
            # print('BLOCO lista Comando')
            # print(bloco_funcao.filhos[2].tipo)
            # print(bloco_funcao.filhos[2].folhas[0])
            if bloco_funcao.filhos[2].tipo == 'LISTA_COM':
                handle_lista_comando(node=bloco_funcao.filhos[2], current_symbol_table=part_of_symbol_table,
                                     escopo=node.filhos[0].filhos[0].folhas[0])

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
        for elemento in creation_of_symbol_table(filho, current_symbol_table=part_of_symbol_table):
            if elemento not in part_of_symbol_table:
                part_of_symbol_table.append(elemento)

    return part_of_symbol_table


filename = 'exampleOfCode.simPascal'
print(filename)
with open(filename, 'r', encoding='utf-8') as arquivo:
    code = arquivo.read()
lexer = my_lexer()
parser = my_parser()
ast = parser.parse(code)
output = json.dumps(creation_of_symbol_table(ast, current_symbol_table=[]), indent=4, ensure_ascii=False)
with open("tabelaDeSimbolos.json", "w") as outfile:
    outfile.write(output)

# ast.printNode()
# Regras semânticas que serão consideradas no trabalho de implementação do compilador:
#
#  [ X ] - Criar tabela de simbolos.
#  [ X ] - Declaração de Id antes do uso. - Parcialmente
#  [   ] - Só permite atribuição com tipos iguais.
#  [   ] - Só posso passar parâmetros para funções.
#  [   ] - Quantidade de parâmetros na chamada da função deve ser igual a da declaração.
#  [   ] - O tipo dos argumentos passados nas funções deve ser igual ao tipo dos parâmetros.
#  [   ] - Só pode usar índice ([]) em variáveis do tipo vetor.
#  [   ] -  Só pode acessar índices entre 1 e o valor passado entre [] em variáveis do tipo vetor#.
#  [   ] -  Só pode usar campo (.) em variáveis do tipo registro.
#  [   ] -  Só posso acessar campo de registro declarado.
