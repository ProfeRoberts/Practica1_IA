import pandas as pd
import numpy as np
from sklearn.model_selection import KFold, train_test_split
from sklearn.utils import resample
from ucimlrepo import fetch_ucirepo


def seleccionar_columnas(dataframe, columnas_seleccionadas):
    nuevo_dataframe = dataframe[columnas_seleccionadas]
    return nuevo_dataframe


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


def imprimir_data(matriz_datos):
    indice = 0
    for fila in matriz_datos:
        print(f"{indice} -  ", end="")
        for elemento in fila:
            print(elemento, end=",  ")
        print("")
        indice += 1


def imprimir_clases(matriz_etiquetas):
    indice = 0
    for fila in matriz_etiquetas:
        print(f"{indice} -  ", end="")
        for elemento in fila:
            print(elemento, end="")
        print("")
        indice += 1


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

            if self.distance_metric == 'euclidean':
                dist = euclidean_distance(x, promedio_por_clase)
            elif self.distance_metric == 'manhattan':
                dist = manhattan_distance(x, promedio_por_clase)
            else:
                raise ValueError("Invalid distance metric. Choose 'euclidean' or 'manhattan'.")

            # Actualizar la clase predicha si encontramos una distancia menor
            if dist < distancia_minima:
                distancia_minima = dist
                clase_predicha = clase

        return clase_predicha


def calcular_eficiencia_y_error(predicciones, etiquetas_reales):
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
    total_instancias = len(etiquetas_reales)

    # Calcular el número de aciertos
    aciertos = sum(1 for pred, real in zip(predicciones, etiquetas_reales) if pred == real)

    # Calcular la eficiencia y el error
    eficiencia = (aciertos / total_instancias) * 100.0
    error = 100.0 - eficiencia

    return eficiencia, error


def validacion_cruzada_kfold_min_distance(X, y, k=5, distance_metric='euclidean'):

    kf = KFold(n_splits=k, shuffle=True, random_state=42)
    totalEf = []
    totalErr = []
    for i, (train_index, test_index) in enumerate(kf.split(X), 1):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        # Inicializar y entrenar el clasificador de mínima distancia
        min_distance_classifier = MinDistanceClassifier(distance_metric=distance_metric)
        min_distance_classifier.fit(X_train, y_train)

        # Realizar predicciones en el conjunto de prueba
        y_pred = min_distance_classifier.predict(X_test)
        print(f"\nGrupo {i}:")
        # Calcular eficiencia y error
        eficiencia, error = calcular_eficiencia_y_error(y_pred, y_test)

        # Mostrar resultados para cada grupo
        print(f" - Porcentaje de Eficiencia: {eficiencia:.2f}%")
        totalEf.append(eficiencia)
        print(f" - Porcentaje de Error: {error:.2f}%")
        totalErr.append(error)
    print(f"\n - Promedio de Eficiencia: {np.mean(totalEf):.2f}%")
    print(f" - Promedio de Error: {np.mean(totalErr):.2f}%")
    print(f"\n - Desviacion Estandar de Eficiencia: {np.std(totalEf):.2f}")
    print(f" - Desviacion Estandar de Error: {np.std(totalErr):.2f}")


def validacion_bootstrap_min_distance(X, y, n_iterations=100, size=0.8, test_size=0.2, distance_metric='euclidean'):
    totalEf = []
    totalErr = []

    for i in range(n_iterations):
        # Muestreo Bootstrap
        X_bootstrap, y_bootstrap = resample(X, y, replace=True, n_samples=int(len(X) * size))

        # División en conjunto de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X_bootstrap, y_bootstrap, test_size=test_size, random_state=42, stratify=y)

        # Inicializar y entrenar el clasificador de mínima distancia
        min_distance_classifier = MinDistanceClassifier(distance_metric=distance_metric)
        min_distance_classifier.fit(X_train, y_train)

        # Realizar predicciones en el conjunto de prueba
        y_pred = min_distance_classifier.predict(X_test)

        print(f"\nGrupo {i + 1}:")
        # Calcular eficiencia y error
        eficiencia, error = calcular_eficiencia_y_error(y_pred, y_test)

        # Mostrar resultados para cada grupo
        print(f" - Porcentaje de Eficiencia: {eficiencia:.2f}%")
        totalEf.append(eficiencia)
        print(f" - Porcentaje de Error: {error:.2f}%")
        totalErr.append(error)

    print(f"\n - Promedio de Eficiencia: {np.mean(totalEf):.2f}%")
    print(f" - Promedio de Error: {np.mean(totalErr):.2f}%")
    print(f"\n - Desviacion Estandar de Eficiencia: {np.std(totalEf):.2f}")
    print(f" - Desviacion Estandar de Error: {np.std(totalErr):.2f}")


entrada1 = int(input("Desea : \n (0)Usar un archivo .csv\n (1)Ingresar un id de la pagina 'UC Irvine'\n :"))
if entrada1 == 0:
    entrada = int(input("\nDesea : \n (0)Usar iris.csv\n (1)Ingresar otro csv\n :"))
    if entrada == 0:
        ruta_archivo = "iris.csv"
    elif entrada == 1:
        ruta_archivo = input("\nIngrese el nombre del archivo: ")
    # Lee el conjunto de datos desde un archivo CSV
    datos = pd.read_csv(ruta_archivo)

elif entrada1 == 1:
    id = int(input("\nIngrese el id de la base de datos :"))
    base = fetch_ucirepo(id=id)
    datos = base.data.original


# Imprimir el DataFrame original
print("\n - DataFrame original:")
print(datos)

columnas_disponibles = datos.columns
print("\nColumnas disponibles: ", columnas_disponibles)

# Vector de entrada
print("\n  ** Columnas para el vector de entrada **")
columnas_a_seleccionar = input("Ingrese las columnas que desea seleccionar (separadas por comas): ").split(',')
columnas_a_seleccionar = [columna.strip() for columna in columnas_a_seleccionar]

# Verificar si las columnas ingresadas existen en el DataFrame
columnas_invalidas = [columna for columna in columnas_a_seleccionar if columna not in columnas_disponibles]

if columnas_invalidas:
    print(f"\nError: Las siguientes columnas no existen en el DataFrame: {', '.join(columnas_invalidas)}")
else:
    Xdata = seleccionar_columnas(datos, columnas_a_seleccionar)
    print("\nNuevo DataFrame con Vector de Entrada:")
    print(Xdata)

X = Xdata.values

# Vector de salida
print("\n  ** Columnas para el vector de salida **")
columnas_a_seleccionar = input("Ingrese las columnas que desea seleccionar (separadas por comas): ").split(',')
columnas_a_seleccionar = [columna.strip() for columna in columnas_a_seleccionar]

# Verificar si las columnas ingresadas existen en el DataFrame
columnas_invalidas = [columna for columna in columnas_a_seleccionar if columna not in columnas_disponibles]

if columnas_invalidas:
    print(f"\nError: Las siguientes columnas no existen en el DataFrame: {', '.join(columnas_invalidas)}")
else:
    yclase = seleccionar_columnas(datos, columnas_a_seleccionar)
    print("\nNuevo DataFrame con Vector de Salida:")
    print(yclase)
    for columna in columnas_a_seleccionar:
        yclase = seleccionar_columnas(datos, [columna])
        print(f"\nSalida con la columna seleccionada '{columna}':")
        print(yclase)

        y = yclase.iloc[:, -1].values

        percent = int(input("\n \t *** Train and test ***\nIngrese el porcentaje de datos a ser testeados (%): "))
        percent = percent/100

        # Dividir el conjunto de datos en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=percent, random_state=42, stratify=y)
        print(y_train)
        print(y_test)
        # Inicializar y entrenar el clasificador de mínima distancia
        min_distance_classifier = MinDistanceClassifier()
        min_distance_classifier.fit(X_train, y_train)
        
        # Realizar predicciones en el conjunto de prueba
        y_pred = min_distance_classifier.predict(X_test)
        print("\n\t\t - Predicciones finales -\n")
        eficiencia, error = calcular_eficiencia_y_error(y_pred, y_test)

        print(f"Porcentaje de Eficiencia: {eficiencia:.2f}%")
        print(f"Porcentaje de Error: {error:.2f}%")

        k = int(input("\n \t *** Validacion cruzada kfold ***\nIngrese el valor de k : "))
        validacion_cruzada_kfold_min_distance(X, y, k)

        kbt = int(input("\n \t *** Validacion Bootstrap ***\nIngrese el numero de experimentos (k) : "))
        tamaño = int(input("\nIngrese el tamaño de los subconjuntos bootstrap(%) :"))
        tamaño = tamaño/100
        testbt = int(input("\nIngrese el porcentaje de prueba de cada subconjunto(%) :"))
        testbt = testbt/100
        validacion_bootstrap_min_distance(X, y, kbt, tamaño, testbt)