import tkinter as tk
from tkinter import ttk
import json

class PathPlannerApp(tk.Tk):
    '''Instancia una interfaz grafica que permite ingreso de datos de 
       coordenadas: origen, destino, puntos intermedios y modo de transporte
      .Posteriormente son almacenados y enviados con el metodo enviar_coordenadas'''
    
    def __init__(self):
        
        super().__init__()
        #Titulo de la interfaz y su resolucion
        self.title("PathPlanner")
        self.geometry("300x580")

        #Etiqueta del titulo
        title = tk.Label(self, text="PathPlanner", font=("Helvetica", 20))
        title.pack(pady=10)

        #Inicializar lista que almacenara todas las coordenadas incluidas el origen y destino
        self.puntos_lista = []

        #Inicializar framework para el ingreso de la coordenada origen
        frame_puntoPartida = ttk.LabelFrame(self, text="Ingrese punto de partida:", padding=(10, 5))
        frame_puntoPartida.pack(padx=10, pady=10, fill="x")
        tk.Label(frame_puntoPartida, text="Latitud").grid(row=0,column=0, padx=5, pady=5, sticky="e")
        self.latitud_puntoPartida = tk.Entry(frame_puntoPartida)
        self.latitud_puntoPartida.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_puntoPartida, text="Longitud").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.longitud_puntoPartida = tk.Entry(frame_puntoPartida)
        self.longitud_puntoPartida.grid(row=1, column=1, padx=5, pady=5)

        #Inicializar framework para el ingreso de la coordenada destino
        frame_puntoLlegada = ttk.LabelFrame(self, text="Ingrese punto de llegada:", padding=(10, 5))
        frame_puntoLlegada.pack(padx=10, pady=10, fill="x")
        tk.Label(frame_puntoLlegada, text="Latitud").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.latitud_puntoLlegada = tk.Entry(frame_puntoLlegada)
        self.latitud_puntoLlegada.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_puntoLlegada, text="Longitud").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.longitud_puntoLlegada = tk.Entry(frame_puntoLlegada)
        self.longitud_puntoLlegada.grid(row=1, column=1, padx=5, pady=5)

        #Inicializar framework para el ingreso de la coordenadas intermedias
        frame_puntoIntermedio = ttk.LabelFrame(self, text="Ingrese punto intermedio:", padding=(10, 5))
        frame_puntoIntermedio.pack(padx=10, pady=10, fill="x")
        tk.Label(frame_puntoIntermedio,text="Latitud").grid(row=0,column=0, padx=5, pady=5, sticky="e")
        self.latitud_puntoIntermedio = tk.Entry(frame_puntoIntermedio)
        self.latitud_puntoIntermedio.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_puntoIntermedio, text="Longitud").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.longitud_puntoIntermedio = tk.Entry(frame_puntoIntermedio)
        self.longitud_puntoIntermedio.grid(row=1, column=1, padx=5, pady=5)

        # Instanciar boton 'insertar', el cual almacena coordenadas intermedias
        insert_button = tk.Button(frame_puntoIntermedio,text='Ingresar',command=self.ingresar_intermedios)
        insert_button.grid(pady=5,column=1)

        # modo de transporte
        frame_MetodoTransporte = ttk.LabelFrame(self, text="Modo de transporte:", padding=(10, 5))
        frame_MetodoTransporte.pack(padx=10, pady=10, fill="x")
        transporte_modo = ["drive", "walk", "bike", "all"]
        self.transporte_modo = ttk.Combobox(frame_MetodoTransporte, values=transporte_modo)
        self.transporte_modo.grid(row=0, column=0, padx=5, pady=5)
        self.transporte_modo.current(0)  # Seleccionar la primera opción por defecto

        # Instancia botón 'enviar'
        send_button = tk.Button(self, text="Enviar", command=self.enviar_coordenadas)
        send_button.pack(pady=20)

    def ingresar_intermedios(self):
        '''Almacena las coordenas intermedias en una lista de tuplas'''
            
        intermedio_latitud = float(self.latitud_puntoIntermedio.get())
        intermedio_longitud = float(self.longitud_puntoIntermedio.get())

        self.puntos_lista.append((intermedio_longitud,intermedio_latitud))
        #Limpiar las entradas para ingresar nuevas
        self.latitud_puntoIntermedio.delete(0,tk.END)
        self.longitud_puntoIntermedio.delete(0,tk.END)

    def enviar_coordenadas(self):
        '''Almacena el origen y destino en la lista de tuplas y retorna 4 objetos: origen, destino, lista y metodo de transporte'''

        inicio_latitud = float(self.latitud_puntoPartida.get())
        inicio_longitud = float(self.longitud_puntoPartida.get())
        final_latitud = float(self.latitud_puntoLlegada.get())
        final_longitud = float(self.longitud_puntoLlegada.get())

        origen = (inicio_longitud,inicio_latitud)
        destino = (final_longitud,final_latitud)
        self.puntos_lista.append(origen)
        self.puntos_lista.append(destino)

        #Obtenemos metodo de transporte
        transporte = self.transporte_modo.get()

        #Almacenar los datos un archivo json
        data = {
            'origen': origen,
            'destino': destino,
            'puntos_lista': self.puntos_lista,
            'transporte':transporte
        }
        with open('data.json','w') as f:
            json.dump(data,f)

        self.destroy()  


