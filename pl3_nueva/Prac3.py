from colorama import Fore, Style, Back
from colorama import init as colorama_init
from termcolor import colored

class Node():
    #A node class for A* Pathfinding

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def printMaze(maze, m, n, mazeCamino):
    for i in range(0, m):
        for j in range(0, n):
            if (str(maze[i][j]) == '0'):
                print(Style.DIM + Fore.LIGHTWHITE_EX + str(maze[i][j]), end=" ")
                print(Style.RESET_ALL, end="")
            elif (str(maze[i][j]) == '1'):
                print(Style.DIM + Fore.LIGHTRED_EX + str(maze[i][j]), end=" ")
                print(Style.RESET_ALL, end="")
            elif (str(maze[i][j]) == '2'):
                print(Style.BRIGHT + Fore.CYAN + str(maze[i][j]), end=" ")
                print(Style.RESET_ALL, end="")
            elif (str(maze[i][j]) == '3'):
                print(Style.BRIGHT + Fore.YELLOW + str(maze[i][j]), end=" ")
                print(Style.RESET_ALL, end="")
            elif (str(maze[i][j]) == '4'):
                print(Style.BRIGHT + Fore.GREEN + str(maze[i][j]), end=" ")
                print(Style.RESET_ALL, end="")
            else:
                print(Style.BRIGHT + Fore.WHITE + str(maze[i][j]), end=" ")
                print(Style.RESET_ALL, end="")

        print("     ", end=" ")

        for j in range(0, n):
            if (i,j) in visitado:
                if (str(mazeCamino[i][j]) == '0'):
                    print(Fore.LIGHTWHITE_EX + str(mazeCamino[i][j]), end=" ")
                    print(Style.RESET_ALL, end="")
                elif (str(mazeCamino[i][j]) == '1'):
                    print(Fore.LIGHTRED_EX + str(mazeCamino[i][j]), end=" ")
                    print(Style.RESET_ALL, end="")
                elif (str(mazeCamino[i][j]) == '2'):
                    print(Fore.CYAN + str(mazeCamino[i][j]), end=" ")
                    print(Style.RESET_ALL, end="")
                elif (str(mazeCamino[i][j]) == '3'):
                    print(Fore.YELLOW + str(mazeCamino[i][j]), end=" ")
                    print(Style.RESET_ALL, end="")
                elif (str(mazeCamino[i][j]) == '4'):
                    print(Fore.GREEN + str(mazeCamino[i][j]), end=" ")
                    print(Style.RESET_ALL, end="")
                elif (str(mazeCamino[i][j]) == 'X'):
                    print(Fore.MAGENTA + str(mazeCamino[i][j]), end=" ")
                    print(Style.RESET_ALL, end="")
            else:
                print(Fore.BLACK + Back.BLACK + ".", end=" ")
                print(Style.RESET_ALL, end="")
        print('\n', end="")

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
                print(Style.DIM + Fore.LIGHTWHITE_EX + str(maze[i][j]), end="   ")
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
            else:
                print(Style.BRIGHT + Fore.WHITE + str(maze[i][j]), end="   ")
                print(Style.RESET_ALL, end="")
        print('\n', end="")


def astar(maze, start, end, esPrimerPersonaje):
    #Returns a list of tuples as a path from the given start to the given end in the given maze

    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    global visitado
    visitado = []
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

        # Found the goal
        if current_node == end_node:
            for pos in open_list + closed_list:
                visitado.append(pos.position)
            path = []
            current = current_node
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

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            numeroASumar = 0
            if esPrimerPersonaje:
                if (maze[current_node.position[0]][current_node.position[1]] == 0):
                    numeroASumar = 1000
                elif (maze[current_node.position[0]][current_node.position[1]] == 1):
                    numeroASumar = 2
                elif (maze[current_node.position[0]][current_node.position[1]] == 2):
                    numeroASumar = 4
                elif (maze[current_node.position[0]][current_node.position[1]] == 3):
                    numeroASumar = 3
                elif (maze[current_node.position[0]][current_node.position[1]] == 4):
                    numeroASumar = 1
            else:
                if (maze[current_node.position[0]][current_node.position[1]] == 0):
                    numeroASumar = 1000
                elif (maze[current_node.position[0]][current_node.position[1]] == 1):
                    numeroASumar = 2
                elif (maze[current_node.position[0]][current_node.position[1]] == 2):
                    numeroASumar = 1
                elif (maze[current_node.position[0]][current_node.position[1]] == 3):
                    numeroASumar = 1000
                elif (maze[current_node.position[0]][current_node.position[1]] == 4):
                    numeroASumar = 3

            numeroASumar = numeroASumar * 2
            # Create the f, g, and h values
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


def llenarMapaSecundario(mazeCamino, path):
    for i in path:
        cadenaSinParentesis = str(i).replace('(', '')
        cadenaSinParentesis = cadenaSinParentesis.replace(')', '')
        cadenaPartida = cadenaSinParentesis.split(',')
        mazeCamino[int(cadenaPartida[0])][int(cadenaPartida[1])] = 'X'

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

def main():
    maze = [[4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4],
            [4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 4, 3, 4, 4, 4],
            [4, 4, 4, 2, 2, 4, 1, 4, 1, 1, 3, 3, 4, 1, 1],
            [4, 4, 2, 2, 2, 2, 1, 4, 1, 1, 3, 3, 1, 1, 1],
            [4, 4, 2, 2, 2, 2, 1, 4, 4, 1, 1, 3, 1, 1, 1],
            [4, 4, 4, 2, 2, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3],
            [4, 4, 4, 0, 0, 0, 1, 1, 1, 1, 1, 3, 3, 3, 3],
            [4, 4, 4, 1, 0, 4, 4, 1, 1, 3, 3, 3, 3, 2, 2],
            [4, 4, 4, 1, 1, 4, 4, 0, 1, 3, 3, 3, 2, 2, 2],
            [4, 4, 1, 1, 1, 1, 0, 0, 0, 3, 3, 2, 2, 2, 2],
            [4, 4, 1, 1, 1, 1, 1, 1, 3, 3, 3, 2, 2, 2, 2],
            [4, 4, 1, 1, 1, 1, 1, 1, 3, 3, 2, 2, 2, 2, 2],
            [4, 4, 1, 4, 4, 1, 1, 3, 3, 3, 2, 2, 2, 2, 2],
            [4, 4, 4, 4, 4, 4, 1, 3, 3, 3, 2, 2, 2, 2, 2],
            [4, 4, 4, 4, 4, 4, 1, 3, 3, 3, 2, 2, 2, 2, 2]]

    mazeCami = [[4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4],
                [4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 4, 3, 4, 4, 4],
                [4, 4, 4, 2, 2, 4, 1, 4, 1, 1, 3, 3, 4, 1, 1],
                [4, 4, 2, 2, 2, 2, 1, 4, 1, 1, 3, 3, 1, 1, 1],
                [4, 4, 2, 2, 2, 2, 1, 4, 4, 1, 1, 3, 1, 1, 1],
                [4, 4, 4, 2, 2, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3],
                [4, 4, 4, 0, 0, 0, 1, 1, 1, 1, 1, 3, 3, 3, 3],
                [4, 4, 4, 1, 0, 4, 4, 1, 1, 3, 3, 3, 3, 2, 2],
                [4, 4, 4, 1, 1, 4, 4, 0, 1, 3, 3, 3, 2, 2, 2],
                [4, 4, 1, 1, 1, 1, 0, 0, 0, 3, 3, 2, 2, 2, 2],
                [4, 4, 1, 1, 1, 1, 1, 1, 3, 3, 3, 2, 2, 2, 2],
                [4, 4, 1, 1, 1, 1, 1, 1, 3, 3, 2, 2, 2, 2, 2],
                [4, 4, 1, 4, 4, 1, 1, 3, 3, 3, 2, 2, 2, 2, 2],
                [4, 4, 4, 4, 4, 4, 1, 3, 3, 3, 2, 2, 2, 2, 2],
                [4, 4, 4, 4, 4, 4, 1, 3, 3, 3, 2, 2, 2, 2, 2]]

    #printMaze(maze, m=15, n=15, mazeCamino=mazeCami)
    printMaze2(maze, 15, 15)
    print()

    personaje = input("Ingrese el personaje a elegir:  M(Mono) o O(Pulpo)\n :")

    if (personaje == 'M'):
        esPrimerPersonaje = True
    else:
        esPrimerPersonaje = False

    primero = False
    while primero == False:
        print("\n0 Montaña    1 Tierra    2 Agua\n3 Arena    4 Bosque")
        pos1 = int(input("\nPosicion Inicial:\nIngrese el numero de fila: "))
        pos2 = int(input("Ingrese el numero de columna :"))
        fin1 = int(input("Posicion Final:\nIngrese el numero de fila: "))
        fin2 = int(input("Ingrese el numero de columna :"))
        if checarpos(maze, pos1, pos2, esPrimerPersonaje) == False or checarpos(maze, fin1, fin2, esPrimerPersonaje) == False:
            print("Valores no validos, intente de nuevo")
            primero = False
        else:
            primero = True
    start = (pos1, pos2)
    end = (fin1, fin2)
    path = astar(maze, start, end, esPrimerPersonaje)

    llenarMapaSecundario(mazeCamino=mazeCami, path=path)

    print()

    printMaze(maze, m=15, n=15, mazeCamino=mazeCami)

    print(path)

if __name__ == '__main__':
    main()
