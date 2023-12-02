#
#   |     |     |
#   2     |     |
#   3     1     |
# ----- ----- -----


def define_varetas(discos):
    varetas = [[], [], []]
    varetas[0] = [i for i in range(discos, 0, -1)]

    total = len(varetas[0]) + 1

    varetas[0].insert(0, total)
    varetas[1] = [total]
    varetas[2] = [total]

    return varetas


def desenha_hanoi(varetaA, varetaB, varetaC, discos):
    lista_desenho = []
    desenho = ""
    total = discos + 1
    for i in range(total):
        linha = ""
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

    for i in range(discos, 0, -1):
        desenho += f"{lista_desenho[i]} \n"

    desenho += "----- ----- -----\n  A     B     C"
    return desenho


def hanoi(dados, lista_ver, disco):
    varetaA = dados[0]
    varetaB = dados[1]
    varetaC = dados[2]
    discos = dados[3]
    disco1 = dados[4]

    tupla_cond = (
        lista_ver[0] == True and varetaA[-1] < varetaC[-1],
        lista_ver[1] == True and varetaA[-1] < varetaB[-1],
        lista_ver[2] == True and varetaC[-1] < varetaB[-1],
        lista_ver[3] == True and varetaC[-1] < varetaA[-1],
        lista_ver[4] == True and varetaB[-1] < varetaA[-1],
        lista_ver[5] == True and varetaB[-1] < varetaC[-1],
    )

    if tupla_cond[0]:
        disco = varetaA.pop()
        if disco1 == disco:
            varetaA.append(disco)
            lista_ver[0] = False
            return hanoi(dados, lista_ver, disco)
        else:
            varetaC.append(disco)

    elif tupla_cond[1]:
        disco = varetaA.pop()
        if disco1 == disco:
            varetaA.append(disco)
            lista_ver[1] = False
            return hanoi(dados, lista_ver, disco)
        else:
            varetaB.append(disco)

    elif tupla_cond[2]:
        disco = varetaC.pop()
        if disco1 == disco:
            varetaC.append(disco)
            lista_ver[2] = False
            return hanoi(dados, lista_ver, disco)
        else:
            varetaB.append(disco)

    elif tupla_cond[3]:
        disco = varetaC.pop()
        if disco1 == disco:
            varetaC.append(disco)
            lista_ver[3] = False
            return hanoi(dados, lista_ver, disco)
        else:
            varetaA.append(disco)

    elif tupla_cond[4]:
        disco = varetaB.pop()
        if disco1 == disco:
            varetaB.append(disco)
            lista_ver[4] = False
            return hanoi(dados, lista_ver, disco)
        else:
            varetaA.append(disco)

    elif tupla_cond[5]:
        disco = varetaB.pop()
        if disco1 == disco:
            varetaB.append(disco)
            lista_ver[5] = False
            return hanoi(dados, lista_ver, disco)
        else:
            varetaC.append(disco)

    disco1 = disco
    dados = [varetaA, varetaB, varetaC, discos, disco1]
    return (desenha_hanoi(varetaA, varetaB, varetaC, discos), dados)


def resolver(dados):
    discos = dados[3]
    total = discos + 1
    varetas = define_varetas(discos)
    dados = [varetas[0], varetas[1], varetas[2], discos, 0]

    resultado = hanoi(dados, [True, True, True, True, True, True], dados[4])
    resposta = resultado[0] + "\n\n"

    while len(resultado[1][1]) != total and len(resultado[1][2]) != total:
        resultado = hanoi(
            resultado[1],
            [True, True, True, True, True, True],
            resultado[1][4],
        )
        resposta += resultado[0] + "\n\n"

    return resposta


def jogada(dados, pos):
    varetaA = dados[0]
    varetaB = dados[1]
    varetaC = dados[2]
    discos = dados[3]
    total = discos + 1

    if len(varetaB) != total and len(varetaC) != total:
        disco = int(pos[0])
        vareta = pos[1]
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

        dados[4] = disco

    if len(varetaB) == total or len(varetaC) == total:
        return (
            "Você ganhou!\n" + desenha_hanoi(varetaA, varetaB, varetaC, discos),
            dados,
            False,
        )

    return (desenha_hanoi(varetaA, varetaB, varetaC, discos), dados, True)


def menu():
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
