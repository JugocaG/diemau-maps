import math
import heapq
from typing import Optional, Tuple, List, Dict


class Nodo:
    def __init__(self, nombre: str, latitud: float, longitud: float) -> None:
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud

    # distancia euclídea (suficiente para la demo; cambia a Haversine si usas coords reales)
    def distancia(self, otro: "Nodo") -> float:
        return math.sqrt(
            (self.latitud - otro.latitud) ** 2 + (self.longitud - otro.longitud) ** 2
        )


class Arista:
    def __init__(self, origen: str, destino: str, peso: float, bidireccional: bool = True) -> None:
        self.origen = origen
        self.destino = destino
        self.peso = peso
        self.bidireccional = bidireccional


class Grafo:
    def __init__(self) -> None:
        # nombre → Nodo
        self.nodos: Dict[str, Nodo] = {}
        # nombre → {vecino: peso}
        self.adyacencia: Dict[str, Dict[str, float]] = {}
        # Lista de aristas para mantener el registro de conexiones
        self.aristas: List[Arista] = []

    # ---------- CRUD de Nodos ----------------------------------------
    def agregar_nodo(self, nombre: str, latitud: float, longitud: float) -> None:
        if nombre in self.nodos:
            raise ValueError(f"El nodo «{nombre}» ya existe.")

        nuevo = Nodo(nombre, latitud, longitud)
        self.nodos[nombre] = nuevo
        self.adyacencia[nombre] = {}

    def editar_nodo(self, nombre: str, latitud: float, longitud: float) -> None:
        if nombre not in self.nodos:
            raise KeyError(f"No existe el nodo «{nombre}».")

        nodo = self.nodos[nombre]
        nodo.latitud, nodo.longitud = latitud, longitud

        # Actualiza los pesos de las aristas conectadas
        for arista in self.aristas:
            if arista.origen == nombre or arista.destino == nombre:
                self._actualizar_arista(arista)

    def eliminar_nodo(self, nombre: str) -> None:
        if nombre not in self.nodos:
            raise KeyError(f"No existe el nodo «{nombre}».")

        # Elimina todas las aristas conectadas al nodo
        self.aristas = [a for a in self.aristas 
                       if a.origen != nombre and a.destino != nombre]
        
        del self.nodos[nombre]
        del self.adyacencia[nombre]
        for vecinos in self.adyacencia.values():
            vecinos.pop(nombre, None)

    # ---------- CRUD de Aristas --------------------------------------
    def agregar_arista(self, origen: str, destino: str, bidireccional: bool = True) -> None:
        if origen not in self.nodos or destino not in self.nodos:
            raise KeyError("El nodo de origen o destino no existe.")
        
        if origen == destino:
            raise ValueError("No se puede conectar un nodo consigo mismo.")

        # Calcula la distancia entre los nodos
        peso = self.nodos[origen].distancia(self.nodos[destino])
        
        # Crea la arista
        arista = Arista(origen, destino, peso, bidireccional)
        self.aristas.append(arista)
        
        # Actualiza la matriz de adyacencia
        self.adyacencia[origen][destino] = peso
        if bidireccional:
            self.adyacencia[destino][origen] = peso

    def eliminar_arista(self, origen: str, destino: str) -> None:
        # Encuentra y elimina la arista
        self.aristas = [a for a in self.aristas 
                       if not (a.origen == origen and a.destino == destino)]
        
        # Actualiza la matriz de adyacencia
        if destino in self.adyacencia[origen]:
            del self.adyacencia[origen][destino]
        if origen in self.adyacencia[destino]:
            del self.adyacencia[destino][origen]

    def _actualizar_arista(self, arista: Arista) -> None:
        # Actualiza el peso de la arista basado en las nuevas posiciones
        peso = self.nodos[arista.origen].distancia(self.nodos[arista.destino])
        arista.peso = peso
        
        # Actualiza la matriz de adyacencia
        self.adyacencia[arista.origen][arista.destino] = peso
        if arista.bidireccional:
            self.adyacencia[arista.destino][arista.origen] = peso

    # ---------- Dijkstra --------------------------------------------
    def dijkstra(self, inicio: str, fin: str) -> Optional[Tuple[List[str], float]]:
        if inicio not in self.nodos or fin not in self.nodos:
            raise KeyError("El nodo de inicio o fin no existe.")

        dist: Dict[str, float] = {n: math.inf for n in self.nodos}
        previo: Dict[str, Optional[str]] = {n: None for n in self.nodos}

        dist[inicio] = 0
        cola: List[Tuple[float, str]] = [(0, inicio)]

        while cola:
            d, u = heapq.heappop(cola)
            if d > dist[u]:
                continue
            if u == fin:  # encontrado el destino
                break
            for v, peso in self.adyacencia[u].items():
                alt = d + peso
                if alt < dist[v]:
                    dist[v] = alt
                    previo[v] = u
                    heapq.heappush(cola, (alt, v))

        if dist[fin] is math.inf:
            return None  # no hay ruta

        # reconstruye camino
        camino: List[str] = []
        actual: Optional[str] = fin
        while actual is not None:
            camino.insert(0, actual)
            actual = previo[actual]
        return camino, dist[fin]

    def obtener_aristas(self) -> List[Tuple[str, str, float, bool]]:
        """Retorna una lista de tuplas (origen, destino, peso, bidireccional)"""
        return [(a.origen, a.destino, a.peso, a.bidireccional) for a in self.aristas]

    # ---------- Serialización --------------------------------------
    def to_dict(self) -> Dict:
        """Convierte el grafo a un diccionario serializable a JSON."""
        return {
            "nodos": [
                {
                    "nombre": nombre,
                    "lat": nodo.latitud,
                    "lon": nodo.longitud,
                }
                for nombre, nodo in self.nodos.items()
            ],
            "aristas": [
                {
                    "origen": a.origen,
                    "destino": a.destino,
                    "bidireccional": a.bidireccional,
                }
                for a in self.aristas
            ],
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Grafo":
        """Crea un grafo a partir de un diccionario con la misma estructura que produce to_dict."""
        grafo = cls()
        for nodo in data.get("nodos", []):
            grafo.agregar_nodo(nodo["nombre"], nodo["lat"], nodo["lon"])
        for arista in data.get("aristas", []):
            grafo.agregar_arista(
                arista["origen"],
                arista["destino"],
                arista.get("bidireccional", True),
            )
        return grafo
