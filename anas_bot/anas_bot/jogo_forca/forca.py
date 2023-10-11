#  |
#  |_0
#   /|\
#   / \

import os
from random import *


def menu():
    """Esta função pergunta ao usuário qual a palavra ou se ele deseja sortear do arquivo

    Returns:
        str: palavra a ser adivinhada no jogo da forca
    """

    if "amigo" in input(
        "Você deseja desafiar um amigo ou sortear uma palavra do arquivo? \n"
    ):
        palavra = input("Escreva uma palavra para ele adivinhar: ")
    else:
        nivel = input("Escolha um nível (fácil, médio ou difícil): ")
        palavra = sorteia_palavra(nivel)

    return palavra


def sorteia_palavra(nivel):
    """Essa função sorteia uma palavra de acordo com o nível de dificuldade

    Args:
        nivel (str): nível de dificuldade da palavra

    Returns:
        str: palavra sorteada do arquivo
    """

    # abre o arquivo de acordo com o usuário
    user = os.getcwd()
    doc_palavras = open(
        user + "\\anas_bot\\anas_bot\\jogo_forca\\palavras.txt",
        encoding="utf-8",
        mode="r",
    )

    # decide as linhas a serem sorteadas de acordo com o nível
    if nivel == "fácil":
        linha = randint(1, 30)
    elif nivel == "médio":
        linha = randint(33, 62)
    elif nivel == "difícil":
        linha = randint(65, 93)

    # lê o documento até chegar na linha sorteada
    contador = 0
    for i in doc_palavras:
        if contador == linha:
            palavra = i.strip("\n")
            # print(palavra)
            break
        contador += 1
    doc_palavras.close()

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
    i = 0
    # repete a ação pela quantidade de vezes que a letra ou sílaba aparece na palavra
    for vezes in range(palavra.count(letra)):
        # i recebe o index da primeira aparição da letra ou sílaba a partir do i anterior
        i = palavra.index(letra, i)
        # percorre todos os index das letras da sílaba
        for j in range(len(letra)):
            # o index é a soma do index da letra ou sílaba na palavra e do index da letra na sílaba
            index = i + j
            # substitui o espaço em branco pela letra testada
            chute = chute[:index] + letra[j] + chute[index + 1 :]
        # soma 1 ao i atual para ler a próxima aparição da palavra
        i += 1

    return chute


def forca_simples(palavra):
    """Essa função testa as letras ou sílabas digitadas, desenha a forca e controla a vida do jogador,
    decidindo o resultado final do jogo

    Args:
        palavra (str): palavra a ser adivinhada

    Returns:
        str: resultado do jogo
    """

    chute = len(palavra) * "_"
    usados = []
    vida = 6

    # prende o jogador até ele acertar a palavra ou perder o jogo
    while palavra != chute:
        # desenha a forca de acordo com a vida
        print(
            forca[vida]
            + "\n"
            + " ".join(chute)
            + "\nLetras testadas: "
            + " ".join(usados)
        )

        if vida == 0:
            return "Você perdeu"
        else:
            letra = retira_acento(input())
            palavra_formatada = retira_acento(palavra)

            # prende o jogador até ele usar uma nova letra
            while letra in usados:
                print("Já usou essa letra")
                letra = input()

            # testa se a letra está na palavra
            if letra in palavra_formatada:
                chute = letra_certa(letra, palavra_formatada, chute)
                # retorna os acentos para o chute
                for i in range(len(chute)):
                    if chute[i] != "_":
                        chute = chute[:i] + palavra[i] + chute[i + 1 :]
            else:
                vida -= 1
                print(
                    'A palavra não tem "' + letra + '", você pode errar mais',
                    vida,
                    "vezes",
                )

            #adiciona a letra ou sílaba testada para a lista de usados
            usados.append(letra)

    return "Parabéns! A palavra era " + palavra

#desenho da forca
forca = (
    "| \n|_0 \n /|\\ \n / \\",
    "| \n|_0 \n /|\\ \n /",
    "| \n|_0\n /|\\ \n",
    "| \n|_0\n /| \n",
    "| \n|_0 \n  | \n",
    "| \n|_0 \n\n",
    "| \n|_ \n\n",
)

if __name__ == "__main__":
    print(forca_simples(menu()))
