<div align="center">
  <img src=""><br>
  //foto discord
</div>

-----------------

# Ana's bot: jogos tradicionais para discord com python.

| | |
| --- | --- |
| Testing | [![CI - Test](https://github.com/pandas-dev/pandas/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/pandas-dev/pandas/actions/workflows/unit-tests.yml) [![Coverage](https://codecov.io/github/pandas-dev/pandas/coverage.svg?branch=main)](https://codecov.io/gh/pandas-dev/pandas) |
| Package | [![PyPI Latest Release](https://img.shields.io/pypi/v/pandas.svg)](https://pypi.org/project/pandas/) [![PyPI Downloads](https://img.shields.io/pypi/dm/pandas.svg?label=PyPI%20downloads)](https://pypi.org/project/pandas/) [![Conda Latest Release](https://anaconda.org/conda-forge/pandas/badges/version.svg)](https://anaconda.org/conda-forge/pandas) [![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/pandas.svg?label=Conda%20downloads)](https://anaconda.org/conda-forge/pandas) |
| Meta | [![Powered by NumFOCUS](https://img.shields.io/badge/powered%20by-NumFOCUS-orange.svg?style=flat&colorA=E1523D&colorB=007D8A)](https://numfocus.org) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3509134.svg)](https://doi.org/10.5281/zenodo.3509134) [![License - BSD 3-Clause](https://img.shields.io/pypi/l/pandas.svg)](https://github.com/pandas-dev/pandas/blob/main/LICENSE) [![Slack](https://img.shields.io/badge/join_Slack-information-brightgreen.svg?logo=slack)](https://pandas.pydata.org/docs/dev/development/community.html?highlight=slack#community-slack) |


## Descrição

O projeto **"Ana's Bot"** é um projeto Python desenvolvido com a biblioteca **discord.py**, criado para a disciplina de Computação 1 na UFRJ. O projeto se resume em um bot que oferece jogos interativos para os usuários de um servidor do Discord, com o objetivo de aprimorar habilidades de resolução de problemas, estratégia e colaboração dos usuários, ou só ajudá-los a passar o tempo enquanto esperam um amigo chegar. As principais características do bot incluem a capacidade de jogar três jogos populares: Forca, Jogo da Velha e Torre de Hanói. 


## Sumário

- [Features](#features)
- [Utilização](#utilização)
- [Dependencies](#dependencies)
- [License](#license)
- [Documentação](#documentação)
- [Discussão e Desenvolvimento](#discussão-e-desenvolvimento)
- [Contribuir com o bot](#contribuir-com-o-bot)
- [Créditos](#créditos)

## Features

* **Forca:** O bot permite que os usuários joguem o clássico jogo da Forca. Os usuários podem escolher uma palavra ou frase para que outros tentem adivinhar, e o bot acompanha o progresso do jogo, mostrando a forca e as letras adivinhadas. Os usuários também podem escolher jogar individualmemte, escolhendo sortear uma palavra do arquivo de palavras.

* **Jogo da Velha:** Os usuários podem jogar o Jogo da Velha (ou Tic-Tac-Toe) com o bot ou entre si. O bot gerencia o tabuleiro, verifica as vitórias e empates e permite que os jogadores se divirtam com esse jogo clássico.

* **Torre de Hanói:** O bot oferece a possibilidade de jogar o desafiador quebra-cabeça da Torre de Hanói, no qual os jogadores devem mover discos entre três pinos, respeitando as regras do jogo. O bot ajuda a acompanhar o progresso do jogo e a encontrar a solução para o quebra-cabeça.

* **Comandos de ajuda:** O bot oferece comandos de ajuda para que os usuários possam acessar informações sobre como usar as funcionalidades disponíveis.

* **Comandos de informações:** Os usuários podem obter informações sobre o bot, seus criadores e a disciplina de Computação 1 da UFRJ.

* **Integração com o servidor do Discord:** O bot é configurado para interagir com os membros do servidor, reconhecendo comandos específicos e respondendo a interações dos usuários.


   [missing-data]: https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html
   [insertion-deletion]: https://pandas.pydata.org/pandas-docs/stable/user_guide/dsintro.html#column-selection-addition-deletion
   [alignment]: https://pandas.pydata.org/pandas-docs/stable/user_guide/dsintro.html?highlight=alignment#intro-to-data-structures
   [groupby]: https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#group-by-split-apply-combine
   [conversion]: https://pandas.pydata.org/pandas-docs/stable/user_guide/dsintro.html#dataframe
   [slicing]: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#slicing-ranges
   [fancy-indexing]: https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html#advanced
   [subsetting]: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#boolean-indexing
   [merging]: https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html#database-style-dataframe-or-named-series-joining-merging
   [joining]: https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html#joining-on-index
   [reshape]: https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html
   [pivot-table]: https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html
   [mi]: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#hierarchical-indexing-multiindex
   [flat-files]: https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#csv-text-files
   [excel]: https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#excel-files
   [db]: https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#sql-queries
   [hdfstore]: https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#hdf5-pytables
   [timeseries]: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#time-series-date-functionality

## Utilização
The source code is currently hosted on GitHub at:
https://github.com/pandas-dev/pandas

Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/pandas) and on [Conda](https://docs.conda.io/en/latest/).

```sh
# conda
conda install -c conda-forge pandas
```

```sh
# or PyPI
pip install pandas
```

The list of changes to pandas between each release can be found
[here](https://pandas.pydata.org/pandas-docs/stable/whatsnew/index.html). For full
details, see the commit logs at https://github.com/pandas-dev/pandas.

## Dependencies
- [NumPy - Adds support for large, multi-dimensional arrays, matrices and high-level mathematical functions to operate on these arrays](https://www.numpy.org)
- [python-dateutil - Provides powerful extensions to the standard datetime module](https://dateutil.readthedocs.io/en/stable/index.html)
- [pytz - Brings the Olson tz database into Python which allows accurate and cross platform timezone calculations](https://github.com/stub42/pytz)

See the [full installation instructions](https://pandas.pydata.org/pandas-docs/stable/install.html#dependencies) for minimum supported versions of required, recommended and optional dependencies.

## License
Free software: GNU General Public License v3

## Documentação
Disponível neste repositório em: https://anas-bot.readthedocs.io.

## Discussão e desenvolvimento
Most development discussions take place on GitHub in this repo, via the [GitHub issue tracker](https://github.com/pandas-dev/pandas/issues).

Further, the [pandas-dev mailing list](https://mail.python.org/mailman/listinfo/pandas-dev) can also be used for specialized discussions or design issues, and a [Slack channel](https://pandas.pydata.org/docs/dev/development/community.html?highlight=slack#community-slack) is available for quick development related questions.

There are also frequent [community meetings](https://pandas.pydata.org/docs/dev/development/community.html#community-meeting) for project maintainers open to the community as well as monthly [new contributor meetings](https://pandas.pydata.org/docs/dev/development/community.html#new-contributor-meeting) to help support new contributors.

Additional information on the communication channels can be found on the [contributor community](https://pandas.pydata.org/docs/development/community.html) page.

## Contribuir com o bot

[![Open Source Helpers](https://www.codetriage.com/pandas-dev/pandas/badges/users.svg)](https://www.codetriage.com/pandas-dev/pandas)

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

A detailed overview on how to contribute can be found in the **[contributing guide](https://pandas.pydata.org/docs/dev/development/contributing.html)**.

If you are simply looking to start working with the pandas codebase, navigate to the [GitHub "issues" tab](https://github.com/pandas-dev/pandas/issues) and start looking through interesting issues. There are a number of issues listed under [Docs](https://github.com/pandas-dev/pandas/issues?labels=Docs&sort=updated&state=open) and [good first issue](https://github.com/pandas-dev/pandas/issues?labels=good+first+issue&sort=updated&state=open) where you could start out.

You can also triage issues which may include reproducing bug reports, or asking for vital information such as version numbers or reproduction instructions. If you would like to start triaging issues, one easy way to get started is to [subscribe to pandas on CodeTriage](https://www.codetriage.com/pandas-dev/pandas).

Or maybe through using pandas you have an idea of your own or are looking for something in the documentation and thinking ‘this can be improved’...you can do something about it!

Feel free to ask questions on the [mailing list](https://groups.google.com/forum/?fromgroups#!forum/pydata) or on [Slack](https://pandas.pydata.org/docs/dev/development/community.html?highlight=slack#community-slack).

As contributors and maintainers to this project, you are expected to abide by pandas' code of conduct. More information can be found at: [Contributor Code of Conduct](https://github.com/pandas-dev/.github/blob/master/CODE_OF_CONDUCT.md)

## Créditos

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

<hr>

[Go to Top](#table-of-contents)