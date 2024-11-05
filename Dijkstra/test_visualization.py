import unittest
from graph import Graphe, Noeud, Lien
from visualization import dessiner_graphe
import matplotlib.pyplot as plt

class TestVisualization(unittest.TestCase):

    def setUp(self):
        # Configuration d'un graphe de test
        self.noeud1 = Noeud(id=1, type="Routeur", coordonnees=(0, 0))
        self.noeud2 = Noeud(id=2, type="Switch", coordonnees=(1, 1))
        self.noeud3 = Noeud(id=3, type="Serveur", coordonnees=(2, 2))
        
        self.lien1 = Lien(source=self.noeud1, destination=self.noeud2, capacite_max=100, latence=5, bande_passante=10, charge=2, fiabilite=0.99)
        self.lien2 = Lien(source=self.noeud2, destination=self.noeud3, capacite_max=200, latence=2, bande_passante=20, charge=4, fiabilite=0.95)
        
        self.graphe = Graphe()
        self.graphe.ajouter_noeud(self.noeud1)
        self.graphe.ajouter_noeud(self.noeud2)
        self.graphe.ajouter_noeud(self.noeud3)
        self.graphe.ajouter_lien(self.lien1)
        self.graphe.ajouter_lien(self.lien2)

    def test_dessiner_graphe(self):
        # Vérifie que la fonction de visualisation peut être exécutée sans erreur
        try:
            dessiner_graphe(self.graphe)
        except Exception as e:
            self.fail(f"dessiner_graphe a levé une exception : {e}")

if __name__ == '__main__':
    unittest.main()
