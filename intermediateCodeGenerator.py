label_counter = 0
temp_counter = 0


def intermediateCodeGenerator(tree):
    intermediate_code = ''
    if tree.tipo == 'Vazio':
        return ''

    for filho in tree.filhos:
        intermediate_code = intermediate_code + intermediateCodeGenerator(filho)
    return intermediate_code + handleIntermediateCode(tree)


def handleDefFunction(node):
    code = ''
    if node.tipo == 'Vazio':
        return code

    if node.filhos[0].tipo == 'FUNCAO':
        code = code + handleFunction(node.filhos[0])
    if node.filhos[1].tipo == 'DEF_FUNC':
        code = code + handleDefFunction(node.filhos[1])
    return code


def handleFunction(node):
    global label_counter
    code = ''
    function_name = ''
    param_args = ''

    if node.filhos[0].tipo == 'NOME_FUNCAO':
        nome_funcao = node.filhos[0]
        if nome_funcao.filhos[0].tipo == 'IDENTIFIER':
            function_name = nome_funcao.filhos[0].folhas[0]
        if nome_funcao.filhos[1].tipo == 'PARAM_FUNC':
            param_func = nome_funcao.filhos[1]
            if param_func.filhos[0].tipo == 'CAMPOS':
                param_args = handleCampos(param_func.filhos[0])

    if node.filhos[1].tipo == 'BLOCO_FUNCAO':
        blocoComando = node.filhos[1]
        if blocoComando.filhos[1].tipo.find('COMANDO') != -1:
            code = code + handleComando(blocoComando.filhos[1])
        if blocoComando.filhos[2].tipo == 'LISTA_COM':
            code = code + handleListaCom(blocoComando.filhos[2])

    popCommand = ''

    # return address - RA
    if type(param_args) is str:
        param_args = ['RA']
    else:
        param_args.append('RA')

    for i in range(0, len(param_args)):
        popCommand = f'POP ftemp{i} {param_args[i]}\n'

    startFunction = f'Label{label_counter} {function_name}\n' + popCommand
    endFunction = f'RET ftemp{i}\n'

    return startFunction + code + endFunction


def handleCampos(campos):
    param_args = []
    if campos.filhos[0].tipo == 'IDENTIFIER':
        param_args.append(campos.filhos[0].folhas[0])
    if campos.filhos[2].tipo == 'LISTA_CAMPOS':
        lista_campos = campos.filhos[2]
        if lista_campos.filhos[0].tipo == 'CAMPOS':
            for element in handleCampos(lista_campos.filhos[0]):
                if element not in param_args:
                    param_args.append(element)
    return param_args

def handleComando(comando):
    code = ''
    aliasType = comando.filhos[0].tipo
    if aliasType.find('WHILE') != -1:
        if comando.filhos[0].tipo.find('EXP_LOGICA') != -1:
            code = code + handleExpLogica(comando.filhos[0])
        if comando.filhos[1].tipo == 'BLOCO':
            code = code + handleBloco(comando.filhos[1])



    elif aliasType.find('IF') != -1:
        if comando.filhos[0].tipo.find('EXP_LOGICA') != -1:
            code = code + handleExpLogica(comando.filhos[0])
        if comando.filhos[1].tipo == 'BLOCO':
            code = code + handleBloco(comando.filhos[1])
    # elif aliasType.find('WRITE') != -1:
    # @todo verificar depois se é necessário lidar com tipo CONST_VALOR
    elif aliasType.find('READ') != -1:
        if comando.filhos[0].tipo == 'ID':
            code = code + handleIdentifier(comando.filhos[0])
        if comando.filhos[1].tipo == 'NOME':
            return code + handleNome(comando.filhos[1])
    elif aliasType.find('puro') != -1:
        if comando.filhos[0].tipo == 'ID':
            code = code + handleIdentifier(comando.filhos[0])
        if comando.filhos[1].tipo == 'NOME':
            code = code + handleNome(comando.filhos[1])
        if comando.filhos[2].tipo == 'EXP_MAT':
            code = code + handleExpMat(comando.filhos[2])
    return code


def handleExpLogica(ExpLogica):
    isShortExpression = ExpLogica.filhos[0].tipo.find('curta') != -1
    isEXP_MAT = ExpLogica.filhos[0].tipo.find('EXP_MAT') != -1

    if isEXP_MAT and isShortExpression:
        return handleExpMat(ExpLogica.filhos[0])

    elif isEXP_MAT and ExpLogica.filhos[1].tipo.find('longa') != -1:
        code = handleExpMat(ExpLogica.filhos[0])
        op = code + handleOPLogico(ExpLogica.filhos[1])
        return op + handleExpLogica(ExpLogica.filhos[2])


def handleOPLogico(op):
    if op.tipo == '>':
        # comparison greater than
        return f'CGT'
    elif op.tipo == '<':
        # comparison smaller than
        return f'CST'
    elif op.tipo == '=':
        # comparison is equal
        return f'CIE'
    elif op.tipo == '!':
        # logical negation
        return f'LNG'


def handleOPMat(op):
    if op.tipo == '+':
        return f'ADD'
    elif op.tipo == '-':
        return f'SUB'
    elif op.tipo == '*':
        return f'MUL'
    elif op.tipo == '/':
        return f'DIV'


def handleExpMat(expMat):
    if expMat.filhos[0].tipo == 'PARAMETRO':
        #  Aqui retornará algo como
        code = handleParametro(expMat.filhos[0])
        op = code + handleOPMat(expMat.filhos[1])
        return op + handleExpMat(expMat.filhos[2])
    elif expMat.filhos[0].tipo == 'NUMERO':
        #  Aqui ira retornar algo como : '7'
        return expMat.filhos[0].folhas[0]


def handleParametro(parametro):
    if parametro.filhos[0].tipo == 'ID':
        code = handleIdentifier(parametro.filhos[0])
        return code + handleNome(parametro.filhos[0])
    elif parametro.filhos[0].tipo == 'NUMERO':
        return parametro.filhos[0].folhas[0]


def handleListaParam(listaParam):
    code = ''

    if listaParam.filhos[0].tipo == 'PARAMETRO':
        code = code + handleParametro(listaParam.filhos[0])
    if listaParam.filhos[1].tipo == 'LISTA_PARAM':
        code = code + handleListaParam(listaParam.filhos[1])

    return code


def handleIdentifier(identifier):
    return identifier.folhas[0]


def handleNome(nome):
    if nome.folhas[0] == '[':
        return handleParametro(nome.filhos[0])
    elif nome.folhas[0] == '(':
        return handleListaParam(nome.filhos[0])
    elif nome.folhas[0] == '.':
        return handleIdentifier(nome.filhos[0])


def handleBloco(bloco):
    code = ''
    hasComando = bloco.filhos[0].tipo.find('COMANDO') != -1
    hasBegin = bloco.filhos[0].folhas[0] == 'begin'
    if hasComando:
        handleComando(bloco.filhos[0])
    if hasBegin and bloco.filhos[1].tipo.find('LISTA_COM') != -1:
        handleListaCom(bloco.filhos[1])
    return code


def handleElseBloco(elseBloco):
    return elseBloco(elseBloco.filhos[0])


def handleListaCom(listaCom):
    code = ''
    if listaCom.filhos[0].tipo.find('COMANDO') != -1:
        handleComando(listaCom.filhos[0])
    if listaCom.filhos[1].tipo == 'LISTA_COM':
        handleListaCom(listaCom.filhos[1])

    return code


def handleIntermediateCode(node):
    global temp_counter
    global label_counter
    code = ''
    if node.tipo == 'Vazio':
        return code
    elif node.tipo == 'DEF_FUNC':
        code = handleDefFunction(node)
    elif node.tipo == 'PARAMETRO id':
        code = f'MOV temp{temp_counter} {node.filhos[0].folhas[0]}\n'
        temp_counter += + 1
    elif node.tipo == 'PARAMETRO numero':
        code = f'MOV temp{temp_counter} {node.filhos[0].folhas[0]}\n'
        temp_counter += + 1

    return code
