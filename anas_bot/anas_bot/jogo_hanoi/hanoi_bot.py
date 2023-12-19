"""
Módulo das funções assíncronas para processar os menus de escolha e o jogo da Torre de Hanoi no discord

Funções:
    bot_hanoi(jogador = Member, discos = int)
    hanoi(channel = str, jogador = Member, message = Message, jogos_hanoi = dict)
    menu_hanoi(channel = str, jogador = Member, jogos_hanoi = dict, bot = Bot)
    verifica_hanoi(channel = str, jogador = Member, jogos_hanoi = dict, bot = Bot)
"""

import asyncio
import comandos.pede_mensagem as p
import jogo_hanoi.torre_de_hanoi as h
import comandos.trata_arquivo as a


async def bot_hanoi(jogador, discos):
    """Essa função resolve a torre de hanoi e envia o a solução

    Args:
        jogador (Member or str): informações do usuário ou canal para o qual a solução deve ser enviada
        discos (int): quantidade de discos jogáveis na torre
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
    """Essa função verifica se o usuário pode jogar e processa a jogada desejada, atualizando o estado do jogo

    Args:
        channel (str): nome do canal de texto das mensagens
        jogador (Member): informações do usuário que deseja jogar
        message (Message): mensagem enviada pelo usuário no discord
        jogos_hanoi (dict): dados gerais, inclui pilhas de cada vareta, total de discos jogáveis e último disco jogado.

    Returns:
        dict : jogos_hanoi com a jogada atualizada
    """
    if jogador.name in jogos_hanoi:
        msg = message.content.strip("$% ")
        vareta = msg[-1]
        disco = msg.strip(msg[-1])
        resultado = h.jogada(jogos_hanoi[jogador.name], (disco, vareta))

        jogos_hanoi[jogador.name] = resultado[1]

        desenho = h.desenha_hanoi(jogos_hanoi[jogador.name])
        await channel.send(
            f"**Torre de {jogador.name}**\nObs: digite '$% discoVareta' para fazer sua jogada"
        )
        await channel.send(desenho)
        await channel.send(f"{jogador.name}, {resultado[0]}")

        # Verfica se o jogo acabou e retira os dados do jogo
        if not resultado[2]:
            jogos_hanoi.pop(jogador.name)

        # Atualiza o jogo no arquivo
        a.salva_json(jogos_hanoi, "jogo_hanoi\\", "estados_hanoi.json")
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
        jogos_hanoi (dict): dados gerais, inclui pilhas de cada vareta, total de discos jogáveis e último disco jogado.
        bot (Bot): dados do objeto "bot"

    Returns:
        tuple: nome do jogador (Member) e jogos_hanoi com configurações iniciais (dict)
        bool: caso false, não se criará um novo jogo
    """
    # menu para decidir os parâmetros iniciais do jogo da Torre de Hanói
    descri = "escolha uma opção:"
    escolhas = ("Jogar a Torre de Hanói", "Desafiar um amigo", "Ver instruções")
    res = await p.menu3(channel, jogador, "Menu Torre de Hanoi", descri, escolhas, bot)
    if not res:
        return False

    # Jogar a Torre
    if res == "1":
        descri = "escolha um nível:"
        escolhas = ("Fácil", "Médio", "Difícil")
        nivel = await p.menu3(channel, jogador, "Nível da Torre", descri, escolhas, bot)
        if not nivel:
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
        if not jogador1:
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
            if not res:
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
        instru = a.ler_doc("jogo_hanoi\\", "instru_hanoi.txt")
        await channel.send(instru)
        return False

    # Salva os parâmetros
    disco1 = 0
    varetas = h.define_varetas(discos)

    jogos_hanoi.update(
        {jogador.name: [varetas[0], varetas[1], varetas[2], discos, disco1]}
    )
    a.salva_json(jogos_hanoi, "jogo_hanoi\\", "estados_hanoi.json")

    return (jogador, jogos_hanoi)


async def verifica_hanoi(channel, jogador, jogos_hanoi, bot):
    """Essa função verifica se o usuário já está em um jogo ou não, e, de acordo com as escolhas do usuário,
    o direciona para o menu para criar um novo jogo ou retorna para o jogo antigo

    Args:
        channel (str): nome do canal de texto que solicitou as mensagens
        jogador (Member): informações do usuário que deseja jogar
        jogos_hanoi (dict): dados gerais, inclui pilhas de cada vareta, total de discos jogáveis e último disco jogado.
        bot (Bot): dados do objeto "bot"

    Returns:
        dict: jogos_hanoi com configurações do jogo novo ou antigo
        bool: caso false, não se criará um novo jogo
    """
    # Jogo em andamento
    if jogador.name in jogos_hanoi:
        descri = "você já está jogando a Torre de Hanói, escolha:"
        escolhas = (
            "Continuar jogo antigo",
            "Ver uma possível solução",
            "Ir para menu",
        )
        res = await p.menu3(channel, jogador, "Jogando a torre", descri, escolhas, bot)
        if not res:
            return False
        # Volta para o jogo antigo
        if res == "1":
            desenho = h.desenha_hanoi(jogos_hanoi[jogador.name])
            await channel.send(
                f"**Torre de {jogador.name}**\nObs: digite '$% discoVareta' para fazer sua jogada."
            )
            await channel.send(desenho)
        # Manda a resolução no privado
        elif res == "2":
            await bot_hanoi(jogador, jogos_hanoi[jogador.name][3])
            await channel.send(
                f"{jogador.name}, a solução foi enviada para você, tente continuar seu jogo:"
            )
            desenho = h.desenha_hanoi(jogos_hanoi[jogador.name])
            await channel.send(
                f"**Torre de {jogador.name}**\nObs: digite '$% discoVareta' para fazer sua jogada."
            )
            await channel.send(desenho)
        # Vai para menu
        elif res == "3":
            info = await menu_hanoi(channel, jogador, jogos_hanoi, bot)
            if info:
                jogador = info[0]
                jogos_hanoi = info[1]
                desenho = h.desenha_hanoi(jogos_hanoi[jogador.name])
                await channel.send(
                    f"**Torre de {jogador.name}**\nObs: digite '$% discoVareta' para fazer sua jogada."
                )
                await channel.send(desenho)
    # Novo jogo
    else:
        info = await menu_hanoi(channel, jogador, jogos_hanoi, bot)
        if info:
            jogador = info[0]
            jogos_hanoi = info[1]
            desenho = h.desenha_hanoi(jogos_hanoi[jogador.name])
            await channel.send(
                f"**Torre de {jogador.name}**\nObs: digite '$% discoVareta' para fazer sua jogada."
            )
            await channel.send(desenho)

    return jogos_hanoi
