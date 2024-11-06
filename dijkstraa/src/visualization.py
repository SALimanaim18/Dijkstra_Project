import matplotlib.pyplot as plt
import networkx as nx
from graph import Graphe, Noeud, Lien
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os

def dessiner_graphe(graphe, chemin_optimal=None, distance_totale=None):
    G = nx.DiGraph()

    # Ajouter les noeuds
    for noeud in graphe.noeuds:
        G.add_node(noeud.id)

    # Ajouter les liens avec les poids
    for lien in graphe.liens:
        G.add_edge(lien.source.id, lien.destination.id, weight=lien.calculer_cout())

    # Positionnement des noeuds
    pos = nx.circular_layout(G)

    # Charger l'image du routeur
    router_image = plt.imread("./1918.png")

    # Afficher les noeuds avec une image
    fig, ax = plt.subplots()
    for node in G.nodes:
        x, y = pos[node]
        ab = AnnotationBbox(OffsetImage(router_image, zoom=0.1), (x, y), frameon=False)
        ax.add_artist(ab)

    # Dessiner les arêtes sans flèches
    nx.draw_networkx_edges(G, pos, ax=ax, arrows=False)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)

    # Dessiner les étiquettes des noeuds
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif', ax=ax)

    # Ajouter des flèches manuelles pour chaque lien
    for (u, v, d) in G.edges(data=True):
        x_start, y_start = pos[u]
        x_end, y_end = pos[v]
        ax.annotate(
            "", xy=(x_end, y_end), xytext=(x_start, y_start),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.5),
        )

    # Afficher le chemin optimal et la distance
    if chemin_optimal and distance_totale is not None:
        chemin_text = "Chemin optimal: " + " -> ".join([str(noeud.id) for noeud in chemin_optimal])
        distance_text = f"Distance totale: {distance_totale}"
        plt.text(1.05, 0.5, chemin_text + "\n" + distance_text, transform=ax.transAxes, 
                 fontsize=12, verticalalignment='center', bbox=dict(boxstyle="round,pad=0.3", edgecolor="gray"))

    plt.title("Visualisation du Graphe avec Liens Orientés")
    plt.axis('off')  # Désactiver l'axe
    plt.show()
