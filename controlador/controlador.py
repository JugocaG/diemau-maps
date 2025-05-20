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
        Calcula una ruta que pasa por todos los puntos intermedios en orden optimizado.
        
        Args:
            inicio: Nodo inicial
            fin: Nodo final
            waypoints: Lista de nodos intermedios por los que debe pasar la ruta
        """
        try:
            if not waypoints:
                # Si no hay puntos intermedios, simplemente calcula la ruta directa
                return self.calcular_ruta(inicio, fin)
                
            # Crear una matriz de distancias entre todos los puntos (incluidos inicio y fin)
            todos_puntos = [inicio] + waypoints + [fin]
            n_puntos = len(todos_puntos)
            
            # Matriz para almacenar distancias entre todos los pares de puntos
            matriz_distancias = {}
            caminos_entre_puntos = {}
            
            # Calcular las distancias entre todos los pares de puntos
            for i in range(n_puntos):
                origen = todos_puntos[i]
                for j in range(n_puntos):
                    if i == j:
                        continue
                    destino = todos_puntos[j]
                    resultado = self.grafo.dijkstra(origen, destino)
                    if resultado is None:
                        self.vista.mostrar_ruta(f"No existe una ruta entre {origen} y {destino}.")
                        self.vista.actualizar_aristas(self.grafo.obtener_aristas())
                        return
                    
                    camino, distancia = resultado
                    matriz_distancias[(origen, destino)] = distancia
                    caminos_entre_puntos[(origen, destino)] = camino
            
            # Encontrar la mejor secuencia de puntos intermedios
            # Para problemas pequeños, podemos probar todas las permutaciones
            # En problemas más grandes, se debería usar una heurística más sofisticada
            
            import itertools
            
            # Solo permutamos los waypoints (mantenemos inicio y fin fijos)
            mejor_distancia = float('inf')
            mejor_secuencia = None
            
            for perm in itertools.permutations(waypoints):
                secuencia_actual = [inicio] + list(perm) + [fin]
                distancia_total = 0
                
                # Calcular la distancia total de esta secuencia
                for i in range(len(secuencia_actual) - 1):
                    origen = secuencia_actual[i]
                    destino = secuencia_actual[i + 1]
                    distancia_total += matriz_distancias[(origen, destino)]
                
                # Actualizar la mejor secuencia si esta es mejor
                if distancia_total < mejor_distancia:
                    mejor_distancia = distancia_total
                    mejor_secuencia = secuencia_actual
            
            # Construir la ruta completa con la mejor secuencia
            ruta_completa = []
            for i in range(len(mejor_secuencia) - 1):
                origen = mejor_secuencia[i]
                destino = mejor_secuencia[i + 1]
                camino = caminos_entre_puntos[(origen, destino)]
                
                if i == 0:
                    ruta_completa.extend(camino)
                else:
                    # Evitar duplicar el punto de conexión
                    ruta_completa.extend(camino[1:])
            
            # Mostrar la ruta completa
            texto = f"Ruta optimizada: {' → '.join(ruta_completa)} | Distancia total: {mejor_distancia:.2f}"
            self.vista.mostrar_ruta(texto)
            self.vista.actualizar_aristas(self.grafo.obtener_aristas(), ruta_completa, mejor_secuencia)
            
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
