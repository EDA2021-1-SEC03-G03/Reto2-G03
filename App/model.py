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
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos.
El catálogo tendrá dos listas, una para los videos,
    otra para las categorias de los mismos.
"""
# ==============================
# Construccion de modelos
# ==============================


def newCatalog():
    '''
        Creamos el catalogo para agegar la informacion necesaria
    '''

    catalog = {'videos': None,
               'category': None}

    catalog['videos'] = lt.newList('ARRAY_LIST')

    catalog["category"] = mp.newMap(33,
                                    maptype='CHAINING',
                                    loadfactor=4.0,
                                    comparefunction=compareCategories)

    return catalog


def newCategory():
    '''
        Catalogo especial para las categorias y sus id's
    '''
    category = {'name': None}

    category["name"] = mp.newMap(33,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareCategories)    

    return category

# ==============================
# Funciones para creacion de datos
# ==============================


def videoCategories():
    catcatalog = {'videos': None}
    catcatalog['videos'] = lt.newList("ARRAY_LIST")
    return catcatalog


# ==============================
# Funciones para agregar informacion al catalogo
# ==============================


def addVideoToCat(catalog, video):
    lt.addLast(catalog['videos'], video)


def addCategoryInfo(catCategory, category):
    '''Esta funcion agrega en un mapa especial las categorias
       cuya llave es el id correspondiente
    '''
    mp.put(catCategory['name'], category['id'], category['name'])


def addVideo(catalog, video, catCategory):
    '''
        Funcion que agrega la informacion de los videos
        en funcion de la categoria a la que pertenece.
    '''
    categories = catalog['category']
    catName = traduceIdtoCat(catCategory, video['category_id'])
    present = mp.contains(categories, catName)
    if present:
        entry = mp.get(categories, catName)
        cat = me.getValue(entry)
    else:
        cat = videoCategories()
        mp.put(categories, catName, cat)
    lt.addLast(cat['videos'], video)


# ==============================
# Funciones de consulta
# ==============================


def traduceIdtoCat(catCategory, categoryId):
    pair = mp.get(catCategory['name'], categoryId)
    return pair['value']


def reqNvideos(catalog, name, size):
    value = mp.get(catalog['category'], name)
    print(value)
    '''
    ready = me.getValue(value)['videos']
    newlist = sortVideos(ready, size)
    return newlist'''


def videosSize(catalog):
    """
    Número de libros en el catago
    """
    return lt.size(catalog['videos'])

# ==============================
# Funciones de Comparacion
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


# ==============================
# Funciones de ordenamiento
# ==============================


def sortVideos(catalog, size):
    sublist = lt.subList(catalog, 0, size)
    newlist = sa.sort(sublist, cmpVideosByLikes)
    return newlist
