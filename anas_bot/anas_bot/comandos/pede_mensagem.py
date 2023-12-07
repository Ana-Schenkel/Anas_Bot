# Esse módulo reune funções assíncronas para pedir e verificar mensagens do usuário

import discord


async def menu2(channel, jogador, titulo, descri, escolhas, bot):
    """Essa função recebe as características de um embed de menu com duas escolhas e retorna a resposta do usuário

    Args:
        channel (str): nome do canal de texto que solicitou as mensagens
        jogador (Member): informações do usuário que irá responder
        titulo (str): title do embed
        descri (str): descrição do menu
        escolhas (tuple): possíveis escolhas do usuário

    Returns:
        str: conteúdo da resposta do usuário

    """

    def check_menu2(m):
        autor = m.channel == channel and m.author == jogador
        resposta = m.content == "1" or m.content == "2"
        return autor and resposta

    embed = discord.Embed(
        title=titulo,
        description=f"{jogador.name}, {descri} \n 1 - {escolhas[0]} \n 2 - {escolhas[1]}",
        color=0xFF5733,
    )
    await channel.send(embed=embed)
    try:
        msg = await bot.wait_for("message", timeout=120.0, check=check_menu2)
    except TimeoutError:
        await channel.send(
            f"O tempo de responder ao {titulo} acabou {jogador.name}, tente novamente"
        )
        return False

    return msg.content


async def menu3(channel, jogador, titulo, descri, escolhas, bot):
    """Essa função recebe as características de um embed de menu com três escolhas e retorna a resposta do usuário

    Args:
        channel (str): nome do canal de texto que solicitou as mensagens
        jogador (Member): informações do usuário que irá responder
        titulo (str): title do embed
        descri (str): descrição do menu
        escolhas (tuple): possíveis escolhas do usuário

    Returns:
        str: conteúdo da resposta do usuário

    """

    def check_menu3(m):
        autor = m.channel == channel and m.author == jogador
        resposta = m.content == "1" or m.content == "2" or m.content == "3"
        return autor and resposta

    embed = discord.Embed(
        title=titulo,
        description=f"{jogador.name}, {descri} \n 1 - {escolhas[0]} \n 2 - {escolhas[1]} \n 3 - {escolhas[2]}",
        color=0xFF5733,
    )
    await channel.send(embed=embed)

    try:
        msg = await bot.wait_for("message", timeout=120.0, check=check_menu3)
    except TimeoutError:
        await channel.send(
            f"O tempo de responder ao {titulo} acabou {jogador.name}, tente novamente"
        )
        return False

    return msg.content


async def pede_mention(channel, jogador, titulo, descri, bot):
    """Essa função recebe as características de um embed que pede que o usuário marque outra pessoa

    Args:
        channel (str): nome do canal de texto que solicitou as mensagens
        jogador (Member): informações do usuário que irá responder
        titulo (str): title do embed
        descri (str): descrição do embed

    Returns:
        Member: pessoa marcada pelo usuário

    """

    def check_mention(m):
        autor = m.channel == channel and m.author == jogador
        mention = m.mentions
        if len(mention) > 1 or mention == []:
            return False
        else:
            return True and autor

    embed = discord.Embed(
        title=titulo,
        description=f"{jogador.name}, {descri} (marque com @nome)",
        color=0xFF5733,
    )
    await channel.send(embed=embed)
    try:
        pessoa = await bot.wait_for("message", timeout=120.0, check=check_mention)
        pessoa = pessoa.mentions
        pessoa = pessoa[0]
    except TimeoutError:
        await channel.send(
            f"O tempo de responder ao {titulo} acabou {jogador.name}, tente novamente"
        )
        return False

    return pessoa


async def pede_dm(jogador, descri, bot):
    """Essa função recebe as características de uma mensagem a ser enviada na dm e retorna a resposta do usuário

    Args:
        jogador (Member): informações do usuário que irá responder
        descri (str): descrição da mensagem enviada pelo bot

    Returns:
        str: conteúdo da resposta do usuário

    """
    await jogador.send(descri)
    try:
        palavra = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda x: x.channel == jogador.dm_channel and x.author == jogador,
        )
        palavra = palavra.content
    except TimeoutError:
        await jogador.send(
            f"O tempo de digitar a palavra acabou {jogador.name}, tente novamente"
        )
        return False
    return palavra


async def pede_num(channel, jogador, titulo, descri, bot):
    """Essa função recebe as características de um embed "digite um número" e retorna a resposta do usuário

    Args:
        channel (str): nome do canal de texto que solicitou as mensagens
        jogador (Member): informações do usuário que irá responder
        titulo (str): title do embed
        descri (str): descrição da mensagem

    Returns:
        int: conteúdo da resposta do usuário

    """

    def check_num(m):
        autor = m.channel == channel and m.author == jogador
        resposta = m.content in "2 3 4 5 6 7 8 9 10 11 12 13 14"
        return autor and resposta

    embed = discord.Embed(
        title=titulo,
        description=f"{jogador.name}, {descri}",
        color=0xFF5733,
    )
    await channel.send(embed=embed)
    try:
        msg = await bot.wait_for("message", timeout=120.0, check=check_num)
    except TimeoutError:
        await channel.send(
            f"O tempo de responder ao {titulo} acabou {jogador.name}, tente novamente"
        )
        return False

    return int(msg.content)
