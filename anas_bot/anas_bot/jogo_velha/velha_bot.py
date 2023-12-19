"""
Módulo das funções assíncronas para processar os menus de escolha e o jogo da Velha no discord

Funções:
    bot_velha(channel = str, jogadores = tuple, jogos_velha = dict, bot = Bot)
    velha(channel = str, jogador = Member, message = Message, jogos_velha = dict, bot = Bot)
    menu_velha(channel = str, jogador = Member, jogos_velha = dict, bot = Bot)
    verifica_velha(channel = str, jogador = Member, jogos_velha = dict, bot = Bot)
"""

import jogo_velha.jogo_da_velha as v
import comandos.pede_mensagem as p
import comandos.trata_arquivo as a


async def bot_velha(channel, jogadores, jogos_velha, bot):
    """Essa função processa a jogada do bot, envia e salva seu resultado

    Args:
        channel (str): nome do canal de texto que solicitou as mensagens
        jogadores (tuple): nomes dos jogadores que estão no jogo: bot e usuário
        jogos_velha (dict): dados gerais, inclui o índice do próximo jogador, a grade e a mensagem de orientação.
        bot (Bot): dados do objeto "bot"

    Returns:
        dict : jogos_velha com a jogada atualizada

    """
    str_jogadores = jogadores[0] + "," + jogadores[1]
    # Pega o número que deve ser jogado pelo bot
    resultado = v.jogo_da_velha(
        jogos_velha[str_jogadores], jogadores, bot.user.name, ""
    )
    # Envia a jogada do bot no discord
    desenho = v.imprime_grade(resultado[1])
    await channel.send(f"**Jogo da Velha de {jogadores[0]} e {jogadores[1]}**")
    await channel.send(desenho)
    await channel.send(resultado[2])

    if resultado[3]:
        # Atualiza os dados do jogo do dicionário
        jogos_velha[str_jogadores] = [
            resultado[0],
            resultado[1],
            resultado[2],
        ]
    else:
        jogos_velha.pop(str_jogadores)
    # Salva resultado no arquivo
    a.salva_json(jogos_velha, "jogo_velha\\", "estados_velha.json")

    return jogos_velha


async def velha(channel, jogador, message, jogos_velha, bot):
    """Essa função verifica se o usuário pode jogar e processa a jogada desejada, atualizando o estado do jogo

    Args:
        channel (str): nome do canal de texto das mensagens
        jogador (Member): informações do usuário que deseja jogar
        message (Message): mensagem enviada pelo usuário no discord
        jogos_velha (dict): dados gerais, inclui o índice do próximo jogador, a grade e a mensagem de orientação.
        bot (Bot): dados do objeto "bot"

    Returns:
        dict : jogos_velha com a jogada atualizada
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
            await channel.send(f"**Jogo da Velha de {jogadores[0]} e {jogadores[1]}**")
            await channel.send(desenho)
            await channel.send(resultado[2])
            # Salva a jogada no dicionário
            jogos_velha[str_jogadores] = [resultado[0], resultado[1], resultado[2]]
            # Verifica se o jogo acabou
            if not resultado[3]:
                # Retira o jogo do dicionário
                jogos_velha.pop(str_jogadores)
            # Atualiza os dados do jogo no arquivo
            a.salva_json(jogos_velha, "jogo_velha\\", "estados_velha.json")
            # Verfica se o jogo continua
            if resultado[3]:
                # Verifica se o próximo jogador é o bot e faz a jogada dele
                if bot.user.name == jogadores[jogos_velha[str_jogadores][0]]:
                    await bot_velha(channel, jogadores, jogos_velha, bot)
        # Não é a vez do jogador
        else:
            await channel.send("Não é sua vez " + jogador.name)
    # Jogador não tem jogo aberto
    else:
        await channel.send(
            jogador.name + ", você ainda não iniciou um jogo da velha, digite '$velha'"
        )

    return jogos_velha


async def menu_velha(channel, jogador, jogos_velha, bot):
    """Essa função opera o menu das configurações iniciais do jogo da velha

    Args:
        channel (str): nome do canal de texto que solicitou as mensagens
        jogador (Member): informações do usuário que deseja jogar
        jogos_velha (dict): dados gerais, inclui o índice do próximo jogador, a grade e a mensagem de orientação.
        bot (Bot): dados do objeto "bot"

    Returns:
        tuple : tupla dos nomes dos jogadores e dicionário jogos_velha com configurações iniciais
        bool: caso false, não se criará um novo jogo

    """
    # menu para decidir os parâmetros iniciais do jogo da forca
    descri = "escolha uma opção:"
    escolhas = ("Jogar com o bot", "Desafiar um amigo", "Ver instruções")
    res = await p.menu3(channel, jogador, "Menu Jogo da Velha", descri, escolhas, bot)
    if not res:
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
        if not jogador1:
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
            if not res:
                return False
            # A pessoa não aceitou o desafio
            if res == "2":
                return jogadores

    # Mostra as instruções
    elif res == "3":
        instru = a.ler_doc("jogo_velha\\", "instru_velha.txt")
        await channel.send(instru)
        return False

    # Menu para decidir a ordem de quem jogará primeiro
    descri = "escolha uma opção:"
    escolhas = ("Sortear ordem de jogada", "Escolher o primeiro jogador")
    res = await p.menu2(channel, jogador, "Sortear Velha", descri, escolhas, bot)
    if not res:
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
        if not primeiro_jogador:
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
    a.salva_json(jogos_velha, "jogo_velha\\", "estados_velha.json")
    # retorna a tupla de jogadores na ordem de jogada
    return (jogadores, jogos_velha)


async def verifica_velha(channel, jogador, jogos_velha, bot):
    """Essa função verifica se o usuário já está em um jogo ou não, e, de acordo com as escolhas do usuário,
    o direciona para o menu para criar um novo jogo ou retorna para o jogo antigo

    Args:
        channel (str): nome do canal de texto que solicitou as mensagens
        jogador (Member): informações do usuário que deseja jogar
        jogos_velha (dict): dados gerais, inclui o índice do próximo jogador, a grade e a mensagem de orientação.
        bot (Bot): dados do objeto "bot"

    Returns:
        dict : jogos_velha com configurações do jogo novo ou antigo
        bool: caso false, não se criará um novo jogo

    """
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
        if not res:
            return False
        # Volta para jogo antigo
        if res == "1":
            desenho = v.imprime_grade(jogos_velha[str_jogadores][1])
            await channel.send(f"**Jogo da Velha de {jogadores[0]} e {jogadores[1]}**")
            await channel.send(desenho)
            await channel.send(jogos_velha[str_jogadores][2])
        # Vai para menu
        elif res == "2":
            info = await menu_velha(channel, jogador, jogos_velha, bot)
            if info:
                jogadores = info[0]
                jogos_velha = info[1]
                if bot.user.name == jogadores[jogos_velha[str_jogadores][0]]:
                    await bot_velha(channel, jogadores, jogos_velha, bot)
    # Novo jogo
    else:
        info = await menu_velha(channel, jogador, jogos_velha, bot)
        if info:
            jogadores = info[0]
            jogos_velha = info[1]
            if (
                bot.user.name
                == jogadores[jogos_velha[jogadores[0] + "," + jogadores[1]][0]]
            ):
                await bot_velha(channel, jogadores, jogos_velha, bot)

    return jogos_velha
