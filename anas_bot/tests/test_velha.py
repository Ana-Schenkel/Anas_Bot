"""Testes para as funções síncronas do jogo da velha."""

import anas_bot.jogo_velha.jogo_da_velha as v


def test_sorteia_jogadores():
    expected_result = type(("jogador1", "jogador2"))
    actual_result = type(v.sorteia_jogadores("jogador1", "jogador2"))
    assert expected_result == actual_result


def test_faz_jogada():
    expected_result = 0
    actual_result = v.faz_jogada(1, [" ", " ", " ", " ", "X", " ", " ", " ", " "])
    assert expected_result == actual_result


def test_imprime_grade():
    expected_result = (
        "```\n"
        + " O |   |   \n"
        + "___|___|___\n"
        + "   | X |   \n"
        + "___|___|___\n"
        + "   |   |   \n"
        + "   |   |   \n"
        + "```"
    )
    actual_result = v.imprime_grade(["O", " ", " ", " ", "X", " ", " ", " ", " "])
    assert expected_result == actual_result


def test_verifica_vitoria():
    expected_result = "XOO XXO OXX XXO OXX OOX XXX OXO"
    actual_result = v.verifica_vitoria(["X", "O", "O", "X", "X", "O", "O", "X", "X"])
    assert expected_result == actual_result


def test_jogo_da_velha():
    expected_result = (
        1,
        ["O", " ", "X", " ", "X", " ", " ", " ", " "],
        "jogador1 jogou! Vez de jogador2 (digite '$#' antes do número da sua jogada)",
        True,
    )
    actual_result = v.jogo_da_velha(
        [0, ["O", " ", " ", " ", "X", " ", " ", " ", " "], " "],
        ("jogador1", "jogador2"),
        "Ana's Bot",
        "3",
    )
    assert expected_result == actual_result
