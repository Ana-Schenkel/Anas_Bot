# """Main module."""

import json
import os

import discord
import jogo_forca.forca as f
from discord.ext import commands

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all(), help_command=None)
user = os.getcwd()

# Pega os estados dos jogos anteriores
doc = open(
    user + "\\anas_bot\\anas_bot\\jogo_forca\\estados_forca.json",
    encoding="utf-8",
    mode="r",
)
jogos_forca = json.load(doc)
doc.close()


async def instru(game, channel):
    """Essa função lê o arquivo de instruções de um jogo

    Args:
        game (str): jogo que precisa das instruções
        channel (str): nome do canal de texto que solicitou as mensagens

    """
    instru = open(
        user + "\\anas_bot\\anas_bot\\jogo_" + game + "\\instru_" + game + ".txt",
        encoding="utf-8",
        mode="r",
    )
    instru_ = instru.read()
    instru.close()
    await channel.send(instru_)


async def menu_forca(channel, jogador):
    """Essa função opera o menu das configurações iniciais do jogo da forca

    Args:
        channel (str): nome do canal de texto que solicitou as mensagens
        jogador (Member): informações do usuário que deseja jogar

    Returns:
        str: member que irá jogar

    """

    # **************************************************checks******************************************************
    # funções para conferir se s mensagens enviadas no canal de texto devem ser analisadas
    def check_menu2(m):
        autor = m.channel == channel and m.author == jogador
        resposta = m.content == "1" or m.content == "2"
        return autor and resposta

    def check_menu3(m):
        autor = m.channel == channel and m.author == jogador
        resposta = m.content == "1" or m.content == "2" or m.content == "3"
        return autor and resposta

    def check_mention(m):
        autor = m.channel == channel and m.author == jogador
        mention = m.mentions
        if len(mention) > 1 or mention == []:
            return False
        else:
            return True and autor

    # ****************************************************menu******************************************************
    # menu para decidir os parâmetros iniciais do jogo da forca

    embed = discord.Embed(
        title="Menu Forca",
        description=f"{jogador.name}, escolha uma opção: \n 1 - Sortear uma palavra \n 2 - Desafiar um amigo",
        color=0xFF5733,
    )
    await channel.send(embed=embed)

    msg = await bot.wait_for("message", check=check_menu2)

    if msg.content == "1":
        embed = discord.Embed(
            title="Sorteio Forca",
            description=f"{jogador.name}, escolha uma nível: \n 1 - Fácil \n 2 - Médio \n 3 - Difícil",
            color=0xFF5733,
        )
        await channel.send(embed=embed)
        nivel = await bot.wait_for("message", check=check_menu3)
        nivel = nivel.content
        await channel.send(
            f"Olá {msg.author}, uma palavra de nivel {nivel} foi sorteada!"
        )
        palavra = f.sorteia_palavra(nivel)
        jogador1 = "bot"

    elif msg.content == "2":
        await jogador.send("Digite a palavra que você deseja que adivinhem!")
        palavra = await bot.wait_for(
            "message",
            check=lambda x: x.channel == jogador.dm_channel and x.author == jogador,
        )
        palavra = palavra.content
        embed = discord.Embed(
            title="Desafio forca",
            description=f"{jogador.name}, digite quem você deseja desafiar",
            color=0xFF5733,
        )
        await channel.send(embed=embed)
        jogador1 = await bot.wait_for("message", check=check_mention)
        jogador1 = jogador1.mentions
        jogador1 = jogador1[0]
        await channel.send(f"{jogador1} você foi desafiado para o jogo da forca!")
        jogador = jogador1

    chute = len(palavra) * "_"
    usados = []
    vida = 6

    jogos_forca.update({jogador.name: [palavra, chute, usados, vida]})
    doc = open(user + "\\anas_bot\\anas_bot\\jogo_forca\\estados_forca.json", "w")
    json.dump(jogos_forca, doc)
    doc.close()

    return jogador


@bot.event
async def on_ready():
    print("Logado")


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


@bot.event
async def on_message(message):
    await bot.process_commands(message)  # faz os comandos processarem

    # print(message.content)
    # print(message.channel)
    # print(bot.user)
    channel = message.channel
    jogador = message.author

    # **************************************************checks******************************************************
    # funções para conferir se s mensagens enviadas no canal de texto devem ser analisadas
    def check(m):
        return m.channel == channel and m.author == jogador

    def check_menu2(m):
        autor = m.channel == channel and m.author == jogador
        resposta = m.content == "1" or m.content == "2"
        return autor and resposta

    def check_menu3(m):
        autor = m.channel == channel and m.author == jogador
        resposta = m.content == "1" or m.content == "2" or m.content == "3"
        return autor and resposta

    def check_mention(m):
        autor = m.channel == channel and m.author == jogador
        mention = m.mentions
        if len(mention) > 1 or mention == []:
            return False
        else:
            return True and autor

    # ************************************************* Jogo Forca *************************************************
    # caso o usuário digite $forca, verifica se o usuário tem um jogo em andamento e/ou inicia novos jogos

    if message.content.startswith("$forca"):
        if jogador.name in jogos_forca:
            embed = discord.Embed(
                title="Jogando",
                description=f"{jogador.name}, você já está jogando a forca, escolha: \n 1 - Continuar jogo antigo \n 2 - Iniciar novo jogo \n 3 - Ver instruções",
                color=0xFF5733,
            )
            await channel.send(embed=embed)
            msg = await bot.wait_for("message", check=check_menu3)

            if msg.content == "1":
                desenho = f.desenha_forca(jogos_forca[jogador.name])
                await channel.send(f"**Forca de {jogador.name}** {desenho}")
            elif msg.content == "2":
                jogador = await menu_forca(channel, jogador)
                desenho = f.desenha_forca(jogos_forca[jogador.name])
                await channel.send(desenho)
            elif msg.content == "3":
                await instru("forca", channel)

        else:
            await instru("forca", channel)
            jogador = await menu_forca(channel, jogador)
            desenho = f.desenha_forca(jogos_forca[jogador.name])
            await channel.send(desenho)

    # faz rodar a forca caso o usuário digite $$letra
    if message.content.startswith("$$"):
        if jogador.name in jogos_forca:
            msg = message.content.strip("$ ")
            resultado = f.forca(jogos_forca[jogador.name], msg)
            print(resultado)
            await channel.send(resultado[0])
            jogos_forca[jogador.name] = resultado[1]

            desenho = f.desenha_forca(jogos_forca[jogador.name])
            await channel.send(f"**Forca de {jogador.name}** {desenho}")

            if resultado[2] == False:
                jogos_forca.pop(jogador.name)

            doc = open(
                user + "\\anas_bot\\anas_bot\\jogo_forca\\estados_forca.json",
                encoding="utf-8",
                mode="w",
            )
            json.dump(jogos_forca, doc)
            doc.close()
        else:
            await channel.send(
                "Você ainda não iniciou um novo jogo de forca, digite '$forca'!"
            )

    # ************************************************* Jogo da Velha *************************************************

    if message.content.startswith("$velha"):
        velha = open(
            user + "\\anas_bot\\anas_bot\\jogo_velha\\instru_velha.txt",
            encoding="utf-8",
            mode="r",
        )
        velha = velha.read()
        await channel.send(velha)

        await channel.send(
            "Escolha uma opção: \n 1 - Jogar com o bot \n 2 - Desafiar um amigo"
        )
        msg = await bot.wait_for("message", check=check_menu2)

        if msg.content == "1":
            await channel.send(f"Hello {msg.author}, você vai jogar contra o bot!")
            jogador1 = bot.user
            # adicionar jogador bot
        elif msg.content == "2":
            await channel.send("Marque o amigo com quem vai jogar")
            jogador1 = await bot.wait_for("message", check=check_mention)
            jogador1 = jogador1.mentions
            jogador1 = jogador1[0]
            await channel.send(f"{jogador1} você foi desafiado para o jogo da velha!")
            # adicionar outro jogador

        await channel.send(
            "Escolha uma opção: \n 1 - Sortear ordem de jogada \n 2 - Escolher o primeiro jogador"
        )
        msg = await bot.wait_for("message", check=check_menu2)

        if msg.content == "1":
            await channel.send(f"Hello {msg.author}, vamos começar!")
            # sortear começar jogo da velha
        elif msg.content == "2":
            await channel.send("Marque quem irá jogar primeiro")
            primeiro_jogador = await bot.wait_for("message", check=check_mention)
            primeiro_jogador = primeiro_jogador.mentions
            primeiro_jogador = primeiro_jogador[0]
            if primeiro_jogador == jogador:
                await channel.send(f"Hello {jogador}, você é o primeiro!")
                # ordenar jogador como primeiro
            elif primeiro_jogador == jogador1:
                await channel.send(f"Hello {jogador1}, você é o primeiro!")
                # ordenar jogador1 como primeiro
            # começar jogo da velha

    # ************************************************* Torre de Hanoi *************************************************

    if message.content.startswith("$hanoi"):
        hanoi = open(
            user + "\\anas_bot\\anas_bot\\comandos\\instru_hanoi.txt",
            encoding="utf-8",
            mode="r",
        )
        hanoi = hanoi.read()
        await channel.send(hanoi)


# roda o bot definido no token
token = open(
    user + "\\anas_bot\\anas_bot\\token.txt",
    encoding="utf-8",
    mode="r",
)
token = token.read()
bot.run(token)
