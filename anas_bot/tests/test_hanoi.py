"""Testes para as funções síncronas da Torre de Hanói."""

import anas_bot.jogo_hanoi.torre_de_hanoi as h


def test_define_varetas():
    expected_result = [[4, 3, 2, 1], [4], [4]]
    actual_result = h.define_varetas(3)
    assert expected_result == actual_result


def test_desenha_hanoi():
    expected_result = (
        "```"
        + "  |     |     |    \n"
        + "  2     |     |    \n"
        + "  3     |     1    \n"
        + "----- ----- -----\n  A     B     C ```"
    )
    actual_result = h.desenha_hanoi([[4, 3, 2], [4], [4, 1], 3, 1])
    assert expected_result == actual_result


def test_hanoi_function():
    expected_result = (
        "```"
        + "  |     |     |    \n"
        + "  |     |     |    \n"
        + "  3     2     1    \n"
        + "----- ----- -----\n  A     B     C ```",
        [[4, 3], [4, 2], [4, 1], 3, 2],
    )
    actual_result = h.hanoi(
        [[4, 3, 2], [4], [4, 1], 3, 1], [True, True, True, True, True, True], 1
    )
    assert expected_result == actual_result


def test_resolver():
    expected_result = (
        "  |     |     |    \n"
        + "  2     |     1    \n"
        + "----- ----- -----\n  A     B     C \n\n"
        + "  |     |     |    \n"
        + "  |     2     1    \n"
        + "----- ----- -----\n  A     B     C \n\n"
        + "  |     1     |    \n"
        + "  |     2     |    \n"
        + "----- ----- -----\n  A     B     C \n\n"
    )
    actual_result = h.resolver([[3, 2, 1], [3], [3], 2, 0])
    assert expected_result == actual_result


def test_jogada():
    expected_result = (
        "você moveu o disco 2 para a vareta B.",
        [[4, 3], [4, 2], [4, 1], 3, 2],
        True,
    )
    actual_result = h.jogada([[4, 3, 2], [4], [4, 1], 3, 1], (2, "b"))
    assert expected_result == actual_result
