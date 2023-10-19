#  X | O | O
# ___|___|___
#  O | X | O
# ___|___|___
#    | X | X
#    |   |

from random import *


def lista_jogadores():
    """Essa função pergunta ao usuário quem participará do jogo e qual a ordem de jogada

    Returns:
        list: todos os jogadores da partida na ordem de jogada
    """
    jogador1 = input("Digite o nome do jogador 1: ").lower()
    jogador2 = input("Digite o nome do jogador 2: ").lower()

    if "s" in input("Devo sortear quem joga primeiro?\n").lower():
        i = randint(0, 1)
        jogadores[i] = jogador1
        jogadores[not i] = jogador2
    else:
        jogadores[0] = jogador1
        jogadores[1] = jogador2

    return jogadores


def faz_jogada(jogador):
    """Essa função processa a próxima jogada do bot ou solicita que o usuário digite sua jogada.

    Args:
       jogador (int): index do jogador na lista "jogadores"

    Returns:
       int: posição da jogada na grade
    """
    # vez do bot
    if "bot" in jogadores[jogador]:
        print(jogadores[jogador], "jogou:")
        # duas varíaveis para apoiar o processamento da jogada: cópia da grade e
        # verificador de vezes em que todos escolhas foram percorridos
        grade_apoio = grade.copy()
        ver = 0
        # listas de prioridades de combinações
        urgencias = (("X*X", "XX*", "*XX"), ("O*O", "OO*", "*OO"))
        interessantes = (
            ("X* ", "X *", "*X ", " X*", "* X", " *X"),
            ("O* ", "O *", "*O ", " O*", "* O", " *O"),
        )
        # lista de todas as escolhas possíveis
        lista_escolhas = []
        jogada = -1

        while jogada == -1:
            if grade_apoio.count(" ") != 0:
                # verifica a próxima escolha possível
                escolha = grade_apoio.index(" ")
            else:
                # muda o verificador e "reinicia" a grade depois que todas as escolhas são percorridas
                for i in range(grade_apoio.count("*")):
                    grade_apoio[grade_apoio.index("*")] = " "
                escolha = grade_apoio.index(" ")
                ver += 1

            # marca a escolha em análise
            grade_apoio[escolha] = "*"
            lista_escolhas.append(escolha)

            analise = verifica_vitoria(grade_apoio)

            match ver:
                # ordena as prioridades de jogada
                case 0:
                    lista_analise = urgencias[jogador]
                case 1:
                    lista_analise = urgencias[not jogador]
                case 2:
                    lista_analise = interessantes[jogador]
                case 3:
                    lista_analise = interessantes[not jogador]
                case 4:
                    # prioridades gerais, como no início do jogo
                    if 4 in lista_escolhas:
                        escolha = 4
                    elif 0 in lista_escolhas:
                        escolha = 0
                    elif 2 in lista_escolhas:
                        escolha = 2
                    elif 6 in lista_escolhas:
                        escolha = 6
                    elif 8 in lista_escolhas:
                        escolha = 8
                    jogada = escolha
                    return jogada
            # verifica cada valor na ordem de prioridade, caso a escolha coincida com
            # alguma opção de prioridade, retorna a escolha como jogada
            for i in lista_analise:
                if i in analise:
                    jogada = escolha
                    return jogada
    # vez do usuário
    else:
        jogada = (
            int(input("Digite a posição da sua jogada " + jogadores[jogador] + ": "))
            - 1
        )
        return jogada


def imprime_grade(grade_desenho):
    """Essa função organiza os valores da grade em um tabuleiro de jogo da velha.

    Args:
       grade_desenho (interável): os valores com index da grade

    Returns:
      str : desenho do tabuleiro
    """

    desenho = "\n"
    # variável que auxilia a contar as linhas a serem concatenadas, "contador"
    cont = 0
    # percorre as linhas
    for linha in range(3):
        if linha != 2:
            divisao = "\n___|___|___\n"
        else:
            divisao = "\n   |   |   \n"
        # percorre os valores das linhas
        for i in range(3):
            desenho += " " + grade_desenho[i + cont] + " |"
        desenho = desenho.strip("|") + divisao
        # a cada linha percorrida, soma 3 ao contador
        cont += 3

    return desenho


def verifica_vitoria(grade_vitoria):
    """Essa função verifica os valores da grade recebida e retorna as combinações das retas de vitória.

    Args:
        grade_vitoria (list): valores com index do tabuleiro.

    Returns:
        str : combinaçõess das retas de vitória separadas por espaço.
    """
    # dicionário com retas de vitória
    vitoria = {
        "linhas": ["", "", ""],
        "colunas": [
            "",
            "",
            "",
        ],
        "diagonais": ["", ""],
    }

    for chave in vitoria:
        # variável que auxilia a contar os valores a serem concatenados, "contador"
        cont = 0
        match chave:
            case "linhas":
                for linha in range(len(vitoria[chave])):
                    # percorre os valores de uma linha
                    for i in range(3):
                        vitoria[chave][linha] += grade_vitoria[i + cont]
                    # adiciona 3 ao contador quando uma linha é percorrida, ou seja, recebe o
                    # index do primeiro valor da próxima linha
                    cont += 3
            case "colunas":
                for coluna in range(len(vitoria[chave])):
                    # percorre os valores de uma coluna
                    for i in range(3):
                        vitoria[chave][coluna] += grade_vitoria[i + cont]
                        # a cada valor adiciona 2 ao contador, pois em uma coluna o próximo valor
                        # está dois valores na frente do próximo index
                        cont += 2
                    # o contador recebe o index do primeiro valor da próxima coluna
                    cont = coluna + 1
            case "diagonais":
                for diagonal in range(len(vitoria[chave])):
                    # percorre os valores de uma diagonal
                    for i in range(3):
                        vitoria[chave][diagonal] += grade_vitoria[i + cont]
                        if diagonal == 0:
                            # a cada valor adiciona 3 ao contador, pois está na primeira diagonal
                            cont += 3
                        if diagonal == 1:
                            # a cada valor adiciona 1 ao contador, pois está na segunda diagonal
                            cont += 1
                    # o contador recebe o index do primeiro valor da próxima diagonal
                    cont = 2
    # transforma o dicionário em uma string
    vitoria = " ".join([" ".join(i) for i in vitoria.values()])
    return vitoria


def jogo_da_velha():
    """Essa função controla a vez de cada jogador e quem é o vencedor.

    Returns:
        int: index do vencedor na lista de jogadores
    """

    # setup inicial do jogo
    str_vitoria = verifica_vitoria(grade)
    print("Essas são as posições das jogadas: \n", imprime_grade("123456789"))
    jogador = 0

    # laço que prende os jogadores até o fim do jogo
    while not ("XXX" in str_vitoria or "OOO" in str_vitoria):
        if grade.count(" ") == 0:
            jogador = 2
            return jogador

        jogada = faz_jogada(jogador)

        # força o usuário a jogar em um espaço vazio
        while grade[jogada] != " ":
            print("Espaço ocupado, tente novamente.")
            jogada = int(input())

        # marca a jogada e troca o jogador
        if jogador == 0:
            grade[jogada] = "X"
            jogador += 1
        elif jogador == 1:
            grade[jogada] = "O"
            jogador -= 1

        # atualiza o desenho da grade e as retas de vitória
        str_vitoria = verifica_vitoria(grade)
        print(imprime_grade(grade))

    return not jogador


grade = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
jogadores = ["", "", "Velha"]

if __name__ == "__main__":
    lista_jogadores()
    print(jogadores[jogo_da_velha()], "ganhou")
