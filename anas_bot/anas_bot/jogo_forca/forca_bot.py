# Esse módulo reune funções assíncronas para processar os menus de escolha e o jogo da Forca no discord

import discord
from comandos.pede_mensagem import *
import jogo_forca.forca as f


async def forca(channel, jogador, message, jogos_forca):
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
        salva_json(jogos_forca, "jogo_forca\\", "estados_forca.json")

    # Pede para o jogador criar um jogo novo
    else:
        await channel.send(
            jogador.name
            + ", você ainda não iniciou um novo jogo de forca, digite '$forca'!"
        )
    return jogos_forca


async def menu_forca(channel, jogador, jogos_forca, bot):
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
    res = await menu3(channel, jogador, "Menu Forca", descri, escolhas, bot)
    if res == False:
        return False

    # Sortear Palavra
    if res == "1":
        descri = "escolha um nível:"
        escolhas = ("Fácil", "Médio", "Difícil")
        nivel = await menu3(channel, jogador, "Sorteia Forca", descri, escolhas, bot)
        if nivel == False:
            return False

        await channel.send(f"Olá {jogador}, uma palavra de nivel {nivel} foi sorteada!")
        palavra = f.sorteia_palavra(nivel)

    # Desafiar Amigo
    elif res == "2":
        palavra = await pede_dm(
            jogador, "Digite a palavra que você deseja que adivinhem na forca!", bot
        )
        if palavra == False:
            return False

        # Pede o nome do jogador
        descri = "digite quem você deseja desafiar"
        jogador1 = await pede_mention(channel, jogador, "Desafio forca", descri, bot)
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
                channel, jogador, "Aceitar desafio da forca?", descri, escolhas, bot
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
    salva_json(jogos_forca, "jogo_forca\\", "estados_forca.json")

    return (jogador, jogos_forca)


async def verifica_forca(channel, jogador, jogos_forca, bot):
    # Jogo em andamento
    if jogador.name in jogos_forca:
        descri = "você já está jogando a forca, escolha:"
        escolhas = ("Continuar jogo antigo", "Ir para menu")
        res = await menu2(channel, jogador, "Jogando a forca", descri, escolhas, bot)
        if res == False:
            return False
        # Volta para o jogo antigo
        if res == "1":
            desenho = f.desenha_forca(jogos_forca[jogador.name])
            await channel.send(f"**Forca de {jogador.name}** {desenho}")
        # Vai para menu
        elif res == "2":
            info = await menu_forca(channel, jogador, jogos_forca, bot)
            if info:
                jogador = info[0]
                jogos_forca = info[1]
                desenho = f.desenha_forca(jogos_forca[jogador.name])
                await channel.send(f"**Forca de {jogador.name}**{desenho}")
    # Novo jogo
    else:
        info = await menu_forca(channel, jogador, jogos_forca, bot)
        if info:
            jogador = info[0]
            jogos_forca = info[1]
            desenho = f.desenha_forca(jogos_forca[jogador.name])
            await channel.send(f"**Forca de {jogador.name}**{desenho}")

    return jogos_forca
