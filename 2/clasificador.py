import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from collections import Counter


def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2)**2))


def manhattan_distance(x1, x2):
    return np.sum(np.abs(x1 - x2))


def calcular_promedio_por_columna(matriz):
    return np.mean(matriz, axis=0)


def calcular_promedio_por_clase(matriz_datos, matriz_etiquetas, clase):
    # Filtrar las filas correspondientes a la clase
    filas_clase = matriz_datos[matriz_etiquetas == clase]
    # Calcular el promedio por columna para las filas de esa clase
    return np.mean(filas_clase, axis=0)

def imprimir_clases(matriz_etiquetas):
    indice = 0
    for fila in matriz_etiquetas:
        print(f"{indice} -  ", end="")
        for elemento in str(fila):
            print(elemento, end="")
        print("")
        indice += 1


def imprimir_data(matriz_datos):
    indice = 0
    for fila in matriz_datos:
        print(f"{indice} -  ", end="")
        for elemento in fila:
            print(elemento, end=",  ")
        print("")
        indice += 1


def predicciones_finales(predicciones, etiquetas_reales):
    cont = 0
    errores = []
    print("     Predicciones \t Valores reales")
    for pred, real in zip(predicciones, etiquetas_reales):
        print(f" {cont} - {pred} \t {real}")
        if pred != real:
            errores.append(cont)
        cont += 1
    print("  ** Indice de los errores: ")
    print(errores)


class KNNClassifier:
    def __init__(self, k=3, distance_metric='euclidean'):
        self.k = k
        self.distance_metric = distance_metric

    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

    def predict(self, X_test):
        predictions = [self._predict(x) for x in X_test]
        return np.array(predictions)

    def _predict(self, x):
        if self.distance_metric == 'euclidean':
            distances = [euclidean_distance(x, x_train) for x_train in self.X_train]
        elif self.distance_metric == 'manhattan':
            distances = [manhattan_distance(x, x_train) for x_train in self.X_train]
        else:
            raise ValueError("Invalid distance metric. Choose 'euclidean' or 'manhattan'.")

        k_indices = np.argsort(distances)[:self.k]
        k_nearest_labels = [self.y_train[i] for i in k_indices]
        # Usar Counter para contar la frecuencia de cada elemento
        contador = Counter(k_nearest_labels)
        # Encontrar el elemento más común y su frecuencia
        clase_mas_comun, frecuencia = contador.most_common(1)[0]
        return clase_mas_comun


class MinDistanceClassifier:
    def __init__(self, distance_metric='euclidean'):
        self.distance_metric = distance_metric

    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

    def predict(self, X_test):
        predictions = [self._predict(x) for x in X_test]
        return np.array(predictions)

    def _predict(self, x):
        clases_unicas = np.unique(y_train)
        distancia_minima = float('inf')
        clase_predicha = None
        for clase in clases_unicas:
            promedio_por_clase = calcular_promedio_por_clase(X_train, y_train, clase)
            # print(f"\nPromedio por clase :")
            # print(promedio_por_clase)

            if self.distance_metric == 'euclidean':
                dist = euclidean_distance(x, promedio_por_clase)
            elif self.distance_metric == 'manhattan':
                dist = manhattan_distance(x, promedio_por_clase)
            else:
                raise ValueError("Invalid distance metric. Choose 'euclidean' or 'manhattan'.")

            # print(f"\nDistancia a la clase : {dist}")

            # Actualizar la clase predicha si encontramos una distancia menor
            if dist < distancia_minima:
                distancia_minima = dist
                clase_predicha = clase

        return clase_predicha


def eliminar_filas_columnas(dataframe, filas=None, columnas=None):
    if filas is not None:
        dataframe = dataframe.drop(filas, axis=0)

    if columnas is not None:
        dataframe = dataframe.drop(columnas, axis=1)

    return dataframe


entrada = int(input("Desea : \n (0)Usar iris.csv\n (1)Ingresar otro csv\n :"))

if entrada == 0:
    ruta_archivo = "iris.csv"
elif entrada == 1:
    ruta_archivo = input("\nIngrese el nombre del archivo: ")

# Lee el conjunto de datos desde un archivo CSV
datos = pd.read_csv(ruta_archivo)

print("\n - DataFrame original:")
print(datos)

ciclo = 1
while ciclo != 0:
    ciclo = int(input("\nDesea : \n (0) No eliminar nada\n (1) Eliminar una fila\n (2) Eliminar una columna\n :"))
    if ciclo == 1:
        fila = int(input("\nIngrese el indice de la fila :"))
        datos = eliminar_filas_columnas(datos, filas=[fila], columnas=None)
        print("\n - DataFrame después de eliminar la fila:")
        print(datos)
    elif ciclo == 2:
        columna = input("\nIngrese el nombre de la columna :")
        datos = eliminar_filas_columnas(datos, filas=None, columnas=columna)
        print("\n - DataFrame después de eliminar la columna:")
        print(datos)

clase = input("\nIngrese el nombre de la columna de clases: ")

Xdata = datos.copy()
Xdata.drop(clase, axis=1, inplace=True)

yclase = datos[[clase]].copy()

percent = int(input("Ingrese el porcentaje de datos a ser testeados (%): "))
percent = percent/100

X = Xdata.values
y = yclase.iloc[:, -1].values

# Dividir el conjunto de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=percent, random_state=42, stratify=y)

print("\n\t\t - Conjunto de datos para entrenamiento -\n")
# print(X_train)
imprimir_data(X_train)

print("\n\t\t - Clases para entrenamiento -\n")
imprimir_clases(y_train)

print("\n\t\t - Conjunto de datos para test -\n")
# print(X_test)
imprimir_data(X_test)
print("\n\t\t - Clases para test -\n")
# print(y_test)
imprimir_clases(y_test)

op = int(input("Desea usar: \n (1)K-NN\n (2)Minima Distancia\n :"))

distancia = 'no'
while distancia == 'no':
    dist = int(input("Elija entre distancia \n (1)Euclidiana\n (2)Manhattan\n :"))
    if dist == 1:
        distancia = 'manhattan'
    elif dist == 2:
        distancia = 'euclidean'
    else:
        print("Intente de nuevo \n")

if op == 1:
    k = int(input("Ingrese el valor de k: "))
    # Inicializar y entrenar el clasificador k-NN
    knn_classifier = KNNClassifier(k, distance_metric=distancia)
    knn_classifier.fit(X_train, y_train)

    # Realizar predicciones en el conjunto de prueba
    y_pred = knn_classifier.predict(X_test)
    print("\n\t\t - Predicciones finales -\n")
    predicciones_finales(y_pred, y_test)

elif op == 2:
    # Inicializar y entrenar el clasificador de mínima distancia
    min_distance_classifier = MinDistanceClassifier(distance_metric=distancia)
    min_distance_classifier.fit(X_train, y_train)

    # Realizar predicciones en el conjunto de prueba
    y_pred = min_distance_classifier.predict(X_test)
    print("\n\t\t - Predicciones finales -\n")
    predicciones_finales(y_pred, y_test)

else:
    print("Valor invalido")
