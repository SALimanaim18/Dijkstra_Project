class Noeud:
    def __init__(self, id: int, type: str, coordonnees: tuple, etat: bool = True):
        self.id = id
        self.type = type
        self.coordonnees = coordonnees
        self.etat = etat
        self.voisins = []

    def ajouter_voisin(self, lien):
        self.voisins.append(lien)

    def obtenir_voisins(self):
        return self.voisins

    def est_actif(self):
        return self.etat

    def activer(self):
        self.etat = True

    def desactiver(self):
        self.etat = False

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Noeud):
            return self.id == other.id
        return False

    def __lt__(self, other):
        if isinstance(other, Noeud):
            return self.id < other.id  # Comparer par identifiant pour la file de priorité
        return NotImplemented



class Lien:
    def __init__(self, source: Noeud, destination: Noeud, capacite_max: float, latence: float, bande_passante: float, charge: float, fiabilite: float):
        self.source = source
        self.destination = destination
        self.capacite_max = capacite_max
        self.latence = latence
        self.bande_passante = bande_passante
        self.charge = charge
        self.fiabilite = fiabilite

    def calculer_cout(self):
        return self.latence + (self.charge / self.bande_passante)

    def mettre_a_jour(self, nouvelle_charge: float, nouvelle_fiabilite: float):
        self.charge = nouvelle_charge
        self.fiabilite = nouvelle_fiabilite


class Graphe:
    def __init__(self):
        self.noeuds = []
        self.liens = []

    def ajouter_noeud(self, noeud: Noeud):
        self.noeuds.append(noeud)

    

    def supprimer_noeud(self, noeud: Noeud):
        self.noeuds.remove(noeud)
        self.liens = [lien for lien in self.liens if lien.source != noeud and lien.destination != noeud]

    def supprimer_lien(self, lien):
        self.liens.remove(lien)

    def initialiser_graphe(self):
        self.noeuds = []
        self.liens = []

    def afficher_graphe(self):
        for lien in self.liens:
            print(f"{lien.source.id} -> {lien.destination.id} (Cout: {lien.calculer_cout()})")

    def trouver_noeud(self, id_noeud):
        """Recherche un nœud par son ID et le retourne, ou None s'il n'est pas trouvé."""
        for noeud in self.noeuds:
            if noeud.id == id_noeud:
                return noeud
        return None   
    def ajouter_lien(self, lien: Lien):
        self.liens.append(lien)
        lien.source.ajouter_voisin(lien)  # Ajout du lien aux voisins du nœud source