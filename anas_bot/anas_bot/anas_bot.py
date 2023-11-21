# """Main module."""

import os

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all(), help_command=None)
user = os.getcwd()


@bot.event
async def on_ready():
    print("Logado")


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


@bot.event
async def on_message(message):
    await bot.process_commands(message)  # faz os comandos processarem

    # print(message.content)
    # print(message.channel)
    # print(bot.user)
    channel = message.channel
    jogador = message.author

    def check_menu(m):
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

    if message.content.startswith("$forca"):
        forca = open(
            user + "\\anas_bot\\anas_bot\\jogo_forca\\instru_forca.txt",
            encoding="utf-8",
            mode="r",
        )
        forca = forca.read()
        await channel.send(forca)

        await channel.send(
            "Escolha uma opção: \n 1 - Sortear uma palavra \n 2 - Desafiar um amigo"
        )

        msg = await bot.wait_for("message", check=check_menu)

        if msg.content == "1":
            await channel.send(
                "Escolha uma nível: \n 1 - Fácil \n 2 - Médio \n 3 - Difícil "
            )
            nivel = await bot.wait_for("message", check=check_menu3)
            await channel.send(
                f"Hello {msg.author}, uma palavra de nivel {nivel.content} vai ser sorteada!"
            )
            # palavra = forca.sortea_palavra()
        elif msg.content == "2":
            await jogador.send("Digite a palavra que você deseja que adivinhem!")
            palavra = await bot.wait_for(
                "message",
                check=lambda x: x.channel == jogador.dm_channel and x.author == jogador,
            )
            palavra = palavra.content
            await channel.send("Digite quem você deseja desafiar")
            jogador1 = await bot.wait_for("message", check=check_mention)
            jogador1 = jogador1.mentions
            jogador1 = jogador1[0]
            await channel.send(f"{jogador1} você foi desafiado para o jogo da forca!")
            # palavra = o que ele disser no privado

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
        msg = await bot.wait_for("message", check=check_menu)

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
        msg = await bot.wait_for("message", check=check_menu)

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
        velha = open(
            user + "\\anas_bot\\anas_bot\\comandos\\instru_hanoi.txt",
            encoding="utf-8",
            mode="r",
        )
        velha = velha.read()
        await channel.send(velha)


# roda o bot definido no token
token = open(
    user + "\\anas_bot\\anas_bot\\token.txt",
    encoding="utf-8",
    mode="r",
)
token = token.read()
bot.run(token)
