"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
"""


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import quicksort as qs
from DISClib.DataStructures import arraylistiterator as ite
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos
listas, una para los videos, otra para las categorias de los mismos.
"""


# ==============================
# Construccion de modelos
# ==============================

def newCatalog():
    '''
    Creamos un catalogo donde se agregara toda
    la informacion de los videos
    '''
    catalog = {'videos': None,
               'category_id': None,
               'category': None,
               'country': None,
               'days': None}
    '''
    Definimos los TAD que cada parte del catalago
    va a tener
    '''
    catalog['videos'] = lt.newList('ARRAY_LIST')

    catalog['category_id'] = mp.newMap(33,
                                       maptype='PROBING',
                                       loadfactor=0.5,
                                       comparefunction=compareCategories)

    catalog["category"] = mp.newMap(33,
                                    maptype='PROBING',
                                    loadfactor=0.5,
                                    comparefunction=compareCategories)

    catalog["country"] = mp.newMap(11,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareCategories)

    return catalog


# ==============================
# Funciones para agregar informacion al catalogo
# ==============================


def addVideoToCat(catalog, video):
    '''
    Esta funcion agrega toda la informacion del archivo
    en una lista de tipo ARRAY_LIST, esta la usamos para
    conocer el size que lo necesitamos en varias funciones
    '''
    lt.addLast(catalog['videos'], video)


def addCategoryInfo(catalog, category):
    '''
    Esta funcion agrega la relacion de las categorias con
    su id en el catalogo en la llave "category_id"
    '''
    mp.put(catalog['category_id'], category['id'], category['name'].lower())


def addVideo(catalog, video):
    '''
        Funcion que agrega la informacion de los videos en
        el catalogo en la llave "category" segun a la categoria
        a la que pertenecen. La llave mencionada es un mapa por
        lo que la categoria va a ser la llave y el valor va a
        ser una lista con todos los videos y su informacion que
        pertenecen a esa categoria
    '''
    categories = catalog['category']
    catName = convertIdtoCat(catalog, video['category_id'])
    present = mp.contains(categories, catName)
    if present:
        entry = mp.get(categories, catName)
        cat = me.getValue(entry)
    else:
        cat = videoCatalog()
        mp.put(categories, catName, cat)
    lt.addLast(cat['videos'], video)


def addCountry(catalog, video):
    '''
        Funcion que agrega la informacion de los videos en
        el catalogo en la llave "country" segun al pais
        al que pertenecen. La llave mencionada es un mapa por
        lo que el nombre del pais va a ser la llave y el valor va a
        ser una lista con todos los videos y su informacion que
        pertenecen a ese pais.
    '''
    country = catalog['country']
    countryName = video['country'].lower()
    present = mp.contains(country, countryName)
    if present:
        entry = mp.get(country, countryName)
        cat = me.getValue(entry)
    else:
        cat = videoCatalog()
        mp.put(country, countryName, cat)
    lt.addLast(cat['videos'], video)


# ==============================
# Funciones para creacion de datos
# ==============================

def videoCatalog():
    '''
    Esta funcion crea una lista en donde se almacenaran
    todos los videos de una categoria y retornara la lista
    llena
    '''
    vidcatalog = {'videos': None}
    vidcatalog['videos'] = lt.newList("ARRAY_LIST")
    return vidcatalog


# ==============================
# Funciones de consulta
# ==============================

def convertIdtoCat(catalog, categoryId):
    '''
    Esta funcion traduce el id de una categoria en su
    respectivo valor (el nombre de la categoria) y
    lo retorna
    '''
    pair = mp.get(catalog['category_id'], categoryId)
    return pair['value']


def getVideosCat(catalog, category, country):
    '''
    Esta funcion retorna una lista con todos los videos
    y su informacion que hay en una categoria y pais pasados
    por parametro, esta es proporcionada por el usuario
    '''
    # Tiene un espacio porque los nombres de las categorias se guardaron asi
    parameter = ' ' + category
    # Obtenemos la pareja llave valor de la categoria
    pair = mp.get(catalog['category'], parameter)
    if pair is None:
        newlist = 1
    else:
        # Sacamos la informacion de la pareja y es la lista con los videos
        category_list = me.getValue(pair)
        countryList = lt.newList('ARRAY_LIST')
        iterator = ite.newIterator(category_list['videos'])
        while ite.hasNext(iterator):
            info = ite.next(iterator)
            if info['country'] == country:
                lt.addLast(countryList, info)
        # Organizamos la lista de los videos por la cantidad de likes
        newlist = sortVideos(countryList, cmpVideosByViews)
    return newlist


def mostTrendingVideoCountry(catalog, country):
    '''
    Esta funcion retorna el elemento que estuvo mas dias en
    trending en una categoria especifica y la cantidad de dias
    '''

    # Obtenemos la pareja llave valor de la categoria
    pair = mp.get(catalog['country'], country)
    if pair is None:
        newlist = 1
        days = 0
    else:
        # Sacamos la informacion de la pareja y es la lista con los videos
        country_list = me.getValue(pair)
        dictionary = {}
        iterator = ite.newIterator(country_list['videos'])
        while ite.hasNext(iterator):
            info = ite.next(iterator)
            # Seleccionamos los valores que son utiles para la busqueda
            newinfo = (info['title'], info['channel_title'],
                       info['country'])
            '''
            Iniciamos una lista con 1 que va a ser la primera vez que la info
            de un video se guardo en el diccionario. Cada vez que se encuentra
            la misma informacion agrega un 1 a la lista que es valor del
            diccionario la cantidad de dias que estuvo en trending es en len()
            de la lista valor
            '''
            llist = [1]
            if newinfo in dictionary:
                dictionary[newinfo].append(1)
            else:
                dictionary[newinfo] = llist
        # Sacamos la llave del dicionario cuyo valor es el mayor
        newlist = max(dictionary, key=dictionary.get)
        days = dictionary[newlist]

    return newlist, days


def mostTrendingVideoCat(catalog, category):
    '''
    Esta funcion retorna el elemento que estuvo mas dias en
    trending en una categoria especifica y la cantidad de dias
    '''
    # Tiene un espacio porque los nombres de las categorias se guardaron asi
    parameter = ' ' + category
    # Obtenemos la pareja llave valor de la categoria
    pair = mp.get(catalog['category'], parameter)
    if pair is None:
        newlist = 1
        days = 0
    else:
        # Sacamos la informacion de la pareja y es la lista con los videos
        category_list = me.getValue(pair)
        dictionary = {}
        iterator = ite.newIterator(category_list['videos'])
        while ite.hasNext(iterator):
            info = ite.next(iterator)
            # Seleccionamos los valores que son utiles para la busqueda
            newinfo = (info['title'], info['channel_title'],
                       info['category_id'])
            '''
            Iniciamos una lista con 1 que va a ser la primera vez que la info
            de un video se guardo en el diccionario. Cada vez que se encuentra
            la misma informacion agrega un 1 a la lista que es valor del
            diccionario la cantidad de dias que estuvo en trending es en len()
            de la lista valor
            '''
            llist = [1]
            if newinfo in dictionary:
                dictionary[newinfo].append(1)
            else:
                dictionary[newinfo] = llist
        # Sacamos la llave del dicionario cuyo valor es el mayor
        newlist = max(dictionary, key=dictionary.get)
        days = dictionary[newlist]

    return newlist, days


def mostLikedVideosCountryTag(catalog, country, tag):
    '''
    funcion que retorna una lista con los videos de 
    un pais pasado por parametro y que contenga el tag
    deseado por el usuario
    '''
    # Obtenemos la pareja llave valor de la categoria
    pair = mp.get(catalog['country'], country)
    if pair is None:
        newList = 1
    else:
        # Obtenemos la lista con los videos de ese pais
        countryList = me.getValue(pair)
        '''
        Creamos una lista donde guardaremos los videos que
        contienen los tags deseados por el usuario
        '''
        finalList = lt.newList('ARRAY_LIST')
        iterator = ite.newIterator(countryList['videos'])
        while ite.hasNext(iterator):
            info = ite.next(iterator)
            # Buscamos los tags que desea el usuario
            if tag in info['tags']:
                # Verificamos que no hayan repeticiones de videos
                lt.addLast(finalList, info)
            # Le hacemos un sort a la lista dependiendo de los likes
        newList = sortVideos(finalList, cmpVideosByLikes)
        return newList


def videosSize(catalog):
    """
    Número de libros en el catago
    """
    return lt.size(catalog)


# ==============================
# Funciones utilizadas para comparar elementos dentro de una lista
# ==============================

def compareVideosId(id, entry):
    identry = me.getKey(entry)
    if (int(id) == int(identry)):
        return 0
    elif (int(id) > int(identry)):
        return 1
    else:
        return 0


def compareCategories(name, category):
    catentry = me.getKey(category)
    if (name == catentry):
        return 0
    elif (name > catentry):
        return 1
    else:
        return -1


def compareCategoryId(id, catid):
    identry = me.getKey(catid)
    if (int(id) == int(identry)):
        return 0
    elif (int(id) > int(identry)):
        return 1
    else:
        return 0


def cmpVideosByLikes(video1, video2):
    return (float(video1['likes']) > float(video2['likes']))


def cmpVideosByViews(video1, video2):
    return (float(video1['views']) > float(video2['views']))


# ==============================
# Funciones de ordenamiento
# ==============================

def sortVideos(value_list, cmp):
    '''
    Esta funcion organiza los videos por la cantidad
    de likes que tiene el video y retorna la lista
    ordenada
    '''
    if lt.isEmpty(value_list):
        newlist = 1
    else:
        newlist = qs.sort(value_list, cmp)
    return newlist
