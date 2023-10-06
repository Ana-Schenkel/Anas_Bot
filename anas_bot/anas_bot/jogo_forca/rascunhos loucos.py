# import os
# pasta = os.getcwd()
# print(pasta)
# doc_palavras = open(pasta + "\\anas_bot\\anas_bot\\jogo_forca\\palavras.txt", "r")

# j = 0

# for i in doc_palavras:
#     if j == 3:
#         print(i)
#     j += 1

def verifica_acento (palavra):
    
    acentos = {"a":"áàãâ", "e":"éê", "i":"í", "o":"óõô", "u":"ú", "c":"ç"}

    for letra in acentos:
        for acento in acentos[letra]:
            if acento in palavra:
                palavra = palavra.replace(acento, letra)
    
    return palavra

    
    for i in letra:
        ver = True
        if i in "aeiouc":
            for j in acentos[i]:
                if ((letra_acento + j) in palavra):
                    letra_acento += j
                    ver = False
        if ver:
            letra_acento += i
    return letra_acento

print(verifica_acento(input()))