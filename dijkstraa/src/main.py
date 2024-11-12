import json
from graph import Graphe, Noeud, Lien
from dijkstra import Dijkstra
from visualization import dessiner_graphe
import os

def charger_graphe_depuis_fichier(chemin_fichier):
    """Charge un graphe à partir d'un fichier JSON."""
    graphe = Graphe()
    try:
        with open(chemin_fichier, 'r') as f:
            data = json.load(f)
            for noeud_data in data['noeuds']:
                noeud = Noeud(noeud_data['id'], noeud_data.get('type', ''))
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
                else:
                    print(f"Lien non ajouté : {lien_data['source']} -> {lien_data['destination']} (nœud manquant)")
    except FileNotFoundError:
        print("Erreur : le fichier n'a pas été trouvé. Vérifiez le chemin.")
    except json.JSONDecodeError:
        print("Erreur de lecture du fichier JSON. Assurez-vous que le fichier est bien formaté.")
    return graphe

def saisie_manuelle_graphe():
    """Permet à l'utilisateur de saisir les nœuds et liens du graphe manuellement, en évitant les doublons."""
    graphe = Graphe()
    print("\n=== Saisie des nœuds ===\n")
    while True:
        id_noeud = input("Entrez l'ID du nœud (ou -1 pour terminer) : ")
        if id_noeud == "-1":
            break
        # Vérification des doublons
        if graphe.trouver_noeud(id_noeud):
            print(f"Erreur : un nœud avec l'ID {id_noeud} existe déjà.")
            continue
        type_noeud = input("Type de nœud : ")
        graphe.ajouter_noeud(Noeud(id_noeud, type_noeud))
        print(f"Nœud ajouté : {id_noeud} ({type_noeud})")

    print("\n=== Saisie des liens ===\n")
    while True:
        source_id = input("ID du nœud source (ou -1 pour terminer) : ")
        if source_id == "-1":
            break
        destination_id = input("ID du nœud destination : ")
        # Vérification des doublons pour les liens
        if source_id == destination_id:
            print("Erreur : le nœud source et le nœud destination ne peuvent pas être identiques.")
            continue
        try:
            capacite_max = float(input("Capacité maximale : "))
            latence = float(input("Latence : "))
            bande_passante = float(input("Bande passante : "))
            charge = float(input("Charge : "))
            fiabilite = float(input("Fiabilité : "))
            source = graphe.trouver_noeud(source_id)
            destination = graphe.trouver_noeud(destination_id)
            if source and destination:
                # Vérification si le lien existe déjà
                if any(lien.source == source and lien.destination == destination for lien in graphe.liens):
                    print("Erreur : un lien entre ces deux nœuds existe déjà.")
                    continue
                graphe.ajouter_lien(Lien(source, destination, capacite_max, latence, bande_passante, charge, fiabilite))
                print(f"Lien ajouté : {source_id} -> {destination_id}")
            else:
                print("Erreur : l'un des nœuds spécifiés est introuvable.")
        except ValueError:
            print("Erreur de saisie : veuillez entrer des valeurs numériques valides.")

    return graphe

def initialiser_donnees_statiques():
    """Initialise un graphe avec des données statiques."""
    graphe = Graphe()
    noeud1 = Noeud("1", "Type1")
    noeud2 = Noeud("2", "Type2")
    noeud3 = Noeud("3", "Type3")
    noeud4 = Noeud("4", "Type1")
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
    """Permet à l'utilisateur d'ajouter ou de supprimer des nœuds et des liens dans le graphe, en évitant les doublons."""
    while True:
        choix = input("\n1 - Ajouter un nœud\n2 - Supprimer un nœud\n3 - Ajouter un lien\n4 - Supprimer un lien\n5 - Terminer les modifications\nVotre choix : ")
        if choix == '1':
            id_noeud = input("Entrez l'ID du nouveau nœud : ")
            # Vérification des doublons
            if graphe.trouver_noeud(id_noeud):
                print(f"Erreur : un nœud avec l'ID {id_noeud} existe déjà.")
                continue
            type_noeud = input("Type de nœud : ")
            noeud = Noeud(id_noeud, type_noeud)
            graphe.ajouter_noeud(noeud)
            print(f"Nœud ajouté : {id_noeud} ({type_noeud})")
        elif choix == '2':
            id_noeud = input("Entrez l'ID du nœud à supprimer : ")
            noeud = graphe.trouver_noeud(id_noeud)
            if noeud:
                graphe.supprimer_noeud(noeud)
                print(f"Nœud {id_noeud} supprimé.")
            else:
                print("Nœud introuvable.")
        elif choix == '3':
            source_id = input("ID du nœud source : ")
            destination_id = input("ID du nœud destination : ")
            if source_id == destination_id:
                print("Erreur : le nœud source et le nœud destination ne peuvent pas être identiques.")
                continue
            capacite_max = float(input("Capacité maximale : "))
            latence = float(input("Latence : "))
            bande_passante = float(input("Bande passante : "))
            charge = float(input("Charge : "))
            fiabilite = float(input("Fiabilité : "))
            source = graphe.trouver_noeud(source_id)
            destination = graphe.trouver_noeud(destination_id)
            if source and destination:
                # Vérification si le lien existe déjà
                if any(lien.source == source and lien.destination == destination for lien in graphe.liens):
                    print("Erreur : un lien entre ces deux nœuds existe déjà.")
                    continue
                lien = Lien(source, destination, capacite_max, latence, bande_passante, charge, fiabilite)
                graphe.ajouter_lien(lien)
                print(f"Lien ajouté : {source_id} -> {destination_id}")
            else:
                print("Nœud source ou destination introuvable.")
        elif choix == '4':
            source_id = input("ID du nœud source : ")
            destination_id = input("ID du nœud destination : ")
            source = graphe.trouver_noeud(source_id)
            destination = graphe.trouver_noeud(destination_id)
            if source and destination:
                lien = next((lien for lien in graphe.liens if lien.source == source and lien.destination == destination), None)
                if lien:
                    graphe.supprimer_lien(lien)
                    print(f"Lien supprimé : {source_id} -> {destination_id}")
                else:
                    print("Lien introuvable.")
            else:
                print("Nœud source ou destination introuvable.")
        elif choix == '5':
            break
        else:
            print("Choix invalide. Veuillez réessayer.")


def main():
        print("=== Bienvenue dans l'application de routage ===")
    
    
        print("\nChoisissez une option pour initialiser le graphe (ou entrez 'q' pour quitter) :\n")
        print("1 - Charger le graphe depuis un fichier")
        print("2 - Saisie manuelle du graphe")
        print("3 - Utiliser des données statiques")
        choix = input("Votre choix : ")
        
        if choix == 'q':
            print("Merci d'avoir utilisé l'application. À bientôt !")
              # Quitte l'application si l'utilisateur entre 'q'
        
        if choix == '1':
            while True:
                ch = input("\nType de fichier :\n1 - JSON\n2 - Excel\nou 'q' pour quitter\nVotre choix : ")
                if ch == 'q':
                    print("Merci d'avoir utilisé l'application. À bientôt !")
                    return  # Quitte l'application si l'utilisateur entre 'q'
                elif ch == '1':
                    chemin_fichier = input("Entrez le chemin du fichier JSON : ")
                    # Vérification de l'extension du fichier
                    if not chemin_fichier.endswith('.json'):
                        print("Erreur : le fichier doit avoir l'extension .json.")
                        continue  # Redemande l'entrée si l'extension est invalide
                    graphe = charger_graphe_depuis_fichier(chemin_fichier)
                    break  # Sort de la boucle une fois que le fichier est chargé
                elif ch == '2':
                    chemin_fichier = input("Entrez le chemin du fichier Excel : ")
                    # Vérification de l'extension du fichier
                    if not chemin_fichier.endswith('.xlsx'):
                        print("Erreur : le fichier doit avoir l'extension .xlsx.")
                        continue  # Redemande l'entrée si l'extension est invalide
                    graphe = Graphe(chemin_fichier)  # Initialiser pour Excel si méthode disponible
                    break  # Sort de la boucle une fois que le fichier est chargé
                else:
                    print("Erreur : choix de fichier invalide.")
                    continue  # Redemande l'entrée si le choix est invalide

        elif choix == '2':
            graphe = saisie_manuelle_graphe()
             # Sort de la boucle une fois que la saisie manuelle est terminée

        elif choix == '3':
            graphe = initialiser_donnees_statiques()
            modifier_graphe(graphe)
             # Sort de la boucle une fois que l'initialisation est terminée

        else:
            print("Erreur : choix invalide.")
              # Redemande l'entrée si le choix est invalide

        print("\n=== Configuration du routage ===")
        while True:
            try:
                origine_id = input("Entrez l'ID du nœud d'origine (ou 'q' pour quitter) : ")
                if origine_id == 'q':
                    print("Merci d'avoir utilisé l'application. À bientôt !")
                    return  # Quitte l'application si l'utilisateur entre 'q'
                    
                destination_id = input("Entrez l'ID du nœud de destination (ou 'q' pour quitter) : ")
                if destination_id == 'q':
                    print("Merci d'avoir utilisé l'application. À bientôt !")
                    return  # Quitte l'application si l'utilisateur entre 'q'

                origine = graphe.trouver_noeud(origine_id)
                destination = graphe.trouver_noeud(destination_id)
                if origine is None or destination is None:
                    print("Erreur : nœud d'origine ou de destination introuvable.")
                    continue  # Redemande les entrées si les nœuds ne sont pas trouvés

                historique, distance_totale, chemin_optimal = Dijkstra.calculer_chemin_optimal(graphe, origine, destination)
                print("\n=== Résultat du chemin optimal ===")
                print("Chemin optimal : ", " -> ".join([noeud.id for noeud in chemin_optimal]))
                print("Distance totale : ", distance_totale if distance_totale < float('inf') else "Aucun chemin trouvé")
                dessiner_graphe(graphe, historique=historique, chemin_optimal=chemin_optimal, distance_totale=distance_totale)
                break  # Sort de la boucle une fois que tout est calculé et affiché

            except ValueError:
                print("Erreur de saisie : veuillez vérifier les données entrées.")
                continue  # Redemande l'entrée en cas d'erreur


if __name__ == "__main__":
    main()




# def main():
#     print("=== Bienvenue dans l'application de routage ===")
#     print("Choisissez une option pour initialiser le graphe :\n")
#     print("1 - Charger le graphe depuis un fichier")
#     print("2 - Saisie manuelle du graphe")
#     print("3 - Utiliser des données statiques")
#     choix = input("Votre choix : ")

#     if choix == '1':
#         ch = input("\nType de fichier :\n1 - JSON\n2 - Excel\nVotre choix : ")
#         if ch == '1':
#             chemin_fichier = input("Entrez le chemin du fichier JSON : ")
#             graphe = charger_graphe_depuis_fichier(chemin_fichier)
#         elif ch == '2':
#             chemin_fichier = input("Entrez le chemin du fichier Excel : ")
#             graphe = Graphe(chemin_fichier)  # Initialiser pour Excel si méthode disponible
#         else:
#             print("Erreur : choix de fichier invalide.")
#             return
#     elif choix == '2':
#         graphe = saisie_manuelle_graphe()
#     elif choix == '3':
#         graphe = initialiser_donnees_statiques()
#         modifier_graphe(graphe)
#     else:
#         print("Erreur : choix invalide.")
#         return

#     print("\n=== Configuration du routage ===")
#     try:
#         origine_id = input("Entrez l'ID du nœud d'origine : ")
#         destination_id = input("Entrez l'ID du nœud de destination : ")
#         origine = graphe.trouver_noeud(origine_id)
#         destination = graphe.trouver_noeud(destination_id)
#         if origine is None or destination is None:
#             print("Erreur : nœud d'origine ou de destination introuvable.")
#             return

#         historique, distance_totale, chemin_optimal = Dijkstra.calculer_chemin_optimal(graphe, origine, destination)
#         print("\n=== Résultat du chemin optimal ===")
#         print("Chemin optimal : ", " -> ".join([noeud.id for noeud in chemin_optimal]))
#         print("Distance totale : ", distance_totale if distance_totale < float('inf') else "Aucun chemin trouvé")
#         dessiner_graphe(graphe, historique=historique, chemin_optimal=chemin_optimal, distance_totale=distance_totale)

#     except ValueError:
#         print("Erreur de saisie : veuillez vérifier les données entrées.")

# if __name__ == "__main__":
#     main() 
