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
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos


def newCatalog():

    catalog = {'videos': None,
               'video_id': None,
               'category_id': None,
               'videos_id': 0}

    catalog['videos'] = lt.newList('ARRAY_LIST')

    catalog["category"] = mp.newMap(1,
                                    maptype='PROBING',
                                    loadfactor=0.5,
                                    comparefunction=compareCategories)

    catalog['category_id'] = mp.newMap(37,
                                       maptype='PROBING',
                                       loadfactor=0.5,
                                       comparefunction=compareCategoryId)

    catalog['videos_id'] = mp.newMap(1,
                                     maptype='CHAINING',
                                     loadfactor=4.0,
                                     comparefunction=compareVideosId)

    return catalog


def newCategory(name, catid):
    category = {'id': None,
                'category': "",
                'total_videos': 0,
                'videos': None}

    category['id'] = catid
    category['category'] = name
    category['videos'] = lt.newList
    return category


# Funciones para creacion de datos


# Funciones para agregar informacion al catalogo


# ==============================
# Funciones de consulta
# ==============================


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
