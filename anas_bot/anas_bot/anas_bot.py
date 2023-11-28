# """Main module."""

import json
import os

import discord
import jogo_forca.forca as f
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


# Funções assíncronas para pedir e verificar mensagens do usuário ****************************************************
async def menu2(channel, jogador, titulo, descri, escolhas):
    """Essa função recebe as características de um embed de menu com duas escolhas e retorna a resposta do usuário

    Args:
        channel (str): nome do canal de texto que solicitou as mensagens
        jogador (Member): informações do usuário que irá responder
        titulo (str): title do embed
        descri (str): descrição do menu
        escolhas (tuple): possíveis escolhas do usuário

    Returns:
        str: conteúdo da resposta do usuário

    """

    def check_menu2(m):
        autor = m.channel == channel and m.author == jogador
        resposta = m.content == "1" or m.content == "2"
        return autor and resposta

    embed = discord.Embed(
        title=titulo,
        description=f"{jogador.name}, {descri} \n 1 - {escolhas[0]} \n 2 - {escolhas[1]}",
        color=0xFF5733,
    )
    await channel.send(embed=embed)
    try:
        msg = await bot.wait_for("message", timeout=120.0, check=check_menu2)
    except TimeoutError:
        await channel.send(
            f"O tempo de responder ao {titulo} acabou {jogador.name}, tente novamente"
        )
        return False

    return msg.content


async def menu3(channel, jogador, titulo, descri, escolhas):
    """Essa função recebe as características de um embed de menu com três escolhas e retorna a resposta do usuário

    Args:
        channel (str): nome do canal de texto que solicitou as mensagens
        jogador (Member): informações do usuário que irá responder
        titulo (str): title do embed
        descri (str): descrição do menu
        escolhas (tuple): possíveis escolhas do usuário

    Returns:
        str: conteúdo da resposta do usuário

    """

    def check_menu3(m):
        autor = m.channel == channel and m.author == jogador
        resposta = m.content == "1" or m.content == "2" or m.content == "3"
        return autor and resposta

    embed = discord.Embed(
        title=titulo,
        description=f"{jogador.name}, {descri} \n 1 - {escolhas[0]} \n 2 - {escolhas[1]} \n 3 - {escolhas[2]}",
        color=0xFF5733,
    )
    await channel.send(embed=embed)

    try:
        msg = await bot.wait_for("message", timeout=120.0, check=check_menu3)
    except TimeoutError:
        await channel.send(
            f"O tempo de responder ao {titulo} acabou {jogador.name}, tente novamente"
        )
        return False

    return msg.content


async def pede_mention(channel, jogador, titulo, descri):
    """Essa função recebe as características de um embed que pede que o usuário marque outra pessoa

    Args:
        channel (str): nome do canal de texto que solicitou as mensagens
        jogador (Member): informações do usuário que irá responder
        titulo (str): title do embed
        descri (str): descrição do embed

    Returns:
        Member: pessoa marcada pelo usuário

    """

    def check_mention(m):
        autor = m.channel == channel and m.author == jogador
        mention = m.mentions
        if len(mention) > 1 or mention == []:
            return False
        else:
            return True and autor

    embed = discord.Embed(
        title=titulo,
        description=f"{jogador.name}, {descri} (marque com @nome)",
        color=0xFF5733,
    )
    await channel.send(embed=embed)
    try:
        pessoa = await bot.wait_for("message", timeout=120.0, check=check_mention)
        pessoa = pessoa.mentions
        pessoa = pessoa[0]
    except TimeoutError:
        await channel.send(
            f"O tempo de responder ao {titulo} acabou {jogador.name}, tente novamente"
        )
        return False

    return pessoa


async def pede_dm(jogador, descri):
    """Essa função recebe as características de um embed de menu com duas escolhas e retorna a resposta do usuário

    Args:
        channel (str): nome do canal de texto que solicitou as mensagens
        jogador (Member): informações do usuário que irá responder
        descri (str): descrição da mensagem enviada pelo bot

    Returns:
        str: conteúdo da resposta do usuário

    """
    await jogador.send(descri)
    try:
        palavra = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda x: x.channel == jogador.dm_channel and x.author == jogador,
        )
        palavra = palavra.content
    except TimeoutError:
        await jogador.send(
            f"O tempo de digitar a palavra acabou {jogador.name}, tente novamente"
        )
        return False
    return palavra


# Funções assíncronas que definem os parâmetros inciais dos jogos ****************************************************
async def menu_forca(channel, jogador):
    """Essa função opera o menu das configurações iniciais do jogo da forca

    Args:
        channel (str): nome do canal de texto que solicitou as mensagens
        jogador (Member): informações do usuário que deseja jogar

    Returns:
        str: member que irá jogar
        bool: caso false, não se criará um novo jogo

    """
    # menu para decidir os parâmetros iniciais do jogo da forca
    descri = "escolha uma opção:"
    escolhas = ("Sortear uma palavra", "Desafiar um amigo", "Ver instruções")
    res = await menu3(channel, jogador, "Menu Forca", descri, escolhas)
    if res == False:
        return False

    # Sortear Palavra
    if res == "1":
        descri = "escolha uma nível:"
        escolhas = ("Fácil", "Médio", "Difícil")
        nivel = await menu3(channel, jogador, "Sorteia Forca", descri, escolhas)
        if nivel == False:
            return False

        await channel.send(f"Olá {jogador}, uma palavra de nivel {nivel} foi sorteada!")
        palavra = f.sorteia_palavra(nivel)

    # Desafiar Amigo
    elif res == "2":
        # Pede uma palavra na DM
        # await jogador.send("Digite a palavra que você deseja que adivinhem na forca!")
        # try:
        #     palavra = await bot.wait_for(
        #         "message",
        #         timeout=300.0,
        #         check=lambda x: x.channel == jogador.dm_channel and x.author == jogador,
        #     )
        # except TimeoutError:
        #     await channel.send(
        #         f"O tempo de digitar a palavra acabou {jogador.name}, tente novamente"
        #     )
        #     return False

        palavra = await pede_dm(
            jogador, "Digite a palavra que você deseja que adivinhem na forca!"
        )
        if palavra == False:
            return False

        # Pede o nome do jogador
        descri = "digite quem você deseja desafiar"
        jogador1 = await pede_mention(channel, jogador, "Desafio forca", descri)
        if jogador1 == False:
            return False
        jogador = jogador1

        # Verifica quem foi desafiado e o direciona
        # Já estava jogando antes
        if jogador.name in jogos_forca:
            await channel.send(f"{jogador} você foi desafiado para o jogo da forca!")
            # Pergunta se a pessoa quer o desafiou ou não
            descri = "você já estava com um jogo em andamento, escolha:"
            escolhas = (
                "Aceitar novo desafio",
                "Retomar jogo anterior e desistir do desafio",
            )
            res = await menu2(
                channel, jogador, "Aceitar desafio da forca?", descri, escolhas
            )
            if res == False:
                return False
            # Retorna caso a pessoa não aceite
            if res == "2":
                return jogador
        # Desafiou o bot
        elif jogador == bot.user:
            await channel.send(
                "Você não pode me desafiar! (eu já sei a palavra huahua)"
            )
            return False
        # Desafiou uma pessoa nova
        else:
            await channel.send(f"{jogador} você foi desafiado para o jogo da forca!")

    # Ver Instruções
    elif res == "3":
        instru = ler_doc("jogo_forca\\", "instru_forca.txt")
        await channel.send(instru)
        return False

    # Salva os parâmetros
    chute = ""
    for i in range(len(palavra)):
        if palavra[i] == " ":
            chute += " "
        else:
            chute += "_"

    usados = []
    vida = 6

    jogos_forca.update({jogador.name: [palavra, chute, usados, vida]})
    doc = open(user + "\\anas_bot\\anas_bot\\jogo_forca\\estados_forca.json", "w")
    json.dump(jogos_forca, doc)
    doc.close()

    return jogador


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
    res = await menu3(channel, jogador, "Menu Jogo da Velha", descri, escolhas)
    if res == False:
        return False

    # Adiciona outro jogador como o bot
    if res == "1":
        await channel.send(f"Olá {jogador}, você vai jogar contra mim!")
        jogador1 = bot.user

    # Adiciona o outro jogador como a pessoa marcada
    elif res == "2":
        descri = "marque o amigo com quem vai jogar"
        jogador1 = await pede_mention(channel, jogador, "Desafio da Velha", descri)
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
            res = await menu2(
                channel, jogador1, "Aceitar desafio da velha?", descri, escolhas
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
    res = await menu2(channel, jogador, "Sortear Velha", descri, escolhas)
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
        primeiro_jogador = await pede_mention(
            channel, jogador, "Ordem de jogada", descri
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


# Funções assíncronas de processamento dos jogos *********************************************************************
async def forca(channel, jogador, message):
    """Essa função verifica se o usuário pode jogar e testa a letra digitada pelo jogador, atualizando o estado do jogo

    Args:
        channel (str): nome do canal de texto das mensagens
        jogador (Member): informações do usuário que deseja jogar
        message (Message): mensagem enviada no discord
    """

    # verifica se o jogador tem um jogo salvo
    if jogador.name in jogos_forca:
        msg = message.content.strip("$ ")
        resultado = f.forca(
            jogos_forca[jogador.name], msg
        )  # função que processa a letra

        await channel.send(resultado[0])
        jogos_forca[jogador.name] = resultado[1]

        desenho = f.desenha_forca(jogos_forca[jogador.name])
        await channel.send(f"**Forca de {jogador.name}** {desenho}")

        # Verfica se o jogo acabou e retira os dados do jogo
        if resultado[2] == False:
            jogos_forca.pop(jogador.name)

        # Atualiza o jogo no arquivo
        doc = open(
            user + "\\anas_bot\\anas_bot\\jogo_forca\\estados_forca.json",
            encoding="utf-8",
            mode="w",
        )
        json.dump(jogos_forca, doc)
        doc.close()
    # Pede para o jogador criar um jogo novo
    else:
        await channel.send(
            jogador.name
            + ", você ainda não iniciou um novo jogo de forca, digite '$forca'!"
        )


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
        f"**Jogo da Velha de {jogadores[0]} e {jogadores[1]}** \n{resultado[2]} {desenho}"
    )

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
                f"**Jogo da Velha de {jogadores[0]} e {jogadores[1]}** \n{resultado[2]} {desenho}"
            )
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
    ajuda = open(
        user + "\\anas_bot\\anas_bot\\comandos\\help.txt",
        encoding="utf-8",
        mode="r",
    )
    ajuda_ = ajuda.read()
    ajuda.close()
    await ctx.send(ajuda_)


@bot.command()
async def info(ctx):
    """Essa função lê o arquivo de informações/curiosidades do bot

    Args:
        ctx (str): canal de texto da mensagem enviada

    """
    info = open(
        user + "\\anas_bot\\anas_bot\\comandos\\info.txt",
        encoding="utf-8",
        mode="r",
    )
    info_ = info.read()
    info.close()
    await ctx.send(info_)


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

    # caso o usuário digite $forca, verifica se o usuário tem um jogo em andamento e/ou inicia novos jogos
    if message.content.startswith("$forca"):
        # Jogo em andamento
        if jogador.name in jogos_forca:
            descri = "você já está jogando a forca, escolha:"
            escolhas = ("Continuar jogo antigo", "Ir para menu")
            res = await menu2(channel, jogador, "Jogando a forca", descri, escolhas)
            if res == False:
                return False
            # Volta para o jogo antigo
            if res == "1":
                desenho = f.desenha_forca(jogos_forca[jogador.name])
                await channel.send(f"**Forca de {jogador.name}** {desenho}")
            # Vai para menu
            elif res == "2":
                jogador = await menu_forca(channel, jogador)
                if jogador:
                    desenho = f.desenha_forca(jogos_forca[jogador.name])
                    await channel.send(f"**Forca de {jogador.name}**{desenho}")
        # Novo jogo
        else:
            jogador = await menu_forca(channel, jogador)
            if jogador:
                desenho = f.desenha_forca(jogos_forca[jogador.name])
                await channel.send(f"**Forca de {jogador.name}**{desenho}")

    # faz rodar a forca caso o usuário digite $$letra
    if message.content.startswith("$$"):
        await forca(channel, jogador, message)

    # ************************************************* Jogo da Velha *************************************************

    # caso o usuário digite $velha, verifica se o usuário tem um jogo em andamento e/ou inicia novos jogos
    if message.content.startswith("$velha"):
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
            res = await menu2(
                channel, jogador, "Jogando o jogo da velha", descri, escolhas
            )
            if res == False:
                return False
            # Volta para jogo antigo
            if res == "1":
                desenho = v.imprime_grade(jogos_velha[str_jogadores][1])
                await channel.send(
                    f"**Jogo da Velha de {jogadores[0]} e {jogadores[1]}** \n{jogos_velha[str_jogadores][2]} {desenho}"
                )
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

    # faz rodar o jogo da velha caso o usuário digite $#número
    if message.content.startswith("$#"):
        await velha(channel, jogador, message)

    # ************************************************* Torre de Hanoi *************************************************

    if message.content.startswith("$hanoi"):
        hanoi = open(
            user + "\\anas_bot\\anas_bot\\comandos\\intru_hanoi.txt",
            encoding="utf-8",
            mode="r",
        )
        hanoi = hanoi.read()
        await channel.send(hanoi)


# roda o bot definido no token
token = ler_doc("", "token.txt")
try:
    bot.run(token)
except:
    print("Algo errado com o arquivo token.txt, confira!")
