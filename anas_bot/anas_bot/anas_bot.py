# """Main module."""

import comandos.pede_mensagem as p
import discord
import jogo_forca.forca_bot as f
import jogo_hanoi.hanoi_bot as h
import jogo_velha.velha_bot as v
from discord.ext import commands

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all(), help_command=None)

# Pega os estados dos jogos anteriores e salva em um dicionário
jogos_forca = p.ler_doc("jogo_forca\\", "estados_forca.json")
jogos_velha = p.ler_doc("jogo_velha\\", "estados_velha.json")
jogos_hanoi = p.ler_doc("jogo_hanoi\\", "estados_hanoi.json")


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
    ajuda = p.ler_doc("comandos\\", "help.txt")
    await ctx.send(ajuda)


@bot.command()
async def info(ctx):
    """Essa função lê o arquivo de informações/curiosidades do bot

    Args:
        ctx (str): canal de texto da mensagem enviada

    """
    info = p.ler_doc("comandos\\", "info.txt")
    await ctx.send(info)


# Bloco para processar toda mensagem enviada ************************************************************************
@bot.event
async def on_message(message):
    await bot.process_commands(message)  # faz os comandos processarem

    channel = message.channel
    jogador = message.author

    if jogador == bot.user:
        return

    # ************************************************* Jogo Forca *************************************************

    global jogos_forca

    # caso o usuário digite $forca, verifica se o usuário tem um jogo em andamento e/ou inicia novos jogos
    if message.content.startswith("$forca"):
        jogos_forca = await f.verifica_forca(channel, jogador, jogos_forca, bot)

    # faz rodar a forca caso o usuário digite $$letra
    if message.content.startswith("$$"):
        jogos_forca = await f.forca(channel, jogador, message, jogos_forca)

    # ************************************************* Jogo da Velha *************************************************

    global jogos_velha

    # caso o usuário digite $velha, verifica se o usuário tem um jogo em andamento e/ou inicia novos jogos
    if message.content.startswith("$velha"):
        jogos_velha = await v.verifica_velha(channel, jogador, jogos_velha, bot)

    # faz rodar o jogo da velha caso o usuário digite $#número
    if message.content.startswith("$#"):
        jogos_velha = await v.velha(channel, jogador, message, jogos_velha, bot)

    # ************************************************* Torre de Hanoi *************************************************

    global jogos_hanoi

    # caso o usuário digite $velha, verifica se o usuário tem um jogo em andamento e/ou inicia novos jogos
    if message.content.startswith("$hanoi"):
        jogos_hanoi = await h.verifica_hanoi(channel, jogador, jogos_hanoi, bot)

    # faz rodar o jogo da velha caso o usuário digite $#número
    if message.content.startswith("$%"):
        jogos_hanoi = await h.hanoi(channel, jogador, message, jogos_hanoi)


# roda o bot definido no token
token = p.ler_doc("", "token.txt")
try:
    bot.run(token)
except:
    print("Algo errado com o arquivo token.txt, confira!")
