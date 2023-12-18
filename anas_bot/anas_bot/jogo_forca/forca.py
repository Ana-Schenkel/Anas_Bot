"""
Módulo das funções síncronas para o jogo da forca, inclui a lógica fundamental para o funcionamento do jogo.

Variável global:
    tuple : tupla_forca

Funções:
    sorteia_palavra(nivel = str)
    retira_acento(palavra = str)
    letra_certa(letra = str, palavra = str, chute = str)
    desenha_forca(dados = list)
    forca(dados = list, mensagem = str)
"""
#  |
#  |_0
#   /|\
#   / \

import os
from random import randint


def sorteia_palavra(nivel):
    """Essa função sorteia uma palavra de acordo com o nível de dificuldade escolhido

    Args:
        nivel (str): nível de dificuldade da palavra

    Returns:
        str: palavra sorteada do arquivo
    """

    # decide as linhas a serem sorteadas de acordo com o nível
    if nivel == "1":
        linha = randint(1, 30)
    elif nivel == "2":
        linha = randint(33, 62)
    elif nivel == "3":
        linha = randint(65, 93)

    # abre o arquivo de acordo com o usuário
    path = os.path.dirname(__file__)
    with open(path + "\\palavras.txt", encoding="utf-8", mode="r") as doc_palavras:
        # lê o documento até chegar na linha sorteada
        contador = 0
        for i in doc_palavras:
            if contador == linha:
                palavra = i.strip("\n")
                # print(palavra)
                break
            contador += 1

    return palavra


def retira_acento(palavra):
    """Essa função retira os acentos e maiúsculas de uma str

    Args:
        palavra (str): palavra a ser formatada

    Returns:
        str: palavra formatada
    """
    acentos = {"a": "áàãâ", "e": "éê", "i": "í", "o": "óõô", "u": "ú", "c": "ç"}

    # percorre as chaves (letras sem acentos) do dicionário acentos
    for letra in acentos:
        # percorre os acentos de cada letra
        for acento in acentos[letra]:
            if acento in palavra:
                palavra = palavra.replace(acento, letra)
    palavra = palavra.lower()

    return palavra


def letra_certa(letra, palavra, chute):
    """Essa função incorpora a nova letra ou sílaba testada no "chute"
    (palavra formada de acordo com as letras testadas)

    Args:
        letra (str): letra ou sílaba testada pelo usuário
        palavra (str): palavra a ser adivinhada
        chute (str): palavra formada com as letras testadas

    Returns:
        str: palavra formada com a nova letra ou sílaba testada
    """
    # variável auxiliar para o index da letra ou sílaba testada na palavra
    index_silaba = 0
    # repete a ação pela quantidade de vezes que a letra ou sílaba aparece na palavra
    vezes = 0
    while vezes != palavra.count(letra):
        # i recebe o index da primeira aparição da letra ou sílaba a partir do i anterior
        index_silaba = palavra.index(letra, index_silaba)
        # percorre todos os index das letras da sílaba
        for index_letra in range(len(letra)):
            # o index é a soma do index da letra ou sílaba na palavra e do index da letra na sílaba
            index = index_silaba + index_letra
            # substitui o espaço em branco pela letra testada
            chute = chute[:index] + letra[index_letra] + chute[index + 1 :]
        # soma 1 ao i atual para ler a próxima aparição da palavra
        index_silaba += 1
        vezes += 1

    return chute


def desenha_forca(dados):
    """Essa função desenha a forca de acordo com os parâmetros atuais

    Args:
        dados (list): lista com os parâmetros atuais do jogo [palavra, chute, usados, vida]

    Returns:
        str: desenho da forca
    """

    chute = dados[1]
    usados = dados[2]
    vida = dados[3]

    # desenha a forca de acordo com a vida
    return (
        "\nObs: digite '$$' antes da letra\n"
        "```"
        + tupla_forca[vida]
        + "\n"
        + " ".join(chute)
        + "\nLetras testadas: "
        + " ".join(usados)
        + "```"
    )


def forca(dados, mensagem):
    """Essa função testa as letras ou sílabas digitadas e controla a vida do jogador,
    decidindo o resultado final do jogo

    Args:
        dados (list): lista com os parâmetros atuais do jogo [palavra, chute, usados, vida]
        mensagem (str): letra ou sílaba a ser testada

    Returns:
        tupla: resultado do teste (str), parâmetros alterados (list), se o jogo continua (bool)
    """
    # estabelesce os parâmetros do jogo de acordo com os dados
    palavra = dados[0]
    chute = dados[1]
    usados = dados[2]
    vida = int(dados[3])

    # verifica se o jogador já acertou a palavra
    if palavra != chute:
        letra = retira_acento(mensagem)
        palavra_formatada = retira_acento(palavra)

        # verifica se o jogador já usou essa letra ou sílaba
        if letra in usados:
            return ("Já usou essa letra", dados, True)

        # testa se a letra está na palavra
        if letra in palavra_formatada:
            chute = letra_certa(letra, palavra_formatada, chute)
            # retorna os acentos para o chute
            for i in range(len(chute)):
                if chute[i] != "_":
                    chute = chute[:i] + palavra[i] + chute[i + 1 :]
            # adiciona a letra ou sílaba testada para a lista de usados
            usados.append(letra)
            # verifica se a palavra está completa
            if palavra == chute:
                return (
                    "Você venceu! A palavra era " + palavra + "  :snake:",
                    [palavra, chute, usados, vida],
                    False,
                )
            else:
                return ("Tem essa letra", [palavra, chute, usados, vida], True)
        else:  # a letra não está na palavra
            vida -= 1
            # adiciona a letra ou sílaba testada para a lista de usados
            usados.append(letra)
            if vida == 0:
                return (
                    "Você perdeu, a palavra era " + palavra + "  :eagle:",
                    [palavra, chute, usados, vida],
                    False,
                )
            else:
                return (
                    'A palavra não tem "'
                    + letra
                    + '", você pode errar mais '
                    + str(vida)
                    + " vezes",
                    [palavra, chute, usados, vida],
                    True,
                )

    else:
        return "Parabéns! A palavra era " + palavra


# desenho da forca
tupla_forca = (
    "| \n|_0 \n /|\\ \n / \\",
    "| \n|_0 \n /|\\ \n /",
    "| \n|_0\n /|\\ \n",
    "| \n|_0\n /| \n",
    "| \n|_0 \n  | \n",
    "| \n|_0 \n\n",
    "| \n|_ \n\n",
)

if __name__ == "__main__":
    print(
        "Infelizamente, esse jogo está adaptado para o discord e não para o terminal."
    )
