from collections import deque
from colorama import Fore, Back, Style
import time

class Laberinto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node:
    def __init__(self, pos: Laberinto, cost):
        self.pos = pos
        self.cost = cost

def display_node_data(nodes: deque):
    """
    Prints the x, y coordinates and cost of each node in the array.
    """
    nodosAbajo = deque()
    nodosPrincipal = deque()
    nodosArribaIzquierda = deque()
    nodosArribaDerecha = deque()
    nodosExtraU = deque()
    nodosExtraR = deque()
    nodosExtraD = deque()

    esCaminoPrincipal = True
    for node in nodes:
        if esCaminoPrincipal:
            nodosPrincipal.append(node)
        elif node.pos.y > 2 and node.pos.x > 5:
            nodosAbajo.append(node)
        elif node.pos.y < 4 and node.pos.x < 6:
            nodosArribaIzquierda.append(node)
        elif node.pos.y > 7 > node.pos.x:
            if node.pos.y == 8 and node.pos.x == 1:
                nodosArribaIzquierda.append(node)
            elif node.pos.y == 8 and node.pos.x == 0:
                nodosExtraU.append(node)
            elif node.pos.y > 8 and node.pos.x == 1:
                nodosExtraR.append(node)
            else:
                nodosExtraD.append(node)
        else:
            nodosArribaDerecha.append(node)
        if node.pos.y == 3 and node.pos.x == 6:
            esCaminoPrincipal = False
        #print(f"Nodo: ({node.pos.x}, {node.pos.y}), Costo: {node.cost}   --->", end= "   ")

    for node in nodosPrincipal:
        print(f"Nodo: ({node.pos.x}, {node.pos.y}), Costo: {node.cost}   --->", end="\t")

    print()
    for node in nodosAbajo:
        print(f"\t Nodo: ({node.pos.x}, {node.pos.y}), Costo: {node.cost}   --->", end="")

    print()
    for node in nodosArribaIzquierda:
        print(f"\t Nodo: ({node.pos.x}, {node.pos.y}), Costo: {node.cost}   --->", end="")
        if node.pos.x == 3 and node.pos.y == 3:
            print("\t", end="\n\t")

    print("\t", end="\n\t")
    for node in nodosArribaDerecha:
        print(f"\t Nodo: ({node.pos.x}, {node.pos.y}), Costo: {node.cost}   --->", end="")

    print("\t", end="\n\t\t")
    for node in nodosExtraU:
        print(f"\t Nodo: ({node.pos.x}, {node.pos.y}), Costo: {node.cost}   --->", end="")

    print("\t", end="\n\t\t")
    for node in nodosExtraR:
        print(f"\t Nodo: ({node.pos.x}, {node.pos.y}), Costo: {node.cost}   --->", end="")

    print("\t", end="\n\t\t")
    for node in nodosExtraD:
        print(f"\t Nodo: ({node.pos.x}, {node.pos.y}), Costo: {node.cost}   --->", end="")

    print("\n")

def busquedaPorAnchura(Grid, dest: Laberinto, start: Laberinto, GridCamino, esPorDecision: bool):
    adj_cell_x = [1 if x == "B" else -1 if x == "A" else 0 for x in prior]
    adj_cell_y = [1 if x == "D" else -1 if x == "I" else 0 for x in prior]
    m, n = (len(Grid), len(Grid))
    visited_blocks = [[False for i in range(m)]
                      for j in range(n)]
    visited_blocks[start.x][start.y] = True
    queue = deque()
    arbolGeneral = deque()
    tree = ""
    sol = Node(start, 0)
    queue.append(sol)
    arbolGeneral.append(sol)
    GridCamino[start.x][start.y] = 'X'
    cells = 4
    cost = 0
    while queue:
        current_block = queue.popleft()
        current_pos = current_block.pos
        if current_pos.x == dest.x and current_pos.y == dest.y:
            if esPorDecision:
                printMaze(Grid, m=15, n=15, mazeCamino=GridCamino, visitados=visitadosA)
                print()
                print()
            print("Algoritmo Usado: Búsqueda por anchura")
            print("Camino encontrado!!")
            print("Nodos Totales Visitados = ", cost)
            print("Arbol = ", tree)
            display_node_data(arbolGeneral)
            return current_block.cost

        if current_block not in visited_blocks:
            visited_blocks[current_pos.x][current_pos.y] = True
            cost = cost + 1
        x_pos = current_pos.x
        y_pos = current_pos.y
        entre = 0
        for i in range(cells):
            if x_pos == len(Grid) - 1 and adj_cell_x[i] == 1:
                x_pos = current_pos.x
                y_pos = current_pos.y + adj_cell_y[i]
            if y_pos == 0 and adj_cell_y[i] == -1:
                x_pos = current_pos.x + adj_cell_x[i]
                y_pos = current_pos.y
            else:
                x_pos = current_pos.x + adj_cell_x[i]
                y_pos = current_pos.y + adj_cell_y[i]
            if 15 > x_pos >= 0 and 15 > y_pos >= 0:
                visitadosA.append((x_pos, y_pos))
                if Grid[x_pos][y_pos] == 1:
                    if not visited_blocks[x_pos][y_pos]:
                        entre = entre + 1
                        next_cell = Node(Laberinto(x_pos, y_pos),
                                         current_block.cost + 1)
                        GridCamino[x_pos][y_pos] = 'X'
                        visited_blocks[x_pos][y_pos] = True
                        queue.append(next_cell)
                        arbolGeneral.append(next_cell)
                        if (esPorDecision and entre > 1):
                            tree += "[" + str(x_pos) + ", " + str(y_pos) + "]   "
                            printMaze(Grid, m=15, n=15, mazeCamino=GridCamino, visitados=visitadosA)
                            print()
                            print()
                        elif not esPorDecision:
                            tree += "[" + str(x_pos) + ", " + str(y_pos) + "]   "
                            printMaze(Grid, m=15, n=15, mazeCamino=GridCamino, visitados=visitadosA)
                            print()
                            print()
        time.sleep(1)
    return -1


def create_node(x, y, c):
    val = Laberinto(x, y)
    return Node(val, c + 1)

def printMaze(maze, m, n, mazeCamino, visitados):
    for i in range(0, m):
        for j in range(0, n):
            if (str(maze[i][j]) == '0'):
                print(Fore.BLACK + str(maze[i][j]), end="  ")
                print(Style.RESET_ALL, end="")
            elif (str(maze[i][j]) == '1'):
                print(Fore.GREEN + str(maze[i][j]), end="  ")
                print(Style.RESET_ALL, end="")
            else:
                print(Fore.WHITE + str(maze[i][j]), end="  ")
                print(Style.RESET_ALL, end="")

        print("     ", end=" ")

        for j in range(0, n):
            if (i,j) in visitados:
                if (str(mazeCamino[i][j]) == '0'):
                    print(Fore.BLACK + str(mazeCamino[i][j]), end="  ")
                    print(Style.RESET_ALL, end="")
                elif (str(mazeCamino[i][j]) == '1'):
                    print(Fore.GREEN + str(mazeCamino[i][j]), end="  ")
                    print(Style.RESET_ALL, end="")
                elif (str(mazeCamino[i][j]) == 'X'):
                    print(Fore.CYAN + str(mazeCamino[i][j]), end="  ")
                    print(Style.RESET_ALL, end="")
                else:
                    print(Fore.WHITE + str(maze[i][j]), end="  ")
                    print(Style.RESET_ALL, end="")
            else:
                print(Fore.BLACK + Back.BLACK + ".", end="  ")
                print(Style.RESET_ALL, end="")
        print('\n', end="")

def printMaze2(maze, m, n):
    print("\t   ", end="")
    for k in range(10):
        print(k, end="   ")
    for k in range(10, 15):
        print(k, end="  ")
    print("")
    for i in range(0, m):
        print(i, "\t|  ", end="")
        for j in range(0, n):
            if (str(maze[i][j]) == '0'):
                print(Style.DIM + Fore.BLACK + str(maze[i][j]), end="   ")
                print(Style.RESET_ALL, end="")
            elif (str(maze[i][j]) == '1'):
                print(Style.BRIGHT + Fore.GREEN + str(maze[i][j]), end="   ")
                print(Style.RESET_ALL, end="")
            else:
                print(Fore.WHITE + str(maze[i][j]), end="   ")
                print(Style.RESET_ALL, end="")

        print('\n', end="")

def busquedaPorProfundidad(Grid, dest: Laberinto, start: Laberinto, GridCamino, esPorDecision: bool):
    adj_cell_x = [1 if x == "A" else -1 if x == "B" else 0 for x in prior]
    adj_cell_y = [1 if x == "I" else -1 if x == "D" else 0 for x in prior]
    m, n = (len(Grid), len(Grid))
    visited_blocks = [[False for i in range(m)]
                      for j in range(n)]
    visited_blocks[start.x][start.y] = True
    stack = deque()
    arbolGeneral = deque()
    sol = Node(start, 0)
    GridCamino[start.x][start.y] = 'X'
    stack.append(sol)
    arbolGeneral.append(sol)
    tree = ""
    neigh = 4
    cost = 0
    while stack:
        current_block = stack.pop()
        current_pos = current_block.pos
        if current_pos.x == dest.x and current_pos.y == dest.y:
            if esPorDecision:
                printMaze(Grid, m=15, n=15, mazeCamino=GridCamino, visitados=visitadosP)
                print()
                print()
            print("Algoritmo Usado: Búsqueda por profundidad")
            print("Camino encontrado!!")
            print("Nodos Totales Visitados = ", cost)
            print("Arbol = ", tree)
            display_node_data(arbolGeneral)
            return current_block.cost
        x_pos = current_pos.x
        y_pos = current_pos.y
        entre = 0
        for i in range(neigh):
            if x_pos == len(Grid) - 1 and adj_cell_x[i] == 1:
                x_pos = current_pos.x
                y_pos = current_pos.y + adj_cell_y[i]
            if y_pos == 0 and adj_cell_y[i] == -1:
                x_pos = current_pos.x + adj_cell_x[i]
                y_pos = current_pos.y
            
            else:
                x_pos = current_pos.x + adj_cell_x[i]
                y_pos = current_pos.y + adj_cell_y[i]
            if x_pos != 15 and x_pos != -1 and y_pos != 15 and y_pos != -1:
                visitadosP.append((x_pos, y_pos))
                if Grid[x_pos][y_pos] == 1:
                    if not visited_blocks[x_pos][y_pos]:
                        entre = entre + 1
                        cost += 1
                        GridCamino[x_pos][y_pos] = 'X'
                        visited_blocks[x_pos][y_pos] = True
                        stack.append(create_node(x_pos, y_pos, current_block.cost))
                        arbolGeneral.append(create_node(x_pos, y_pos, current_block.cost))
                        if (esPorDecision and entre > 1):
                            tree += "[" + str(x_pos) + ", " + str(y_pos) + "]   "
                            printMaze(Grid, m=15, n=15, mazeCamino=GridCamino, visitados=visitadosP)
                            print()
                            print()
                        elif not esPorDecision:
                            tree += "[" + str(x_pos) + ", " + str(y_pos) + "]   "
                            printMaze(Grid, m=15, n=15, mazeCamino=GridCamino, visitados=visitadosP)
                            print()
                            print()
        time.sleep(1)
    return -1

def checarpos(table, pos1, pos2):
    if pos2 > 14 or pos1 > 14 or pos1 < 0 or pos2 < 0 or table[pos1][pos2] == 0:
        return False
    else:
        return True

def main():
    global visitadosA, visitadosP
    visitadosA = []
    visitadosP = []
    maze = [[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]]

    mazeCamino = [[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                  [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                  [0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                  [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]]

    printMaze2(maze, 15, 15)
    print("Start\nDesea que la busqueda se realize:")
    print("A) Por nodo")
    print("B) Por Decisión")
    seleccion = input()
    esPorDecision = False
    if (seleccion == 'B'):
        esPorDecision = True

    primero = False
    while primero == False:
        print("0 Pared \t 1 Camino")
        pos1 = int(input("\nPosicion Inicial:\nIngrese el numero de fila: "))
        pos2 = int(input("Ingrese el numero de columna :"))
        fin1 = int(input("Posicion Final:\nIngrese el numero de fila: "))
        fin2 = int(input("Ingrese el numero de columna :"))
        if checarpos(maze, pos1, pos2) is False or checarpos(maze, fin1, fin2) is False:
            print("Valores no validos, intente de nuevo")
            primero = False
        else:
            primero = True

    destination = Laberinto(fin1, fin2)
    starting_position = Laberinto(pos1, pos2)
    global prior
    prior = []
    prior.append(input("Ingrese la prioridad de direcciones: \n :"))
    prior.append(input("\n :"))
    prior.append(input("\n :"))
    prior.append(input("\n :"))

    res = busquedaPorAnchura(maze, destination, starting_position, GridCamino=mazeCamino, esPorDecision=esPorDecision)

    mazeCamino = [[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                  [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                  [0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                  [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]]

    res2 = busquedaPorProfundidad(maze, destination, starting_position, mazeCamino, esPorDecision=esPorDecision)


if __name__ == '__main__':
    main()