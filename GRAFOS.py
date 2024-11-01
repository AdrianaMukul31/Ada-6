import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations

# Crear el grafo con rutas entre estados y sus costos de viaje
G = nx.Graph()
rutas = [
    ("Sonora", "Chihuahua", 120), ("Sonora", "Baja California", 80), ("Sonora", "Sinaloa", 60),
    ("Chihuahua", "Coahuila", 150), ("Coahuila", "Nuevo Leon", 100),
    ("Nuevo Leon", "Tamaulipas", 130), ("Tamaulipas", "Veracruz", 90),
    ("Sinaloa", "Veracruz", 70)
]
G.add_weighted_edges_from(rutas)

# Función para encontrar un ciclo Hamiltoniano (recorrido sin repetir)
def ciclo_hamiltoniano(grafo, inicio):
    estados = list(grafo.nodes())
    estados.remove(inicio)
    costo_min_ciclo = float('inf')
    
    # Probar todas las posibles rutas entre los estados para encontrar la más corta
    for perm in permutations(estados):
        costo = 0
        es_valido = True
        for u, v in zip((inicio, *perm), (*perm, inicio)):
            if grafo.has_edge(u, v):
                costo += grafo[u][v]['weight']
            else:
                es_valido = False
                break
        
        if es_valido:
            costo_min_ciclo = min(costo_min_ciclo, costo)
    
    # Si encontró un ciclo válido, devuelve el costo mínimo; si no, None
    return costo_min_ciclo if costo_min_ciclo != float('inf') else None

# Función DFS para encontrar un camino con repeticiones
def dfs_con_repetir(grafo, inicio):
    visitados, pila, costo_total = set(), [(inicio, 0)], 0
    while pila:
        estado, costo = pila.pop()
        costo_total += costo
        visitados.add(estado)
        for vecino, datos in grafo[estado].items():
            if vecino not in visitados or len(visitados) < len(grafo):
                pila.append((vecino, datos['weight']))
    return costo_total

# Resultados de los recorridos
estado_inicio = "Sonora"
costo_hamiltoniano = ciclo_hamiltoniano(G, estado_inicio)
costo_dfs_repetir = dfs_con_repetir(G, estado_inicio)

print(f"Costo del ciclo sin repetir: {costo_hamiltoniano}")
print(f"Costo del recorrido con repeticiones: {costo_dfs_repetir}")

# Dibujar el grafo con las rutas y sus costos
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightcoral', node_size=2000)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()
