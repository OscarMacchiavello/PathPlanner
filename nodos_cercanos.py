import osmnx as ox

def encontrar_nodos_cercanos(origen,destino,puntos_lista,G):
    '''Retorna una lista de nodos cercanos a cada coordenada obtenida de los parametros'''
    # punto_cercano_inicio = ox.nearest_nodes(G, X=punto_inicio_x, Y=punto_inicio_y)
    # punto_cercano_final = ox.nearest_nodes(G, X=punto_final_x, Y=punto_final_y)
    nodos_cercanos = [ox.nearest_nodes(G,X=nodo[0],Y=nodo[1]) for nodo in puntos_lista]
    nodo_origen = ox.nearest_nodes(G,X=origen[0],Y=origen[1])
    nodo_destino = ox.nearest_nodes(G,X=destino[0],Y=destino[1])

    return nodo_origen,nodo_destino,nodos_cercanos