from random import *
import os

def sorteia_palavra (nivel):
    user = os.getcwd()
    doc_palavras = open(user + "\\anas_bot\\anas_bot\\jogo_forca\\palavras.txt", "r")
    
    if nivel == "fácil":
        linha = randint(1, 30)
    elif nivel == "médio":
        linha = randint(33, 62)
    elif nivel == "difícil":
        linha = randint(65, 93)
    
    contador = 0
    for i in doc_palavras:
        if contador == linha:
            palavra = i.strip("\n")
            print(palavra)
            break
        contador += 1
    doc_palavras.close()
    return palavra


def retira_acento (palavra):
    
    acentos = {"a":"áàãâ", "e":"éê", "i":"í", "o":"óõô", "u":"ú", "c":"ç"}

    for letra in acentos:
        for acento in acentos[letra]:
            if acento in palavra:
                palavra = palavra.replace(acento, letra)
    palavra = palavra.lower()

    return palavra


def letra_certa (letra, palavra, chute):
    i = 0
    
    for x in range(palavra.count(letra)):
        i = palavra.index(letra, i)
        for j in range(len(letra)):
            index = i+j
            chute = chute[:index] + letra[j] + chute[index+1:] 
        i+=1
    
    return chute


def forca_simples (palavra):
    
    chute = len(palavra)*"_"
    usados = []
    vida = 6
    
    while palavra != chute:
        
        print(forca[vida] + "\n" + " ".join(chute) + "\nLetras testadas: " + " ".join(usados))
        
        if vida == 0:
            return "Você perdeu"
        else:
            letra = retira_acento(input())
            palavra_formatada = retira_acento(palavra)

            while letra in usados:
                print("Já usou essa letra")
                letra = input()
            
            if letra in palavra_formatada:
                chute = letra_certa (letra, palavra_formatada, chute)
                for i in range(len(chute)):
                    if chute[i] != "_":
                        chute = chute[:i] + palavra[i] + chute[i+1:]
            else:
                vida -= 1
                print("A palavra não tem \"" + letra + "\", você pode errar mais", vida, "vezes")

            usados.append(letra)
    
    return "Parabéns! A palavra era " + palavra
            


forca = ("| \n|_0 \n /|\\ \n / \\", 
        "| \n|_0 \n /|\\ \n /", 
        "| \n|_0\n /|\\ \n",
        "| \n|_0\n /| \n",
        "| \n|_0 \n  | \n",
        "| \n|_0 \n\n",
        "| \n|_ \n\n")
#  |
#  |_0
#   /|\
#   / \


if __name__ == "__main__":
    print(forca_simples(sorteia_palavra(input())))