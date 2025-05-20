"""
Punto de entrada de la aplicación.

Asume que los archivos:
    - grafo.py
    - controlador.py
    - interfaz.py
están en el mismo directorio que main.py.
"""

from vista.interfaz import Vista
from controlador.controlador import Controlador


def main() -> None:
    vista = Vista()
    Controlador(vista)  # inyecta el controlador en la vista
    vista.mainloop()    # lanza la GUI


if __name__ == "__main__":
    main()
