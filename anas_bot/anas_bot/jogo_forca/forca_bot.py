"""
Módulo das funções assíncronas para processar os menus de escolha e o jogo da Forca no discord

Funções:
    forca(channel = str, jogador = Member, message = Message, jogos_forca = dict)
    menu_forca(channel = str, jogador = Member, jogos_forca = dict, bot = Bot)
    verifica_forca(channel = str, jogador = Member, jogos_forca = dict, bot = Bot)
"""

import jogo_forca.forca as f
import comandos.pede_mensagem as p
import comandos.trata_arquivo as a


async def forca(channel, jogador, message, jogos_forca):
    """Essa função verifica se o usuário pode jogar e testa a letra digitada pelo jogador, atualizando o estado do jogo

    Args:
        channel (str): nome do canal de texto das mensagens
        jogador (Member): informações do usuário que deseja jogar
        message (Message): mensagem enviada no discord
        jogos_forca (dict): dados gerais do jogo, inclui a palavra, seu chute, letras usadas e a vida atual.

    Returns:
        dict : jogos_forca atualizado
    """
    # verifica se o jogador tem um jogo salvo
    if jogador.name in jogos_forca:
        msg = message.content.strip("$ ")
        resultado = f.forca(
            jogos_forca[jogador.name], msg
        )  # função que processa a letra

        jogos_forca[jogador.name] = resultado[1]

        desenho = f.desenha_forca(jogos_forca[jogador.name])
        await channel.send(f"**Forca de {jogador.name}**")
        await channel.send(desenho)
        await channel.send(resultado[0])

        # Verfica se o jogo acabou e retira os dados do jogo
        if not resultado[2]:
            jogos_forca.pop(jogador.name)

        # Atualiza o jogo no arquivo
        a.salva_json(jogos_forca, "jogo_forca\\", "estados_forca.json")

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
        jogos_forca (dict): dados gerais do jogo, inclui a palavra, seu chute, letras usadas e a vida atual.
        bot (Bot): dados do objeto "bot"

    Returns:
        tuple : nome do jogador (Member) e jogos_forca com configurações iniciais (dict)
        bool: caso false, não se criará um novo jogo

    """
    # menu para decidir os parâmetros iniciais do jogo da forca
    descri = "escolha uma opção:"
    escolhas = ("Sortear uma palavra", "Desafiar um amigo", "Ver instruções")
    res = await p.menu3(channel, jogador, "Menu Forca", descri, escolhas, bot)
    if not res:
        return False

    # Sortear Palavra
    if res == "1":
        descri = "escolha um nível:"
        escolhas = ("Fácil", "Médio", "Difícil")
        nivel = await p.menu3(channel, jogador, "Sorteia Forca", descri, escolhas, bot)
        if not nivel:
            return False

        await channel.send(f"Olá {jogador}, uma palavra de nivel {nivel} foi sorteada!")
        palavra = f.sorteia_palavra(nivel)

    # Desafiar Amigo
    elif res == "2":
        palavra = await p.pede_dm(
            jogador, "Digite a palavra que você deseja que adivinhem na forca!", bot
        )
        if not palavra:
            return False

        # Pede o nome do jogador
        descri = "digite quem você deseja desafiar"
        jogador1 = await p.pede_mention(channel, jogador, "Desafio forca", descri, bot)
        if not jogador1:
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
            res = await p.menu2(
                channel, jogador, "Aceitar desafio da forca?", descri, escolhas, bot
            )
            if not res:
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
        instru = a.ler_doc("jogo_forca\\", "instru_forca.txt")
        await channel.send(instru)
        return False

    # Salva os parâmetros
    chute = ""
    for letra in palavra:
        if letra == " ":
            chute += " "
        else:
            chute += "_"

    usados = []
    vida = 6

    jogos_forca.update({jogador.name: [palavra, chute, usados, vida]})
    a.salva_json(jogos_forca, "jogo_forca\\", "estados_forca.json")

    return (jogador, jogos_forca)


async def verifica_forca(channel, jogador, jogos_forca, bot):
    """Essa função verifica se o usuário já está em um jogo ou não, e, de acordo com as escolhas do usuário,
    o direciona para o menu para criar um novo jogo ou retorna para o jogo antigo

    Args:
        channel (str): nome do canal de texto que solicitou as mensagens
        jogador (Member): informações do usuário que deseja jogar
        jogos_forca (dict): dados gerais do jogo, inclui a palavra, seu chute, letras usadas e a vida atual.
        bot (Bot): dados do objeto "bot"

    Returns:
        dict: jogos_forca com configurações do jogo novo ou antigo
        bool: caso false, não se criará um novo jogo
    """
    # Jogo em andamento
    if jogador.name in jogos_forca:
        descri = "você já está jogando a forca, escolha:"
        escolhas = ("Continuar jogo antigo", "Ir para menu")
        res = await p.menu2(channel, jogador, "Jogando a forca", descri, escolhas, bot)
        if not res:
            return False
        # Volta para o jogo antigo
        if res == "1":
            desenho = f.desenha_forca(jogos_forca[jogador.name])
            await channel.send(f"**Forca de {jogador.name}**")
            await channel.send(desenho)
        # Vai para menu
        elif res == "2":
            info = await menu_forca(channel, jogador, jogos_forca, bot)
            if info:
                jogador = info[0]
                jogos_forca = info[1]
                desenho = f.desenha_forca(jogos_forca[jogador.name])
                await channel.send(f"**Forca de {jogador.name}**")
                await channel.send(desenho)
    # Novo jogo
    else:
        info = await menu_forca(channel, jogador, jogos_forca, bot)
        if info:
            jogador = info[0]
            jogos_forca = info[1]
            desenho = f.desenha_forca(jogos_forca[jogador.name])
            await channel.send(f"**Forca de {jogador.name}**")
            await channel.send(desenho)

    return jogos_forca
