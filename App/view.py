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
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


# ==============================
# Menu de opciones
# ==============================

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar las tendencias por pais y categoria")
    print("3- Consultar el video mas trending por país")
    print("4- Consultar el video mas trending por categoria")
    print("5- Pendiente")


# ==============================
# Funciones de inicializacion
# ==============================

def initCatalog():
    """
        Inicializa el catalogo de libros
    """
    return controller.initCatalog()


def loadData(catalog):
    """
        Carga los libros en el catalogo
    """
    time = controller.loadData(catalog)

    return time


def printNVideosCat(catalog, size):
    video = catalog['elements']
    print("\nLos primeros", str(size), "videos ordenados son: ")
    i = 0
    while i < size:
        print('\nVideo:', i + 1)
        print('\n\tTrending date: [', video[i]['trending_date'],
              ']\n\tTitle: [', video[i]['title'],
              ']\n\tChannel title: [', video[i]['channel_title'],
              ']\n\tPublish time: [', video[i]['publish_time'],
              ']\n\tViews: [', video[i]['views'],
              ']\n\tLikes: [', video[i]['likes'],
              ']\n\tDislikes: [', video[i]['dislikes'],
              ']')
        i += 1


def printMostTrendingVideoByCountry(video, days):
    print("\nEl video con mas dias en tendencia de la catgoria es: ")
    print('\n\tTitle: [', video[0],
          ']\n\tChannel title: [', video[1],
          ']\n\tCountry: [', video[2],
          ']\n\tDays: [', len(days),
          ']')


def printMostTrendingVideoByCategory(video, days):
    print("\nEl video con mas dias en tendencia de la catgoria es: ")
    print('\n\tTitle: [', video[0],
          ']\n\tChannel title: [', video[1],
          ']\n\tCategory Id: [', video[2],
          ']\n\tDays: [', len(days),
          ']')


def printMostLikedCountryTag(catalog, size):
    video = catalog['elements']
    print("\nLos primeros", str(size), "videos ordenados son: ")
    i = 0
    while i < size:
        print('\nVideo:', i + 1)
        print('\n\tTitle: [', video[i]['title'],
              ']\n\tChannel title: [', video[i]['channel_title'],
              ']\n\tPublish time: [', video[i]['publish_time'],
              ']\n\tViews: [', video[i]['views'],
              ']\n\tLikes: [', video[i]['likes'],
              ']\n\tDislikes: [', video[i]['dislikes'],
              ']\n\tTags: [', video[i]['tags'],
              ']\n')
        i += 1


# ==============================
# Menu principal
# ==============================

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        print("Inicializando Catálogo ....")
        # Inicia el catalogo y carga la informacion en el
        catalog = initCatalog()
        time = loadData(catalog)
        # Imprime la cantidad de videos cargados
        print('Videos cargados: ' + str(controller.videosSize(catalog['videos']
                                                              )))
        # Imprime el tiempo y memoria consumida en el proceso
        print("Tiempo [ms]: ", f"{time[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{time[1]:.3f}")

    elif int(inputs[0]) == 2:
        # Recibe la categoria y la cantidad de videos que el usuario desea ver
        country = input("Ingrese el pais que desea consultar:\n").lower()
        category = input("Ingrese la categoria que desea consultar:\n").lower()
        size = int(input("Ingrese la cantidad de videos que desea ver:\n"))

        if size < 1:
            print("El numero ingresado es mucho menor a lo esperado,",
                  " trate con uno mayor")
            break

        elif size > controller.videosSize(catalog['videos']):
            print("El numero es demasiado grande trate con uno menor")
            break
        # Si los parametros son correctos el programa procede con la busqueda
        result = controller.getVideosCat(catalog, category, country)
        if result == 1:
            print('\n# ======================================================')
            print('No se encontraron videos en el pais y categoria deseados')
            print('# ======================================================\n')
        else:
            print("Cargando información de los archivos ....")
            printNVideosCat(result[0], size)

        # Imprime el tiempo y memoria consumida en el proceso
        print("Tiempo [ms]: ", f"{result[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{result[2]:.3f}")

    elif int(inputs[0]) == 3:
        # Recibe la categoria y la cantidad de videos que el usuario desea ver
        country = input("Ingrese el pais que desea consultar:\n").lower()

        # Si los parametros son correctos el programa procede con la busqueda
        result = controller.mostTrendingVideoCountry(catalog, country)
        if result == 1:
            print('\n# ======================================================')
            print('No se encontraron videos en el pais y categoria deseados')
            print('# ======================================================\n')
        else:
            print("Cargando información de los archivos ....")
            printMostTrendingVideoByCountry(result[0], result[1])

        # Imprime el tiempo y memoria consumida en el proceso
        print("Tiempo [ms]: ", f"{result[2]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{result[3]:.3f}")

    elif int(inputs[0]) == 4:
        # Recibe la categoria y la cantidad de videos que el usuario desea ver
        category = input("Ingrese la categoria que desea consultar:\n").lower()

        # Si los parametros son correctos el programa procede con la busqueda
        result = controller.mostTrendingVideoCat(catalog, category)
        if result[0] == 1 and result[1] == 0:
            print('\n# ======================================================')
            print('No se encontraron videos en el pais y categoria deseados')
            print('# ======================================================\n')
        else:
            print("Cargando información de los archivos ....")
            printMostTrendingVideoByCategory(result[0], result[1])

        # Imprime el tiempo y memoria consumida en el proceso
        print("Tiempo [ms]: ", f"{result[2]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{result[3]:.3f}")

    elif int(inputs[0]) == 5:
        # Recibe la categoria y la cantidad de videos que el usuario desea ver
        country = input("Ingrese el pais que desea consultar:\n").lower()
        tag = input("Ingrese el tag que desea consultar:\n")
        size = int(input("Ingrese la cantidad de videos que desea ver:\n"))

        if size < 1:
            print("El numero ingresado es mucho menor a lo esperado,",
                  " trate con uno mayor")
            break

        elif size > controller.videosSize(catalog['videos']):
            print("El numero es demasiado grande trate con uno menor")
            break
        # Si los parametros son correctos el programa procede con la busqueda
        result = controller.mostLikedVideosCountryTag(catalog, country, tag)
        if result == 1:
            print('\n# ======================================================')
            print('No se encontraron videos en el pais y categoria deseados')
            print('# ======================================================\n')
        else:
            print("Cargando información de los archivos ....")
            printMostLikedCountryTag(result[0], size)

        # Imprime el tiempo y memoria consumida en el proceso
        print("Tiempo [ms]: ", f"{result[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{result[2]:.3f}")

    else:
        sys.exit(0)
sys.exit(0)
