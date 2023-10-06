#  X | O | O
# ___|___|___
#  O | X | O
# ___|___|___
#    | X | X
#    |   |


def jogo_da_velha ():
    grade = (["_", "_", "_"], 
            ["_", "_", "_"], 
            ["_", "_", "_"])
    
    posicao = {"1": grade[0][0], "2":grade[0][1], "3":grade[0][2], 
            "4":grade[1][0], "5":grade[1][1], "6":grade[1][2], 
            "7":grade[2][0], "8":grade[2][1], "9":grade[2][2]}
    vitoria = {"linha1": "".join(grade[0]), "linha2": "".join(grade[1]), "linha3": "".join(grade[2]),
            "coluna1": posicao["1"]+posicao["4"]+posicao["7"], "coluna2": posicao["2"]+posicao["5"]+posicao["8"], "coluna3": posicao["3"]+posicao["6"]+posicao["9"],
            "diagonal1": posicao["1"]+posicao["5"]+posicao["9"], "diagonal2": posicao["3"]+posicao["5"]+posicao["7"]}
    lista_vitoria = vitoria.values()
    
    grade[1][1] = "X"

    jogador = 1
    
    while not("XXX" in lista_vitoria or "OOO" in lista_vitoria):
    
        jogada = int(input())

        print(posicao[jogada])

        while posicao[jogada] != "_":
            print("Espaço ocupado, tente novamente.")
            jogada = int(input())
        
        # if jogador == 1:
        #     grade[coordenadas]= "X"
        #     jogador += 1
        # elif jogador == 2:
        #     posicao[jogada] = "O"
        #     jogador -= 1





print(jogo_da_velha())