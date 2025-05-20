from modelo.grafo import Grafo
import json


class Controlador:
    """
    Orquesta la interacción entre la vista (interfaz) y el modelo (grafo).
    """

    def __init__(self, vista):
        self.vista = vista
        self.grafo = Grafo()
        # la vista nos necesita para llamar a las acciones
        self.vista.set_controlador(self)

    # ---------- CRUD sobre nodos ------------------------------------
    def agregar(self, nombre: str, lat: str, lon: str):
        try:
            self.grafo.agregar_nodo(nombre, float(lat), float(lon))
            self.vista.actualizar_lista(self.grafo.nodos.keys())
            self.vista.actualizar_aristas(self.grafo.obtener_aristas())
        except Exception as e:
            self.vista.mostrar_error(str(e))

    def editar(self, nombre: str, lat: str, lon: str):
        try:
            self.grafo.editar_nodo(nombre, float(lat), float(lon))
            self.vista.actualizar_lista(self.grafo.nodos.keys())
            self.vista.actualizar_aristas(self.grafo.obtener_aristas())
        except Exception as e:
            self.vista.mostrar_error(str(e))

    def eliminar(self, nombre: str):
        try:
            self.grafo.eliminar_nodo(nombre)
            self.vista.actualizar_lista(self.grafo.nodos.keys())
            self.vista.actualizar_aristas(self.grafo.obtener_aristas())
        except Exception as e:
            self.vista.mostrar_error(str(e))

    # ---------- CRUD sobre aristas ----------------------------------
    def agregar_arista(self, origen: str, destino: str, bidireccional: bool = True):
        try:
            self.grafo.agregar_arista(origen, destino, bidireccional)
            self.vista.actualizar_aristas(self.grafo.obtener_aristas())
        except Exception as e:
            self.vista.mostrar_error(str(e))

    def eliminar_arista(self, origen: str, destino: str):
        try:
            self.grafo.eliminar_arista(origen, destino)
            self.vista.actualizar_aristas(self.grafo.obtener_aristas())
        except Exception as e:
            self.vista.mostrar_error(str(e))

    # ---------- rutas -----------------------------------------------
    def calcular_ruta(self, inicio: str, fin: str):
        try:
            resultado = self.grafo.dijkstra(inicio, fin)
            if resultado is None:
                self.vista.mostrar_ruta("No existe una ruta entre los nodos seleccionados.")
                self.vista.actualizar_aristas(self.grafo.obtener_aristas())
            else:
                camino, distancia = resultado
                texto = f"Ruta: {' → '.join(camino)} | Distancia: {distancia:.2f}"
                self.vista.mostrar_ruta(texto)
                self.vista.actualizar_aristas(self.grafo.obtener_aristas(), camino)
        except Exception as e:
            self.vista.mostrar_error(str(e))

    def calcular_ruta_con_paradas(self, inicio: str, fin: str, waypoints: list):
        """
        Calcula una ruta que pasa por todos los puntos intermedios en el orden especificado.
        
        Args:
            inicio: Nodo inicial
            fin: Nodo final
            waypoints: Lista de nodos intermedios por los que debe pasar la ruta
        """
        try:
            # Lista para almacenar todas las rutas parciales
            rutas_parciales = []
            distancia_total = 0
            
            # Calcular ruta desde el inicio hasta el primer waypoint
            puntos = [inicio] + waypoints + [fin]
            
            for i in range(len(puntos) - 1):
                resultado = self.grafo.dijkstra(puntos[i], puntos[i + 1])
                if resultado is None:
                    self.vista.mostrar_ruta(f"No existe una ruta entre {puntos[i]} y {puntos[i + 1]}.")
                    self.vista.actualizar_aristas(self.grafo.obtener_aristas())
                    return
                
                camino, distancia = resultado
                rutas_parciales.append(camino)
                distancia_total += distancia
            
            # Combinar todas las rutas parciales
            ruta_completa = []
            for i, ruta in enumerate(rutas_parciales):
                if i == 0:
                    ruta_completa.extend(ruta)
                else:
                    # Evitar duplicar el punto de conexión
                    ruta_completa.extend(ruta[1:])
            
            # Mostrar la ruta completa
            texto = f"Ruta: {' → '.join(ruta_completa)} | Distancia total: {distancia_total:.2f}"
            self.vista.mostrar_ruta(texto)
            self.vista.actualizar_aristas(self.grafo.obtener_aristas(), ruta_completa)
            
        except Exception as e:
            self.vista.mostrar_error(str(e))

    # ---------- persistencia ----------------------------------------
    def guardar_datos(self, ruta: str) -> None:
        """Guarda el grafo actual en un archivo JSON."""
        if not ruta:
            return  # operación cancelada
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(self.grafo.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.vista.mostrar_error(f"Error al guardar: {e}")

    def cargar_datos(self, ruta: str) -> None:
        """Carga un grafo desde un archivo JSON."""
        if not ruta:
            return  # operación cancelada
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.grafo = Grafo.from_dict(data)
            # Actualiza la vista
            self.vista.actualizar_lista(self.grafo.nodos.keys())
            self.vista.actualizar_aristas(self.grafo.obtener_aristas())
        except Exception as e:
            self.vista.mostrar_error(f"Error al cargar: {e}")
