<div align="center">
  <img src="https://i.pinimg.com/originals/88/00/5f/88005f7b9247e2dd7a1f8dd8b1034100.jpg" height=80><br>
  <h1> Ana's Bot </h1>
  <h2> ~ jogos tradicionais para discord com python ~ </h2>
  <h2>  </h2>
</div>

## Descrição

O projeto **"Ana's Bot"** é um projeto Python desenvolvido com a biblioteca **discord.py**, criado para a disciplina de Computação 1 na UFRJ. O projeto se resume em um bot que oferece uma variedade de jogos interativos para os usuários de um servidor do Discord, que visam aprimorar habilidades de resolução de problemas, estratégia e colaboração dos usuários, ou só ajudá-los a passar o tempo enquanto esperam um amigo chegar. As principais características do bot incluem a capacidade de jogar três jogos populares: Forca, Jogo da Velha e Torre de Hanói.

## Sumário

- [Features](#features)
- [Utilização](#utilização)
- [Dependencies](#dependencies)
- [License](#license)
- [Discussão e Desenvolvimento](#discussão-e-desenvolvimento)
- [Contribuir com o bot](#contribuir-com-o-bot)
- [Créditos](#créditos)

## Features

- **Forca:** O bot permite que os usuários joguem o clássico jogo da Forca. Os usuários podem escolher uma palavra ou frase para que outros tentem adivinhar, e o bot acompanha o progresso do jogo, mostrando a forca e as letras adivinhadas. Os usuários também podem escolher jogar individualmemte, escolhendo sortear uma palavra do arquivo de palavras.

- **Jogo da Velha:** Os usuários podem jogar o Jogo da Velha (ou Tic-Tac-Toe) com o bot ou entre si. O bot gerencia o tabuleiro, verifica as vitórias e empates e permite que os jogadores se divirtam com esse jogo clássico.

- **Torre de Hanói:** O bot oferece a possibilidade de jogar o desafiador quebra-cabeça da Torre de Hanói, no qual os jogadores devem mover discos entre três pinos, respeitando as regras do jogo. O bot ajuda a acompanhar o progresso do jogo e a encontrar a solução para o quebra-cabeça.

- **Comandos de ajuda:** O bot oferece comandos de ajuda para que os usuários possam acessar informações sobre como usar as funcionalidades disponíveis.

- **Comandos de informações:** Os usuários podem obter informações sobre o bot, seus criadores e a disciplina de Computação 1 da UFRJ.

- **Integração com o servidor do Discord:** O bot é configurado para interagir com os membros do servidor, reconhecendo comandos específicos e respondendo a interações dos usuários.

## Utilização

Para utilizar o bot você deve seuir as instruções abaixo:

1. Crie um fork do repositório `Anas_Bot`, disponível em: https://github.com/Ana-Schenkel/Anas_Bot.
2. Faça um clone local do seu fork com:

```sh
#gitbash
    $ git clone link_do_seu_fork_aqui
```

3. Instale as bibliotecas do requirements.txt no seu ambiente de programação.
4. Rode o código uma vez (terá uma mensagem de erro) para aparecer o arquivo token.env na pasta "anas_bot".
5. Crie o seu bot no discord com as devidas permissões (administrador para facilitar), adicione-o em um servidor, e copie seu token para o arquivo token.env.
6. O bot deve entrar online assim que você rodar o código principal em seu computador.

Problemas frequentes:
 - Dificuldade para instalar a biblioteca discord.py, um erro comum é "Could not build wheels for multidict...", esse vídeo pode ajudar: https://www.youtube.com/watch?v=hgNxAxyncdc

## Dependencies

- [Discord.py - Permite criar e rodar um bot capaz de enviar e receber mensagens no aplicativo do discord](https://pypi.org/project/discord.py/)

## License

Free software: GNU General Public License v3

## Discussão e desenvolvimento

Esse projeto foi criado com o objetivo de aprimorar habilidades básicas da programação em python, como lógica de programação clássica (por exemplo criando um jogo da velha com bot), manipulação de estruturas de dados iteráveis e de coleção com encadeamento (string com a Forca, listas com o Jogo da Velha e pilhas com a Torre de Hanoi), manipulação de arquivos (lendo instruções e salvando os jogos iniciados), modularização (criando um projeto com várias pastas, arquivos e funções), documentação (com docstrings, comentários, README.md e requirements.txt), git workflow (com várias branchs organizadas), entre outras.
Além dessas habilidades, o projeto também proporcionou a exploração dos conceitos da programação assíncrona e um maior entendimento do uso de bibliotecas com API, utilizando o discord.py.
Pretende-se melhorar o projeto a partir do hosteamento em nuvem, para que o bot permaneça online sem a necessidade de um computador como servidor.

## Contribuir com o bot

Todas as contribuições com o projeto são muito bem vindas! Caso tenha alguma sugestão por favor comunique <3

Aqui estão algumas formas de contribuir com o projeto Ana's Bot:

- **Reportar Bugs:**

  Você pode reportar problemas em https://github.com/Ana-Schenkel/anas_bot/issues.

  Caso seja o seu caso, por favor inclua:

  - Nome e versão do seu sistema operacional.
  - Quaisquer detalhes sobre sua configuração local que possam ser úteis na solução de problemas.
  - Etapas detalhadas para replicar o bug.

- **Consertar Bugs**

  Vasculhe o GitHub Issues desse repositório, qualquer coisa com as tags "bug" e "help wanted" estão abertas para quem quiser resolver.

- **Criar Features**

  Vasculhe o GitHub Issues desse repositório, qualquer coisa com as tags "enhancement" e "help wanted" estão abertas para quem quiser implemetar.

- **Enviar Feedback**

  O melhor jeito de enviar feedbacks é submeter um problema em https://github.com/Ana-Schenkel/anas_bot/issues.

  Se você deseja incluir uma nova feature, por favor inclua:

  - Explicação detalhada de como sua feature funciona.
  - Features de escopos simples, para facilitar a implementação.

- **Criar Projeto Similar**

  Siga as instruções de utilização do bot desse repositório para preparar seu ambiente de programação, crie seu próprio projeto e adicione o link https://github.com/Ana-Schenkel/Anas_Bot nos créditos do seu README.md.

## Créditos

Para esse projeto, foi utilizado o o template pypackage do projeto `audreyr/cookiecutter-pypackage` com Cookiecutter.

- `audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

Também deixo como referência a série de vídeos do @CivoCode sobre a biblioteca discord.py.
- https://www.youtube.com/watch?v=kcgQfOpazhU&list=PLW9I0hYEya07AHzGNHh470BODgNae8RPh&pp=iAQB
  
<hr>

[Go to Top](#table-of-contents)
