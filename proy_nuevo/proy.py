from colorama import Fore, Style
from colorama import init as colorama_init
from termcolor import colored
import random
import time

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0 # Es el costo acumulado
        self.h = 0 # Es la distancia manhattan
        self.f = 0 # Es la suma de g y h

    def __eq__(self, other):
        return self.position == other.position

def printMaze2(maze, m, n):
    print("\t   ", end="")
    for k in range(0, 10):
        print(k, end="   ")
    for k in range(10, m):
        print(k, end="  ")
    print("")
    for i in range(0, m):
        print(i, "\t|  ", end="")
        for j in range(0, n):
            if (str(maze[i][j]) == '0'):
                print(Style.DIM + Fore.BLACK + str(maze[i][j]), end="   ")
                print(Style.RESET_ALL, end="")
            elif (str(maze[i][j]) == '1'):
                print(Style.DIM + Fore.LIGHTRED_EX + str(maze[i][j]), end="   ")
                print(Style.RESET_ALL, end="")
            elif (str(maze[i][j]) == '2'):
                print(Style.BRIGHT + Fore.CYAN + str(maze[i][j]), end="   ")
                print(Style.RESET_ALL, end="")
            elif (str(maze[i][j]) == '3'):
                print(Style.BRIGHT + Fore.YELLOW + str(maze[i][j]), end="   ")
                print(Style.RESET_ALL, end="")
            elif (str(maze[i][j]) == '4'):
                print(Style.BRIGHT + Fore.GREEN + str(maze[i][j]), end="   ")
                print(Style.RESET_ALL, end="")
            elif (str(maze[i][j]) == 'H'):
                print(Fore.MAGENTA + str(maze[i][j]), end="   ")
                print(Style.RESET_ALL, end="")
            elif (str(maze[i][j]) == 'O'):
                print(Fore.WHITE + str(maze[i][j]), end="   ")
                print(Style.RESET_ALL, end="")
            else:
                print(Style.BRIGHT + Fore.WHITE + str(maze[i][j]), end="   ")
                print(Style.RESET_ALL, end="")
        print('\n', end="")

def astar(maze, start, end, esPrimerPersonaje):
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
                # print(current_node.f, "Current cost F")

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        print(current_node.position)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            if esPrimerPersonaje:
                costh.append(int(current_node.g))
            else:
                costo.append(int(current_node.g))
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        numero = 0
        stri = ""

        # Loop through children
        for child in children:
            numero = numero + 1

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            numeroASumar = 0
            if esPrimerPersonaje:
                if (maze[current_node.position[0]][current_node.position[1]] == 0):
                    numeroASumar = 1000
                else:
                    numeroASumar = maze[current_node.position[0]][current_node.position[1]]
            else:
                if (maze[current_node.position[0]][current_node.position[1]] == 0):
                    numeroASumar = 1000
                elif (maze[current_node.position[0]][current_node.position[1]] == 1):
                    numeroASumar = 4
                elif (maze[current_node.position[0]][current_node.position[1]] == 2):
                    numeroASumar = 1
                elif (maze[current_node.position[0]][current_node.position[1]] == 3):
                    numeroASumar = 1000
                elif (maze[current_node.position[0]][current_node.position[1]] == 4):
                    numeroASumar = 3





            numeroASumar = numeroASumar * 2

            child.g = current_node.g + numeroASumar
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

            stri = stri + str(child.position) + "--->"

            if numero == 4:
                print(stri)
                print()
                print()


def llenarMapaSecundario(mazeCamino, path, esPrimerPersonaje):
    if esPrimerPersonaje:
        for i in path:
            cadenaSinParentesis = str(i).replace('(', '')
            cadenaSinParentesis = cadenaSinParentesis.replace(')', '')
            cadenaPartida = cadenaSinParentesis.split(',')
            mazeCamino[int(cadenaPartida[0])][int(cadenaPartida[1])] = 'H'
            printMaze2(mazeCamino, m=15, n=15)
            time.sleep(1)
            print()
    else:
        for i in path:
            cadenaSinParentesis = str(i).replace('(', '')
            cadenaSinParentesis = cadenaSinParentesis.replace(')', '')
            cadenaPartida = cadenaSinParentesis.split(',')
            mazeCamino[int(cadenaPartida[0])][int(cadenaPartida[1])] = 'O'
            printMaze2(mazeCamino, m=15, n=15)
            time.sleep(1)
            print()

def checarpos(table, pos1, pos2, avatar):
    if pos2 > 14 or pos1 > 14 or pos1 < 0 or pos2 < 0:
        return False
    elif avatar == True:
        if table[pos1][pos2] == 0:
            return False
        else:
            return True
    elif avatar == False:
        if table[pos1][pos2] == 0:
            return False
        elif table[pos1][pos2] == 3:
            return False
        else:
            return True

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
    return terreno

def main():
    global costh, costo
    costh = []
    costo = []
    maze = obt_mapa("tablero.txt")
    mazeCami = obt_mapa("tablero.txt")

    printMaze2(maze, 15, 15)
    primero = False
    while primero == False:
        print("\n0 - Montaña    1 - Tierra    2 - Agua    3 - Arena    4 - Bosque")
        H1 = int(input("\nPosicion Inicial De Humano:\nIngrese el numero de fila: "))
        H2 = int(input("Ingrese el numero de columna :"))
        O1 = int(input("\nPosicion Inicial De Pulpo:\nIngrese el numero de fila: "))
        O2 = int(input("Ingrese el numero de columna :"))

        D1 = int(input("\nPosicion Del Templo:\nIngrese el numero de fila: "))
        D2 = int(input("Ingrese el numero de columna :"))
        K1 = int(input("\nPosicion De La LLave:\nIngrese el numero de fila: "))
        K2 = int(input("Ingrese el numero de columna :"))

        P1 = int(input("\nPosicion Del Portal:\nIngrese el numero de fila: "))
        P2 = int(input("Ingrese el numero de columna :"))

        if checarpos(maze, H1, H2, True) == False or checarpos(maze, O1, O2, False) == False or checarpos(maze, D1, D2, True) == False or checarpos(maze, K1, K2, True) == False or checarpos(maze, P1, P2, False) == False:
            print("Valores no validos, intente de nuevo")
            primero = False
        else:
            primero = True

    portal = (P1, P2)

    auto = int(input("\nDesea (0)Ingresar  las rutas o (1)Que sea automatica: "))
    if auto == 0:
        RH1 = int(input("\nRuta del Humano:\nPrimero ira a:\n(0)Templo, (1)LLave, (2)Ninguno\n:"))
        if RH1 != 2:
            RH2 = int(input("Despues va a :\n(0)Templo, (1)LLave, (2)Ninguno\n:"))
        else:
            RH2 = 2
            endh = (H1, H2)

        RO1 = int(input("\nRuta del Pulpo:\nPrimero ira a:\n(0)Templo, (1)LLave, (2)Ninguno\n:"))
        if RO1 != 2:
            RO2 = int(input("Despues va a :\n(0)Templo, (1)LLave, (2)Ninguno\n:"))
        else:
            RO2 = 2
            end = (O1, O2)
    else:
        if maze[D1][D2] == 3 and maze[K1][K2] == 3:
            RH1 = 0
            RH2 = 1
            RO1 = 2
            RO2 = 2
        elif maze[D1][D2] != 3 and maze[K1][K2] == 3 or (((H1 - D1) ** 2) + ((H2 - D2) ** 2)) >= (((H1 - K1) ** 2) + ((H2 - K2) ** 2)):
            RH1 = 1
            RH2 = 2
            RO1 = 0
            RO2 = 2
        elif maze[D1][D2] == 3 and maze[K1][K2] != 3 or (((H1 - D1) ** 2) + ((H2 - D2) ** 2)) < (((H1 - K1) ** 2) + ((H2 - K2) ** 2)):
            RH1 = 0
            RH2 = 2
            RO1 = 1
            RO2 = 2

    humano = []
    pulpo = []
    if RH1 == 0:
        start = (H1, H2)
        endh = (D1, D2)
        path1 = astar(maze, start, endh, esPrimerPersonaje=True)
        humano.append(path1)
        llenarMapaSecundario(mazeCamino=mazeCami, path=path1, esPrimerPersonaje=True)
        if RH2 == 1:
            start = (D1, D2)
            endh = (K1, K2)
            path1 = astar(maze, start, endh, esPrimerPersonaje=True)
            humano.append(path1)
            llenarMapaSecundario(mazeCamino=mazeCami, path=path1, esPrimerPersonaje=True)
    elif RH1 == 1:
        start = (H1, H2)
        endh = (K1, K2)
        path1 = astar(maze, start, endh, esPrimerPersonaje=True)
        humano.append(path1)
        llenarMapaSecundario(mazeCamino=mazeCami, path=path1, esPrimerPersonaje=True)
        if RH2 == 0:
            start = (K1, K2)
            endh = (D1, D2)
            path1 = astar(maze, start, endh, esPrimerPersonaje=True)
            humano.append(path1)
            llenarMapaSecundario(mazeCamino=mazeCami, path=path1, esPrimerPersonaje=True)
    path1 = astar(maze, endh, portal, esPrimerPersonaje=True)
    humano.append(path1)
    llenarMapaSecundario(mazeCamino=mazeCami, path=path1, esPrimerPersonaje=True)

    if RO1 == 0:
        start = (O1, O2)
        end = (D1, D2)
        path2 = astar(maze, start, end, esPrimerPersonaje=False)
        pulpo.append(path2)
        llenarMapaSecundario(mazeCamino=mazeCami, path=path2, esPrimerPersonaje=False)
        if RO2 == 1:
            start = (D1, D2)
            end = (K1, K2)
            path2 = astar(maze, start, end, esPrimerPersonaje=False)
            pulpo.append(path2)
            llenarMapaSecundario(mazeCamino=mazeCami, path=path2, esPrimerPersonaje=False)
    elif RO1 == 1:
        start = (O1, O2)
        end = (K1, K2)
        path2 = astar(maze, start, end, esPrimerPersonaje=False)
        pulpo.append(path2)
        llenarMapaSecundario(mazeCamino=mazeCami, path=path2, esPrimerPersonaje=False)
        if RH2 == 0:
            start = (K1, K2)
            end = (D1, D2)
            path2 = astar(maze, start, end, esPrimerPersonaje=False)
            pulpo.append(path2)
            llenarMapaSecundario(mazeCamino=mazeCami, path=path2, esPrimerPersonaje=False)
    path2 = astar(maze, end, portal, esPrimerPersonaje=False)
    pulpo.append(path2)
    llenarMapaSecundario(mazeCamino=mazeCami, path=path2, esPrimerPersonaje=False)

    print()

    printMaze2(mazeCami, m=15, n=15)

    print(Fore.GREEN + "Camino del Humano (H): ", humano)
    print()
    print("Costo del Humano: " + str(costh))
    print("Total: " + str(sum(costh)))
    print()
    print(Fore.CYAN + "Camino del Pulpo (O): ", pulpo)
    print()
    print("Costo del Pulpo: " + str(costo))
    print("Total: " + str(sum(costo)))

if __name__ == '__main__':
    main()