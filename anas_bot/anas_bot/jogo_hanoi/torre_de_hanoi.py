"""
Módulo das funções síncronas para o jogo da Torre de Hanói, inclui a lógica fundamental para o funcionamento do jogo.

Funções:
    define_varetas(discos = int)
    desenha_hanoi(dados = list)
    hanoi(dados = list, lista_ver = list, disco = int)
    resolver(dados = list)
    jogada(dados = list, pos = tuple)
"""
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
    # cada lista recebe um disco de base, de valor maior que o último disco jogável, para evitar erros de índice
    varetas[0] = list(range(discos, 0, -1))
    total = len(varetas[0]) + 1
    varetas[0].insert(0, total)
    varetas[1] = [total]
    varetas[2] = [total]

    return varetas


def desenha_hanoi(dados):
    """Essa função desenha o jogo de acordo com os estados de cada lista de vareta

    Args:
        dados (list): lista com dados do jogo, inclui as listas das varetas, o total de discos e o último disco jogado

    Returns:
        str: desenho das varetas
    """
    # deixa os dados mais legíveis
    varetaA = dados[0]
    varetaB = dados[1]
    varetaC = dados[2]
    discos = dados[3]

    lista_desenho = []
    desenho = ""
    total = discos + 1
    # o desenho terá a quantidade de linhas = quantidade de discos
    # percorre e "forma" cada linha do desenho
    for i in range(total):
        linha = ""
        # verifica se há disco na vareta, adiciona o disco ou um "|"
        try:
            if varetaA[i] < 10:
                linha += f"  {varetaA[i]}   "
            elif varetaA[i] >= 10:
                linha += f" {varetaA[i]}   "

        except IndexError:
            linha += "  |   "
        try:
            if varetaB[i] < 10:
                linha += f"  {varetaB[i]}   "
            elif varetaB[i] >= 10:
                linha += f" {varetaB[i]}   "
        except IndexError:
            linha += "  |   "
        try:
            if varetaC[i] < 10:
                linha += f"  {varetaC[i]}   "
            elif varetaC[i] >= 10:
                linha += f" {varetaC[i]}   "
        except IndexError:
            linha += "  |   "

        lista_desenho.append(linha)
    # ordena as linhas
    for i in range(discos, 0, -1):
        desenho += f"{lista_desenho[i]} \n"
    # adiciona linha de base e retorna
    desenho = "```" + desenho + "----- ----- -----\n  A     B     C ```"
    return desenho


def hanoi(dados, lista_ver, disco):
    """Essa função resolve uma jogada da torre de hanoi, de acordo com o estado do jogo
    (não avança se o estado do jogo estiver diferente do 'ideal')

    Args:
        dados (list): lista com dados do jogo, inclui as listas das varetas, o total de discos e o último disco jogado
        lista_ver: lista de bool para verificar se cada condição já foi feita
        disco: disco que está tentando mover

    Returns:
        str: a próxima jogada certa
    """
    # torna os dados mais legíveis
    varetaA = dados[0]
    varetaB = dados[1]
    varetaC = dados[2]
    discos = dados[3]
    disco1 = dados[4]
    # tupla das condições de todos os movimentos possíveis em ordem de prioridade
    tupla_cond = (
        lista_ver[0] and varetaA[-1] < varetaC[-1],  # A -> C
        lista_ver[1] and varetaA[-1] < varetaB[-1],  # A -> B
        lista_ver[2] and varetaC[-1] < varetaB[-1],  # C -> B
        lista_ver[3] and varetaC[-1] < varetaA[-1],  # C -> A
        lista_ver[4] and varetaB[-1] < varetaA[-1],  # B -> A
        lista_ver[5] and varetaB[-1] < varetaC[-1],  # B -> C
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
        # finaliza o movimento
        varetaC.append(disco)
    # verifica o segundo movimento possível A -> B
    elif tupla_cond[1]:
        disco = varetaA.pop()
        if disco1 == disco:
            varetaA.append(disco)
            lista_ver[1] = False
            return hanoi(dados, lista_ver, disco)
        varetaB.append(disco)
    # verifica o terceiro movimento possível C -> B
    elif tupla_cond[2]:
        disco = varetaC.pop()
        if disco1 == disco:
            varetaC.append(disco)
            lista_ver[2] = False
            return hanoi(dados, lista_ver, disco)
        varetaB.append(disco)
    # verifica o quarto movimento possível C -> A
    elif tupla_cond[3]:
        disco = varetaC.pop()
        if disco1 == disco:
            varetaC.append(disco)
            lista_ver[3] = False
            return hanoi(dados, lista_ver, disco)
        varetaA.append(disco)
    # verifica o quinto movimento possível B -> A
    elif tupla_cond[4]:
        disco = varetaB.pop()
        if disco1 == disco:
            varetaB.append(disco)
            lista_ver[4] = False
            return hanoi(dados, lista_ver, disco)
        varetaA.append(disco)
    # verifica o sexto movimento possível B -> C
    elif tupla_cond[5]:
        disco = varetaB.pop()
        if disco1 == disco:
            varetaB.append(disco)
            lista_ver[5] = False
            return hanoi(dados, lista_ver, disco)
        varetaC.append(disco)
    # atualiza o último disco jogado e retorna o resultado de uma jogada
    disco1 = disco
    dados = [varetaA, varetaB, varetaC, discos, disco1]
    return (desenha_hanoi(dados), dados)


def resolver(dados):
    """Essa função mostra uma solução possível para o jogo

    Args:
        dados (list): lista com dados do jogo, inclui as listas das varetas, o total de discos e o último disco jogado

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
    resposta = resultado[0].strip("`") + "\n\n"
    # prende o código até resolver todo o jogo
    while len(resultado[1][1]) != total and len(resultado[1][2]) != total:
        resultado = hanoi(
            resultado[1],
            [True, True, True, True, True, True],
            resultado[1][4],
        )
        resposta += resultado[0].strip("`") + "\n\n"

    return resposta


def jogada(dados, pos):
    """Essa função move os discos nas varetas de acordo com o usuário

    Args:
        dados (list): lista com dados do jogo, inclui as listas das varetas, o total de discos e o último disco jogado
        pos (tuple): jogada do usuário, (número, letra)

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
            letra = "A"
        elif vareta in "Bb":
            vareta = varetaB
            dados[1] = vareta
            letra = "B"
        elif vareta in "Cc":
            vareta = varetaC
            dados[2] = vareta
            letra = "C"
        else:
            return (
                "essa posição é inválida, tente novamente.",
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
                    "você não pode mexer esse disco, tente novamente.",
                    dados,
                    True,
                )
        else:
            return (
                "você não pode colocar um disco maior em cima de um menor.",
                dados,
                True,
            )

        dados[4] = disco
    # verifica se o jogo acabou
    if len(varetaB) == total or len(varetaC) == total:
        return (
            "você ganhou!!  :snake:",
            dados,
            False,
        )
    # retorna a jogada com sucesso
    return (f"você moveu o disco {disco} para a vareta {letra}.", dados, True)


if __name__ == "__main__":
    print(
        "Infelizamente, esse jogo está adaptado para o discord e não para o terminal."
    )
    disc = input(
        "Se quiser, você pode ver uma solução por aqui, digite o número de discos.\n"
    )
    print(resolver([0, 0, 0, int(disc)]))
