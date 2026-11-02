"""
Problema de los Misioneros y Caníbales.

Este programa modela el problema clásico de transportar a tres
misioneros y tres caníbales de una orilla a otra mediante un bote
con capacidad máxima de dos personas.

Representación del estado:
    (misioneros_izq, canibales_izq, bote_izq)

Donde:
    - misioneros_izq: cantidad de misioneros en la orilla izquierda.
    - canibales_izq: cantidad de caníbales en la orilla izquierda.
    - bote_izq: 1 si el bote está a la izquierda y 0 si está a la derecha.

Posteriormente se implementarán los algoritmos de búsqueda BFS y DFS.
"""

# Cantidad total de misioneros y caníbales.
N = 3

# Capacidad máxima del bote.
CAPACIDAD = 2

# Estado inicial: todos están en la orilla izquierda.
S0 = (N, N, 1)

# Estado objetivo: todos están en la orilla derecha.
META = (0, 0, 0)


def es_seguro(s):
    """
    Verifica si un estado cumple las restricciones del problema.

    Un estado es seguro cuando:
        - Las cantidades de personas están dentro de los límites.
        - El bote se encuentra en una de las dos orillas.
        - Los caníbales nunca superan en número a los misioneros
          en una orilla donde haya misioneros.

    Parámetros:
        s (tuple): Estado representado por (m, c, b).

    Retorna:
        bool: True si el estado es válido y seguro; False en caso contrario.
    """
    m, c, b = s

    # Validar cantidades y posición del bote.
    if not (0 <= m <= N and 0 <= c <= N):
        return False

    if b not in (0, 1):
        return False

    # Calcular las personas que están en la orilla derecha.
    m_der = N - m
    c_der = N - c

    # Comprobar la seguridad de ambas orillas.
    seguro_izq = (m == 0) or (m >= c)
    seguro_der = (m_der == 0) or (m_der >= c_der)

    return seguro_izq and seguro_der