import unittest
from src.graph import Graphe, Noeud, Lien

class TestGraphe(unittest.TestCase):

    def setUp(self):
        # Initialisation d'un graphe pour les tests
        self.graphe = Graphe()
        self.noeud1 = Noeud(1, "Type1", (0, 0), True)
        self.noeud2 = Noeud(2, "Type2", (1, 1), True)
        self.lien = Lien(self.noeud1, self.noeud2, 10, 1, 5, 0, 0.9)

        self.graphe.ajouter_noeud(self.noeud1)
        self.graphe.ajouter_noeud(self.noeud2)
        self.graphe.ajouter_lien(self.lien)

    def test_ajouter_noeud(self):
        noeud3 = Noeud(3, "Type3", (2, 2), True)
        self.graphe.ajouter_noeud(noeud3)
        self.assertIn(noeud3, self.graphe.noeuds)

    def test_supprimer_noeud(self):
        self.graphe.supprimer_noeud(self.noeud1)
        self.assertNotIn(self.noeud1, self.graphe.noeuds)

    def test_ajouter_lien(self):
        noeud3 = Noeud(3, "Type3", (2, 2), True)
        self.graphe.ajouter_noeud(noeud3)
        lien2 = Lien(self.noeud2, noeud3, 5, 1, 5, 0, 0.9)
        self.graphe.ajouter_lien(lien2)
        self.assertIn(lien2, self.graphe.liens)

    def test_supprimer_lien(self):
        self.graphe.supprimer_lien(self.lien)
        self.assertNotIn(self.lien, self.graphe.liens)

if __name__ == '__main__':
    unittest.main()
