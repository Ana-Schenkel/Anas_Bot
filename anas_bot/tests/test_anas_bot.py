"""Tests for `anas_bot` package."""

import pytest
import anas_bot.jogo_forca.forca as f


def test_sorteia_palavra():
    #    expected_result = "str"
    actual_result = type(f.sorteia_palavra("fácil"))


#    assert


def test_retira_acento():
    f.retira_acento("ações")


def test_letra_certa():
    f.letra_certa("a", "passarinho", "__________")


def test_desenha_forca():
    f.desenha_forca(["Parque", "______", ["i", "o"], 4])


def test_forca():
    f.forca(["Parque", "______", ["i", "o"], 4], "")


# @pytest.fixture
# def response():
#     """Sample pytest fixture.

#     See more at: http://doc.pytest.org/en/latest/fixture.html
#     """
#     # import requests
#     # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


# def test_content(response):
#     """Sample pytest test function with the pytest fixture as an argument."""
#     # from bs4 import BeautifulSoup
#     # assert 'GitHub' in BeautifulSoup(response.content).title.string
