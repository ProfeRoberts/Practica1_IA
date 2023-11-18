import numpy as np

def obt_mapa(texto, delim):
    archivo = open(texto)
    temp = []
    matriz = []
    for line in archivo:
        line = line.rstrip()
        line += ','
        numero = ""
        for x in line:
            if x.find(delim):
                numero += str(x)
            else:
                temp.append(numero)
                numero = ""
        matriz.append(temp)
        temp = []
    return np.array(matriz)

entrada = int(input("¿Cual info desea cargar? : \n(0)Laberinto\n(1)Testo\n :"))

delim = input("Ingrese el separador de atributos :")

if entrada == 0:
    data = obt_mapa('laberinto.txt', delim)
elif entrada == 1:
    data = obt_mapa('testo.txt', delim)

print("\nNumero de atributos (Columnas): " + str(data.shape[1]) + "\nNumero de patrones (renglones): " + str(data.shape[0]))
print(data)

opc = int(input("Desea seleccionar: \n(1)Columnas\n(2)Renglones\n :"))
selector = 0
nueva = []
while selector != -1:
    selector = int(input("\nSi desea dejar de seleccionar ingrese -1\nIngrese el indice :"))
    if opc == 1 and selector != -1:
        print([fila[selector] for fila in data])
        nueva.append([fila[selector] for fila in data])
    elif opc == 2 and selector != -1:
        print(data[selector])
        nueva.append(data[selector])

nueva = str(np.array(nueva))
print(nueva)

file = open("sample.txt", "w+")
nueva = nueva.replace("' '", ",")
nueva = nueva.replace("[['", "")
nueva = nueva.replace("']]", ",")
nueva = nueva.replace(" ['", "")
nueva = nueva.replace("']", ",")
nueva = nueva.replace("'\n  '", ",")
print(nueva)
file.write(nueva)
file.close()