import unittest
from graph import Graphe, Noeud, Lien
from dijkstra import Dijkstra

class TestDijkstra(unittest.TestCase):

    def setUp(self):
        # Créer un graphe pour les tests
        self.graphe = Graphe()

        # Créer des nœuds
        n1 = Noeud('A')
        n2 = Noeud('B')
        n3 = Noeud('C')
        n4 = Noeud('D')

        # Ajouter les nœuds au graphe
        self.graphe.ajouter_noeud(n1)
        self.graphe.ajouter_noeud(n2)
        self.graphe.ajouter_noeud(n3)
        self.graphe.ajouter_noeud(n4)

        # Créer des liens avec des poids
        l1 = Lien(n1, n2, 1)
        l2 = Lien(n2, n3, 2)
        l3 = Lien(n3, n4, 1)
        l4 = Lien(n1, n3, 4)

        # Ajouter les liens au graphe
        self.graphe.ajouter_lien(l1)
        self.graphe.ajouter_lien(l2)
        self.graphe.ajouter_lien(l3)
        self.graphe.ajouter_lien(l4)

    def test_chemin_optimal_existe(self):
        # Calculer le chemin optimal entre deux nœuds
        chemin, distance = Dijkstra.calculer_chemin_optimal(self.graphe, self.graphe.noeuds['A'], self.graphe.noeuds['D'])
        
        # Vérifier le chemin attendu
        self.assertEqual([noeud.id for noeud in chemin], ['A', 'B', 'C', 'D'])
        self.assertEqual(distance, 4)

    def test_chemin_inexistant(self):
        # Créer un nœud isolé
        n5 = Noeud('E')
        self.graphe.ajouter_noeud(n5)

        # Calculer le chemin vers un nœud isolé
        chemin, distance = Dijkstra.calculer_chemin_optimal(self.graphe, self.graphe.noeuds['A'], n5)
        
        # Vérifier qu'il n'y a pas de chemin
        self.assertEqual(chemin, [])
        self.assertEqual(distance, float('infinity'))

    def test_chemin_optimal_vers_soi_meme(self):
        # Calculer le chemin vers le même nœud
        chemin, distance = Dijkstra.calculer_chemin_optimal(self.graphe, self.graphe.noeuds['A'], self.graphe.noeuds['A'])
        
        # Vérifier que le chemin est uniquement le nœud lui-même et que la distance est 0
        self.assertEqual([noeud.id for noeud in chemin], ['A'])
        self.assertEqual(distance, 0)

if __name__ == '__main__':
    unittest.main()
