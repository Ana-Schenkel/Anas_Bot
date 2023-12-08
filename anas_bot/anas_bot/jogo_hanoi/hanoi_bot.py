# Esse módulo reune funções assíncronas para processar os menus de escolha e o jogo da Velha no discord

import asyncio
import discord
from comandos.pede_mensagem import *
import jogo_hanoi.torre_de_hanoi as h


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


async def hanoi(channel, jogador, message, jogos_hanoi):
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
        salva_json(jogos_hanoi, "jogo_hanoi\\", "estados_hanoi.json")
    # Pede para o jogador criar um jogo novo
    else:
        await channel.send(
            jogador.name
            + ", você ainda não iniciou um novo jogo da Torre de Hanói, digite '$hanoi'!"
        )

    return jogos_hanoi


async def menu_hanoi(channel, jogador, jogos_hanoi, bot):
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
    res = await menu3(channel, jogador, "Menu Torre de Hanoi", descri, escolhas, bot)
    if res == False:
        return False

    # Jogar a Torre
    if res == "1":
        descri = "escolha um nível:"
        escolhas = ("Fácil", "Médio", "Difícil")
        nivel = await menu3(channel, jogador, "Nível da Torre", descri, escolhas, bot)
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
        discos = await pede_num(
            channel, jogador, "Tamanho do Desafio Torre", descri, bot
        )

        # Pede o nome do jogador
        descri = "digite quem você deseja desafiar."
        jogador1 = await pede_mention(channel, jogador, "Desafio Torre", descri, bot)
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
            res = await menu2(
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
    salva_json(jogos_hanoi, "jogo_hanoi\\", "estados_hanoi.json")

    return (jogador, jogos_hanoi)


async def verifica_hanoi(channel, jogador, jogos_hanoi, bot):
    if jogador.name in jogos_hanoi:
        descri = "você já está jogando a Torre de Hanói, escolha:"
        escolhas = (
            "Continuar jogo antigo",
            "Ver uma possível solução",
            "Ir para menu",
        )
        res = await menu3(channel, jogador, "Jogando a torre", descri, escolhas, bot)
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
            info = await menu_hanoi(channel, jogador, jogos_hanoi, bot)
            if info:
                jogador = info[0]
                jogos_hanoi = info[1]
                desenho = h.desenha_hanoi(jogos_hanoi[jogador.name])
                await channel.send(
                    f"**Torre de {jogador.name}**\nObs: digite '$% discoVareta' para fazer sua jogada. {desenho}"
                )
    # Novo jogo
    else:
        info = await menu_hanoi(channel, jogador, jogos_hanoi, bot)
        if info:
            jogador = info[0]
            jogos_hanoi = info[1]
            desenho = h.desenha_hanoi(jogos_hanoi[jogador.name])
            await channel.send(
                f"**Torre de {jogador.name}**\nObs: digite '$% discoVareta' para fazer sua jogada. {desenho}"
            )

    return jogos_hanoi
