from shapely.geometry import box
import osmnx as ox

def obtener_rectangulo(puntos_lista,transporte):
    '''Se calcula el rectangulo que contiene a los puntos y se crea el mapa
    con osmnx'''
    #Minimo y maximo en la coordenada x
    min_x = min(tupla[0] for tupla in puntos_lista)
    max_x = max(tupla[0] for tupla in puntos_lista)
    #Minimo y maximo en coordenada y
    min_y = min(tupla[1] for tupla in puntos_lista)
    max_y = max(tupla[1] for tupla in puntos_lista)

    distancia = ((min_x - max_x)**2 + (min_y - max_y)**2)**0.5
    
    distancia_adicional = 0.3 * distancia
    
    min_x -= distancia_adicional
    min_y -= distancia_adicional
    max_x += distancia_adicional
    max_y += distancia_adicional

    rectangulo = box(minx=min_x,miny=min_y,maxx=max_x,maxy=max_y)

    G_mapa = ox.graph_from_polygon(rectangulo, network_type=transporte)
    ox.plot_graph(G_mapa)

    return G_mapa