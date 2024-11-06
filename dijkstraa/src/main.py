import json
from graph import Graphe, Noeud, Lien
from dijkstra import Dijkstra
from visualization import dessiner_graphe

def charger_graphe_depuis_fichier(chemin_fichier):
    """Charge un graphe à partir d'un fichier JSON."""
    graphe = Graphe()
    try:
        with open(chemin_fichier, 'r') as f:
            data = json.load(f)
            for noeud_data in data['noeuds']:
                noeud = Noeud(noeud_data['id'], noeud_data.get('type', ''), tuple(noeud_data['coordonnees']))
                graphe.ajouter_noeud(noeud)
            for lien_data in data['liens']:
                source = graphe.trouver_noeud(lien_data['source'])
                destination = graphe.trouver_noeud(lien_data['destination'])
                if source and destination:
                    lien = Lien(
                        source, destination,
                        lien_data['capacite_max'], lien_data['latence'],
                        lien_data['bande_passante'], lien_data['charge'],
                        lien_data['fiabilite']
                    )
                    graphe.ajouter_lien(lien)
    except FileNotFoundError:
        print("Le fichier n'a pas été trouvé. Vérifiez le chemin.")
    except json.JSONDecodeError:
        print("Erreur de lecture du fichier JSON.")
    return graphe

def saisie_manuelle_graphe():
    """Permet à l'utilisateur de saisir les nœuds et liens du graphe manuellement."""
    graphe = Graphe()
    print("Saisie des nœuds (entrer -1 pour arrêter)")
    while True:
        try:
            id_noeud = int(input("Entrez l'ID du nœud : "))
            if id_noeud == -1:
                break
            type_noeud = input("Type de nœud : ")
            coord_x = float(input("Coordonnée X : "))
            coord_y = float(input("Coordonnée Y : "))
            noeud = Noeud(id_noeud, type_noeud, (coord_x, coord_y))
            graphe.ajouter_noeud(noeud)
        except ValueError:
            print("Entrée invalide. Veuillez réessayer.")

    print("Saisie des liens (entrer -1 pour arrêter)")
    while True:
        try:
            source_id = int(input("ID du nœud source : "))
            if source_id == -1:
                break
            destination_id = int(input("ID du nœud destination : "))
            capacite_max = float(input("Capacité maximale : "))
            latence = float(input("Latence : "))
            bande_passante = float(input("Bande passante : "))
            charge = float(input("Charge : "))
            fiabilite = float(input("Fiabilité : "))
            source = graphe.trouver_noeud(source_id)
            destination = graphe.trouver_noeud(destination_id)
            if source and destination:
                lien = Lien(source, destination, capacite_max, latence, bande_passante, charge, fiabilite)
                graphe.ajouter_lien(lien)
            else:
                print("Nœud source ou destination introuvable.")
        except ValueError:
            print("Entrée invalide. Veuillez réessayer.")

    return graphe

def initialiser_donnees_statiques():
    """Initialise un graphe avec des données statiques."""
    graphe = Graphe()
    noeud1 = Noeud(1, "Type1", (0, 0))
    noeud2 = Noeud(2, "Type2", (1, 1))
    noeud3 = Noeud(3, "Type3", (2, 2))
    noeud4 = Noeud(4, "Type1", (3, 3))
    graphe.ajouter_noeud(noeud1)
    graphe.ajouter_noeud(noeud2)
    graphe.ajouter_noeud(noeud3)
    graphe.ajouter_noeud(noeud4)

    lien1 = Lien(noeud1, noeud2, 20, 10, 50, 5, 0.9)
    lien2 = Lien(noeud2, noeud3, 20, 2, 10, 0, 0.8)
    lien3 = Lien(noeud1, noeud3, 15, 1.5, 8, 0, 0.85)
    graphe.ajouter_lien(lien1)
    graphe.ajouter_lien(lien2)
    graphe.ajouter_lien(lien3)

    return graphe

def modifier_graphe(graphe):
    """Permet à l'utilisateur d'ajouter ou de supprimer des nœuds et des liens dans le graphe."""
    while True:
        choix = input("\n1 - Ajouter un nœud\n2 - Supprimer un nœud\n3 - Ajouter un lien\n4 - Supprimer un lien\n5 - Terminer les modifications\nVotre choix : ")
        if choix == '1':
            id_noeud = int(input("Entrez l'ID du nouveau nœud : "))
            type_noeud = input("Type de nœud : ")
            coord_x = float(input("Coordonnée X : "))
            coord_y = float(input("Coordonnée Y : "))
            noeud = Noeud(id_noeud, type_noeud, (coord_x, coord_y))
            graphe.ajouter_noeud(noeud)
        elif choix == '2':
            id_noeud = int(input("Entrez l'ID du nœud à supprimer : "))
            noeud = graphe.trouver_noeud(id_noeud)
            if noeud:
                graphe.supprimer_noeud(noeud)
            else:
                print("Nœud introuvable.")
        elif choix == '3':
            source_id = int(input("ID du nœud source : "))
            destination_id = int(input("ID du nœud destination : "))
            capacite_max = float(input("Capacité maximale : "))
            latence = float(input("Latence : "))
            bande_passante = float(input("Bande passante : "))
            charge = float(input("Charge : "))
            fiabilite = float(input("Fiabilité : "))
            source = graphe.trouver_noeud(source_id)
            destination = graphe.trouver_noeud(destination_id)
            if source and destination:
                lien = Lien(source, destination, capacite_max, latence, bande_passante, charge, fiabilite)
                graphe.ajouter_lien(lien)
            else:
                print("Nœud source ou destination introuvable.")
        elif choix == '4':
            source_id = int(input("ID du nœud source : "))
            destination_id = int(input("ID du nœud destination : "))
            source = graphe.trouver_noeud(source_id)
            destination = graphe.trouver_noeud(destination_id)
            if source and destination:
                lien = next((lien for lien in graphe.liens if lien.source == source and lien.destination == destination), None)
                if lien:
                    graphe.supprimer_lien(lien)
                else:
                    print("Lien introuvable.")
            else:
                print("Nœud source ou destination introuvable.")
        elif choix == '5':
            break
        else:
            print("Choix invalide.")

def main():
    print("Bienvenue dans l'application de routage !")
    choix = input("Choisissez une option :\n1 - Charger le graphe depuis un fichier JSON\n2 - Saisie manuelle du graphe\n3 - Utiliser des données statiques\nVotre choix : ")

    if choix == '1':
        chemin_fichier = input("Entrez le chemin du fichier JSON : ")
        graphe = charger_graphe_depuis_fichier(chemin_fichier)
    elif choix == '2':
        graphe = saisie_manuelle_graphe()
    elif choix == '3':
        graphe = initialiser_donnees_statiques()
        modifier_graphe(graphe)
    else:
        print("Choix invalide.")
        return

    # Saisie des nœuds d'origine et de destination
    try:
        origine_id = int(input("Entrez l'ID du nœud d'origine : "))
        destination_id = int(input("Entrez l'ID du nœud de destination : "))
        origine = graphe.trouver_noeud(origine_id)
        destination = graphe.trouver_noeud(destination_id)
        if origine is None or destination is None:
            print("Nœud d'origine ou de destination introuvable.")
            return

        # Calcul du chemin optimal avec Dijkstra
        chemin_optimal, distance_totale = Dijkstra.calculer_chemin_optimal(graphe, origine, destination)
        print("Chemin optimal:", [noeud.id for noeud in chemin_optimal])
        print("Distance totale:", distance_totale)

        # Visualisation du graphe avec le chemin optimal et la distance
        dessiner_graphe(graphe, chemin_optimal=chemin_optimal, distance_totale=distance_totale)

    except ValueError:
        print("Entrée invalide.")

if __name__ == "__main__":
    main()
