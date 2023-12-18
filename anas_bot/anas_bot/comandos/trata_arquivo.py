"""Esse módulo reune funções para ler e salvar arquivos

Funções:
    pega_token(arquivo = str)
    ler_doc(pasta = str, arquivo = str)
    salva_json(dicionario = dict, pasta = str, arquivo = str)
"""

import json
import os
from dotenv import load_dotenv


def pega_token(arquivo):
    """Essa função lê a variável "TOKEN" de um arquivo .env

    Args:
        arquivo (str): nome do arquivo .env

    Returns:
        str: conteúdo da variável "TOKEN"
    """
    path = os.path.dirname(__file__)
    path = path.rstrip("comandos")
    file_path = path + arquivo

    if os.path.isfile(file_path):
        load_dotenv(file_path)
        token = os.environ.get("TOKEN")
        return token
    else:
        with open(file_path, encoding="utf-8", mode="w") as doc:
            doc.write("TOKEN= 'seu_token_aqui'")
            print("O arquivo " + arquivo + " foi resetado, confira!")
        return " "


def ler_doc(pasta, arquivo):
    """Essa função lê um arquivo e retorna o seu conteúdo

    Args:
        pasta (str): pasta do arquivo  com '\\'
        arquivo (str): nome do arquivo com o tipo

    Returns:
        str: conteúdo do arquivo .txt
        dict: conteúdo do arquivo .json

    """
    path = os.path.dirname(__file__)
    path = path.rstrip("comandos")
    doc_cont = {}

    try:
        with open(path + pasta + arquivo, encoding="utf-8", mode="r") as doc:
            if "json" in arquivo:
                doc_cont = json.load(doc)
            else:
                doc_cont = doc.read()
    except FileNotFoundError:
        with open(path + pasta + arquivo, encoding="utf-8", mode="w") as doc:
            doc.write('{"arquivo foi resetado": []}')
            print("O arquivo " + arquivo + " foi resetado, confira!")
            doc_cont = {}

    return doc_cont


def salva_json(dicionario, pasta, arquivo):
    """Essa função salva o conteúdo de um dicionário em um arquivo json

    Args:
        dicionario (dict): conteúdo para ser salvo no arquivo
        pasta (str): pasta do arquivo  com '\\'
        arquivo (str): nome do arquivo com o tipo
    """
    path = os.path.dirname(__file__)
    path = path.rstrip("comandos")
    with open(path + pasta + arquivo, encoding="utf-8", mode="w") as doc:
        json.dump(dicionario, doc, ensure_ascii=False)
