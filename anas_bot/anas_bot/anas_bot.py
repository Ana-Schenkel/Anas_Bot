# """Main module."""

import asyncio
import json
import os

import discord
import comandos.pede_mensagem as p
import jogo_forca.forca_bot as forc
import jogo_forca.forca as f
import jogo_hanoi.torre_de_hanoi as h
import jogo_velha.jogo_da_velha as v
from discord.ext import commands

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all(), help_command=None)
user = os.getcwd()


# Função síncrona para ler documentos
def ler_doc(pasta, arquivo):
    """Essa função lê um arquivo e retorna o seu conteúdo

    Args:
        pasta (str): pasta do arquivo  com '\\'
        arquivo (str): nome do arquivo com o tipo

    Returns:
        str: conteúdo do arquivo .txt
        dict: conteúdo do arquivo .json

    """
    try:
        doc = open(
            user + "\\anas_bot\\anas_bot\\" + pasta + arquivo,
            encoding="utf-8",
            mode="r",
        )
        if "json" in arquivo:
            doc_cont = json.load(doc)
        else:
            doc_cont = doc.read()
        doc.close()
    except:
        doc = open(
            user + "\\anas_bot\\anas_bot\\" + pasta + arquivo,
            encoding="utf-8",
            mode="w",
        )
        doc.write('{"arquivo foi resetado": []}')
        print("O arquivo " + arquivo + " foi resetado, confira!")
        doc_cont = {}

    return doc_cont


# Pega os estados dos jogos anteriores e salva em um dicionário
jogos_forca = ler_doc("jogo_forca\\", "estados_forca.json")
jogos_velha = ler_doc("jogo_velha\\", "estados_velha.json")
jogos_hanoi = ler_doc("jogo_hanoi\\", "estados_hanoi.json")


# Funções assíncronas de processamento dos jogos *********************************************************************


async def bot_velha(channel, jogadores):
    """Essa função processa a jogada do bot, envia e salva seu resultado

    Args:
        channel (str): nome do canal de texto que solicitou as mensagens
        jogadores (tuple): nomes dos jogadores que estão no jogo: bot e usuário

    """
    # Pega o número que deve ser jogado pelo bot
    resultado = v.jogo_da_velha(
        jogos_velha[jogadores[0] + "," + jogadores[1]], jogadores, bot.user.name, ""
    )
    # Envia a jogada do bot no discord
    desenho = v.imprime_grade(resultado[1])
    await channel.send(
        f"**Jogo da Velha de {jogadores[0]} e {jogadores[1]}** \n{resultado[2]}"
    )
    await channel.send(desenho)

    # Atualiza os dados do jogo do dicionário e no arquivo
    jogos_velha[jogadores[0] + "," + jogadores[1]] = [
        resultado[0],
        resultado[1],
        resultado[2],
    ]
    doc = open(user + "\\anas_bot\\anas_bot\\jogo_velha\\estados_velha.json", "w")
    json.dump(jogos_velha, doc)
    doc.close()


async def velha(channel, jogador, message):
    """Essa função verifica se o usuário pode jogar e processa a jogada desejada, atualizando o estado do jogo

    Args:
        channel (str): nome do canal de texto das mensagens
        jogador (Member): informações do usuário que deseja jogar
        message (Message): mensagem enviada pelo usuário no discord
    """
    # Verifica se o jogador está com um jogo em andamento
    jogadores = False
    str_jogadores = ""
    for i in jogos_velha:
        if jogador.name in i:
            jogadores = tuple(i.split(","))
            str_jogadores = i
    # Jogador está com um jogo aberto
    if jogadores:
        # Está na vez do jogador
        if jogador.name == jogadores[jogos_velha[str_jogadores][0]]:
            # Processa a jogada que o jogador deseja fazer
            msg = message.content.strip("$# ")
            if not (msg in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]):
                await channel.send(
                    jogador.name + ", essa não é uma opção possível no jogo da velha"
                )
                return
            resultado = v.jogo_da_velha(
                jogos_velha[str_jogadores], jogadores, bot.user.name, msg
            )
            # Manda se a jogada do usuário ou se ele precisa escolher outra
            desenho = v.imprime_grade(resultado[1])
            await channel.send(
                f"**Jogo da Velha de {jogadores[0]} e {jogadores[1]}** \n{resultado[2]}"
            )
            await channel.send(desenho)
            # Salva a jogada no dicionário
            jogos_velha[str_jogadores] = [resultado[0], resultado[1], resultado[2]]
            # Verifica se o jogo acabou
            if resultado[3] == False:
                # Retira o jogo do dicionário
                jogos_velha.pop(str_jogadores)
            # Atualiza os dados do jogo no arquivo
            doc = open(
                user + "\\anas_bot\\anas_bot\\jogo_velha\\estados_velha.json", "w"
            )
            json.dump(jogos_velha, doc)
            doc.close()
            # Verfica se o jogo continua
            if resultado[3]:
                # Verifica se o próximo jogador é o bot e faz a jogada dele
                if bot.user.name == jogadores[jogos_velha[str_jogadores][0]]:
                    await bot_velha(channel, jogadores)
        # Não é a vez do jogador
        else:
            await channel.send("Não é sua vez " + jogador.name)
    # Jogador não tem jogo aberto
    else:
        await channel.send(
            jogador.name + ", você ainda não iniciou um jogo da velha, digite '$velha'"
        )


async def bot_hanoi(jogador, discos):
    """Essa função resolve a torre de hanoi e envia o a solução

    Args:
        jogador (Member or str): informações do usuário ou canal para o qual a solução deve ser enviada


    """
    # retorna para dados do início do jogo
    total = discos + 1
    varetas = h.define_varetas(discos)
    dados = [varetas[0], varetas[1], varetas[2], discos, 0]
    desenho = h.desenha_hanoi(dados)
    await jogador.send(
        f"**Aqui está uma solução para a sua Torre de Hanói:**\n {desenho}\n"
    )
    # resolve a primera jogada
    resultado = h.hanoi(dados, [True, True, True, True, True, True], dados[4])
    await jogador.send(f"{resultado[0]} \n\n")
    # prende o código até resolver todo o jogo
    while len(resultado[1][1]) != total and len(resultado[1][2]) != total:
        resultado = h.hanoi(
            resultado[1],
            [True, True, True, True, True, True],
            resultado[1][4],
        )
        await jogador.send(f"{resultado[0]}\n")
        await asyncio.sleep(1)


async def hanoi(channel, jogador, message):
    if jogador.name in jogos_hanoi:
        msg = message.content.strip("$% ")
        vareta = msg[-1]
        disco = msg.strip(msg[-1])
        resultado = h.jogada(jogos_hanoi[jogador.name], (disco, vareta))

        await channel.send(f"{jogador.name}, {resultado[0]}")
        jogos_hanoi[jogador.name] = resultado[1]

        desenho = h.desenha_hanoi(jogos_hanoi[jogador.name])
        await channel.send(
            f"**Torre de {jogador.name}**\nObs: digite '$% discoVareta' para fazer sua joagada {desenho}"
        )

        # Verfica se o jogo acabou e retira os dados do jogo
        if resultado[2] == False:
            jogos_hanoi.pop(jogador.name)

        # Atualiza o jogo no arquivo
        doc = open(
            user + "\\anas_bot\\anas_bot\\jogo_hanoi\\estados_hanoi.json",
            encoding="utf-8",
            mode="w",
        )
        json.dump(jogos_hanoi, doc)
        doc.close()
    # Pede para o jogador criar um jogo novo
    else:
        await channel.send(
            jogador.name
            + ", você ainda não iniciou um novo jogo da Torre de Hanói, digite '$hanoi'!"
        )


# Funções assíncronas que definem os parâmetros inciais dos jogos ****************************************************


async def menu_velha(channel, jogador):
    """Essa função opera o menu das configurações iniciais do jogo da velha

    Args:
        channel (str): nome do canal de texto que solicitou as mensagens
        jogador (Member): informações do usuário que deseja jogar

    Returns:
        tupla: nome dos jogadores
        bool: caso false, não se criará um novo jogo

    """
    # menu para decidir os parâmetros iniciais do jogo da forca
    descri = "escolha uma opção:"
    escolhas = ("Jogar com o bot", "Desafiar um amigo", "Ver instruções")
    res = await p.menu3(channel, jogador, "Menu Jogo da Velha", descri, escolhas, bot)
    if res == False:
        return False

    # Adiciona outro jogador como o bot
    if res == "1":
        await channel.send(f"Olá {jogador}, você vai jogar contra mim!")
        jogador1 = bot.user

    # Adiciona o outro jogador como a pessoa marcada
    elif res == "2":
        descri = "marque o amigo com quem vai jogar"
        jogador1 = await p.pede_mention(
            channel, jogador, "Desafio da Velha", descri, bot
        )
        if jogador1 == False:
            return False
        await channel.send(f"{jogador1} foi desafiado para o jogo da velha!")
        # Verifica se a pessoa marcada já estava em outro jogo
        jogadores = False
        for i in jogos_velha:
            if jogador1.name in i:
                jogadores = tuple(i.split(","))
        # A pessoa já estava jogando antes
        if jogadores and (jogador1 != bot.user):
            descri = "você já estava com um jogo em andamento, escolha:"
            escolhas = (
                "Aceitar novo desafio",
                "Retomar jogo anterior e desistir do desafio",
            )
            res = await p.menu2(
                channel, jogador1, "Aceitar desafio da velha?", descri, escolhas, bot
            )
            if res == False:
                return False
            # A pessoa não aceitou o desafio
            if res == "2":
                return jogadores

    # Mostra as instruções
    elif res == "3":
        instru = ler_doc("jogo_velha\\", "instru_velha.txt")
        await channel.send(instru)
        return False

    # Menu para decidir a ordem de quem jogará primeiro
    descri = "escolha uma opção:"
    escolhas = ("Sortear ordem de jogada", "Escolher o primeiro jogador")
    res = await p.menu2(channel, jogador, "Sortear Velha", descri, escolhas, bot)
    if res == False:
        return False
    vez = ""

    # Sortear quem joga primeiro
    if res == "1":
        jogadores = v.sorteia_jogadores(jogador.name, jogador1.name)
        vez = f"{jogadores[0]}, você é o primeiro! (digite '$#' antes do número da sua jogada)"
        desenho = v.imprime_grade("123456789")
        await channel.send(
            f"**{jogadores[0]} e {jogadores[1]}, lembrem que essas são as posições das jogadas:** \n {desenho}**{vez}**"
        )
        # começar jogo da velha
    # Escolher quem joga primeiro
    elif res == "2":
        descri = "escreva quem irá jogar primeiro"
        primeiro_jogador = await p.pede_mention(
            channel, jogador, "Ordem de jogada", descri, bot
        )
        if primeiro_jogador == False:
            return False

        if primeiro_jogador == jogador:
            jogadores = (jogador.name, jogador1.name)
            # ordenar jogador como primeiro
        elif primeiro_jogador == jogador1:
            jogadores = (jogador1.name, jogador.name)
            # ordenar jogador1 como primeiro

        vez = f"{jogadores[0]}, você joga primeiro! (digite '$#' antes do número da sua jogada)"

        desenho = v.imprime_grade("123456789")
        await channel.send(
            f"**{jogadores[0]} e {jogadores[1]}, lembrem que essas são as posições das jogadas:** {desenho}{vez}\n"
        )
        # começar jogo da velha

    # Salva os parâmetros do jogo e atualiza o arquivo
    jogos_velha.update(
        {
            jogadores[0]
            + ","
            + jogadores[1]: [0, [" ", " ", " ", " ", " ", " ", " ", " ", " "], vez]
        }
    )
    doc = open(user + "\\anas_bot\\anas_bot\\jogo_velha\\estados_velha.json", "w")
    json.dump(jogos_velha, doc)
    doc.close()
    # retorna a tupla de jogadores na ordem de jogada
    return jogadores


async def menu_hanoi(channel, jogador):
    """Essa função opera o menu das configurações iniciais do jogo da Torre de Hanói

    Args:
        channel (str): nome do canal de texto que solicitou as mensagens
        jogador (Member): informações do usuário que deseja jogar

    Returns:
        Member: nome do jogador
        bool: caso false, não se criará um novo jogo

    """
    # menu para decidir os parâmetros iniciais do jogo da Torre de Hanói
    descri = "escolha uma opção:"
    escolhas = ("Jogar a Torre de Hanói", "Desafiar um amigo", "Ver instruções")
    res = await p.menu3(channel, jogador, "Menu Torre de Hanoi", descri, escolhas, bot)
    if res == False:
        return False

    # Jogar a Torre
    if res == "1":
        descri = "escolha um nível:"
        escolhas = ("Fácil", "Médio", "Difícil")
        nivel = await p.menu3(channel, jogador, "Nível da Torre", descri, escolhas, bot)
        if nivel == False:
            return False

        await channel.send(f"Olá {jogador}, uma torre de nivel {nivel} foi feita!")
        if nivel == "1":
            discos = 3
        elif nivel == "2":
            discos = 4
        elif nivel == "3":
            discos = 5

    # Desafiar Amigo
    elif res == "2":
        # Pede para o jogador decidir o tamnaho da Torre
        descri = "digite um número entre 2 e 14 para definir a quantidade de discos."
        discos = await p.pede_num(
            channel, jogador, "Tamanho do Desafio Torre", descri, bot
        )

        # Pede o nome do jogador
        descri = "digite quem você deseja desafiar."
        jogador1 = await p.pede_mention(channel, jogador, "Desafio Torre", descri, bot)
        if jogador1 == False:
            return False
        jogador = jogador1
        await channel.send(
            f"{jogador} você foi desafiado para a Torre de Hanoi com {discos} discos!"
        )

        # Verifica quem foi desafiado e o direciona
        # Já estava jogando antes
        if jogador.name in jogos_hanoi:
            # Pergunta se a pessoa quer o desafiou ou não
            descri = "você já estava com um jogo em andamento, escolha:"
            escolhas = (
                "Aceitar novo desafio",
                "Retomar jogo anterior e desistir do desafio",
            )
            res = await p.menu2(
                channel, jogador, "Aceitar desafio da Torre?", descri, escolhas, bot
            )
            if res == False:
                return False
            # Retorna caso a pessoa não aceite
            if res == "2":
                return jogador
        # Desafiou o bot
        elif jogador == bot.user:
            await channel.send("Eu sempre sei resolver esse desafio!")
            # resolve a torre
            await bot_hanoi(channel, discos)

            return False

    # Ver Instruções
    elif res == "3":
        instru = ler_doc("jogo_hanoi\\", "instru_hanoi.txt")
        await channel.send(instru)
        return False

    # Salva os parâmetros
    disco1 = 0
    varetas = h.define_varetas(discos)

    jogos_hanoi.update(
        {jogador.name: [varetas[0], varetas[1], varetas[2], discos, disco1]}
    )
    doc = open(user + "\\anas_bot\\anas_bot\\jogo_hanoi\\estados_hanoi.json", "w")
    json.dump(jogos_hanoi, doc)
    doc.close()

    return jogador


# Funções assíncronas para processar a mensagem enviada **************************************************************


async def verifica_velha(channel, jogador):
    # verifica se já existe um jogo com esse usuário
    jogadores = False
    str_jogadores = ""
    for i in jogos_velha:
        if jogador.name in i:
            jogadores = tuple(i.split(","))
            str_jogadores = i
    # Jogo em andamento
    if jogadores:
        descri = "você já está jogando o jogo da velha, escolha:"
        escolhas = ("Continuar jogo antigo", "Ir para menu")
        res = await p.menu2(
            channel, jogador, "Jogando o jogo da velha", descri, escolhas, bot
        )
        if res == False:
            return False
        # Volta para jogo antigo
        if res == "1":
            desenho = v.imprime_grade(jogos_velha[str_jogadores][1])
            await channel.send(
                f"**Jogo da Velha de {jogadores[0]} e {jogadores[1]}** \n{jogos_velha[str_jogadores][2]}"
            )
            await channel.send(desenho)
        # Vai para menu
        elif res == "2":
            jogadores = await menu_velha(channel, jogador)
            if jogadores:
                if bot.user.name == jogadores[jogos_velha[str_jogadores][0]]:
                    await bot_velha(channel, jogadores)
    # Novo jogo
    else:
        jogadores = await menu_velha(channel, jogador)
        if jogadores:
            if (
                bot.user.name
                == jogadores[jogos_velha[jogadores[0] + "," + jogadores[1]][0]]
            ):
                await bot_velha(channel, jogadores)


async def verifica_hanoi(channel, jogador):
    if jogador.name in jogos_hanoi:
        descri = "você já está jogando a Torre de Hanói, escolha:"
        escolhas = (
            "Continuar jogo antigo",
            "Ver uma possível solução",
            "Ir para menu",
        )
        res = await p.menu3(channel, jogador, "Jogando a torre", descri, escolhas, bot)
        if res == False:
            return False
        # Volta para o jogo antigo
        if res == "1":
            desenho = h.desenha_hanoi(jogos_hanoi[jogador.name])
            await channel.send(
                f"**Torre de {jogador.name}**\nObs: digite '$% discoVareta' para fazer sua jogada. {desenho}"
            )
        # Manda a resolução no privado
        elif res == "2":
            await bot_hanoi(jogador, jogos_hanoi[jogador.name][3])
            await channel.send(
                f"{jogador.name}, a solução foi enviada para você, tente continuar seu jogo:"
            )
            desenho = h.desenha_hanoi(jogos_hanoi[jogador.name])
            await channel.send(
                f"**Torre de {jogador.name}**\nObs: digite '$% discoVareta' para fazer sua jogada. {desenho}"
            )
        # Vai para menu
        elif res == "3":
            jogador = await menu_hanoi(channel, jogador)
            if jogador:
                desenho = h.desenha_hanoi(jogos_hanoi[jogador.name])
                await channel.send(
                    f"**Torre de {jogador.name}**\nObs: digite '$% discoVareta' para fazer sua jogada. {desenho}"
                )
    # Novo jogo
    else:
        jogador = await menu_hanoi(channel, jogador)
        if jogador:
            desenho = h.desenha_hanoi(jogos_hanoi[jogador.name])
            await channel.send(
                f"**Torre de {jogador.name}**\nObs: digite '$% discoVareta' para fazer sua jogada. {desenho}"
            )


# Inicialização do bot ***********************************************************************************************
@bot.event
async def on_ready():
    print(bot.user.name, "está logado")


# Comandos do bot ****************************************************************************************************
@bot.command()
async def help(ctx):
    """Essa função lê o arquivo de ajuda do bot (explica o comandos)

    Args:
        ctx (str): canal de texto da mensagem enviada

    """
    ajuda = ler_doc("comandos\\", "help.txt")
    await ctx.send(ajuda)


@bot.command()
async def info(ctx):
    """Essa função lê o arquivo de informações/curiosidades do bot

    Args:
        ctx (str): canal de texto da mensagem enviada

    """
    info = ler_doc("comandos\\", "info.txt")
    await ctx.send(info)


# Bloco para processar toda mensagem enviada ************************************************************************
@bot.event
async def on_message(message):
    await bot.process_commands(message)  # faz os comandos processarem

    # print(message.content)
    # print(message.channel)
    # print(bot.user)
    channel = message.channel
    jogador = message.author
    # if jogador == bot.user:
    #     return

    # ************************************************* Jogo Forca *************************************************

    global jogos_forca

    # caso o usuário digite $forca, verifica se o usuário tem um jogo em andamento e/ou inicia novos jogos
    if message.content.startswith("$forca"):
        jogos_forca = await forc.verifica_forca(channel, jogador, jogos_forca, bot)

    # faz rodar a forca caso o usuário digite $$letra
    if message.content.startswith("$$"):
        jogos_forca = await forc.forca(channel, jogador, message, jogos_forca)

    # ************************************************* Jogo da Velha *************************************************

    # caso o usuário digite $velha, verifica se o usuário tem um jogo em andamento e/ou inicia novos jogos
    if message.content.startswith("$velha"):
        await verifica_velha(channel, jogador)

    # faz rodar o jogo da velha caso o usuário digite $#número
    if message.content.startswith("$#"):
        await velha(channel, jogador, message)

    # ************************************************* Torre de Hanoi *************************************************

    # caso o usuário digite $velha, verifica se o usuário tem um jogo em andamento e/ou inicia novos jogos
    if message.content.startswith("$hanoi"):
        await verifica_hanoi(channel, jogador)

    # faz rodar o jogo da velha caso o usuário digite $#número
    if message.content.startswith("$%"):
        await hanoi(channel, jogador, message)


# roda o bot definido no token
token = ler_doc("", "token.txt")
try:
    bot.run(token)
except:
    print("Algo errado com o arquivo token.txt, confira!")
