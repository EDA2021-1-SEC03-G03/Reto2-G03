def getNode(node, key, cmpfunction):
    """ Retornar el valor asociado a una llave en un sub-árbol binario ordenado.
        Args: node: raíz del sub-arbol.
        key: la llave de busqueda
        cmpfunction(key1, key2): función para comparar dos keys en el árbol. 
        Valores de retorno: 0 si key1 es igual a key2, -1 si key1 < key2, 1 si key1 > key2.
        Returns: el valor asociado a la key (si existe). None si no existe.
    """ 
    
