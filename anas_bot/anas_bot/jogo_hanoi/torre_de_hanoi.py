#
#   |     |     |
#   2     |     |
#   3     1     |
# ----- ----- -----


def define_varetas(discos):
    """Essa função forma as listas de cada vareta de acordo com a quantidade de discos

    Args:
        discos (int): quantidade de discos

    Returns:
        list: listas de cada vareta
    """
    varetas = [[], [], []]
    # cada lista recebe um disco de base, de valor maior que o último disco jogável
    varetas[0] = [i for i in range(discos, 0, -1)]
    total = len(varetas[0]) + 1
    varetas[0].insert(0, total)
    varetas[1] = [total]
    varetas[2] = [total]

    return varetas


def desenha_hanoi(varetaA, varetaB, varetaC, discos):
    """Essa função desenha o jogo de acordo com os estados de cada lista de vareta

    Args:
        discos (int): quantidade de discos

    Returns:
        str: desenho das varetas
    """
    lista_desenho = []
    desenho = ""
    total = discos + 1
    # o desenho terá a quantidade de linhas = quantidade de discos
    # percorre e "forma" cada linha do desenho
    for i in range(total):
        linha = ""
        # verifica se há disco na vareta, adiciona o disco ou um "|"
        try:
            linha += f"  {varetaA[i]}   "
        except IndexError:
            linha += f"  |   "
        try:
            linha += f"  {varetaB[i]}   "
        except IndexError:
            linha += f"  |   "
        try:
            linha += f"  {varetaC[i]}   "
        except IndexError:
            linha += f"  |   "

        lista_desenho.append(linha)
    # ordena as linhas
    for i in range(discos, 0, -1):
        desenho += f"{lista_desenho[i]} \n"
    # adiciona linha de base e retorna
    desenho += "----- ----- -----\n  A     B     C"
    return desenho


def hanoi(dados, lista_ver, disco):
    """Essa função resolve a torre de hanoi

    Args:
        dados (list): lista com os dados do jogo, incluindo as listas das varetas, a quantidade total de discos e o último disco jogado
        lista_ver: lista de bool para verificar se cada condição já foi feita
        disco: disco que está tentando mover

    Returns:
        str: todas as jogadas até chegar na solução
    """
    # torna os dados mais legíveis
    varetaA = dados[0]
    varetaB = dados[1]
    varetaC = dados[2]
    discos = dados[3]
    disco1 = dados[4]
    # tupla das condições de todos os movimentos possíveis em ordem de prioridade
    tupla_cond = (
        lista_ver[0] == True and varetaA[-1] < varetaC[-1],  # A -> C
        lista_ver[1] == True and varetaA[-1] < varetaB[-1],  # A -> B
        lista_ver[2] == True and varetaC[-1] < varetaB[-1],  # C -> B
        lista_ver[3] == True and varetaC[-1] < varetaA[-1],  # C -> A
        lista_ver[4] == True and varetaB[-1] < varetaA[-1],  # B -> A
        lista_ver[5] == True and varetaB[-1] < varetaC[-1],  # B -> C
    )

    # verifica o primeiro movimento possível A -> C
    if tupla_cond[0]:
        # pega o disco da vareta de origem
        disco = varetaA.pop()
        # verifica se o disco é o mesmo que foi jogado anteriormente
        if disco1 == disco:
            # desiste do movimento e chama novamente a função, com essa condição já verificada
            varetaA.append(disco)
            lista_ver[0] = False
            return hanoi(dados, lista_ver, disco)
        else:
            # finaliza o movimento
            varetaC.append(disco)
    # verifica o segundo movimento possível A -> B
    elif tupla_cond[1]:
        disco = varetaA.pop()
        if disco1 == disco:
            varetaA.append(disco)
            lista_ver[1] = False
            return hanoi(dados, lista_ver, disco)
        else:
            varetaB.append(disco)
    # verifica o terceiro movimento possível C -> B
    elif tupla_cond[2]:
        disco = varetaC.pop()
        if disco1 == disco:
            varetaC.append(disco)
            lista_ver[2] = False
            return hanoi(dados, lista_ver, disco)
        else:
            varetaB.append(disco)
    # verifica o quarto movimento possível C -> A
    elif tupla_cond[3]:
        disco = varetaC.pop()
        if disco1 == disco:
            varetaC.append(disco)
            lista_ver[3] = False
            return hanoi(dados, lista_ver, disco)
        else:
            varetaA.append(disco)
    # verifica o quinto movimento possível B -> A
    elif tupla_cond[4]:
        disco = varetaB.pop()
        if disco1 == disco:
            varetaB.append(disco)
            lista_ver[4] = False
            return hanoi(dados, lista_ver, disco)
        else:
            varetaA.append(disco)
    # verifica o sexto movimento possível B -> C
    elif tupla_cond[5]:
        disco = varetaB.pop()
        if disco1 == disco:
            varetaB.append(disco)
            lista_ver[5] = False
            return hanoi(dados, lista_ver, disco)
        else:
            varetaC.append(disco)
    # atualiza o último disco jogado e retorna o resultado de uma jogada
    disco1 = disco
    dados = [varetaA, varetaB, varetaC, discos, disco1]
    return (desenha_hanoi(varetaA, varetaB, varetaC, discos), dados)


def resolver(dados):
    """Essa função mostra uma solução possível para o jogo

    Args:
        dados (list): lista com os dados do jogo, incluindo as listas das varetas, a quantidade total de discos e o último disco jogado

    Returns:
        str: todas as jogadas até chegar na solução
    """
    # retorna para dados do início do jogo
    discos = dados[3]
    total = discos + 1
    varetas = define_varetas(discos)
    dados = [varetas[0], varetas[1], varetas[2], discos, 0]
    # resolve a primera jogada
    resultado = hanoi(dados, [True, True, True, True, True, True], dados[4])
    resposta = resultado[0] + "\n\n"
    # prende o código até resolver todo o jogo
    while len(resultado[1][1]) != total and len(resultado[1][2]) != total:
        resultado = hanoi(
            resultado[1],
            [True, True, True, True, True, True],
            resultado[1][4],
        )
        resposta += resultado[0] + "\n\n"

    return resposta


def jogada(dados, pos):
    """Essa função move os discos nas varetas de acordo com o usuário

    Args:
        dados (list): lista com os dados do jogo, incluindo as listas das varetas, a quantidade total de discos e o último disco jogado
        pos (str): jogada do usuário, "númeroLetra"

    Returns:
        tupla: resultado da jogada, dados e True se o jogo continua
    """
    # tranfere os dados para variáveis mais legíveis
    varetaA = dados[0]
    varetaB = dados[1]
    varetaC = dados[2]
    discos = dados[3]
    total = discos + 1

    # verifica se o jogo continua
    if len(varetaB) != total and len(varetaC) != total:
        disco = int(pos[0])
        vareta = pos[1]
        # verifica para qual vareta o usuário deseja mover o disco
        if vareta in "Aa":
            vareta = varetaA
            dados[0] = vareta
        elif vareta in "Bb":
            vareta = varetaB
            dados[1] = vareta
        elif vareta in "Cc":
            vareta = varetaC
            dados[2] = vareta
        else:
            return (
                "Essa posição é inválida, tente novamente.\n"
                + desenha_hanoi(varetaA, varetaB, varetaC, discos),
                dados,
                True,
            )
        # verifica se o disco a ser movido é menor que o da vareta de destino
        if disco < vareta[-1]:
            # verfica se o disco está por cima
            if disco == varetaA[-1]:
                disco = varetaA.pop()
                vareta.append(disco)
            elif disco == varetaB[-1]:
                disco = varetaB.pop()
                vareta.append(disco)
            elif disco == varetaC[-1]:
                disco = varetaC.pop()
                vareta.append(disco)
            else:
                return (
                    "Você não pode mexer esse disco, tente novamente.\n"
                    + desenha_hanoi(varetaA, varetaB, varetaC, discos),
                    dados,
                    True,
                )
        else:
            return (
                "Você não pode colocar um disco maior em cima de um menor.\n"
                + desenha_hanoi(varetaA, varetaB, varetaC, discos),
                dados,
                True,
            )

        dados[4] = disco
    # verifica se o jogo acabou
    if len(varetaB) == total or len(varetaC) == total:
        return (
            "Você ganhou!\n" + desenha_hanoi(varetaA, varetaB, varetaC, discos),
            dados,
            False,
        )
    # retorna a jogada com sucesso
    return (desenha_hanoi(varetaA, varetaB, varetaC, discos), dados, True)


def menu():
    """Essa função permite jogar pelo terminal, apresentando o menu e pedindo as jogadas"""
    disco1 = 0
    discos = int(input("Número de discos:\n"))
    varetas = define_varetas(discos)
    dados = [varetas[0], varetas[1], varetas[2], discos, disco1]

    jogo = jogada(dados, input())
    print(jogo[0], jogo[1], jogo[2])
    while jogo[2]:
        res = input("Digite sua jogada:\n")
        if res == "1":
            solucao = resolver(jogo[1])
            print(solucao)
            break
        else:
            jogo = jogada(dados, res)
            print(jogo[0])


if __name__ == "__main__":
    menu()
