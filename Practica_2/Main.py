from collections import deque
from colorama import init
from colorama import Fore, Back, Style


# to keep track of the blocks of maze
class Laberinto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# each block will have its own position and cost of steps taken
class Node:
    def __init__(self, pos: Laberinto, cost):
        self.pos = pos
        self.cost = cost


def busquedaPorAnchura(Grid, dest: Laberinto, start: Laberinto, GridCamino, esPorDecision: bool):
    adj_cell_x = [-1, 0, 0, 1]
    adj_cell_y = [0, -1, 1, 0]
    m, n = (len(Grid), len(Grid))
    visited_blocks = [[False for i in range(m)]
                for j in range(n)]
    visited_blocks[start.x][start.y] = True
    queue = deque()
    tree = ""
    sol = Node(start, 0)
    queue.append(sol)
    cells = 4
    cost = 0
    while queue:
        current_block = queue.popleft()
        current_pos = current_block.pos
        if current_pos.x == dest.x and current_pos.y == dest.y:
            if esPorDecision:
                printMaze(Grid, m=15,n=15, mazeCamino=GridCamino)
                print()
                print()
            print("Algoritmo Usado: Búsqueda por anchura")
            print("Camino encontrado!!")
            print("Nodos Totales Visitados = ", cost)
            print("Arbol = ", tree)
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
            if x_pos < 15 and y_pos < 15 and x_pos >= 0 and y_pos >= 0:
                if Grid[x_pos][y_pos] == 1:
                    if not visited_blocks[x_pos][y_pos]:
                        entre = entre +1
                        print("Entre = ", entre)
                        next_cell = Node(Laberinto(x_pos, y_pos),
                                        current_block.cost + 1)
                        GridCamino[x_pos][y_pos] = 'X' 
                        visited_blocks[x_pos][y_pos] = True
                        queue.append(next_cell)
                        if (esPorDecision and entre > 1):
                            tree += "[" + str(x_pos) + ", " + str(y_pos) + "]   "
                            printMaze(Grid, m=15,n=15, mazeCamino=GridCamino)
                            print()
                            print()
                        elif not esPorDecision:
                            tree += "[" + str(x_pos) + ", " + str(y_pos) + "]   "
                            printMaze(Grid, m=15,n=15, mazeCamino=GridCamino)
                            print()
                            print()
    return -1

def create_node(x, y, c):
    val = Laberinto(x, y)
    return Node(val, c + 1)

def printMaze(maze, m, n, mazeCamino):
    for i in range(0, m):
        for j in range(0, n):
            if (str(maze[i][j]) == '0'):
                print(Fore.WHITE + str(maze[i][j]), end=" ")
            elif (str(maze[i][j]) == '1'):
                print(Fore.GREEN + str(maze[i][j]), end=" ")
            elif (str(maze[i][j]) == 'X'):
                print(Fore.CYAN + str(maze[i][j]), end=" ")
            else:
                print(Fore.WHITE + str(maze[i][j]), end=" ")

        print("     ", end=" ")

        for j in range(0, n):
            if (str(mazeCamino[i][j]) == '0'):
                print(Fore.WHITE + str(mazeCamino[i][j]), end=" ")
            elif (str(mazeCamino[i][j]) == '1'):
                print(Fore.GREEN + str(mazeCamino[i][j]), end=" ")
            elif (str(mazeCamino[i][j]) == 'X'):
                print(Fore.CYAN + str(mazeCamino[i][j]), end=" ")
            else:
                print(Fore.WHITE + str(maze[i][j]), end=" ")

        print('\n')

def busquedaPorProfundidad(Grid, dest: Laberinto, start: Laberinto, GridCamino, esPorDecision: bool):
    adj_cell_x = [1, 0, 0, -1]
    adj_cell_y = [0, 1, -1, 0]
    m, n = (len(Grid), len(Grid))
    visited_blocks = [[False for i in range(m)]
               for j in range(n)]
    visited_blocks[start.x][start.y] = True
    stack = deque()
    sol = Node(start, 0)
    stack.append(sol)
    tree = ""
    neigh = 4
    cost = 0
    while stack:
        current_block = stack.pop()
        current_pos = current_block.pos
        if current_pos.x == dest.x and current_pos.y == dest.y:
            if esPorDecision:
                printMaze(Grid, m=15,n=15, mazeCamino=GridCamino)
                print()
                print()
            print("Algoritmo Usado: Búsqueda por profundidad")
            print("Camino encontrado!!")
            print("Nodos Totales Visitados = ", cost)
            print("Arbol = ", tree)
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
                if Grid[x_pos][y_pos] == 1:
                    if not visited_blocks[x_pos][y_pos]:
                        entre = entre +1
                        cost += 1
                        GridCamino[x_pos][y_pos] = 'X' 
                        visited_blocks[x_pos][y_pos] = True
                        stack.append(create_node(x_pos, y_pos, current_block.cost))
                        if (esPorDecision and entre > 1):
                            tree += "[" + str(x_pos) + ", " + str(y_pos) + "]   "
                            printMaze(Grid, m=15,n=15, mazeCamino=GridCamino)
                            print()
                            print()
                        elif not esPorDecision:
                            tree += "[" + str(x_pos) + ", " + str(y_pos) + "]   "
                            printMaze(Grid, m=15,n=15, mazeCamino=GridCamino)
                            print()
                            print()
    return -1


def main():
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
    
    print("Seleccione la opción que desee")
    print("A) Por nodo")
    print("B) Por Decisión")
    seleccion = input()
    esPorDecision = False
    if (seleccion == 'B') :
        esPorDecision = True
    print("Valor de esPorDecision: ", esPorDecision )

    destination = Laberinto(1, 14)
    starting_position = Laberinto(9, 0)
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