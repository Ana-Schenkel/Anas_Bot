def forca_simples (palavra):
    
    gabarito = list(palavra)
    palavra = gabarito.copy()
    chute = []
    usados = []
    vida = 6
    
    for letra in palavra:
        chute += "_"
    
    print(chute)
    
    while gabarito != chute:
        letra = input()

        if letra in usados:
            print("Já usou essa letra")
        
        elif letra in palavra:
            while letra in palavra:
                i = palavra.index(letra)
                chute[i] = letra
                palavra[i] = "*"
            
        else:
            print("A palavra não tem essa letra")
            vida -= 1
        
        usados += letra
        for i in forca[vida]:
            print(i)
        print(chute)
        print("Letras testadas:", usados)
        
        if vida == 0:
            break


forca = {0:["|", "|_0", " /|\\", " / \\"], 
        1:["|", "|_0", " /|\\", " /"], 
        2:["|", "|_0", " /|\\", ""],
        3:["|", "|_0", " /|", ""],
        4:["|", "|_0", " /", ""],
        5:["|", "|_0", "", ""],
        6:["|", "|_", "", ""]}

forca_simples(input())
#  |
#  |_0
#   /|\
#   / \


