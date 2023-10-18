import numpy as np
from colorama import init, Fore, Back, Style
init()

def costo(table, pos1, pos2, avatar, total):
    if avatar == 1:
        if table[pos1, pos2] == 1:
            total += 1
        elif table[pos1, pos2] == 2:
            total += 2
        elif table[pos1, pos2] == 3:
            total += 3
        elif table[pos1, pos2] == 4:
            total += 4
        elif table[pos1, pos2] == 5:
            total += 5
        elif table[pos1, pos2] == 6:
            total += 5
    elif avatar == 2:
        if table[pos1, pos2] == 1:
            total += 2
        elif table[pos1, pos2] == 2:
            total += 4
        elif table[pos1, pos2] == 3:
            total += 3
        elif table[pos1, pos2] == 4:
            total += 1
        elif table[pos1, pos2] == 5:
            total += 5
    elif avatar == 3:
        if table[pos1, pos2] == 1:
            total += 2
        elif table[pos1, pos2] == 2:
            total += 1
        elif table[pos1, pos2] == 4:
            total += 3
        elif table[pos1, pos2] == 5:
            total += 2
    elif avatar == 4:
        if table[pos1, pos2] == 0:
            total += 15
        if table[pos1, pos2] == 1:
            total += 4
        elif table[pos1, pos2] == 4:
            total += 4
        elif table[pos1, pos2] == 5:
            total += 5
        elif table[pos1, pos2] == 6:
            total += 3
    return total

def checarpos(table, pos1, pos2, avatar):
    if pos2 > 14 or pos1 > 14 or pos1 < 0 or pos2 < 0:
        return False
    elif avatar == 1:
        if table[pos1, pos2] == 0:
            return False
        else:
            return True
    elif avatar == 2:
        if table[pos1, pos2] == 0:
            return False
        elif table[pos1, pos2] == 6:
            return False
        else:
            return True
    elif avatar == 3:
        if table[pos1, pos2] == 0:
            return False
        elif table[pos1, pos2] == 6:
            return False
        elif table[pos1, pos2] == 3:
            return False
        else:
            return True
    elif avatar == 4:
        if table[pos1, pos2] == 2:
            return False
        elif table[pos1, pos2] == 3:
            return False
        else:
            return True

def Checar(table, recor, pos1, pos2, avatar, mov):
    if mov == 'd':
        pos2 += 1
    elif mov == 'a':
        pos2 -= 1
    elif mov == 'w':
        pos1 -= 1
    elif mov == 's':
        pos1 += 1
    if pos2 > 14 or pos1 > 14 or pos1 < 0 or pos2 < 0:
        return 0
    elif recor[pos1, pos2] == 2 or recor[pos1, pos2] == 3:
        return 2
    elif recor[pos1, pos2] == 4:
        return 1
    elif avatar == 1:
        if table[pos1, pos2] == 0:
            return 0
        else:
            return 1
    elif avatar == 2:
        if table[pos1, pos2] == 0:
            return 0
        elif table[pos1, pos2] == 6:
            return 0
        else:
            return 1
    elif avatar == 3:
        if table[pos1, pos2] == 0:
            return 0
        elif table[pos1, pos2] == 6:
            return 0
        elif table[pos1, pos2] == 3:
            return 0
        else:
            return 1
    elif avatar == 4:
        if table[pos1, pos2] == 2:
            return 0
        elif table[pos1, pos2] == 3:
            return 0
        else:
            return 1

def checar2op(table, recor, pos1, pos2, avatar):
    posibles = 0
    if Checar(table, recor, pos1, pos2, avatar, 'd') == 1:
        posibles += int(1)
    if Checar(table, recor, pos1, pos2, avatar, 'w') == 1:
        posibles += int(1)
    if Checar(table, recor, pos1, pos2, avatar, 'a') == 1:
        posibles += int(1)
    if Checar(table, recor, pos1, pos2, avatar, 's') == 1:
        posibles += int(1)
    if posibles > 1:
        return True
    else:
        return False

def impTablero2(table):
    print("\t   ", end="")
    for k in range(10):
        print(k, end="   ")
    for k in range(10,15):
        print(k, end="  ")
    print("")
    for i in range(15):
        print(i, "\t|  ", end="")
        for j in range(15):
            if table[i, j] == 0:
                print(Fore.BLACK+"#",end="   ")
                print(Style.RESET_ALL, end="")
            elif table[i, j] == 1:
                print(Fore.CYAN+Style.BRIGHT+"-", end="   ")
                print(Style.RESET_ALL, end="")
            elif table[i, j] == 2:
                print(Fore.BLUE+"~", end="   ")
                print(Style.RESET_ALL, end="")
            elif table[i, j] == 3:
                print(Fore.YELLOW+"=", end="   ")
                print(Style.RESET_ALL, end="")
            elif table[i, j] == 4:
                print(Fore.GREEN+"&", end="   ")
                print(Style.RESET_ALL, end="")
            elif table[i, j] == 5:
                print(Fore.MAGENTA+Style.BRIGHT+"%", end="   ")
                print(Style.RESET_ALL, end="")
            elif table[i, j] == 6:
                print("*", end="   ")
            if j == 14:
                print("")

def impTablero(table, recor, avatar, mask):
    for i in range(15):
        for j in range(15):
            if (recor[i,j] == 0 and mask == 0) or recor[i,j] == 5:
                if table[i, j] == 0:
                    print(Fore.BLACK + "#", end="   ")
                    print(Style.RESET_ALL, end="")
                elif table[i, j] == 1:
                    print(Fore.CYAN + Style.BRIGHT + "-", end="   ")
                    print(Style.RESET_ALL, end="")
                elif table[i, j] == 2:
                    print(Fore.BLUE + "~", end="   ")
                    print(Style.RESET_ALL, end="")
                elif table[i, j] == 3:
                    print(Fore.YELLOW + "=", end="   ")
                    print(Style.RESET_ALL, end="")
                elif table[i, j] == 4:
                    print(Fore.GREEN + "&", end="   ")
                    print(Style.RESET_ALL, end="")
                elif table[i, j] == 5:
                    print(Fore.MAGENTA + Style.BRIGHT + "%", end="   ")
                    print(Style.RESET_ALL, end="")
                elif table[i, j] == 6:
                    print("*", end="   ")
            elif recor[i,j] == 0 and mask == 1:
                print(Fore.BLACK + Back.BLACK + ".", end="   ")
                print(Style.RESET_ALL, end="")
            elif recor[i, j] == 1:
                if avatar == 1:
                    print(Fore.RED+"H", end="   ")
                    print(Style.RESET_ALL, end="")
                elif avatar == 2:
                    print(Fore.RED+"M", end="   ")
                    print(Style.RESET_ALL, end="")
                elif avatar == 3:
                    print(Fore.RED+"P", end="   ")
                    print(Style.RESET_ALL, end="")
                elif avatar == 4:
                    print(Fore.RED+"S", end="   ")
                    print(Style.RESET_ALL, end="")
            elif recor[i, j] == 2:
                print(Fore.RED+"V", end="   ")
                print(Style.RESET_ALL, end="")
            elif recor[i, j] == 3:
                print(Fore.RED+"Vo", end="  ")
                print(Style.RESET_ALL, end="")
            elif recor[i, j] == 4:
                print(Fore.WHITE+Back.RED+"F", end="   ")
                print(Style.RESET_ALL, end="")
            if j == 14:
                print("")

def obt_mapa(texto):
    archivo = open(texto)

    temp = []
    terreno = []
    for line in archivo:
        line = line.rstrip()
        numero = ""
        for x in line:
            if x.find(','):
                numero += str(x)
            else:
                temp.append(int(numero))
                numero = ""
        terreno.append(temp)
        temp = []
    return np.array(terreno)

def mover(recor, entrada, pos1, pos2, tablero, avatar):
    if checar2op(tablero, recor, pos1, pos2, avatar) == True:
        recor[pos1][pos2] = 3
    else:
        recor[pos1][pos2] = 2
    if entrada == 'd':
        pos2 += 1
    elif entrada == 'a':
        pos2 -= 1
    elif entrada == 'w':
        pos1 -= 1
    elif entrada == 's':
        pos1 += 1
    recor[pos1][pos2] = 1
    if pos1 < 14:
        if recor[pos1 + 1][pos2] == 0:
            recor[pos1 + 1][pos2] = 5
    if pos1 > 0:
        if recor[pos1 - 1][pos2] == 0:
            recorrido[pos1 - 1][pos2] = 5
    if pos2 > 0:
        if recor[pos1][pos2 - 1] == 0:
            recorrido[pos1][pos2 - 1] = 5
    if pos2 < 14:
        if recor[pos1][pos2 + 1] == 0:
            recorrido[pos1][pos2 + 1] = 5
    return recor

mask = int(input("Desea ocultar el mapa: \n(0)No\n(1)Si\n :"))
recorrido = np.zeros((15, 15)) #Matriz de recorrido

mapa = int(input("Elija un mapa \n(0)Laberinto\n(1)Naturaleza\n :"))

if mapa == 0:
    tablero = obt_mapa('laberinto.txt')
    avatar = 1
elif mapa == 1:
    tablero = obt_mapa('testo.txt')
    avatar = int(input("Desea ser un \n(1)Humano\n(2)Mono\n(3)Pulpo\n(4)Sasquatch\n :"))

impTablero2(tablero)
primero = False
while primero == False:
    if mapa == 1:
        print("\n# Montaña    - Tierra    ~ Agua    = Arena\n& Bosque    % Pantano    * Nieve")
    pos1 = int(input("\nPosicion Inicial:\nIngrese el numero de fila: "))
    pos2 = int(input("Ingrese el numero de columna :"))
    fin1 = int(input("Posicion Final:\nIngrese el numero de fila: "))
    fin2 = int(input("Ingrese el numero de columna :"))
    if checarpos(tablero, pos1, pos2, avatar) == False or checarpos(tablero, fin1, fin2, avatar) == False:
        print("Valores no validos, intente de nuevo")
        primero = False
    else:
        primero = True

llego = 0
movimientos = 0
total = 0

recorrido[pos1][pos2] = 1
if pos1<14:
    recorrido[pos1+1][pos2] = 5
if pos1>0:
    recorrido[pos1-1][pos2] = 5
if pos2>0:
    recorrido[pos1][pos2-1] = 5
if pos2<14:
    recorrido[pos1][pos2+1] = 5
recorrido[fin1][fin2] = 4

impTablero(tablero, recorrido, avatar, mask)

while llego == 0:
    if mapa == 1:
        print("\n# Montaña    - Tierra    ~ Agua    = Arena\n& Bosque    % Pantano    * Nieve \n")
    print("Puede moverse con WASD\nproximo movimiento :")
    entrada = input()
    if Checar(tablero, recorrido, pos1, pos2, avatar, entrada) == 1 or Checar(tablero, recorrido, pos1, pos2, avatar, entrada) == 2:
        recorrido = mover(recorrido, entrada, pos1, pos2, tablero, avatar)
        if entrada == 'd':
            pos2 += 1
        elif entrada == 'a':
            pos2 -= 1
        elif entrada == 'w':
            pos1 -= 1
        elif entrada == 's':
            pos1 += 1
        total = costo(tablero, pos1, pos2, avatar, total)
        movimientos += 1
        impTablero(tablero, recorrido, avatar, mask)
        if pos1 == fin1 and pos2 == fin2:
            llego += 1
    else:
        print("Movimiento no valido, intente de nuevo")

print("Total de Movimientos: ", movimientos)
print("Costo Total: ", total)

#print(tablero)
#print(recorrido)