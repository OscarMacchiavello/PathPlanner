import osmnx as ox
import matplotlib.pyplot as plt

def pintar_nodos(nodos_cercanos,G):
    '''Pintar de rojos los nodos seleccionados y de negro el origen y final'''
    color_nodos = ['r' if node in nodos_cercanos else (1.0, 1.0, 1.0, 0.5) for node in G.nodes()]
    fig, ax = ox.plot_graph(G, node_color=color_nodos, edge_color='gray', node_size=20, show=False, close=False)
    plt.show()

def pintar_camino(ruta_greedy,nuevo_grafo,G):
    '''Se pintara los nodos y las aristas del camino'''
    color_edges = []
    path = []

    for i,nodo in enumerate(ruta_greedy):
        if i != len(ruta_greedy)-1:
            #Guardar la data de las aristas
            data=nuevo_grafo.get_edge_data(nodo,ruta_greedy[i+1])
            #Concatenar las rutas de la secuencia de los nodos
            path.extend(data['ruta'])

    color_nodos = ['r' if node in path else (1.0, 1.0, 1.0, 0.1) for node in G.nodes()]

    for u, v, key in G.edges(keys=True):
        if u in path and v in path and (path.index(u) == path.index(v) - 1 or path.index(v) == path.index(u) - 1):
            color_edges.append('r')
        else:
            color_edges.append('gray')

    fig, ax = ox.plot_graph(G, node_color=color_nodos, edge_color=color_edges, node_size=20, show=False, close=False)
    plt.show()