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
               'trending_date': None,
               'title': None,
               'channel_title': None,
               'category_id': None,
               'publish_time': None,
               'tags': None,
               'views': None,
               'likes': 0,
               'dislikes': 0,
               'country': None,
               'days': 0}

    catalog['videos'] = lt.newList('ARRAY_LIST')

    catalog['trending_date'] = mp.newMap(10000,
                                         maptype='CHAINING',
                                         loadfactor=4.0)

    catalog['title'] = mp.newMap(10000,
                                 maptype='CHAINING',
                                 loadfactor=4.0)

    catalog['channel_title'] = mp.newMap(10000,
                                         maptype='CHAINING',
                                         loadfactor=4.0)

    catalog['category_id'] = mp.newMap(10000,
                                       maptype='CHAINING',
                                       loadfactor=4.0)

    catalog['publish_time'] = mp.newMap(10000,
                                        maptype='CHAINING',
                                        loadfactor=4.0)

    catalog['tags'] = mp.newMap(10000,
                                maptype='CHAINING',
                                loadfactor=4.0)

    catalog['views'] = mp.newMap(10000,
                                 maptype='CHAINING',
                                 loadfactor=4.0)

    catalog['likes'] = mp.newMap(10000,
                                 maptype='CHAINING',
                                 loadfactor=4.0,
                                 comparefunction=cmpVideosByLikes)

    catalog['dislikes'] = mp.newMap(10000,
                                    maptype='CHAINING',
                                    loadfactor=4.0)

    catalog['country'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0)

    catalog['days'] = mp.newMap(10000,
                                maptype='CHAINING',
                                loadfactor=4.0)
    return catalog


def newCategory():
    category = {'id': None,
                'category': None}

    category['id'] = mp.newMap(10000,
                               maptype='CHAINING',
                               loadfactor=4.0)

    category['category'] = mp.newMap(10000,
                                     maptype='CHAINING',
                                     loadfactor=4.0)
    return category


# Funciones para creacion de datos


# Funciones para agregar informacion al catalogo


def addVideo(catalog, video):

    lt.addLast(catalog['videos'], video)
    mp.put(catalog['title'], video['title'], video)


def addTag(catalog, tag):
    """
    Adiciona un tag a la tabla de tags dentro del catalogo y se
    actualiza el indice de identificadores del tag.
    """
    newtag = catalog(tag['tag_name'], tag['tag_id'])
    mp.put(catalog['tags'], tag['tag_name'], newtag)
    mp.put(catalog['tagIds'], tag['tag_id'], newtag)


# ==============================
# Funciones de consulta
# ==============================


# ==============================
# Funciones de Comparacion
# ==============================


def compareTagNames(name, tag):
    tagentry = me.getKey(tag)
    if (name == tagentry):
        return 0
    elif (name > tagentry):
        return 1
    else:
        return -1


def compareTagIds(id, tag):
    tagentry = me.getKey(tag)
    if (int(id) == int(tagentry)):
        return 0
    elif (int(id) > int(tagentry)):
        return 1
    else:
        return 0


def cmpVideosByLikes(video1, video2):
    return (float(video1['likes']) > float(video2['likes']))

# Funciones de ordenamiento
