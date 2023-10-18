from colorama import Fore, Style
from colorama import init as colorama_init
from termcolor import colored

class Node():
    """A node class for A* Pathfinding"""

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
            elif (str(maze[i][j]) == '1'):
                print(Style.DIM + Fore.LIGHTYELLOW_EX + str(maze[i][j]), end=" ")
            elif (str(maze[i][j]) == '2'):
                print(Style.BRIGHT + Fore.CYAN + str(maze[i][j]), end=" ")
            elif (str(maze[i][j]) == '3'):
                print(Style.BRIGHT + Fore.YELLOW + str(maze[i][j]), end=" ")
            elif (str(maze[i][j]) == '4'):
                print(Style.BRIGHT + Fore.GREEN + str(maze[i][j]), end=" ")
            else:
                print(Style.BRIGHT + Fore.WHITE + str(maze[i][j]), end=" ")

        print("     ", end=" ")

        for j in range(0, n):
            if (str(mazeCamino[i][j]) == '0'):
                print(Fore.LIGHTWHITE_EX + str(mazeCamino[i][j]), end=" ")
            elif (str(mazeCamino[i][j]) == '1'):
                print(Fore.LIGHTRED_EX + str(mazeCamino[i][j]), end=" ")
            elif (str(mazeCamino[i][j]) == '2'):
                print(Fore.CYAN + str(mazeCamino[i][j]), end=" ")
            elif (str(mazeCamino[i][j]) == '3'):
                print(Fore.YELLOW + str(mazeCamino[i][j]), end=" ")
            elif (str(mazeCamino[i][j]) == '4'):
                print(Fore.GREEN + str(mazeCamino[i][j]), end=" ")
            elif (str(mazeCamino[i][j]) == 'X'):
                print(Fore.MAGENTA + str(mazeCamino[i][j]), end=" ")
            else:
                print(Fore.WHITE + str(mazeCamino[i][j]), end=" ")

        print('\n')


def astar(maze, start, end, mazeCamino):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

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
                #print(current_node.f, "Current cost F")

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
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

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
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

    start = (3, 1)
    #end = (3, 6)
    end = (14, 14)

    printMaze(maze, m=15,n=15, mazeCamino=mazeCami)

    print()

    path = astar(maze, start, end, mazeCamino=mazeCami)

    llenarMapaSecundario(mazeCamino=mazeCami, path=path)

    print()

    printMaze(maze, m=15,n=15, mazeCamino=mazeCami)

    print(path)


if __name__ == '__main__':
    main()