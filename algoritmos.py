import networkx as nx

def dijkstra(G, origen, destino, weight='length'):
    # Inicialización
    distancia = {node: float('inf') for node in G.nodes}
    distancia[origen] = 0
    previo = {node: None for node in G.nodes}
    no_visitado = list(G.nodes)

    while no_visitado:
        # Seleccionar el nodo no visitado con la menor distancia
        nodoActual = min(no_visitado, key=lambda node: distancia[node])
        no_visitado.remove(nodoActual)

        # Destino alcanzado
        if nodoActual == destino:
            ruta = []
            while previo[nodoActual] is not None:
                ruta.insert(0, nodoActual)
                nodoActual = previo[nodoActual]
            ruta.insert(0, origen)
            #Retornar la ruta que encontro y su distancia total
            return (ruta,distancia[destino])

        # Actualizar distancias para los vecinos
        for vecino, data in G[nodoActual].items():
            alternativa = distancia[nodoActual] + data[0].get(weight, 1)
            if alternativa < distancia[vecino]:
                distancia[vecino] = alternativa
                previo[vecino] = nodoActual
                
    return None

def crear_grafo(lista_nodos,G):
    '''Creamos un grafo con todos los nodos insertados'''
    nuevo_grafo = nx.Graph()

    for nodo in lista_nodos:
        nuevo_grafo.add_node(nodo,estado=False)
    for i in lista_nodos:
        for j in lista_nodos:
            if i < j:
                ruta, distancia = dijkstra(G,i,j)
                nuevo_grafo.add_edge(i,j,ruta=ruta,distancia=distancia)

    return nuevo_grafo

def encontrar_camino(origen,destino,nuevo_grafo):
    '''Aplicara un algoritmo voraz para encontrar la secuencia de un camino efiente'''
    no_visitados = list(nuevo_grafo.nodes)
    no_visitados.remove(origen)
    no_visitados.remove(destino)

    nodo_actual = origen
    nuevo_grafo.nodes[origen]['estado'] = True
    #Inicializamos el antecesor de cada nodo en None
    previo = {node:None for node in nuevo_grafo}

    while no_visitados:

        distancia = float('inf')

        for vecino,data in nuevo_grafo[nodo_actual].items():
            fue_visitado = nuevo_grafo.nodes[vecino]['estado']
            if vecino != destino  and fue_visitado == False and data['distancia']<distancia:
                distancia = data['distancia']
                nodo_vecino = vecino

        #Evitamos que el nodo elegido se elija denuevo

        nuevo_grafo.nodes[nodo_vecino]['estado'] = True
        previo[nodo_vecino] = nodo_actual
        no_visitados.remove(nodo_vecino)
        nodo_actual = nodo_vecino

    previo[destino] = nodo_actual
    nodo_actual = destino

    ruta_greedy =[]
    while previo[nodo_actual] is not None:
        ruta_greedy.insert(0,nodo_actual)
        nodo_actual = previo[nodo_actual]
    ruta_greedy.insert(0,origen)

    return ruta_greedy




