# """Main module."""

import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all(), help_command=None)
user = os.getcwd()


@bot.event
async def on_ready():
    print("Logado")


@bot.event
async def on_message(message):
    print(message.content)
    print(message.channel)

    def check(m):
        autor = m.channel == channel and m.author == jogador
        resposta = m.content == "1" or m.content == "2"
        return autor and resposta

    def check_privado(m):
        return m.author == jogador

    def check_member(m):
        mention = m.mentions
        if len(mention) > 1 or mention == []:
            return False
        else:
            return True

    if message.content.startswith("$forca"):
        channel = message.channel
        jogador = message.author

        forca = open(
            user + "\\anas_bot\\anas_bot\\comandos\\instru_forca.txt",
            encoding="utf-8",
            mode="r",
        )
        forca = forca.read()
        await channel.send(forca)

        await channel.send(
            "Escolha uma opção: \n 1 - Sortear uma palavra \n 2 - Desafiar um amigo"
        )

        msg = await bot.wait_for("message", check=check)

        if msg.content == "1":
            await channel.send(f"Hello {msg.author}!")
            # palavra = forca.sortea_palavra()
        elif msg.content == "2":
            await jogador.send("Digite a palavra que você deseja que adivinhem!")
            palavra = await bot.wait_for("message", check=check_privado)
            palavra = palavra.content
            print(palavra)
            await channel.send(f"Oi {msg.author}!")
            await channel.send("Digite quem você deseja desafiar")
            jogador1 = await bot.wait_for("message", check=check_member)
            jogador1 = jogador1.mentions
            jogador1 = jogador1[0]
            await channel.send(f"{jogador1} você foi desafiado para o jogo da forca!")
            # palavra = o que ele disser no privado

    if message.content.startswith("$velha"):
        channel = message.channel
        jogador = message.author

        velha = open(
            user + "\\anas_bot\\anas_bot\\comandos\\instru_velha.txt",
            encoding="utf-8",
            mode="r",
        )
        velha = velha.read()
        await channel.send(velha)

        await channel.send(
            "Escolha uma opção: \n 1 - Jogar com o bot \n 2 - Desafiar um amigo"
        )

        msg = await bot.wait_for("message", check=check)

        if msg.content == "1":
            await channel.send(f"Hello {msg.author}!")
            # começar jogo da velha
        elif msg.content == "2":
            await channel.send("Marque o amigo com quem vai jogar")
            jogador1 = await bot.wait_for("message", check=check_member)
            jogador1 = jogador1.mentions
            jogador1 = jogador1[0]
            await channel.send(f"{jogador1} você foi desafiado para o jogo da velha!")
            # palavra = o que ele disser no privado


@bot.command()
async def help(ctx):
    ajuda = open(
        user + "\\anas_bot\\anas_bot\\comandos\\help.txt",
        encoding="utf-8",
        mode="r",
    )
    ajuda = ajuda.read()
    await ctx.send(ajuda)


@bot.command()
async def info(ctx):
    info = open(
        user + "\\anas_bot\\anas_bot\\comandos\\info.txt",
        encoding="utf-8",
        mode="r",
    )
    info = info.read()
    await ctx.send(info)


# @bot.command()
# async def forca(ctx):
#     forca = open(
#         user + "\\anas_bot\\anas_bot\\comandos\\instru_forca.txt",
#         encoding="utf-8",
#         mode="r",
#     )
#     forca = forca.read()
#     await ctx.send(forca)


# @bot.command()
# async def velha(ctx, posicao=None):
#     member = ctx.author
#     print(posicao)
#     print(member)
#     if posicao == None:
#         velha = open(
#             user + "\\anas_bot\\anas_bot\\comandos\\instru_velha.txt",
#             encoding="utf-8",
#             mode="r",
#         )
#         velha = velha.read()
#         await ctx.send(velha)

#     def check(m):
#         return m.content == "hello" and m.channel == ctx.channel

#     msg = await bot.wait_for("on_message")
#     await ctx.send(f"Hello {msg.author}!")


# @bot.command()
# async def hanoi(ctx):
#     hanoi = open(
#         user + "\\anas_bot\\anas_bot\\comandos\\instru_hanoi.txt",
#         encoding="utf-8",
#         mode="r",
#     )
#     hanoi = hanoi.read()
#     await ctx.send(hanoi)


token = open(
    user + "\\anas_bot\\anas_bot\\token.txt",
    encoding="utf-8",
    mode="r",
)
token = token.read()
bot.run(token)
