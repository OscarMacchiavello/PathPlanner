from interfaz import PathPlannerApp
from obtener_datos import obtener
from obtener_rectangulo import obtener_rectangulo
from nodos_cercanos import encontrar_nodos_cercanos
from pintar import pintar_nodos, pintar_camino
from algoritmos import encontrar_camino, crear_grafo

app = PathPlannerApp()
app.mainloop()
data = obtener()
G_mapa = obtener_rectangulo(data['puntos_lista'],data['transporte'])
data['origen'],data['destino'],data['puntos_lista'] = encontrar_nodos_cercanos(
	data['origen'],data['destino'],data['puntos_lista'],G_mapa)
pintar_nodos(data['puntos_lista'],G_mapa)
grafo = crear_grafo(data['puntos_lista'],G_mapa)
ruta = encontrar_camino(data['origen'],data['destino'],grafo)
pintar_camino(ruta,grafo,G_mapa)
