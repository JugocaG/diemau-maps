# Sistema de Navegación

Una aplicación para la visualización y gestión de rutas mediante grafos, desarrollada con Python y Tkinter.

## Descripción

Este sistema permite la creación, manipulación y visualización de grafos para representar ubicaciones y conexiones entre ellas. Utilizando el algoritmo de Dijkstra, calcula las rutas más cortas entre diferentes puntos, lo que lo hace ideal para aplicaciones educativas o demostrativas de navegación.

## Características

- **Gestión de nodos**: Crear, editar y eliminar ubicaciones (nodos).
- **Gestión de caminos**: Establecer conexiones entre ubicaciones.
- **Cálculo de rutas**: Determinar el camino más corto entre dos puntos.
- **Rutas con paradas**: Calcular rutas optimizadas que pasan por puntos intermedios.
- **Visualización gráfica**: Representación visual de las ubicaciones y caminos.
- **Persistencia de datos**: Guardar y cargar configuraciones de grafo en formato JSON.

## Requisitos de Instalación

Para ejecutar la aplicación necesitarás:

1. **Python 3.6+**: La aplicación está desarrollada en Python.
2. **Tkinter**: Para la interfaz gráfica (incluido generalmente con Python).
3. **Matplotlib**: Para la visualización de grafos.

Instala las dependencias necesarias con:

```bash
pip install matplotlib
```

## Uso

1. **Ejecutar la aplicación**:

   ```bash
   python main.py
   ```

2. **Gestión de nodos**:

   - Para agregar un nodo: Introduce nombre, latitud y longitud, luego haz clic en "Agregar".
   - Para editar un nodo: Selecciona un nodo de la lista, modifica sus datos y haz clic en "Editar".
   - Para eliminar un nodo: Selecciona un nodo de la lista y haz clic en "Eliminar".

3. **Gestión de caminos**:

   - Para agregar un camino: Introduce los nombres de origen y destino, marca si es bidireccional y haz clic en "Agregar Camino".
   - Para eliminar un camino: Introduce los nombres de origen y destino y haz clic en "Eliminar Camino".

4. **Cálculo de rutas**:

   - Para calcular una ruta directa: Introduce origen y destino, luego haz clic en "Calcular Ruta".
   - Para calcular una ruta con paradas: Agrega los puntos intermedios en la lista de paradas y haz clic en "Calcular Ruta".

5. **Guardar y cargar datos**:
   - Usa el menú "Archivo" para guardar o cargar configuraciones de grafo.

## Ejemplo de Uso

La aplicación incluye un archivo de ejemplo `locations.json` que contiene una configuración predefinida con varias ubicaciones y conexiones. Puedes cargar este archivo desde el menú "Archivo" > "Cargar" para comenzar a explorar las funcionalidades.

## Estructura del Proyecto

- **main.py**: Punto de entrada de la aplicación.
- **modelo/grafo.py**: Implementación de las clases de grafo y algoritmos.
- **controlador/controlador.py**: Lógica de control y gestión de datos.
- **vista/interfaz.py**: Interfaz gráfica de usuario.
- **locations.json**: Archivo de ejemplo con ubicaciones predefinidas.

## Licencia

Este proyecto está disponible como software libre.
