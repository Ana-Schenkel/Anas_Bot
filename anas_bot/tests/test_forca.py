"""Testes para as funções síncronas do jogo da forca."""

import anas_bot.jogo_forca.forca as f


def test_sorteia_palavra():
    expected_result = type("str")
    actual_result = type(f.sorteia_palavra("1"))
    assert expected_result == actual_result


def test_retira_acento():
    expected_result = "acoes"
    actual_result = f.retira_acento("ações")
    assert expected_result == actual_result


def test_letra_certa():
    expected_result = "_a__a_____"
    actual_result = f.letra_certa("a", "passarinho", "__________")
    assert expected_result == actual_result


def test_desenha_forca():
    expected_result = "\nObs: digite '$$' antes da letra\n```| \n|_0 \n  | \n\n_ _ _ _ _ _\nLetras testadas: i o```"
    actual_result = f.desenha_forca(["Parque", "______", ["i", "o"], 4])
    assert expected_result == actual_result


def test_forca():
    expected_result = ("Tem essa letra", ["Parque", "_a____", ["i", "o", "a"], 4], True)
    actual_result = f.forca(["Parque", "______", ["i", "o"], 4], "a")
    assert expected_result == actual_result
