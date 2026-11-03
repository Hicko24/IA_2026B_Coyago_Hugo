"""
Experimento adicional: sensibilidad de BFS y DFS al orden de las acciones.

Prueba las 120 permutaciones del orden en que se listan las acciones y
resume longitud del camino, nodos expandidos y frontera maxima.

Uso:  python3 experimento_orden.py   (en la misma carpeta que misioneros_canibales.py)
"""
import itertools

import misioneros_canibales as mc

base = list(mc.TODAS_LAS_ACCIONES)
resumen = {"BFS": {"longitud": set(), "expandidos": set(), "frontera": set()},
           "DFS": {"longitud": set(), "expandidos": set(), "frontera": set()}}

for orden in itertools.permutations(base):
    mc.TODAS_LAS_ACCIONES[:] = list(orden)    # cambia el orden en el modulo
    for nombre, algoritmo in (("BFS", mc.bfs), ("DFS", mc.dfs)):
        acciones, _, _, expandidos, frontera_max = algoritmo()
        resumen[nombre]["longitud"].add(len(acciones))
        resumen[nombre]["expandidos"].add(expandidos)
        resumen[nombre]["frontera"].add(frontera_max)

print("Permutaciones probadas:", len(list(itertools.permutations(base))))
for nombre, datos in resumen.items():
    print(nombre,
          "| longitudes:", sorted(datos["longitud"]),
          "| expandidos:", sorted(datos["expandidos"]),
          "| frontera max:", sorted(datos["frontera"]))