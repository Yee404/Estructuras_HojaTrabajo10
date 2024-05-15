import os
import unittest
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


# OPCION 1
# calcular la ruta más corta entre ciudades ingresadas
def RutaCorta(grafo, ciudadOrigen, ciudadDestino):
    if ciudadOrigen not in grafo['vertices'] or ciudadDestino not in grafo['vertices']:
        print("Alguna ciudad no se encuentra en el grafo.")
        return

    idxOrigen = list(grafo['vertices']).index(ciudadOrigen)
    idxDestino = list(grafo['vertices']).index(ciudadDestino)

    distancia = grafo['MatrizADY'][idxOrigen][idxDestino]
    if distancia == float('inf'):
        print("No existe ruta entre las ciudades")
    else:
        print("Ruta más corta: ", distancia)


# OPCION 2
# ubicar el valor del centro de todo el grafo
def CentroGrafo(grafo):
    excentricidad = [max(fila) for fila in grafo['MatrizADY']]
    minExcent = min(excentricidad)
    indCentro = excentricidad.index(minExcent)
    verticeLista = list(grafo['vertices'])
    return verticeLista[indCentro]


# OPCION 3
# se modifica el grafo según la opcion2 que se seleccione
def ModificarGrafo(grafo, opcion):
    if opcion == 'a':
        ciudad1 = input("Primera ciudad: ")
        ciudad2 = input("Segunda ciudad: ")
        InterrupcionTrafico(grafo, ciudad1, ciudad2)
    elif opcion == 'b':
        ciudad1 = input("Primera ciudad: ")
        ciudad2 = input("Segunda ciudad: ")
        tiempoNormal = int(input("Tiempo (normal) de viaje entre ciudades: "))
        tiempoLluvia = int(input("Tiempo de viaje con (lluvia) entre ciudades: "))
        tiempoNieve = int(input("Tiempo de viaje con (nieve) entre las ciudades: "))
        tiempoTormenta = int(input("Tiempo de viaje con (tormenta) entre las ciudades: "))
        AgregarArco(grafo, ciudad1, ciudad2, tiempoNormal, tiempoLluvia, tiempoNieve, tiempoTormenta)
    elif opcion == 'c':
        ciudad1 = input("Ingrese la primera ciudad: ")
        ciudad2 = input("Ingrese la segunda ciudad: ")
        clima = input("Ingrese el clima (normal, lluvia, nieve o tormenta): ")
        cambiarClima(grafo, ciudad1, ciudad2, clima)
    else:
        print("Opción inválida.")



def MENU():
    print("\nMENÚ")
    print("1. Calcular ruta más corta entre dos ciudades")
    print("2. Indicar el nombre de la ciudad que queda en el centro del grafo.")
    print("3. Modificar el grafo. ")
    print("4. Salir del programa")

def main():
    nombreArchivo = "guategrafo.txt"
    grafo = LeerArchivo(nombreArchivo)
    CalcularFloyd(grafo)
    
    while True:
        MENU()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            ciudadOrigen = input("Ingresar ciudad origen: ")
            ciudadDestino = input("Ingresar ciudad destino: ")
            RutaCorta(grafo, ciudadOrigen, ciudadDestino)
        elif opcion == '2':
            centro = CentroGrafo(grafo)
            print("La ciudad en el centro del grafo es: ", centro)
        elif opcion == '3':
            input("a. Hay interrupción de tráfico entre un par de ciudades")
            input("b. Se establece una conexión entre ciudad1 y ciudad2 (por defecto se usa el climaNormal)")
            input("c. Indicar el clima (normal, lluvia, nieve o tormenta) entre un par de ciudades.")
            opcion2 = input("Ingrese la opción seleccionada para modificar el grafo (a-c): ")
            ModificarGrafo(grafo, opcion2)
        elif opcion == '4':
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()


# PRUEBAS UNITARIAS
class TestLeerArchivo(unittest.TestCase):
    def test_LeerArchivo(self):
        # Crear un archivo de prueba con datos conocidos
        with open("test_archivo.txt", "w") as file:
            file.write("Ciudad1 Ciudad2 10 15 20 50\n")
            file.write("Ciudad2 Ciudad3 15 20 30 70\n")
            file.write("Ciudad3 Ciudad4 20 25 35 80\n")

        # Llamar a la función LeerArchivo para leer el archivo de prueba
        grafo = LeerArchivo("test_archivo.txt")

        # Verificar si la estructura del grafo se ha creado correctamente
        self.assertEqual(grafo['vertices'], {'Ciudad1', 'Ciudad2', 'Ciudad3', 'Ciudad4'})
        self.assertEqual(len(grafo['MatrizADY']), 4)

        # Verificar si la matriz de adyacencia se ha construido correctamente
        expected_matriz = [[0, 10, float('inf'), float('inf')],
                           [10, 0, 15, float('inf')],
                           [float('inf'), 15, 0, 20],
                           [float('inf'), float('inf'), 20, 0]]
        np.testing.assert_array_equal(grafo['MatrizADY'], expected_matriz)

        # Eliminar el archivo de prueba después de usarlo
        os.remove("test_archivo.txt")

class TestFuncionesGrafo(unittest.TestCase):
    def setUp(self):
        # Preparar un grafo de prueba
        self.grafo = {'vertices': {'A', 'B', 'C', 'D'},
                      'MatrizADY': [[0, 3, float('inf'), 7],
                                    [8, 0, 2, float('inf')],
                                    [5, float('inf'), 0, 1],
                                    [2, float('inf'), float('inf'), 0]]}

    def test_AgregarVertice(self):
        # Probar agregar un nuevo vértice al grafo
        AgregarVertice(self.grafo, 'E')
        self.assertIn('E', self.grafo['vertices'])

    def test_AgregarArco(self):
        # Probar agregar un nuevo arco al grafo
        AgregarArco(self.grafo, 'A', 'C', 5, 6, 7, 8)
        self.assertEqual(self.grafo['MatrizADY'][0][2], 5)
        self.assertEqual(self.grafo['MatrizADY'][2][0], 5)

    def test_CalcularFloyd(self):
        # Probar el cálculo de Floyd en el grafo
        CalcularFloyd(self.grafo)
        expected_matriz = [[0, 3, 5, 6],
                           [5, 0, 2, 3],
                           [5, 8, 0, 1],
                           [2, 5, 7, 0]]
        np.testing.assert_array_equal(self.grafo['MatrizADY'], expected_matriz)

    def test_CentroGrafo(self):
        # Probar la función para encontrar el centro del grafo
        centro = CentroGrafo(self.grafo)
        self.assertEqual(centro, 'C')

if __name__ == '__main__':
    unittest.main()