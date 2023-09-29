import numpy as np

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

def Checar(table, pos1, pos2, avatar, mov):
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
    elif table[pos1, pos2] == 8 or table[pos1, pos2] == 9:
        return 2
    elif table[pos1, pos2] == 10:
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

def checar2op(table, pos1, pos2, avatar):
    posibles = 0
    if Checar(table, pos1, pos2, avatar, 'd') == 1:
        posibles += int(1)
    if Checar(table, pos1, pos2, avatar, 'w') == 1:
        posibles += int(1)
    if Checar(table, pos1, pos2, avatar, 'a') == 1:
        posibles += int(1)
    if Checar(table, pos1, pos2, avatar, 's') == 1:
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
                print("#", end="   ")
            elif table[i, j] == 1:
                print("-", end="   ")
            elif table[i, j] == 2:
                print("~", end="   ")
            elif table[i, j] == 3:
                print("=", end="   ")
            elif table[i, j] == 4:
                print("&", end="   ")
            elif table[i, j] == 5:
                print("%", end="   ")
            elif table[i, j] == 6:
                print("*", end="   ")
            if j == 14:
                print("")

def impTablero(table, avatar):
    for i in range(15):
        for j in range(15):
            if table[i, j] == 0:
                print("#", end="   ")
            elif table[i, j] == 1:
                print("-", end="   ")
            elif table[i, j] == 2:
                print("~", end="   ")
            elif table[i, j] == 3:
                print("=", end="   ")
            elif table[i, j] == 4:
                print("&", end="   ")
            elif table[i, j] == 5:
                print("%", end="   ")
            elif table[i, j] == 6:
                print("*", end="   ")
            elif table[i, j] == 7:
                if avatar == 1:
                    print("H", end="   ")
                elif avatar == 2:
                    print("M", end="   ")
                elif avatar == 3:
                    print("P", end="   ")
                elif avatar == 4:
                    print("S", end="   ")
            elif table[i, j] == 8:
                print("V", end="   ")
            elif table[i, j] == 9:
                print("Vo", end="  ")
            elif table[i, j] == 10:
                print("F", end="   ")
            if j == 14:
                print("")

avatar = int(input("Desea ser un \n(1)Humano\n(2)Mono\n(3)Pulpo\n(4)Sasquatch"))
tablero = np.array([[0,0,0,0,0,1,6,6,6,6,6,6,6,6,6],
           [0,0,0,0,0,1,1,1,6,6,6,5,5,5,6],
           [0,0,0,0,1,1,6,1,1,5,5,5,5,5,6],
           [0,0,0,0,1,6,0,1,5,5,5,5,5,5,5],
           [0,0,0,1,1,6,4,1,1,5,5,5,5,5,5],
           [0,0,1,1,6,0,4,0,4,0,5,5,5,5,1],
           [1,1,1,6,0,0,4,4,4,4,4,5,5,1,1],
           [4,6,6,0,0,4,4,0,0,0,1,1,1,3,3],
           [4,0,0,0,4,4,0,0,3,3,3,1,1,3,3],
           [4,0,0,4,4,4,4,3,3,3,3,1,2,2,2],
           [4,4,4,4,4,4,0,3,3,3,2,2,2,2,2],
           [0,0,4,4,4,0,0,3,3,2,2,2,2,2,2],
           [4,4,4,4,0,0,3,3,2,2,2,2,2,2,2],
           [0,0,0,4,4,4,3,3,2,2,2,2,2,2,2],
           [4,4,4,4,0,3,3,2,2,2,2,2,2,2,2]])
impTablero2(tablero)
primero = False
while primero == False:
    pos1 = int(input("\n# Montaña    - Tierra    ~ Agua    = Arena\n& Bosque    % Pantano    * Nieve \n\nPosicion Inicial:\nIngrese la coordenada vertical: "))
    pos2 = int(input("Ingrese la coordenada horizontal :"))
    fin1 = int(input("Posicion Final:\nIngrese la coordenada vertical: "))
    fin2 = int(input("Ingrese la coordenada horizontal :"))
    if checarpos(tablero, pos1, pos2, avatar) == False or checarpos(tablero, fin1, fin2, avatar) == False:
        print("Valores no validos, intente de nuevo")
        primero = False
    else:
        primero = True

llego = 0
movimientos = 0
total = 0

tablero[pos1][pos2] = 7
tablero[fin1][fin2] = 10

impTablero(tablero, avatar)

while llego == 0:
    if checar2op(tablero, pos1, pos2, avatar) == True:
        tablero[pos1][pos2] = 9
    else:
        tablero[pos1][pos2] = 8
    print("Puede moverse con WASD, \n# Montaña    - Tierra    ~ Agua    = Arena\n& Bosque    % Pantano    * Nieve\nproximo movimiento :")
    entrada = input()
    if Checar(tablero, pos1, pos2, avatar, entrada) == 1 or Checar(tablero, pos1, pos2, avatar, entrada) == 2:
        if entrada == 'd':
            pos2 += 1
        elif entrada == 'a':
            pos2 -= 1
        elif entrada == 'w':
            pos1 -= 1
        elif entrada == 's':
            pos1 += 1
        total = costo(tablero, pos1, pos2, avatar, total)
        tablero[pos1][pos2] = 7
        movimientos += 1
        impTablero(tablero, avatar)
        if pos1 == fin1 and pos2 == fin2:
            llego += 1
    else:
        print("Movimiento no valido, intente de nuevo")

print("Total de Movimientos: ", movimientos)
print("Costo Total: ", total)
