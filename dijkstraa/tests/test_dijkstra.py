import unittest
from src.graph import Graphe, Noeud, Lien
from src.dijkstra import Dijkstra  # Assurez-vous que Dijkstra est importé

class TestDijkstra(unittest.TestCase):

    def setUp(self):
        # Initialisation d'un graphe pour les tests
        self.graphe = Graphe()
        self.noeud1 = Noeud(1, "Type1", (0, 0), True)
        self.noeud2 = Noeud(2, "Type2", (1, 1), True)
        self.noeud3 = Noeud(3, "Type3", (2, 2), True)
        self.noeud4 = Noeud(4, "Type4", (3, 3), True)

        self.graphe.ajouter_noeud(self.noeud1)
        self.graphe.ajouter_noeud(self.noeud2)
        self.graphe.ajouter_noeud(self.noeud3)
        self.graphe.ajouter_noeud(self.noeud4)

        self.lien1 = Lien(self.noeud1, self.noeud2, 1, 1, 1, 0, 1)
        self.lien2 = Lien(self.noeud2, self.noeud3, 2, 1, 1, 0, 1)
        self.lien3 = Lien(self.noeud1, self.noeud3, 2, 1, 1, 0, 1)
        self.lien4 = Lien(self.noeud3, self.noeud4, 1, 1, 1, 0, 1)

        self.graphe.ajouter_lien(self.lien1)
        self.graphe.ajouter_lien(self.lien2)
        self.graphe.ajouter_lien(self.lien3)
        self.graphe.ajouter_lien(self.lien4)

    def test_calculer_chemin_optimal(self):
        chemin, _ = Dijkstra.calculer_chemin_optimal(self.graphe, self.noeud1, self.noeud4)
        chemin_ids = [noeud.id for noeud in chemin]
        self.assertEqual(chemin_ids, [1, 2, 3, 4])

    def test_calculer_chemin_optimal_no_chemin(self):
        # Test d'un chemin inexistant
        chemin, _ = Dijkstra.calculer_chemin_optimal(self.graphe, self.noeud1, Noeud(5, "Type5", (4, 4), True))
        self.assertEqual(chemin, [])
    
    def test_calculer_chemin_optimal(self):
     chemin, _ = Dijkstra.calculer_chemin_optimal(self.graphe, self.noeud1, self.noeud4)
     chemin_ids = [noeud.id for noeud in chemin]
     self.assertEqual(chemin_ids, [1, 3, 4])  # Changez cela selon le chemin valide.

if __name__ == '__main__':
    unittest.main()
