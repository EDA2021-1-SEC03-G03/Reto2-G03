"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# Menu de opciones


def printMenu():
    print("Bienvenido")
    print("1- Inicializar Catálogo")
    print("2- Cargar los n videos con mas likes en una categoria")


# Funciones de inicializacion

def initCatalog():
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog()


def loadData(catalog, catCategory):
    """
    Carga los libros en el catalogo
    """
    time = controller.loadData(catalog, catCategory)

    return time


def printreq1(catalog, size):
    for video in lt.iterator(catalog):
        print('Titulo: ' + video['video'] + 'Likes: ' + video['likes'])


# Menu principal

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        print("Inicializando Catálogo ....")
        catTuple = initCatalog()
        time = loadData(catTuple[0], catTuple[1])
        print('Videos cargados: ' + str(controller.videosSize(catTuple[0],)))
        print("Tiempo [ms]: ", f"{time[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{time[1]:.3f}")
      
    elif int(inputs[0]) == 2:
        category = input("Ingrese la categoria que desea consultar:\n")
        size = int(input("Ingrese la cantidad de videos que desea ver:\n"))
        if size < 1:
            print("El numero ingresado es mucho menor a lo esperado,",
                  " trate con uno mayor")
            break
        elif size > controller.videosSize(catTuple[0]):
            print("El numero es demasiado grande trate con uno menor")
            break
        result = controller.reqNvideos(catTuple[0], category, size)
        newlist = controller.sortVideos(result, size)
        print("Cargando información de los archivos ....")
        printreq1(newlist, size)

    else:
        sys.exit(0)
sys.exit(0)
