import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import font as tkfont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib as mpl


class Vista(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Sistema de Navegación")
        self.geometry("1200x800")
        self.configure(bg="#f5f6fa")  # Color de fondo principal
        self._configurar_estilos()
        self._crear_menu()
        self._crear_widgets()
        self.controlador = None  # se inyecta después

    def _configurar_estilos(self):
        style = ttk.Style()
        
        # Configuración general
        style.configure(".", 
                       background="#f5f6fa",
                       foreground="#2c3e50",
                       font=("Segoe UI", 10))
        
        # Estilos para frames
        style.configure("TFrame", 
                       background="#ffffff",
                       relief="flat")
        
        # Estilos para labels
        style.configure("TLabel", 
                       background="#ffffff",
                       foreground="#2c3e50",
                       font=("Segoe UI", 10))
        
        style.configure("Header.TLabel", 
                       font=("Segoe UI", 12, "bold"),
                       foreground="#2c3e50")
        
        # Estilos para botones
        style.configure("TButton",
                       font=("Segoe UI", 10),
                       padding=5)
        
        style.map("TButton",
                 background=[("active", "#3498db"), ("!active", "#2980b9")],
                 foreground=[("active", "#ffffff"), ("!active", "#ffffff")])
        
        # Estilos para labelframes
        style.configure("TLabelframe", 
                       background="#ffffff",
                       foreground="#2c3e50",
                       font=("Segoe UI", 10, "bold"))
        
        style.configure("TLabelframe.Label", 
                       background="#ffffff",
                       foreground="#2c3e50",
                       font=("Segoe UI", 10, "bold"))
        
        # Estilos para entry
        style.configure("TEntry",
                       fieldbackground="#ffffff",
                       foreground="#2c3e50",
                       padding=5)
        
        # Estilos para listbox
        style.configure("TListbox",
                       background="#ffffff",
                       foreground="#2c3e50",
                       selectbackground="#3498db",
                       selectforeground="#ffffff",
                       font=("Segoe UI", 10))

    def _crear_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Guardar", command=self._guardar)
        file_menu.add_command(label="Cargar", command=self._cargar)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.quit)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self._mostrar_acerca_de)

    def _crear_widgets(self):
        # Frame principal con padding y fondo
        main_frame = ttk.Frame(self, padding="20", style="TFrame")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Panel izquierdo (formularios)
        left_panel = ttk.Frame(main_frame, style="TFrame")
        left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Frame para el formulario de nodos con sombra y bordes redondeados
        form_frame = ttk.LabelFrame(left_panel, text="Gestión de Nodos", padding="15", style="TLabelframe")
        form_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        # Campos del formulario con mejor espaciado
        ttk.Label(form_frame, text="Nombre:", style="TLabel").grid(row=0, column=0, sticky="e", pady=5)
        ttk.Label(form_frame, text="Latitud:", style="TLabel").grid(row=1, column=0, sticky="e", pady=5)
        ttk.Label(form_frame, text="Longitud:", style="TLabel").grid(row=2, column=0, sticky="e", pady=5)

        self.nombre = ttk.Entry(form_frame, width=25, style="TEntry")
        self.lat = ttk.Entry(form_frame, width=25, style="TEntry")
        self.lon = ttk.Entry(form_frame, width=25, style="TEntry")
        
        self.nombre.grid(row=0, column=1, padx=10, pady=5)
        self.lat.grid(row=1, column=1, padx=10, pady=5)
        self.lon.grid(row=2, column=1, padx=10, pady=5)

        # Botones del formulario con mejor espaciado
        btn_frame = ttk.Frame(form_frame, style="TFrame")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Agregar", command=self._agregar, style="TButton").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Editar", command=self._editar, style="TButton").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self._eliminar, style="TButton").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self._limpiar_campos, style="TButton").pack(side="left", padx=5)

        # Frame para la lista de nodos
        list_frame = ttk.LabelFrame(left_panel, text="Nodos Disponibles", padding="15", style="TLabelframe")
        list_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        # Lista de nodos con scrollbar y mejor estilo
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.lista = tk.Listbox(list_frame, height=10, width=30, 
                               yscrollcommand=scrollbar.set,
                               font=("Segoe UI", 10),
                               bg="#ffffff",
                               fg="#2c3e50",
                               selectbackground="#3498db",
                               selectforeground="#ffffff",
                               relief="flat",
                               borderwidth=1)
        self.lista.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.config(command=self.lista.yview)

        # Frame para gestión de aristas
        edge_frame = ttk.LabelFrame(left_panel, text="Gestión de Caminos", padding="15", style="TLabelframe")
        edge_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        
        # Campos para aristas con mejor espaciado
        ttk.Label(edge_frame, text="Origen:", style="TLabel").grid(row=0, column=0, sticky="e", pady=5)
        ttk.Label(edge_frame, text="Destino:", style="TLabel").grid(row=1, column=0, sticky="e", pady=5)
        
        self.origen = ttk.Entry(edge_frame, width=25, style="TEntry")
        self.destino = ttk.Entry(edge_frame, width=25, style="TEntry")
        
        self.origen.grid(row=0, column=1, padx=10, pady=5)
        self.destino.grid(row=1, column=1, padx=10, pady=5)
        
        # Checkbox para bidireccional con mejor estilo
        self.bidireccional = tk.BooleanVar(value=True)
        ttk.Checkbutton(edge_frame, text="Bidireccional", 
                       variable=self.bidireccional,
                       style="TCheckbutton").grid(row=2, column=0, columnspan=2, pady=10)
        
        # Botones para aristas con mejor espaciado
        edge_btn_frame = ttk.Frame(edge_frame, style="TFrame")
        edge_btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(edge_btn_frame, text="Agregar Camino", 
                  command=self._agregar_arista, style="TButton").pack(side="left", padx=5)
        ttk.Button(edge_btn_frame, text="Eliminar Camino", 
                  command=self._eliminar_arista, style="TButton").pack(side="left", padx=5)

        # Frame para el cálculo de ruta
        route_frame = ttk.LabelFrame(left_panel, text="Cálculo de Ruta", padding="15", style="TLabelframe")
        route_frame.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        
        # Frame para puntos de inicio y fin
        endpoints_frame = ttk.Frame(route_frame, style="TFrame")
        endpoints_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        ttk.Label(endpoints_frame, text="Punto Inicial:", style="TLabel").grid(row=0, column=0, sticky="e", pady=5)
        ttk.Label(endpoints_frame, text="Punto Final:", style="TLabel").grid(row=1, column=0, sticky="e", pady=5)

        self.inicio = ttk.Entry(endpoints_frame, width=25, style="TEntry")
        self.fin = ttk.Entry(endpoints_frame, width=25, style="TEntry")
        
        self.inicio.grid(row=0, column=1, padx=10, pady=5)
        self.fin.grid(row=1, column=1, padx=10, pady=5)

        # Frame para puntos intermedios
        waypoints_frame = ttk.LabelFrame(route_frame, text="Puntos Intermedios", padding="10", style="TLabelframe")
        waypoints_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Lista de puntos intermedios
        self.waypoints_list = tk.Listbox(waypoints_frame, height=4, width=30,
                                       font=("Segoe UI", 10),
                                       bg="#ffffff",
                                       fg="#2c3e50",
                                       selectbackground="#3498db",
                                       selectforeground="#ffffff",
                                       relief="flat",
                                       borderwidth=1)
        self.waypoints_list.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbar para la lista
        waypoints_scrollbar = ttk.Scrollbar(waypoints_frame, orient="vertical")
        waypoints_scrollbar.pack(side="right", fill="y")
        self.waypoints_list.config(yscrollcommand=waypoints_scrollbar.set)
        waypoints_scrollbar.config(command=self.waypoints_list.yview)
        
        # Frame para agregar puntos intermedios
        add_waypoint_frame = ttk.Frame(route_frame, style="TFrame")
        add_waypoint_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        ttk.Label(add_waypoint_frame, text="Agregar punto:", style="TLabel").pack(side="left", padx=(0, 5))
        self.waypoint_entry = ttk.Entry(add_waypoint_frame, width=20, style="TEntry")
        self.waypoint_entry.pack(side="left", padx=5)
        
        ttk.Button(add_waypoint_frame, text="+", 
                  command=self._agregar_waypoint,
                  style="TButton",
                  width=3).pack(side="left", padx=5)
        
        # Botones para gestionar puntos intermedios
        waypoint_btn_frame = ttk.Frame(route_frame, style="TFrame")
        waypoint_btn_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        ttk.Button(waypoint_btn_frame, text="Subir", 
                  command=self._mover_waypoint_arriba,
                  style="TButton").pack(side="left", padx=5)
        ttk.Button(waypoint_btn_frame, text="Bajar", 
                  command=self._mover_waypoint_abajo,
                  style="TButton").pack(side="left", padx=5)
        ttk.Button(waypoint_btn_frame, text="Eliminar", 
                  command=self._eliminar_waypoint,
                  style="TButton").pack(side="left", padx=5)
        ttk.Button(waypoint_btn_frame, text="Limpiar", 
                  command=self._limpiar_waypoints,
                  style="TButton").pack(side="left", padx=5)

        # Botón para calcular ruta
        ttk.Button(route_frame, text="Calcular Ruta", 
                  command=self._calcular_ruta,
                  style="TButton").grid(row=4, column=0, columnspan=2, pady=10)

        # Frame para mostrar la ruta
        result_frame = ttk.LabelFrame(left_panel, text="Resultado", padding="15", style="TLabelframe")
        result_frame.grid(row=4, column=0, padx=5, pady=5, sticky="ew")
        
        self.lbl_ruta = ttk.Label(result_frame, text="", 
                                 wraplength=300, 
                                 justify="left",
                                 style="TLabel")
        self.lbl_ruta.pack(fill="both", expand=True, padx=5, pady=5)

        # Panel derecho (mapa)
        right_panel = ttk.LabelFrame(main_frame, text="Mapa", padding="15", style="TLabelframe")
        right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Configurar estilo de matplotlib
        try:
            plt.style.use('seaborn')
        except:
            # Si seaborn no está disponible, usar un estilo personalizado
            plt.style.use('default')
            mpl.rcParams.update({
                'figure.facecolor': '#ffffff',
                'axes.facecolor': '#ffffff',
                'axes.edgecolor': '#2c3e50',
                'axes.labelcolor': '#2c3e50',
                'xtick.color': '#2c3e50',
                'ytick.color': '#2c3e50',
                'grid.color': '#bdc3c7',
                'grid.linestyle': '--',
                'grid.alpha': 0.7
            })
        
        # Crear figura de matplotlib con estilo mejorado
        self.fig, self.ax = plt.subplots(figsize=(8, 8), facecolor='#ffffff')
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_panel)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Configurar el mapa con mejor estilo
        self.ax.set_title("Mapa de Nodos y Caminos", fontsize=12, pad=20)
        self.ax.set_xlabel("Longitud", fontsize=10, labelpad=10)
        self.ax.set_ylabel("Latitud", fontsize=10, labelpad=10)
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.fig.tight_layout()

        # Barra de estado con mejor estilo
        self.status_bar = ttk.Label(self, 
                                  text="Listo", 
                                  relief="flat",
                                  padding="5",
                                  background="#2c3e50",
                                  foreground="#ffffff",
                                  font=("Segoe UI", 9))
        self.status_bar.grid(row=1, column=0, sticky="ew")

    def _limpiar_campos(self):
        self.nombre.delete(0, tk.END)
        self.lat.delete(0, tk.END)
        self.lon.delete(0, tk.END)
        self.origen.delete(0, tk.END)
        self.destino.delete(0, tk.END)
        self.inicio.delete(0, tk.END)
        self.fin.delete(0, tk.END)
        self.lbl_ruta.config(text="")
        self.status_bar.config(text="Campos limpiados")

    def _guardar(self):
        if self.controlador:
            ruta = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("Archivo JSON", "*.json"), ("Todos los archivos", "*.*")],
            )
            if ruta:
                self.controlador.guardar_datos(ruta)
                self.status_bar.config(text="Datos guardados exitosamente")

    def _cargar(self):
        if self.controlador:
            ruta = filedialog.askopenfilename(
                filetypes=[("Archivo JSON", "*.json"), ("Todos los archivos", "*.*")]
            )
            if ruta:
                self.controlador.cargar_datos(ruta)
                self.status_bar.config(text="Datos cargados exitosamente")

    def _mostrar_acerca_de(self):
        messagebox.showinfo(
            "Acerca de",
            "Sistema de Navegación\nVersión 1.0\n\nUn sistema para calcular rutas entre nodos."
        )

    # ----------------------------------------------------------------
    # Métodos auxiliares llamados por los botones
    # ----------------------------------------------------------------
    def _agregar(self):
        if self.controlador:
            self.controlador.agregar(self.nombre.get(), self.lat.get(), self.lon.get())
            self.status_bar.config(text="Nodo agregado")

    def _editar(self):
        if self.controlador and self.lista.curselection():
            seleccionado = self.lista.get(tk.ACTIVE)
            self.controlador.editar(seleccionado, self.lat.get(), self.lon.get())
            self.status_bar.config(text="Nodo editado")

    def _eliminar(self):
        if self.controlador and self.lista.curselection():
            seleccionado = self.lista.get(tk.ACTIVE)
            self.controlador.eliminar(seleccionado)
            self.status_bar.config(text="Nodo eliminado")

    def _agregar_arista(self):
        if self.controlador:
            self.controlador.agregar_arista(
                self.origen.get(), 
                self.destino.get(), 
                self.bidireccional.get()
            )
            self.status_bar.config(text="Camino agregado")

    def _eliminar_arista(self):
        if self.controlador:
            self.controlador.eliminar_arista(self.origen.get(), self.destino.get())
            self.status_bar.config(text="Camino eliminado")

    def _agregar_waypoint(self):
        """Agrega un punto intermedio a la lista."""
        punto = self.waypoint_entry.get().strip()
        if punto and punto in self.controlador.grafo.nodos:
            self.waypoints_list.insert(tk.END, punto)
            self.waypoint_entry.delete(0, tk.END)
            self.status_bar.config(text=f"Punto intermedio '{punto}' agregado")
        elif punto:
            self.mostrar_error(f"El nodo '{punto}' no existe")

    def _eliminar_waypoint(self):
        """Elimina el punto intermedio seleccionado."""
        if self.waypoints_list.curselection():
            index = self.waypoints_list.curselection()[0]
            punto = self.waypoints_list.get(index)
            self.waypoints_list.delete(index)
            self.status_bar.config(text=f"Punto intermedio '{punto}' eliminado")

    def _mover_waypoint_arriba(self):
        """Mueve el punto intermedio seleccionado una posición arriba."""
        if not self.waypoints_list.curselection():
            return
        index = self.waypoints_list.curselection()[0]
        if index > 0:
            punto = self.waypoints_list.get(index)
            self.waypoints_list.delete(index)
            self.waypoints_list.insert(index - 1, punto)
            self.waypoints_list.selection_set(index - 1)

    def _mover_waypoint_abajo(self):
        """Mueve el punto intermedio seleccionado una posición abajo."""
        if not self.waypoints_list.curselection():
            return
        index = self.waypoints_list.curselection()[0]
        if index < self.waypoints_list.size() - 1:
            punto = self.waypoints_list.get(index)
            self.waypoints_list.delete(index)
            self.waypoints_list.insert(index + 1, punto)
            self.waypoints_list.selection_set(index + 1)

    def _limpiar_waypoints(self):
        """Limpia todos los puntos intermedios."""
        self.waypoints_list.delete(0, tk.END)
        self.status_bar.config(text="Puntos intermedios limpiados")

    def _calcular_ruta(self):
        """Calcula la ruta considerando los puntos intermedios."""
        if self.controlador:
            inicio = self.inicio.get()
            fin = self.fin.get()
            
            # Obtener todos los puntos intermedios
            waypoints = list(self.waypoints_list.get(0, tk.END))
            
            # Verificar que los puntos existan
            todos_puntos = [inicio] + waypoints + [fin]
            for punto in todos_puntos:
                if punto not in self.controlador.grafo.nodos:
                    self.mostrar_error(f"El nodo '{punto}' no existe")
                    return
            
            # Calcular la ruta con puntos intermedios
            self.controlador.calcular_ruta_con_paradas(inicio, fin, waypoints)
            self.status_bar.config(text="Ruta calculada con puntos intermedios")

    # ----------------------------------------------------------------
    # API que el controlador usa para actualizar la vista
    # ----------------------------------------------------------------
    def set_controlador(self, controlador) -> None:
        self.controlador = controlador

    def actualizar_lista(self, nombres) -> None:
        self.lista.delete(0, tk.END)
        for n in sorted(nombres):
            self.lista.insert(tk.END, n)
        self.status_bar.config(text=f"Lista actualizada: {len(nombres)} nodos")

    def actualizar_aristas(self, aristas, camino=None) -> None:
        # Limpiar el mapa
        self.ax.clear()
        
        # Configurar estilo del mapa
        self.ax.set_title("Mapa de Nodos y Caminos", fontsize=12, pad=20)
        self.ax.set_xlabel("Longitud", fontsize=10, labelpad=10)
        self.ax.set_ylabel("Latitud", fontsize=10, labelpad=10)
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Dibujar nodos con mejor estilo
        for nombre, nodo in self.controlador.grafo.nodos.items():
            if camino and nombre in camino:
                self.ax.plot(nodo.longitud, nodo.latitud, 'go', markersize=10, alpha=0.8)
            else:
                self.ax.plot(nodo.longitud, nodo.latitud, 'bo', markersize=8, alpha=0.6)
            self.ax.text(nodo.longitud, nodo.latitud, nombre, 
                        fontsize=9, ha='center', va='bottom',
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=2))

        # Dibujar aristas con mejor estilo
        for origen, destino, peso, bidireccional in aristas:
            nodo_origen = self.controlador.grafo.nodos[origen]
            nodo_destino = self.controlador.grafo.nodos[destino]
            
            es_camino_corto = False
            if camino:
                for i in range(len(camino) - 1):
                    if (camino[i] == origen and camino[i + 1] == destino) or \
                       (camino[i] == destino and camino[i + 1] == origen):
                        es_camino_corto = True
                        break
            
            # Líneas más gruesas y mejor estilo
            color = '#2ecc71' if es_camino_corto else '#3498db'
            alpha = 0.8 if es_camino_corto else 0.5
            linewidth = 2 if es_camino_corto else 1.5
            
            self.ax.plot([nodo_origen.longitud, nodo_destino.longitud],
                        [nodo_origen.latitud, nodo_destino.latitud], 
                        color=color, alpha=alpha, linewidth=linewidth)
            
            if not bidireccional:
                mid_x = (nodo_origen.longitud + nodo_destino.longitud) / 2
                mid_y = (nodo_origen.latitud + nodo_destino.latitud) / 2
                dx = nodo_destino.longitud - nodo_origen.longitud
                dy = nodo_destino.latitud - nodo_origen.latitud
                self.ax.arrow(mid_x, mid_y, dx/4, dy/4, 
                            head_width=0.02, head_length=0.02, 
                            fc=color, ec=color, alpha=alpha)

        # Ajustar límites del mapa con margen
        if self.controlador.grafo.nodos:
            lats = [n.latitud for n in self.controlador.grafo.nodos.values()]
            lons = [n.longitud for n in self.controlador.grafo.nodos.values()]
            self.ax.set_xlim(min(lons) - 0.1, max(lons) + 0.1)
            self.ax.set_ylim(min(lats) - 0.1, max(lats) + 0.1)

        # Mejorar el aspecto general del mapa
        self.fig.tight_layout()
        self.canvas.draw()

    def mostrar_ruta(self, texto: str) -> None:
        self.lbl_ruta.config(text=texto)

    def mostrar_error(self, mensaje: str) -> None:
        messagebox.showerror("Error", mensaje)
        self.status_bar.config(text=f"Error: {mensaje}")


# --------------------------------------------------------------------
# Punto de entrada
# --------------------------------------------------------------------
def main():
    vista = Vista()
    # importación diferida para evitar ciclo
    from controlador.controlador import Controlador

    Controlador(vista)
    vista.mainloop()


if __name__ == "__main__":
    main()
