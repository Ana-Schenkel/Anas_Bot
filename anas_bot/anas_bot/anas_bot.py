# """Main module."""

import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())
user = os.getcwd()


@bot.event
async def on_ready():
    print("Logado")


@bot.command()
async def ajuda(ctx):
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


@bot.command()
async def forca(ctx):
    forca = open(
        user + "\\anas_bot\\anas_bot\\comandos\\instru_forca.txt",
        encoding="utf-8",
        mode="r",
    )
    forca = forca.read()
    await ctx.send(forca)


@bot.command()
async def velha(ctx):
    velha = open(
        user + "\\anas_bot\\anas_bot\\comandos\\instru_velha.txt",
        encoding="utf-8",
        mode="r",
    )
    velha = velha.read()
    await ctx.send(velha)


@bot.command()
async def hanoi(ctx):
    hanoi = open(
        user + "\\anas_bot\\anas_bot\\comandos\\instru_hanoi.txt",
        encoding="utf-8",
        mode="r",
    )
    hanoi = hanoi.read()
    await ctx.send(hanoi)


token = open(
    user + "\\anas_bot\\anas_bot\\token.txt",
    encoding="utf-8",
    mode="r",
)
token = token.read()
bot.run(token)
