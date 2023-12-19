"""Testes para as funções síncronas de tratamento de arquivo"""

import anas_bot.comandos.trata_arquivo as a


def test_pega_token():
    expected_result = type("str")
    actual_result = type(a.pega_token("token.env"))
    assert expected_result == actual_result


def test_ler_doc():
    result = a.ler_doc("comandos\\", "help.txt").startswith("Oii")
    assert result


# def test_salva_json():
#     a.salva_json(
#         {"Teste": "Esse arquivo foi feito pelo pytest"},
#         "comandos\\",
#         "teste.json",
#     )
#     #verificar se o arquivo foi criado com o conteúdo específico
