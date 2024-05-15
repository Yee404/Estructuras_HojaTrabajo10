

import numpy as np

# Leer archivo .txt
def LeerArchivo(nombreArchivo):
    grafo = {'vertices': set()}
    with open(nombreArchivo, 'r') as file:
        for linea in file:
            datos = linea.split()
            ciudad1, ciudad2 = datos[0], datos[1]
            tiempoNormal, tiempoLluvia, tiempoNieve, tiempoTormenta = map(int, datos[2:])
            AgregarVertice(grafo, ciudad1)
            AgregarVertice(grafo, ciudad2)
            AgregarArco(grafo, ciudad1, ciudad2, tiempoNormal, tiempoLluvia, tiempoNieve, tiempoTormenta)
    return grafo


def AgregarVertice(grafo, vertice):
    grafo['vertices'].add(vertice)

def AgregarArco(grafo, origen, destino, tiempoNormal, tiempoLluvia, tiempoNieve, tiempoTormenta):
    if 'MatrizADY' not in grafo:
        n = len(grafo['vertices'])
        grafo['MatrizADY'] = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            grafo['MatrizADY'][i][i] = 0
        
    idxOrigen = list(grafo['vertices']).index(origen)
    idxDestino = list(grafo['vertices']).index(destino)
    
    grafo['MatrizADY'][idxOrigen][idxDestino] = tiempoNormal
    grafo['MatrizADY'][idxDestino][idxOrigen] = tiempoNormal

def CalcularFloyd(grafo):
    n = len(grafo['MatrizADY'])
    A = np.array(grafo['MatrizADY'])
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if A[i][j] > A[i][k] + A[k][j]:
                    A[i][j] = A[i][k] + A[k][j]
    grafo['MatrizADY'] = A.tolist()

def InterrupcionTrafico(grafo, ciudad1, ciudad2):
    if ciudad1 not in grafo['vertices'] or ciudad2 not in grafo['vertices']:
        print("Alguna ciudad no se encuentra en el grafo")
        return

    idxOrigen = list(grafo['vertices']).index(ciudad1)
    idxDestino = list(grafo['vertices']).index(ciudad2)

    grafo['MatrizADY'][idxOrigen][idxDestino] = float('inf')
    grafo['MatrizADY'][idxDestino][idxOrigen] = float('inf')

def cambiarClima(grafo, ciudad1, ciudad2, clima):
    if ciudad1 not in grafo['vertices'] or ciudad2 not in grafo['vertices']:
        print("Alguna ciudad no se encuentra en el grafo.")
        return

    idxOrigen = list(grafo['vertices']).index(ciudad1)
    idxDestino = list(grafo['vertices']).index(ciudad2)

    if clima == 'lluvia':
        grafo['MatrizADY'][idxOrigen][idxDestino] = tiempoLluvia
        grafo['MatrizADY'][idxDestino][idxOrigen] = tiempoLluvia
    elif clima == 'nieve':
        grafo['MatrizADY'][idxOrigen][idxDestino] = tiempoNieve
        grafo['MatrizADY'][idxDestino][idxOrigen] = tiempoNieve
    elif clima == 'tormenta':
        grafo['MatrizADY'][idxOrigen][idxDestino] = tiempoTormenta
        grafo['MatrizADY'][idxDestino][idxOrigen] = tiempoTormenta
    elif clima == 'normal':
        # para el tiempo normal, se vuelve calcular Floyd
        CalcularFloyd(grafo)
    else:
        print("El clima que ha ingresado es inválido")


