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