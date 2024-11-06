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

def main():
    print("Bienvenue dans l'application de routage !")
    choix = input("Choisissez une option :\n1 - Charger le graphe depuis un fichier JSON\n2 - Saisie manuelle du graphe\nVotre choix : ")

    if choix == '1':
        chemin_fichier = input("Entrez le chemin du fichier JSON : ")
        graphe = charger_graphe_depuis_fichier(chemin_fichier)
    elif choix == '2':
        graphe = saisie_manuelle_graphe()
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









