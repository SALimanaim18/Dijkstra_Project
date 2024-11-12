import unittest
from src.visualization import dessiner_graphe
from src.graph import Graphe, Noeud, Lien

class TestVisualization(unittest.TestCase):

    def setUp(self):
        # Initialisation d'un graphe pour les tests
        self.graphe = Graphe()
        self.noeud1 = Noeud(1, "Type1", (0, 0), True)
        self.noeud2 = Noeud(2, "Type2", (1, 1), True)
        self.lien = Lien(self.noeud1, self.noeud2, 10, 1, 5, 0, 0.9)

        self.graphe.ajouter_noeud(self.noeud1)
        self.graphe.ajouter_noeud(self.noeud2)
        self.graphe.ajouter_lien(self.lien)

    def test_dessiner_graphe(self):
        # Ici nous ne pouvons pas réellement tester le dessin,
        # mais nous pouvons vérifier que la fonction ne lève pas d'erreur.
        try:
            dessiner_graphe(self.graphe)
        except Exception as e:
            self.fail(f"dessiner_graphe a levé une exception: {e}")

if __name__ == '__main__':
    unittest.main()
