#  X | O | O
# ___|___|___
#  O | X | O
# ___|___|___
#    | X | X
#    |   |

def faz_jogada (jogador):
     if jogadores[jogador] == "bot":
          
          grade_apoio = grade.copy()
          ver = 0
          
          urgencias = [["X*X", "XX*", "*XX"], ["O*O", "OO*", "*OO"]]
          interessantes = [["X* ", "X *", "*X ", " X*", "* X", " *X"], 
                           ["O* ", "O *", "*O ", " O*", "* O", " *O"]]
          lista_escolhas = []
          jogada = -1
          
          while jogada == -1:
                
                if grade_apoio.count(" ") != 0:
                     escolha = grade_apoio.index(" ")
                else:
                     for i in range(grade_apoio.count("*")):
                        grade_apoio[grade_apoio.index("*")] = " "
                     escolha = grade_apoio.index(" ")
                     ver += 1
                
                grade_apoio[escolha] = "*"
                lista_escolhas.append(escolha)
                        
                analise = verifica_vitoria(grade_apoio)
                
                if ver == 0:
                     for i in urgencias[0]:
                        if i in analise:
                             jogada = escolha
                             return jogada
                     for i in urgencias[1]:
                        if i in analise:
                             jogada = escolha
                             return jogada
                elif ver == 1:
                     
                     for i in interessantes[0]:
                        if i in analise:
                             jogada = escolha
                             return jogada
                     for i in interessantes[1]:
                        if i in analise:
                             jogada = escolha
                             return jogada
                elif ver == 2:
                     if 4 in lista_escolhas:
                        escolha = 4
                     elif 0 in lista_escolhas:
                        escolha = 0
                     elif 2 in lista_escolhas:
                        escolha = 2
                     elif 6 in lista_escolhas:
                        escolha = 6
                     elif 8 in lista_escolhas:
                        escolha = 8
                     jogada = escolha
                     return jogada
     else:
         jogada = int(input())
         return jogada
               

def imprime_grade ():
      desenho_grade = ""
      cont = 0
      
      for j in range(3):
        if j != 2:
              divisao = "\n___|___|___\n"
        else:
              divisao = "\n   |   |   \n"
        
        for i in range(3):
              desenho_grade += " " + grade[i+cont] + " |"
        desenho_grade = desenho_grade.strip("|") + divisao
        
        cont += 3
      
      return desenho_grade

def verifica_vitoria (grade_vitoria):
      vitoria = {"linha": ["","",""],
                "coluna": ["", "", "",],
                "diagonal": ["", ""]}
      
      for chave in vitoria:
        cont = 0
        match chave:
          case "linha":
                for i in range(3):
                  for j in range(3):
                        vitoria[chave][i] += grade_vitoria[j+cont]
                cont += 3
          case "coluna":
                for i in range(3):
                  for j in range(3):
                        vitoria[chave][i] += grade_vitoria[j+cont]
                        cont += 2
                  cont = i+1
          case "diagonal":
                for i in range(2):
                  for j in range(3):
                        vitoria[chave][i] += grade_vitoria[j+cont]
                        if i == 0:
                                cont += 3
                        if i == 1:
                                cont += 1
                  cont = 2
      vitoria = " ".join([" ".join(i) for i in vitoria.values()])
      return vitoria

def jogo_da_velha ():

    str_vitoria = verifica_vitoria(grade)
    imprime_grade()
    print(str_vitoria)
    jogador = 0
    
    while not("XXX" in str_vitoria or "OOO" in str_vitoria):

        jogada = faz_jogada(jogador)

        imprime_grade()

        while grade[jogada] != " ":
            print("Espaço ocupado, tente novamente.")
            jogada = int(input())
        
        if jogador == 0:
            grade[jogada] = "X"
            jogador += 1
        elif jogador == 1:
            grade[jogada] = "O"
            jogador -= 1
        
        str_vitoria = verifica_vitoria(grade)
        print(imprime_grade())
    
    return jogador



grade = [" ", " ", " ", 
        " ", " ", " ", 
        " ", " ", " "]

jogadores = ["nome", "bot"]

print(jogo_da_velha())
