from collections import defaultdict
import heapq
from graph import Graphe, Noeud, Lien


class Dijkstra:

 @staticmethod
 def calculer_chemin_optimal(graphe: Graphe, origine: Noeud, destination: Noeud):
    distances = {noeud: float('infinity') for noeud in graphe.noeuds}
    distances[origine] = 0
    priority_queue = [(0, origine)]
    chemin = {noeud: None for noeud in graphe.noeuds}

    while priority_queue:
        current_distance, current_noeud = heapq.heappop(priority_queue)

        if current_distance > distances[current_noeud]:
            continue

        for lien in current_noeud.voisins:
            distance = current_distance + lien.calculer_cout()

            if distance < distances[lien.destination]:
                distances[lien.destination] = distance
                chemin[lien.destination] = current_noeud
                heapq.heappush(priority_queue, (distance, lien.destination))

    # Vérifiez si le nœud de destination a été atteint
    if distances[destination] == float('infinity'):
        return [], distances[destination]

    chemin_optimal = []
    current_noeud = destination
    while current_noeud is not None:
        chemin_optimal.append(current_noeud)
        current_noeud = chemin[current_noeud]
    chemin_optimal.reverse()

    return chemin_optimal, distances[destination]
