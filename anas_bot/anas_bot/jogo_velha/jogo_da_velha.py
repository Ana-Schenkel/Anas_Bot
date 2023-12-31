"""
Módulo das funções síncronas para o jogo da velha, inclui a lógica fundamental para o funcionamento do jogo.

Funções:
    sorteia_jogadores(jogador1 = str, jogador2 = str)
    faz_jogada(jogador = int, grade = list)
    imprime_grade(grade_desenho = list)
    verifica_vitoria(grade_vitoria = list)
    jogo_da_velha(dados = list, jogadores = tuple, bot = str, mensagem = str)
    
"""
#  X | O | O
# ___|___|___
#  O | X | O
# ___|___|___
#    | X | X
#    |   |

from random import randint


def sorteia_jogadores(jogador1, jogador2):
    """Essa função sorteia a ordem de jogadores

    Returns:
        list: todos os jogadores da partida na ordem de jogada
    """
    jogadores = ["", "", ""]

    i = randint(0, 1)
    jogadores[i] = jogador1
    jogadores[not i] = jogador2

    jogadores[2] = "Velha"

    jogadores = tuple(jogadores)

    return jogadores


def faz_jogada(jogador, grade):
    """Essa função processa a próxima jogada do bot

    Args:
       jogador (int): index do bot na lista "jogadores"
       grade (list): grade que forma o tabuleiro do jogo da velha

    Returns:
       int: posição da jogada na grade
    """
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
        # verifica cada valor na ordem de prioridade, caso a escolha coincida com
        # alguma opção de prioridade, retorna a escolha como jogada
        for i in lista_analise:
            if i in analise:
                jogada = escolha
    return jogada


def imprime_grade(grade_desenho):
    """Essa função organiza os valores da grade em um tabuleiro de jogo da velha.

    Args:
       grade_desenho (interável): os valores com index da grade

    Returns:
      str : desenho do tabuleiro
    """

    desenho = "```\n"
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
    desenho += "```"
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
    # variável auxiliar para determinar o índice do próximo valor da linha, coluna ou diagonal (contador)
    cont = 0
    # percorre cada linha
    for linha in range(len(vitoria["linhas"])):
        # percorre os valores de uma linha
        for i in range(3):
            vitoria["linhas"][linha] += grade_vitoria[i + cont]
        # adiciona 3 ao contador quando uma linha é percorrida, ou seja, recebe o
        # index do primeiro valor da próxima linha
        cont += 3
    cont = 0
    # percorre cada coluna
    for coluna in range(len(vitoria["colunas"])):
        # percorre os valores de uma coluna
        for i in range(3):
            vitoria["colunas"][coluna] += grade_vitoria[i + cont]
            # a cada valor adiciona 2 ao contador, pois em uma coluna o próximo valor
            # está dois valores na frente do próximo index
            cont += 2
        # o contador recebe o index do primeiro valor da próxima coluna
        cont = coluna + 1
    cont = 0
    # percorre cada diagonal
    for diagonal in range(len(vitoria["diagonais"])):
        # percorre os valores de uma diagonal
        for i in range(3):
            vitoria["diagonais"][diagonal] += grade_vitoria[i + cont]
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


def jogo_da_velha(dados, jogadores, bot, mensagem):
    """Essa função controla a vez de cada jogador e quem é o vencedor.

    Args:
        dados (list): dados gerais do jogo, inclui o indice do próximo jogador, a grade e a mensagem de orientação.
        jogadores (tuple): tupla com os dois participantes do jogo
        bot (str): nome do bot
        mensagem (str): jogada do último jogador

    Returns:
        tuple: tupla com os dados do jogo atualizados
    """
    indice_jogador = dados[0]
    grade = dados[1]
    # atualiza as retas de vitória
    str_vitoria = verifica_vitoria(grade)

    # laço que prende os jogadores até o fim do jogo
    if not ("XXX" in str_vitoria or "OOO" in str_vitoria):
        # vez do bot
        if bot == jogadores[indice_jogador]:
            jogada = faz_jogada(indice_jogador, grade)
        # vez do usuário
        else:
            jogada = int(mensagem) - 1

        # força o usuário a jogar em um espaço vazio
        if grade[jogada] != " ":
            return (indice_jogador, grade, "**Espaço ocupado, tente novamente**", True)

        # marca a jogada e troca o jogador
        if indice_jogador == 0:
            grade[jogada] = "X"
            indice_jogador += 1
        elif indice_jogador == 1:
            grade[jogada] = "O"
            indice_jogador -= 1

        # atualiza as retas de vitória
        str_vitoria = verifica_vitoria(grade)

        if grade.count(" ") == 0:
            return (indice_jogador, grade, "**Deu Velha!**  :older_woman:", False)

        elif "XXX" in str_vitoria or "OOO" in str_vitoria:
            return (
                not indice_jogador,
                grade,
                "**" + jogadores[not indice_jogador] + " ganhou!**  :snake:",
                False,
            )
        else:
            return (
                indice_jogador,
                grade,
                jogadores[not indice_jogador]
                + " jogou! Vez de "
                + jogadores[indice_jogador]
                + " (digite '$#' antes do número da sua jogada)",
                True,
            )

    else:
        return (
            indice_jogador,
            grade,
            "**" + jogadores[indice_jogador] + " você ganhou!!**",
            False,
        )


if __name__ == "__main__":
    print(
        "Infelizamente, esse jogo está adaptado para o discord e não para o terminal."
    )
