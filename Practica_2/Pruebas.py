from typing import List

class Node:
    def __init__(self, data: int, children: List[Node] = []):
        self.data = data
        self.children = children

def create_tree_from_array(array: List[int]) -> Node:
    """
    Crea un árbol a partir de un arreglo.

    Args:
        array: El arreglo que contiene los datos del árbol.

    Returns:
        El nodo raíz del árbol.
    """

    # Inicializamos el árbol con el primer elemento del arreglo.
    if array:
        root = Node(array[0])
    else:
        return None

    # Recorremos el arreglo y agregamos cada elemento como hijo del nodo actual.
    for i in range(1, len(array)):
        child = Node(array[i])
        root.children.append(child)

    return root

def draw_tree(node: Node):
    """
    Dibuja un árbol.

    Args:
        node: El nodo raíz del árbol.
    """

    # Imprimimos el dato del nodo actual.
    print(node.data)

    # Recorremos los hijos del nodo actual.
    for child in node.children:
        # Llamamos a la función `draw_tree` para dibujar el árbol de cada hijo.
        draw_tree(child)


def main():
    # Creamos un arreglo de registros.
    array = [1, 2, 3, 4, 5]

    # Creamos el árbol a partir del arreglo.
    root = create_tree_from_array(array)

    # Dibujamos el árbol.
    draw_tree(root)


if __name__ == '__main__':
    main()
