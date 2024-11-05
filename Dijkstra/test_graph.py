import unittest
from graph import Graphe, Noeud, Lien

class TestGraphe(unittest.TestCase):

    def setUp(self):
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

    def test_ajout_noeud(self):
        noeud4 = Noeud(id=4, type="Client", coordonnees=(3, 3))
        self.graphe.ajouter_noeud(noeud4)
        self.assertIn(noeud4, self.graphe.noeuds)

    def test_suppression_noeud(self):
        self.graphe.supprimer_noeud(self.noeud2)
        self.assertNotIn(self.noeud2, self.graphe.noeuds)
        for lien in self.graphe.liens:
            self.assertNotIn(self.noeud2, [lien.source, lien.destination])

    def test_ajout_lien(self):
        self.assertIn(self.lien1, self.graphe.liens)
        self.assertIn(self.lien2, self.graphe.liens)
        self.assertIn(self.lien1, self.noeud1.obtenir_voisins())

    def test_suppression_lien(self):
        self.graphe.supprimer_lien(self.lien1)
        self.assertNotIn(self.lien1, self.graphe.liens)

    def test_calcul_cout_lien(self):
        cout = self.lien1.calculer_cout()
        self.assertEqual(cout, 5 + (2 / 10))

    def test_activation_desactivation_noeud(self):
        self.noeud1.desactiver()
        self.assertFalse(self.noeud1.est_actif())
        self.noeud1.activer()
        self.assertTrue(self.noeud1.est_actif())

    def test_initialiser_graphe(self):
        self.graphe.initialiser_graphe()
        self.assertEqual(len(self.graphe.noeuds), 0)
        self.assertEqual(len(self.graphe.liens), 0)

    def test_affichage_graphe(self):
        # Juste pour s'assurer que la méthode ne lève pas d'erreurs
        try:
            self.graphe.afficher_graphe()
        except Exception as e:
            self.fail(f"afficher_graphe a levé une exception : {e}")

if __name__ == '__main__':
    unittest.main()
