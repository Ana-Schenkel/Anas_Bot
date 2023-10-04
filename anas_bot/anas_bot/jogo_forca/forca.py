from random import *

def sorteia_palavra ():
    
    doc_palavras = open("C:\\Users\\anasc\\Desktop\\Projeto Ana's Bot\\anas_bot\\anas_bot\\jogo_forca\\palavras_forca.txt", "r")
    lista_palavras = doc_palavras.readline().split(" ")
    index = randint(0, len(lista_palavras)-1)
    palavra = lista_palavras[index]
    doc_palavras.close()
    return palavra


def forca_simples (palavra):
    
    chute = len(palavra)*"_"
    usados = []
    vida = 6
    
    while palavra != chute:
        
        print(forca[vida] + "\n" + " ".join(chute) + "\nLetras testadas: " + " ".join(usados))
        
        if vida == 0:
            return "Você perdeu"
        else:
            letra = input()

            while letra in usados:
                print("Já usou essa letra")
                letra = input()
            
            if letra in palavra:
                i = 0
                for x in range(palavra.count(letra)):
                    i = palavra.index(letra, i)
                    for j in range(len(letra)):
                        index = i+j
                        chute = chute[:index] + letra[j] + chute[index+1:] 
                    i+=1
                
            else:
                vida -= 1
                print("A palavra não tem \"" + letra + "\", você pode errar mais", vida, "vezes")
                
            usados.append(letra)
    
    return "Parabéns! A palavra era " + palavra
            


forca = ["| \n|_0 \n /|\\ \n / \\", 
        "| \n|_0 \n /|\\ \n /", 
        "| \n|_0\n /|\\ \n",
        "| \n|_0\n /| \n",
        "| \n|_0 \n  | \n",
        "| \n|_0 \n\n",
        "| \n|_ \n\n"]
#  |
#  |_0
#   /|\
#   / \


if __name__ == "__main__":
    print(forca_simples(sorteia_palavra()))