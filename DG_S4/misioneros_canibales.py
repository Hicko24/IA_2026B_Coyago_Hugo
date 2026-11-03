"""
Misioneros y Caníbales: búsqueda ciega (BFS y DFS).

Notación: s_0, Actions(s), Result(s, a), IsGoal(s), c(s, a, s').
Estado: s = (m_izq, c_izq, b_izq); b_izq = 1 si el bote está en la izquierda.

Convenciones de medición:
  - Un nodo se cuenta como 'expandido' cuando se extrae de la frontera y se
    generan sus sucesores. El test de meta se aplica al extraer el nodo.
  - 'frontera_max' es el mayor tamaño que alcanzó la frontera.
"""
from collections import deque

N = 3            # misioneros (y caníbales) totales
CAPACIDAD = 2    # capacidad máxima del bote

# Estado inicial s_0 y estado objetivo
S0 = (N, N, 1)
META = (0, 0, 0)


def es_seguro(s):
    """
    Comprueba si un estado es válido y seguro.

    Un estado es seguro si está dentro de rango y, en cada orilla, los
    misioneros no son superados en número por los caníbales (salvo que
    no haya misioneros en esa orilla).

    Parámetros:
        s (tuple): Estado (m, c, b).

    Retorna:
        bool: True si el estado es seguro; False en caso contrario.
    """
    m, c, _ = s
    if not (0 <= m <= N and 0 <= c <= N):
        return False

    m_der, c_der = N - m, N - c
    seguro_izq = (m == 0) or (m >= c)
    seguro_der = (m_der == 0) or (m_der >= c_der)
    return seguro_izq and seguro_der


# Generar todas las acciones posibles según la capacidad del bote.
TODAS_LAS_ACCIONES = [
    (m, c)
    for m in range(CAPACIDAD + 1)
    for c in range(CAPACIDAD + 1)
    if 1 <= m + c <= CAPACIDAD
]


def result(s, a):
    """
    Calcula el nuevo estado después de ejecutar una acción.

    Parámetros:
        s (tuple): Estado actual (m, c, b).
        a (tuple): Acción representada por (mover_m, mover_c).

    Retorna:
        tuple: Nuevo estado después del movimiento.
    """
    m, c, b = s
    mover_m, mover_c = a

    if b == 1:
        # El bote se desplaza de izquierda a derecha.
        nuevo_estado = (m - mover_m, c - mover_c, 0)
    else:
        # El bote se desplaza de derecha a izquierda.
        nuevo_estado = (m + mover_m, c + mover_c, 1)

    return nuevo_estado


def actions(s):
    """
    Obtiene las acciones legales disponibles desde un estado.

    Comprueba que existan suficientes personas en la orilla
    de salida y que el nuevo estado sea seguro.

    Parámetros:
        s (tuple): Estado actual (m, c, b).

    Retorna:
        list: Lista de acciones legales disponibles.
    """
    m, c, b = s
    acciones_validas = []

    for a in TODAS_LAS_ACCIONES:
        mover_m, mover_c = a

        # Verificar que existan suficientes personas para el traslado.
        if b == 1:
            if mover_m > m or mover_c > c:
                continue
        else:
            if mover_m > (N - m) or mover_c > (N - c):
                continue

        # Calcular el estado que produciría la acción.
        siguiente = result(s, a)

        # Aceptar únicamente los estados seguros.
        if es_seguro(siguiente):
            acciones_validas.append(a)

    return acciones_validas


def is_goal(s):
    """
    Comprueba si se alcanzó el estado objetivo.

    Parámetros:
        s (tuple): Estado que se desea comprobar.

    Retorna:
        bool: True si se alcanzó la meta; False en caso contrario.
    """
    return s == META


def cost(s, a, s2):
    """
    Calcula el costo de realizar una transición.

    Cada viaje del bote tiene un costo uniforme de 1.

    Parámetros:
        s (tuple): Estado de origen.
        a (tuple): Acción realizada.
        s2 (tuple): Estado resultante.

    Retorna:
        int: Costo de la transición.
    """
    return 1


def _reconstruir(padres, s):
    """
    Reconstruye la solución a partir del registro de padres.

    Parámetros:
        padres (dict): Mapa estado -> (estado_padre, acción) o None.
        s (tuple): Estado meta alcanzado.

    Retorna:
        tuple: (lista de acciones, lista de estados, costo total).
    """
    acciones, estados, costo = [], [s], 0
    while padres[s] is not None:
        s_padre, a = padres[s]
        costo += cost(s_padre, a, s)
        acciones.append(a)
        estados.append(s_padre)
        s = s_padre
    acciones.reverse()
    estados.reverse()
    return acciones, estados, costo


def bfs():
    """
    Búsqueda en anchura (BFS): la frontera es una cola FIFO.

    Retorna:
        tuple: (acciones, estados, costo, nodos expandidos, frontera máxima).
    """
    frontera = deque([S0])
    padres = {S0: None}               # estado -> (padre, acción)
    explorados = set()
    expandidos = 0
    frontera_max = 1

    while frontera:
        s = frontera.popleft()        # FIFO: el más antiguo primero
        if s in explorados:
            continue
        explorados.add(s)

        if is_goal(s):
            acciones, estados, costo = _reconstruir(padres, s)
            return acciones, estados, costo, expandidos, frontera_max

        expandidos += 1
        for a in actions(s):
            s2 = result(s, a)
            if s2 not in explorados and s2 not in padres:
                padres[s2] = (s, a)
                frontera.append(s2)
        frontera_max = max(frontera_max, len(frontera))

    return None, None, None, expandidos, frontera_max