import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from ucimlrepo import fetch_ucirepo
from collections import Counter
from tabulate import tabulate
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif, f_regression, chi2
#Se importan librerias necesarias para el manejo de datos y las operaciones de aprendizaje automático.

#Obtiene un dataframe y devuelve otro, pero unicamente con las columnas relacionadas
def seleccionar_columnas(dataframe, columnas_seleccionadas):
    nuevo_dataframe = dataframe[columnas_seleccionadas]
    return nuevo_dataframe

#Mide la distancia euclidiana para 2 datos
def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))

#Mide la distancia manhattan entre 2 datos
def manhattan_distance(x1, x2):
    return np.sum(np.abs(x1 - x2))


def calcular_promedio_por_columna(matriz):
    return np.mean(matriz, axis=0)

#Obtiene el promedio por clase
def calcular_promedio_por_clase(matriz_datos, matriz_etiquetas, clase):
    # Filtrar las filas correspondientes a la clase
    filas_clase = matriz_datos[matriz_etiquetas == clase]
    # Calcular el promedio por columna para las filas de esa clase
    return np.mean(filas_clase, axis=0)


#Imprime la matriz de datos recibida
def imprimir_data(matriz_datos):
    indice = 0
    for fila in matriz_datos:
        print(f"{indice} -  ", end="")
        for elemento in fila:
            print(elemento, end=",  ")
        print("")
        indice += 1


#Impime la clases
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

    #Evalua las clases unicas disponibles, se calcula el promedio por clase,
    # posteriormente si la distancia entre el nuevo punto y el promedio de la clase es menor
    # a la distancia minimala nueva distancia minima de esta clase sera la distancia entre el punto y el promedio
    # Y su clase predicha será cambiada
    def _predict(self, x):
        clases_unicas = np.unique(self.y_train)
        distancia_minima = float('inf')
        clase_predicha = None
        for clase in clases_unicas:
            promedio_por_clase = calcular_promedio_por_clase(self.X_train, self.y_train, clase)

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


def calcular_eficiencia_y_error(predicciones, etiquetas_reales):
    cont = 0
    errores = []
    # print("Índice\tPredicciones\tReales")
    for pred, real in zip(predicciones, etiquetas_reales):
        # print(f"{cont}-\t{pred}\t{real}")
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


def dividir_aleatoria_kfold(tamano_dataset, k=5, seed=None):
    if seed is not None:
        np.random.seed(seed)

    # Generar índices aleatorios
    indices_aleatorios = np.random.permutation(tamano_dataset)

    # Dividir los índices en K grupos
    grupos_indices = np.array_split(indices_aleatorios, k)

    # Crear listas de índices para entrenamiento y prueba
    grupos_entrenamiento = []
    grupos_prueba = []

    for i in range(k):
        # Seleccionar un grupo como conjunto de prueba
        indices_prueba = grupos_indices[i]

        # Los demás grupos forman el conjunto de entrenamiento
        indices_entrenamiento = np.concatenate([grupos_indices[j] for j in range(k) if j != i])

        grupos_entrenamiento.append(indices_entrenamiento)
        grupos_prueba.append(indices_prueba)

    return grupos_entrenamiento, grupos_prueba


def validacion_cruzada_kfold(X, y, k=5, distance_metric='euclidean', clasificador='min_distancia', kn=1):
    tamano_dataset = len(X)
    grupos_entrenamiento, grupos_prueba = dividir_aleatoria_kfold(tamano_dataset, k=k, seed=42)

    totalEf = []
    totalErr = []
    for i in range(k):
        X_train, X_test = X[grupos_entrenamiento[i]], X[grupos_prueba[i]]
        y_train, y_test = y[grupos_entrenamiento[i]], y[grupos_prueba[i]]

        if clasificador == 'min_distancia':
            # Inicializar y entrenar el clasificador de mínima distancia
            min_distance_classifier = MinDistanceClassifier(distance_metric=distance_metric)
            min_distance_classifier.fit(X_train, y_train)
            # Realizar predicciones en el conjunto de prueba
            y_pred = min_distance_classifier.predict(X_test)
        elif clasificador == 'knn':
            # Inicializar y entrenar el clasificador k-NN
            knn_classifier = KNNClassifier(kn)
            knn_classifier.fit(X_train, y_train)
            # Realizar predicciones en el conjunto de prueba
            y_pred = knn_classifier.predict(X_test)

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


def validacion_bootstrap(X, y, n_iterations=100, size=0.8, test_size=0.2, distance_metric='euclidean', clasificador='min_distancia', kn=1):
    totalEf = []
    totalErr = []

    for i in range(n_iterations):
        # Muestreo Bootstrap
        X_bootstrap, y_bootstrap = resample(X, y, replace=True, n_samples=int(len(X) * size))

        # División en conjunto de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X_bootstrap, y_bootstrap, test_size=test_size,
                                                            random_state=42, stratify=y_bootstrap)

        if clasificador == 'min_distancia':
            # Inicializar y entrenar el clasificador de mínima distancia
            min_distance_classifier = MinDistanceClassifier(distance_metric=distance_metric)
            min_distance_classifier.fit(X_train, y_train)
            # Realizar predicciones en el conjunto de prueba
            y_pred = min_distance_classifier.predict(X_test)
        elif clasificador == 'knn':
            # Inicializar y entrenar el clasificador k-NN
            knn_classifier = KNNClassifier(kn)
            knn_classifier.fit(X_train, y_train)
            # Realizar predicciones en el conjunto de prueba
            y_pred = knn_classifier.predict(X_test)

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


def imprimir_resumen_atributos(dataframe, base):
    categoricos = base.variables[base.variables['type'] == 'Categorical']
    binarios = base.variables[base.variables['type'] == 'Binary']
    for columna in dataframe.columns[:10]:
        print(f"\nResumen para la columna: {columna}")
        if columna in categoricos['name'].values:
            print(f"Categorías: {dataframe[columna].unique()}")
        elif columna in binarios['name'].values:
            print(f"Binario: {dataframe[columna].unique()}")
        else:
            print(f"Mínimo: {dataframe[columna].min()}")
            print(f"Máximo: {dataframe[columna].max()}")
            print(f"Promedio: {dataframe[columna].mean()}")
            print(f"Desviación Estándar: {dataframe[columna].std()}")


def imprimir_resumen_atributos_por_clases(dataframe, Xdataframe, base, columna_clases):
    categoricos = base.variables[base.variables['type'] == 'Categorical']
    binarios = base.variables[base.variables['type'] == 'Binary']
    clases_unicas = dataframe[columna_clases].unique()

    for clase in clases_unicas:
        print(f"\n  ** Clase: {clase} **")
        subset_por_clase = Xdataframe[dataframe[columna_clases] == clase]
        for columna in Xdataframe.columns:
            print(f"\nResumen para la columna: {columna}")
            if columna in categoricos['name'].values:
                print(f"Categorías: {subset_por_clase[columna].unique()}")
            elif columna in binarios['name'].values:
                print(f"Binario: {dataframe[columna].unique()}")
            else:
                print(f"Mínimo: {subset_por_clase[columna].min()}")
                print(f"Máximo: {subset_por_clase[columna].max()}")
                print(f"Promedio: {subset_por_clase[columna].mean()}")
                print(f"Desviación Estándar: {subset_por_clase[columna].std()}")


def detectar_valores_faltantes(dataframe):
    # Conjunto de tuplas (Renglon, Columna) en donde faltan los valores
    valores_faltantes = dataframe.isnull().stack()
    tuplas_faltantes = valores_faltantes[valores_faltantes].index.tolist()
    return tuplas_faltantes


def reemplazar_valores_faltantes_con_media(dataframe):
    # Calcular la media de cada columna
    medias = dataframe.mean()
    # Reemplazar valores faltantes con la media de la columna correspondiente
    dataframe_sin_nulos = dataframe.fillna(medias)
    return dataframe_sin_nulos


def normalizar_dataframe(dataframe):
    if all(dataframe[col].dtype == bool for col in dataframe.columns):
        dataframe_normalizado = dataframe.astype(float)
    else:
        # Guardar los nombres de las columnas y sus valores originales
        columnas = dataframe.columns
        valores_originales = dataframe.values
        # Normalizar usando la fórmula min-max
        valores_normalizados = (valores_originales - valores_originales.min(axis=0)) / (
                    valores_originales.max(axis=0) - valores_originales.min(axis=0))
        # Crear un nuevo DataFrame con los valores normalizados
        dataframe_normalizado = pd.DataFrame(valores_normalizados, columns=columnas)

    return dataframe_normalizado


def one_hot_encoding(Xdataframe, base):
    categoricos = base.variables[base.variables['type'] == 'Categorical']

    valores_filtrados = [valor for valor in categoricos.name if valor in Xdataframe.columns]
    # Aplicar One-Hot Encoding
    df_encoded = pd.get_dummies(Xdataframe, columns=valores_filtrados, drop_first=True)

    return df_encoded


def obtener_dos_atributos_menos_significativos(X, y):
    # Inicializar SelectKBest
    selector = SelectKBest(score_func=f_classif, k='all')
    # Aplicar SelectKBest a las características y etiquetas
    selector.fit(X, y)
    # Obtener los nombres de las características
    nombres_caracteristicas = X.columns
    # Obtener los puntajes de las características
    puntajes_caracteristicas = selector.scores_
    print("\t- Puntajes SelectKBest:")
    print(puntajes_caracteristicas)
    # Crear un diccionario de nombres y puntajes de características
    diccionario_puntajes = dict(zip(nombres_caracteristicas, puntajes_caracteristicas))
    # Ordenar el diccionario por puntajes y obtener los dos atributos con los puntajes más bajos
    dos_menos_significativos = sorted(diccionario_puntajes.items(), key=lambda x: x[1])[:2]
    # Obtener los nombres de los dos atributos menos significativos
    nombres, calificaciones = zip(*dos_menos_significativos)

    dataframe_nuevo = X.drop(columns=nombres[1])
    dataframe_nuevo = dataframe_nuevo.drop(columns=nombres[0])
    dataframe_nuevo1 = X.drop(columns=nombres[1])
    dataframe_nuevo2 = X.drop(columns=nombres[0])

    print(f" - Atributos a eliminar : {nombres}")

    return dataframe_nuevo, dataframe_nuevo1, dataframe_nuevo2


def preprocesar_y_balancear(dataframe, base, columna_clase, umbral=1.5):
    continuos = base.variables[base.variables['type'] == 'Continuous']

    # Eliminar filas con valores faltantes
    dataframe = dataframe.dropna()
    indices_atipicos = []
    # Eliminar valores a tipicos
    for atributo in continuos.name:
        # Calcular el primer y tercer cuartil para la clase
        primer_cuartil = dataframe[atributo].quantile(0.25)
        tercer_cuartil = dataframe[atributo].quantile(0.75)

        # Calcular el rango intercuartílico (IQR) para la clase
        iqr = tercer_cuartil - primer_cuartil

        # Calcular los límites para identificar valores atípicos
        limite_inferior = primer_cuartil - umbral * iqr
        limite_superior = tercer_cuartil + umbral * iqr

        # Encontrar índices de filas con valores atípicos para la clase y atributo
        indices_atipicos = dataframe[
            (dataframe[atributo] < limite_inferior) | (dataframe[atributo] > limite_superior)].index
    print(" - Filas con valores atipicos: ")
    print(indices_atipicos)
    dataframe = dataframe.drop(indices_atipicos)

    # Obtener clases únicas y contar el número mínimo de registros por clase
    clases_unicas = dataframe[columna_clase].unique()
    min_registros_clase = dataframe[columna_clase].value_counts().min()
    # Balancear los datos para cada clase
    dataframes_balanceados = []
    for clase in clases_unicas:
        # Filtrar filas por clase
        df_clase = dataframe[dataframe[columna_clase] == clase]
        # Resample para igualar el número de registros por clase
        df_clase_balanceado = resample(df_clase, n_samples=min_registros_clase, random_state=42)
        # Agregar el DataFrame balanceado a la lista
        dataframes_balanceados.append(df_clase_balanceado)

    # Concatenar los DataFrames balanceados
    dataframe_balanceado = pd.concat(dataframes_balanceados)

    return dataframe_balanceado



#Se inicia el programa y se elige si usar un dato por default o buscar por id
entrada1 = int(input("Desea :\n (0)Usar datos predeterminados\n (1)Ingresar un id de la pagina 'UC Irvine'\n :"))
if entrada1 == 0:
    entrada = int(input("\nDatos disponibles : \n (0)Glass Identification\n (1)Congressional voting\n (2)Heart disease\n :"))
    if entrada == 0:
        id = 42
    elif entrada == 1:
        id = 105
    elif entrada == 2:
        id = 45
elif entrada1 == 1:
    id = int(input("\nIngrese el id de la base de datos :"))
base = fetch_ucirepo(id=id)
#Se obtienen los datos, los features y los tragets
datos = base.data.original

features = base.data.features
targets = base.data.targets

# Imprimir el DataFrame original
print("\n - DataFrame original:")
#Se imprimen todos los datos
print(datos)
# print(tabulate(datos, headers = 'keys', tablefmt = 'psql'))

#Separa en categorias los datos en categorycal, binario y otros
#En caso de se categorical, se imprimiran sus posibles categorias
#En caso de ser otros se imprimira el valor minimo, el maximo, su promedio y su desviacion estandar
imprimir_resumen_atributos(datos, base)

#Verifica que valores tienen campos faltantes y que linea estan (Ejemplo (Linea 47, datos faltante: 'Peso'))
tuplas_faltantes = detectar_valores_faltantes(datos)

print("\nTuplas con valores faltantes:")
for tupla in tuplas_faltantes:
    print(tupla)

#Imprime todas las columnas que tiene la base
columnas_disponibles = features.columns
print("\nColumnas disponibles: ", columnas_disponibles)

#En caso de que el usuario seleccione la opción 1 la data se obtendran de los features
#Caso contrario se obtendran unicamente las columnas ingresadas por el usuario y estas tienen que entrar separadas por ,
# Vector de entrada
print("\n  ** Columnas para el vector de entrada **")
colum = int(input("Desea:\n (1)Usar todas las columnas \n (2)Seleccionar algunas columnas\n: "))
if colum == 2:
    Xcolumnas_a_seleccionar = input("Ingrese las columnas que desea seleccionar (separadas por comas): ").split(',')
    Xcolumnas_a_seleccionar = [columna.strip() for columna in Xcolumnas_a_seleccionar]

    # Verificar si las columnas ingresadas existen en el DataFrame
    columnas_invalidas = [columna for columna in Xcolumnas_a_seleccionar if columna not in columnas_disponibles]

    if columnas_invalidas:
        print(f"\nError: Las siguientes columnas no son validas: {', '.join(columnas_invalidas)}")
    else:
        Xdata = seleccionar_columnas(datos, Xcolumnas_a_seleccionar)

elif colum == 1:
    Xdata = features

#Imprime el nuevo vector de entrada segun lo que haya ingresado el usuario anteriormente
print("\nNuevo DataFrame con Vector de Entrada:")
print(Xdata)

# Prepocesamiento
#0 es u no
#1 es un si para realizar one-hot encoding
#Un One-hot encoding se refiere a ver cuantas categorias hay en una columna y separarlos
#Ejemplo:
#Columna sexo tiene femenino y masculino ->  sexo1, sexo2 (sexo 1 tomara valor
# verdadero si es femenino y sexo 2 tomara valor falso)
encoding = int(input("Desea realizar One-hot encoding para atributos categoricos? 0/1 : "))
if encoding == 1:
    Xdata = one_hot_encoding(Xdata, base)
    print("\n - DataFrame con One-hot encoding:")
    print(Xdata)

#0 es no
#1 rellenra los valores faltantes con la media de cada columna,
# en caso de ser categoricos, tambien sacará el promedio de estos igual
if bool(tuplas_faltantes):
    faltantes = int(input("Desea rellenar los datos faltantes? 0/1 : "))
    if faltantes == 1:
        Xdata = reemplazar_valores_faltantes_con_media(Xdata)
        print("\n - DataFrame sin valores faltantes:")
        print(Xdata)
#0 es no
#1 normalizará los valores con:
#Con la siguiente formula (valor - valor minimo)/(valor maximo - valor minimo)
#Es para poner en porcentaje cada valor
normal = int(input("Desea normalizar los valores? 0/1 : "))
if normal == 1:
    Xdata = normalizar_dataframe(Xdata)
    print("\n - DataFrame Normalizado:")
    print(Xdata)

X = Xdata.values

# Vector de salida
#Se observan las columnas que contiene targets
columnas_disponibles = targets.columns
print("\nColumnas disponibles: ", columnas_disponibles)
print("\n  ** Columnas para el vector de salida **")
columnas_a_seleccionar = input("Ingrese las columnas que desea seleccionar (separadas por comas): ").split(',')
columnas_a_seleccionar = [columna.strip() for columna in columnas_a_seleccionar]

# Verificar si las columnas ingresadas existen en el DataFrame
columnas_invalidas = [columna for columna in columnas_a_seleccionar if columna not in columnas_disponibles]
yclase = datos[columnas_a_seleccionar].copy()
if columnas_invalidas:
    print(f"\nError: Las siguientes columnas no son validas: {', '.join(columnas_invalidas)}")
else:
    yclase = seleccionar_columnas(datos, columnas_a_seleccionar)
    print("\nNuevo DataFrame con Vector de Salida:")
    print(yclase)
#Yclase son las columnas seleccionadas del dataframe

    #Se inicia ciclo
    for columna in columnas_a_seleccionar:
        yclase = seleccionar_columnas(datos, [columna])
        print(f"\nSalida con la columna seleccionada '{columna}':")
        print(yclase)
        # imprimir_resumen_atributos_por_clases(datos, Xdata, base, columna)
        #Convierte los datos de columnas a un arreglo
        y = yclase.iloc[:, -1].values

        percent = int(input("\n\t- Minima Distancia -\n \t *** Train and test ***\nIngrese el porcentaje de datos a ser testeados (%): "))
        percent = percent / 100

        # Dividir el conjunto de datos en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=percent, random_state=42, stratify=y)
        #X_train son los datos en x elegidos para entrenar
        #X_test son los datos en x elegidos para ser puestos a prueba
        #Y_train son los datos en y elegidos para entrenar
        #Y_test son los datos en y elegidos para poner a prueba
        # Inicializar y entrenar el clasificador de mínima distancia
        min_distance_classifier = MinDistanceClassifier()
        min_distance_classifier.fit(X_train, y_train)

        # Realizar predicciones en el conjunto de prueba
        y_pred = min_distance_classifier.predict(X_test)

        print("\n\t\t - Predicciones finales -\n")
        #Se compararan los datos del test con la predicción y se mostrarán los resultados
        #Su eficiencia y sus errores
        eficiencia, error = calcular_eficiencia_y_error(y_pred, y_test)

        print(f"Porcentaje de Eficiencia: {eficiencia:.2f}%")
        print(f"Porcentaje de Error: {error:.2f}%")

#####################################################################################################################
        k = int(input("\n \t *** Validacion cruzada kfold ***\nIngrese el valor de k : "))
        #Al llamar este metodo sin establecer knn, se realizara por distancia minima y este se repetira k veces
        validacion_cruzada_kfold(X, y, k)

#####################################################################################################################
        kbt = int(input("\n \t *** Validacion Bootstrap ***\nIngrese el numero de experimentos (k) : "))
        tamaño = int(input("\nIngrese el tamaño de los subconjuntos bootstrap(%) :"))
        tamaño = tamaño / 100
        testbt = int(input("\nIngrese el porcentaje de prueba de cada subconjunto(%) :"))
        testbt = testbt / 100
        validacion_bootstrap(X, y, kbt, tamaño, testbt)

        kn = int(input("\n\t- KNN -\nIngrese el valor de k: "))
        print("\n \t *** Train and test ***")
        # Dividir el conjunto de datos en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=percent, random_state=42, stratify=y)

        # Inicializar y entrenar el clasificador k-NN
        knn_classifier = KNNClassifier(kn)
        knn_classifier.fit(X_train, y_train)

        # Realizar predicciones en el conjunto de prueba
        y_pred = knn_classifier.predict(X_test)

        print("\n\t\t - Predicciones finales -\n")
        eficiencia, error = calcular_eficiencia_y_error(y_pred, y_test)

        print(f"Porcentaje de Eficiencia: {eficiencia:.2f}%")
        print(f"Porcentaje de Error: {error:.2f}%")

#####################################################################################################################
        print("\n \t *** Validacion cruzada kfold ***\n")
        validacion_cruzada_kfold(X, y, k, clasificador='knn', kn=kn)

#####################################################################################################################
        print("\n \t *** Validacion Bootstrap ***\n")
        validacion_bootstrap(X, y, kbt, tamaño, testbt, clasificador='knn', kn=kn)

        # Punto 6. Se eliminan atributos
        print("\n\t *** Eliminacion de Atributos ***")
        Xdata_nuevo, Xdata_nuevo1, Xdata_nuevo2 = obtener_dos_atributos_menos_significativos(Xdata, yclase)
        print("\n \t *************** DataFrame con SelecKBest (Se elimino un atributo) ***************\n")
        print(Xdata_nuevo1)
        X = Xdata_nuevo1.values

        print("\n \t *** Train and test ***")
        # Dividir el conjunto de datos en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=percent, random_state=42, stratify=y)

        min_distance_classifier = MinDistanceClassifier()
        min_distance_classifier.fit(X_train, y_train)
        # Realizar predicciones en el conjunto de prueba
        y_pred = min_distance_classifier.predict(X_test)

        print("\n\t\t - Predicciones finales -\n")
        eficiencia, error = calcular_eficiencia_y_error(y_pred, y_test)
        print(f"Porcentaje de Eficiencia: {eficiencia:.2f}%")
        print(f"Porcentaje de Error: {error:.2f}%")

#####################################################################################################################
        print("\n \t *** Validacion cruzada kfold ***\n")
        validacion_cruzada_kfold(X, y, k)

#####################################################################################################################
        print("\n \t *** Validacion Bootstrap ***\n")
        validacion_bootstrap(X, y, kbt, tamaño, testbt)

        print("\n \t *************** DataFrame con SelecKBest (Se elimino un atributo) ***************\n")
        print(Xdata_nuevo2)
        X = Xdata_nuevo2.values

        print("\n \t *** Train and test ***")
        # Dividir el conjunto de datos en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=percent, random_state=42, stratify=y)

        min_distance_classifier = MinDistanceClassifier()
        min_distance_classifier.fit(X_train, y_train)
        # Realizar predicciones en el conjunto de prueba
        y_pred = min_distance_classifier.predict(X_test)

        print("\n\t\t - Predicciones finales -\n")
        eficiencia, error = calcular_eficiencia_y_error(y_pred, y_test)
        print(f"Porcentaje de Eficiencia: {eficiencia:.2f}%")
        print(f"Porcentaje de Error: {error:.2f}%")

#####################################################################################################################
        print("\n \t *** Validacion cruzada kfold ***\n")
        validacion_cruzada_kfold(X, y, k)

#####################################################################################################################
        print("\n \t *** Validacion Bootstrap ***\n")
        validacion_bootstrap(X, y, kbt, tamaño, testbt)

        print("\n \t *************** DataFrame con SelecKBest (Se eliminaron dos atributo) ***************\n")
        print(Xdata_nuevo)
        X = Xdata_nuevo.values

        print("\n \t *** Train and test ***")
        # Dividir el conjunto de datos en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=percent, random_state=42, stratify=y)

        min_distance_classifier = MinDistanceClassifier()
        min_distance_classifier.fit(X_train, y_train)
        # Realizar predicciones en el conjunto de prueba
        y_pred = min_distance_classifier.predict(X_test)

        print("\n\t\t - Predicciones finales -\n")
        eficiencia, error = calcular_eficiencia_y_error(y_pred, y_test)
        print(f"Porcentaje de Eficiencia: {eficiencia:.2f}%")
        print(f"Porcentaje de Error: {error:.2f}%")

#####################################################################################################################
        print("\n \t *** Validacion cruzada kfold ***\n")
        validacion_cruzada_kfold(X, y, k)

#####################################################################################################################
        print("\n \t *** Validacion Bootstrap ***\n")
        validacion_bootstrap(X, y, kbt, tamaño, testbt)

        # Punto 7
        print("\n \t *** Eliminacion de filas ***")
        datos_balanceado = preprocesar_y_balancear(datos, base, columna)
        # Imprime el nuevo DataFrame preprocesado y balanceado
        print("Nuevo DataFrame:")
        print(datos_balanceado)

        if colum == 1:
            Xdata_balanceado = datos_balanceado.drop(columns=[columna])
        elif colum == 2:
            Xdata_balanceado = seleccionar_columnas(datos_balanceado, Xcolumnas_a_seleccionar)
        yclase_balanceado = seleccionar_columnas(datos_balanceado, [columna])

        if encoding == 1:
            Xdata_balanceado = one_hot_encoding(Xdata_balanceado, base)
            print("\n - DataFrame con One-hot encoding:")
            print(Xdata_balanceado)

        if normal == 1:
            Xdata_balanceado = normalizar_dataframe(Xdata_balanceado)
            print("\n - DataFrame Normalizado:")
            print(Xdata_balanceado)

        X = Xdata_balanceado.values
        y = yclase_balanceado.iloc[:, -1].values

        print("\n \t *** Train and test ***")
        # Dividir el conjunto de datos en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=percent, random_state=42, stratify=y)

        min_distance_classifier = MinDistanceClassifier()
        min_distance_classifier.fit(X_train, y_train)
        # Realizar predicciones en el conjunto de prueba
        y_pred = min_distance_classifier.predict(X_test)

        print("\n\t\t - Predicciones finales -\n")
        eficiencia, error = calcular_eficiencia_y_error(y_pred, y_test)
        print(f"Porcentaje de Eficiencia: {eficiencia:.2f}%")
        print(f"Porcentaje de Error: {error:.2f}%")

#####################################################################################################################
        print("\n \t *** Validacion cruzada kfold ***\n")
        validacion_cruzada_kfold(X, y, k)

#####################################################################################################################
        print("\n \t *** Validacion Bootstrap ***\n")
        validacion_bootstrap(X, y, kbt, tamaño, testbt)
