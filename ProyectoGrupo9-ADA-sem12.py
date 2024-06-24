import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
from tkinter import ttk
import osmnx as ox
from shapely.geometry import Polygon

poligono = None
modoDeTransporte = None
punto_inicio_x = None
punto_inicio_y = None
punto_final_x = None
punto_final_y = None

def calcular_rectangulo(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    
    distancia = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    
    distancia_adicional = 0.4 * distancia
    
    x_min = min(x1, x2) - distancia_adicional
    x_max = max(x1, x2) + distancia_adicional
    y_min = min(y1, y2) - distancia_adicional
    y_max = max(y1, y2) + distancia_adicional
    
    rectangulo = [
        (x_min, y_min),
        (x_max, y_min),
        (x_max, y_max),
        (x_min, y_max)
    ]
    
    return rectangulo

class PathPlannerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PathPlanner")
        self.geometry("300x450")

        title = tk.Label(self, text="PathPlanner", font=("Helvetica", 20))
        title.pack(pady=10)

        # punto de partida
        frame_puntoPartida = ttk.LabelFrame(self, text="Ingrese punto de partida:", padding=(10, 5))
        frame_puntoPartida.pack(padx=10, pady=10, fill="x")
        tk.Label(frame_puntoPartida, text="Latitud").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.latitud_puntoPartida = tk.Entry(frame_puntoPartida)
        self.latitud_puntoPartida.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_puntoPartida, text="Longitud").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.longitud_puntoPartida = tk.Entry(frame_puntoPartida)
        self.longitud_puntoPartida.grid(row=1, column=1, padx=5, pady=5)

        # punto de llegada
        frame_puntoLlegada = ttk.LabelFrame(self, text="Ingrese punto de llegada:", padding=(10, 5))
        frame_puntoLlegada.pack(padx=10, pady=10, fill="x")
        tk.Label(frame_puntoLlegada, text="Latitud").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.latitud_puntoLlegada = tk.Entry(frame_puntoLlegada)
        self.latitud_puntoLlegada.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_puntoLlegada, text="Longitud").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.longitud_puntoLlegada = tk.Entry(frame_puntoLlegada)
        self.longitud_puntoLlegada.grid(row=1, column=1, padx=5, pady=5)

        # modo de transporte
        frame_MetodoTransporte = ttk.LabelFrame(self, text="Modo de transporte:", padding=(10, 5))
        frame_MetodoTransporte.pack(padx=10, pady=10, fill="x")
        transporte_modo = ["drive", "walk", "bike", "all"]
        self.transporte_modo = ttk.Combobox(frame_MetodoTransporte, values=transporte_modo)
        self.transporte_modo.grid(row=0, column=0, padx=5, pady=5)
        self.transporte_modo.current(0)  # Seleccionar la primera opción por defecto

        # botón de enviar
        send_button = tk.Button(self, text="Enviar", command=self.enviar_datos)
        send_button.pack(pady=20)

    def enviar_datos(self):
        inicio_latitud = self.latitud_puntoPartida.get()
        inicio_longitud = self.longitud_puntoPartida.get()
        final_latitud = self.latitud_puntoLlegada.get()
        final_longitud = self.longitud_puntoLlegada.get()

        # Convierte los valores de latitud y longitud a flotantes y crea las tuplas
        # invertir coordenadas de (latitud, longitud) a (longitud, latitud)
        punto_inicio = (float(inicio_longitud), float(inicio_latitud))
        punto_llegada = (float(final_longitud), float(final_latitud))

        global poligono;
        poligono = Polygon(calcular_rectangulo(punto_inicio, punto_llegada))

        global modoDeTransporte;
        modoDeTransporte = self.transporte_modo.get()

        global punto_inicio_x;
        punto_inicio_x = float(inicio_longitud)
        global punto_inicio_y;
        punto_inicio_y = float(inicio_latitud)
        global punto_final_x;
        punto_final_x = float(final_longitud) 
        global punto_final_y;
        punto_final_y = float(final_latitud)

        # cerramos la interfaz
        self.destroy()

app = PathPlannerApp()
app.mainloop()

G = ox.graph_from_polygon(poligono, network_type=modoDeTransporte)
ox.plot_graph(G)

punto_cercano_inicio = ox.nearest_nodes(G, X=punto_inicio_x, Y=punto_inicio_y)
punto_cercano_final = ox.nearest_nodes(G, X=punto_final_x, Y=punto_final_y)
print(f"Nodo mas cercano a punto de inicio: {punto_cercano_inicio}")
print(f"Nodo mas cercano a punto de llegada: {punto_cercano_final}")

# Pintar los nodos inicial y final de rojo
color_nodos = ['r' if node in [punto_cercano_inicio, punto_cercano_final] else 'w' for node in G.nodes()]
fig, ax = ox.plot_graph(G, node_color=color_nodos, edge_color='gray', node_size=20, show=False, close=False)
plt.show()

def dijkstra(G, origen, destino, weight='length'):
    # Inicialización
    distancia = {node: float('inf') for node in G.nodes}
    distancia[origen] = 0
    previo = {node: None for node in G.nodes}
    noVisitado = list(G.nodes)

    while noVisitado:
        # Seleccionar el nodo no visitado con la menor distancia
        nodoActual = min(noVisitado, key=lambda node: distancia[node])
        noVisitado.remove(nodoActual)

        # Destino alcanzado
        if nodoActual == destino:
            ruta = []
            while previo[nodoActual] is not None:
                ruta.insert(0, nodoActual)
                nodoActual = previo[nodoActual]
            ruta.insert(0, origen)
            return ruta

        # Actualizar distancias para los vecinos
        for vecino, data in G[nodoActual].items():
            alternativa = distancia[nodoActual] + data[0].get(weight, 1)
            if alternativa < distancia[vecino]:
                distancia[vecino] = alternativa
                previo[vecino] = nodoActual

    return None


path = dijkstra(G, punto_cercano_inicio, punto_cercano_final)
print(f"El camino más corto de {punto_cercano_inicio} a {punto_cercano_final} es: {path}")

color_nodos = ['r' if node in path else 'w' for node in G.nodes()]
color_edges = []
for u, v, key in G.edges(keys=True):
    if u in path and v in path and (path.index(u) == path.index(v) - 1 or path.index(v) == path.index(u) - 1):
        color_edges.append('r')
    else:
        color_edges.append('gray')
fig, ax = ox.plot_graph(G, node_color=color_nodos, edge_color=color_edges, node_size=20, show=False, close=False)
plt.show()