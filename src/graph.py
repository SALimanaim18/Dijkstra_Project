import pandas as pds
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
        return self.latence + (self.charge) - (self.fiabilite) + (1 / self.bande_passante)

    def mettre_a_jour(self, nouvelle_charge: float, nouvelle_fiabilite: float):
        self.charge = nouvelle_charge
        self.fiabilite = nouvelle_fiabilite


class Graphe:
    def __init__(self, excel_path=None):
        self.noeuds = []
        self.liens = []
        if excel_path:
            self.charger_depuis_excel(excel_path)
    def charger_depuis_excel(self, excel_path):
        df = pds.read_excel(excel_path, sheet_name=None)
        noeuds_df = df["Noeuds"]
        liens_df = df["Liens"]
        
        # Create nodes
        for index, row in noeuds_df.iterrows():
            noeud = Noeud(
                id=row["id"],
                type=row["type"],
                coordonnees=(row["x"], row["y"]),
                etat=row["etat"]
            )
            self.ajouter_noeud(noeud)

        # Create links
        for index, row in liens_df.iterrows():
            source_noeud = self.get_noeud_by_id(row["source_id"])
            destination_noeud = self.get_noeud_by_id(row["destination_id"])
            if source_noeud and destination_noeud:
                lien = Lien(
                    source=source_noeud,
                    destination=destination_noeud,
                    capacite_max=row["capacite_max"],
                    latence=row["latence"],
                    bande_passante=row["bande_passante"],
                    charge=row["charge"],
                    fiabilite=row["fiabilite"]
                )
                self.ajouter_lien(lien)
    
    def ajouter_noeud(self, noeud: Noeud):
        self.noeuds.append(noeud)

    def get_noeud_by_id(self, id):
        for noeud in self.noeuds:
            if noeud.id == id:
                return noeud
        return None

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