
from graph import Graphe, Noeud, Lien
from dijkstra import Dijkstra
from visualization import dessiner_graphe

def main():
    # Création d'un graphe
    graphe = Graphe()

    # Ajout de noeuds
    noeud1 = Noeud(1, "Type1", (0, 0), True)
    noeud2 = Noeud(2, "Type2", (1, 1), True)
    noeud3 = Noeud(3, "Type3", (2, 2), True)
    noeud4 = Noeud(4, "Type1", (3, 3), True)
    noeud5 = Noeud(5, "Type2", (4, 4), True)
    noeud6 = Noeud(6, "Type3", (5, 5), True)

    graphe.ajouter_noeud(noeud1)
    graphe.ajouter_noeud(noeud2)
    graphe.ajouter_noeud(noeud3)
    graphe.ajouter_noeud(noeud4)
    graphe.ajouter_noeud(noeud5)
    graphe.ajouter_noeud(noeud6)

    

    # Ajout de liens supplémentaires pour un graphe plus connecté
    lien1 = Lien(noeud1, noeud2, 20, 10, 50, 5, 0.9)
    lien2 = Lien(noeud2, noeud3, 20, 2, 10, 0, 0.8)
    lien3 = Lien(noeud1, noeud3, 15, 1.5, 8, 0, 0.85)
    lien4 = Lien(noeud3, noeud4, 20, 5, 10, 0, 0.9)   # Nouveau lien
    lien5 = Lien(noeud4, noeud5, 20, 2, 10, 0, 0.8)   # Nouveau lien
    lien6 = Lien(noeud5, noeud6, 15, 1.5, 8, 0, 0.85) # Nouveau lien
    lien7 = Lien(noeud3, noeud6, 30, 5, 8, 0, 0.9)    # Nouveau lien direct

    graphe.ajouter_lien(lien1)
    graphe.ajouter_lien(lien2)
    graphe.ajouter_lien(lien3)
    graphe.ajouter_lien(lien4)
    graphe.ajouter_lien(lien5)
    graphe.ajouter_lien(lien6)
    graphe.ajouter_lien(lien7)
    
    
    # Vérification des voisins
    for noeud in graphe.noeuds:
        voisins = [lien.destination.id for lien in noeud.obtenir_voisins()]
        print(f"Noeud {noeud.id} voisins: {voisins}")

    # Calculer le chemin optimal
    try:
        chemin_optimal, distance_totale = Dijkstra.calculer_chemin_optimal(graphe, noeud1, noeud6)
        print("Chemin optimal:", [noeud.id for noeud in chemin_optimal])
        print("Distance totale:", distance_totale)
    except ValueError as e:
        print(f"Erreur lors du calcul du chemin: {e}")
        chemin_optimal = []
        distance_totale = float('inf')

    # Visualiser le graphe avec le chemin optimal et la distance
    dessiner_graphe(graphe, chemin_optimal=chemin_optimal, distance_totale=distance_totale)

if __name__ == "__main__":
    main()