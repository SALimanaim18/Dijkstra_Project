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

        # Historique pour le tableau
        historique = []
        
        while priority_queue:
            current_distance, current_noeud = heapq.heappop(priority_queue)

            # Capture de l'état actuel pour le tableau
            etape = {noeud.id: (distances[noeud] if distances[noeud] != float('infinity') else '∞') for noeud in graphe.noeuds}
            etape["Nœud fixé"] = current_noeud.id
            historique.append(etape)

            if current_distance > distances[current_noeud]:
                continue

            # Mise à jour des voisins
            for lien in current_noeud.obtenir_voisins():
                distance = current_distance + lien.calculer_cout()
                
                if distance < distances[lien.destination]:
                    distances[lien.destination] = distance
                    chemin[lien.destination] = current_noeud
                    heapq.heappush(priority_queue, (distance, lien.destination))

        # Reconstruire le chemin optimal
        chemin_optimal = []
        noeud_courant = destination
        while noeud_courant is not None:
            chemin_optimal.append(noeud_courant)
            noeud_courant = chemin[noeud_courant]
        
        chemin_optimal.reverse()

        # Retourner l'historique, la distance totale, et le chemin optimal
        return historique, distances[destination], chemin_optimal
