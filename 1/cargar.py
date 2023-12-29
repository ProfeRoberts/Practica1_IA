import pandas as pd
import numpy as np


def obtener_nombre_columna_por_indice(archivo_csv, indice_columna):
    try:
        # Lee el archivo CSV
        datos = pd.read_csv(archivo_csv)
        # Obtiene el nombre de la columna por índice
        nombre_columna = datos.columns[indice_columna]
        return nombre_columna

    except FileNotFoundError:
        return f"Error: El archivo {archivo_csv} no fue encontrado."
    except IndexError:
        return f"Error: Índice de columna {indice_columna} fuera de rango."
    except Exception as e:
        return f"Error: {str(e)}"


def obtener_nombres_columnas(archivo_csv):
    try:
        # Lee el archivo CSV
        datos = pd.read_csv(archivo_csv)
        # Obtiene los nombres de las columnas
        nombres_columnas = datos.columns.tolist()
        return nombres_columnas

    except FileNotFoundError:
        print(f"El archivo {archivo_csv} no fue encontrado.")
        return None
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")
        return None


def recorrer_y_guardar(array, nombre_archivo, nombres_columnas):
    with open(nombre_archivo, 'w') as archivo:
        # Agregar nombres de columnas al final de la matriz
        for nombre_columna in nombres_columnas:
            print(f"{nombre_columna},", end="")
            archivo.write(str(nombre_columna) + ',')
        archivo.write('\n')

        # Guardar el contenido de la matriz
        for fila in array:
            for elemento in fila:
                #print(f"{elemento},", end="")
                archivo.write(str(elemento) + ',')
            archivo.write('\n')
            #print("")


class ManejadorMatriz:
    def __init__(self, ruta_archivo, separador):
        self.df = pd.read_csv(ruta_archivo, sep=separador)
        self.matriz = self.df.values
        self.num_filas, self.num_columnas = self.matriz.shape

    def obtener_matriz(self):
        return self.matriz

    def obtener_dimensiones(self):
        return self.num_filas, self.num_columnas

    def separar_fila(self, indice_fila):
        fila = self.matriz[indice_fila, :]
        nueva_matriz = np.array([fila])
        return nueva_matriz

    def separar_columna(self, indice_columna):
        columna = self.matriz[:, indice_columna]
        nueva_matriz = np.array([columna]).T
        return nueva_matriz


entrada = int(input("Desea : \n (0)Usar avocado.csv\n (1)Ingresar otro csv\n :"))
delim = input("\nIngrese el separador de atributos :")

if entrada == 0:
    ruta_archivo = "avocado.csv"
elif entrada == 1:
    ruta_archivo = input("\nIngrese el nombre del archivo: ")

manejador = ManejadorMatriz(ruta_archivo, delim)

# Obtener la matriz completa
matriz_completa = manejador.obtener_matriz()
print("\nMatriz Completa:")
print(matriz_completa)

# Obtener dimensiones de la matriz
num_filas, num_columnas = manejador.obtener_dimensiones()
print(f"\nNúmero de Filas: {num_filas}, Número de Columnas: {num_columnas}")

opc = int(input("Desea seleccionar: \n (1)Filas\n (2)Columnas\n :"))
salir = 1
cont = 0
cseleccionadas = []

while salir == 1:
    indice = int(input("\nIngrese el indice :"))
    if opc == 1:
        fila_separada = manejador.separar_fila(indice)
        print(f"\nFila {indice} Separada:")
        print(fila_separada)
        if cont == 0:
            nueva = np.array(fila_separada)
        else:
            nueva = np.concatenate((nueva, fila_separada), axis=0)
    elif opc == 2:
        columna_separada = manejador.separar_columna(indice)
        cseleccionadas.append(indice)
        print(f"\nColumna {indice} Separada:")
        print(columna_separada)
        if cont == 0:
            nueva = np.array(columna_separada)
        else:
            nueva = np.concatenate((nueva, columna_separada), axis=1)
    cont += 1
    salir = int(input("\nDesea seguir seleccionando?\n (0)No\n (1)Si\n :"))

print(nueva)
print(f"\nNumero de elementos seleccionados: {cont}")

# Obtener nombres de columnas
if opc == 1:
    nombres_columnas = obtener_nombres_columnas(ruta_archivo)
else:
    nombres_columnas = [obtener_nombre_columna_por_indice(ruta_archivo, i) for i in cseleccionadas]

# Guardar en archivo con nombres de columnas
recorrer_y_guardar(nueva, "valores.txt", nombres_columnas)
