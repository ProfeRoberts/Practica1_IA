import numpy as np
import pandas as pd
from ucimlrepo import fetch_ucirepo


def encontrar_atipicos_por_clase(dataframe, clase, umbral=1.5):
    if clase not in dataframe.columns:
        raise ValueError(f"La columna '{clase}' no existe en el DataFrame.")

    # Obtener atributos excluyendo la columna de clase
    atributos = dataframe.columns.difference([clase])

    # Inicializar el diccionario de índices atípicos por atributo y clase
    indices_atipicos_por_atributo = {atributo: {} for atributo in atributos}

    for atributo in atributos:
        for c in dataframe[clase].unique():
            # Filtrar el DataFrame por clase
            subconjunto = dataframe[dataframe[clase] == c]

            # Calcular el primer y tercer cuartil para la clase
            primer_cuartil = subconjunto[atributo].quantile(0.25)
            tercer_cuartil = subconjunto[atributo].quantile(0.75)

            # Calcular el rango intercuartílico (IQR) para la clase
            iqr = tercer_cuartil - primer_cuartil

            print(f"\n ** {c}, {atributo} **")
            # Calcular los límites para identificar valores atípicos
            limite_inferior = primer_cuartil - umbral * iqr
            print(f"Limite inferior: {limite_inferior}")
            limite_superior = tercer_cuartil + umbral * iqr
            print(f"Limite superior: {limite_superior}")

            # Encontrar índices de filas con valores atípicos para la clase y atributo
            indices_atipicos = subconjunto[(subconjunto[atributo] < limite_inferior) | (subconjunto[atributo] > limite_superior)].index

            # Agregar los índices al diccionario por clase y atributo
            indices_atipicos_por_atributo[atributo][c] = indices_atipicos.tolist()

    return indices_atipicos_por_atributo


def normalizar_dataframe(dataframe):
    # Guardar los nombres de las columnas y sus valores originales
    columnas = dataframe.columns
    valores_originales = dataframe.values

    # Normalizar usando la fórmula min-max
    valores_normalizados = (valores_originales - valores_originales.min(axis=0)) / (
                valores_originales.max(axis=0) - valores_originales.min(axis=0))

    # Crear un nuevo DataFrame con los valores normalizados
    dataframe_normalizado = pd.DataFrame(valores_normalizados, columns=columnas)

    return dataframe_normalizado


def contar_clases_y_porcentaje(dataframe, columna_clases):
    # Contar el número de ocurrencias de cada clase
    conteo_clases = dataframe[columna_clases].value_counts()

    # Calcular el porcentaje que cada clase ocupa en el DataFrame
    porcentaje_clases = (conteo_clases / len(dataframe)) * 100

    # Crear un nuevo DataFrame con la información
    resumen_clases = pd.DataFrame({
        'Clase': conteo_clases.index,
        'Cantidad': conteo_clases.values,
        'Porcentaje(%)': porcentaje_clases.values
    })

    return resumen_clases


# Función para detectar y reportar valores faltantes
def detectar_valores_faltantes(dataframe, clase_col):
    # a. Conjunto de tuplas (Renglon, Columna) en donde faltan los valores
    valores_faltantes = dataframe.isnull().stack()
    tuplas_faltantes = valores_faltantes[valores_faltantes].index.tolist()

    # b. Cantidad y Porcentaje de valores faltantes por Atributo y por atributo-Clase
    for columna in dataframe.columns:
        total_faltantes = dataframe[columna].isnull().sum()
        porcentaje_faltantes = (total_faltantes / len(dataframe)) * 100
        print(f"{columna}: {total_faltantes} faltan ({porcentaje_faltantes:.2f}%)")

        if clase_col in dataframe.columns:
            for clase in dataframe[clase_col].unique():
                total_faltantes_clase = dataframe[dataframe[clase_col] == clase][columna].isnull().sum()
                porcentaje_faltantes_clase = (total_faltantes_clase / len(dataframe[dataframe[clase_col] == clase])) * 100
                print(f"  {clase}: {total_faltantes_clase} faltan ({porcentaje_faltantes_clase:.2f}%)")

    return tuplas_faltantes


def eliminar_filas_columnas(dataframe, filas=None, columnas=None):
    if filas is not None:
        dataframe = dataframe.drop(filas, axis=0)

    if columnas is not None:
        dataframe = dataframe.drop(columnas, axis=1)

    return dataframe


def calcular_estadisticas_por_clase(data, clase_col):
    X = data.values
    y = clase_col.iloc[:, -1].values
    # Obtener las clases únicas en la columna de etiquetas
    clases_unicas = np.unique(y)
    # Inicializar listas para almacenar los resultados
    promedios_por_clase = []
    desviaciones_por_clase = []
    for clase in clases_unicas:
        # Filtrar el DataFrame por clase
        df_clase = X[y == clase]
        promedio = np.mean(df_clase, axis=0)
        desviacion = np.std(df_clase, axis=0)
        promedios_por_clase.append(promedio)
        desviaciones_por_clase.append(desviacion)

    # Concatenar los resultados en un DataFrame final
    return promedios_por_clase, desviaciones_por_clase, clases_unicas


entrada1 = int(input("Desea : \n (0)Usar un archivo .csv\n (1)Ingresar un id de la pagina 'UC Irvine'\n :"))
if entrada1 == 0:
    entrada = int(input("\nDesea : \n (0)Usar iris.csv\n (1)Ingresar otro csv\n :"))
    if entrada == 0:
        ruta_archivo = "iris.csv"
    elif entrada == 1:
        ruta_archivo = input("\nIngrese el nombre del archivo: ")
    # Lee el conjunto de datos desde un archivo CSV
    datos = pd.read_csv(ruta_archivo)

    clase = input("\nIngrese el nombre de la columna de clases: ")

    Xdata = datos.copy()
    Xdata.drop(clase, axis=1, inplace=True)

    yclase = datos[[clase]].copy()

elif entrada1 == 1:
    id = int(input("\nIngrese el id de la base de datos :"))
    base = fetch_ucirepo(id=id)
    datos = base.data.original
    Xdata = base.data.features
    yclase = base.data.targets
    clase = "class"

# Imprimir el DataFrame original
print("\n - DataFrame original:")
print(datos)

conteo = contar_clases_y_porcentaje(datos, clase)
print(conteo)


df_normalizado = normalizar_dataframe(Xdata)
print("\nDataFrame Normalizado:")
print(df_normalizado)

# Calcular estadísticas por clase
promedios_por_clase, desviaciones_por_clase, clases_unicas = calcular_estadisticas_por_clase(Xdata, yclase)

print("\nPromedios por clase: ")
indice = 0
for fila in promedios_por_clase:
    print(f"{clases_unicas[indice]} : ")
    for elemento in fila:
        print("{:.2f}".format(elemento), end="\t")
    print("")
    indice += 1
print("\nDesviacion por clase: ")
indice = 0
for fila in desviaciones_por_clase:
    print(f"{clases_unicas[indice]} : ")
    for elemento in fila:
        print("{:.2f}".format(elemento), end="\t")
    print("")
    indice += 1

valores_atipicos = encontrar_atipicos_por_clase(datos, clase)
print(" *** Valores Atípicos ***")
print(valores_atipicos)

Xdata.iat[0, 0] = 10

datos.iat[0, 0] = None
datos.iat[1, 1] = None
print(datos)

tuplas_faltantes = detectar_valores_faltantes(datos, clase)

print("\nTuplas con valores faltantes:")
for tupla in tuplas_faltantes:
    print(tupla)

ciclo = 1
while ciclo != 0:
    ciclo = int(input("\nDesea : \n (0) Salir\n (1) Eliminar una fila\n (2) Eliminar una columna\n :"))
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