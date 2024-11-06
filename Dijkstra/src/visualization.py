


import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.table import Table
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.animation import FuncAnimation

def dessiner_graphe(graphe, chemin_optimal=None, distance_totale=None, etapes=None):
    G = nx.DiGraph()

    # Ajouter les noeuds et liens dans le graphe
    for noeud in graphe.noeuds:
        G.add_node(noeud.id)
    for lien in graphe.liens:
        G.add_edge(lien.source.id, lien.destination.id, weight=lien.calculer_cout())

    # Position des noeuds
    pos = nx.circular_layout(G)
    router_image = plt.imread("src/1918.png")

    # Dessiner le graphe
    fig, ax = plt.subplots(figsize=(12, 6))
    for node in G.nodes:
        x, y = pos[node]
        ab = AnnotationBbox(OffsetImage(router_image, zoom=0.1), (x, y), frameon=False)
        ax.add_artist(ab)

    nx.draw_networkx_edges(G, pos, arrows=True, ax=ax)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif', ax=ax)

    # Visualiser le chemin optimal en rouge
    if chemin_optimal:
        edges_to_highlight = [(chemin_optimal[i].id, chemin_optimal[i+1].id) for i in range(len(chemin_optimal) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges_to_highlight, edge_color='red', width=2, ax=ax)

    # Afficher un tableau des étapes de Dijkstra
    if etapes:
        tableau_ax = fig.add_axes([0.75, 0.1, 0.2, 0.8])  # Emplacement du tableau
        tableau = Table(tableau_ax, bbox=[0, 0, 1, 1])
        tableau_ax.axis('off')

        # En-têtes du tableau
        headers = ["Nœud", "Distance", "File des distances"]
        tableau.add_row(headers, loc='center', cellLoc='center', fontsize=10, edgecolor="black", facecolor="lightgrey")

        # Ajout des étapes
        for etape in etapes:
            noeud_id, distance, file_distances = etape
            file_distances_str = ', '.join([f"{n}:{d}" for n, d in file_distances])
            row = [str(noeud_id), f"{distance:.2f}", file_distances_str]
            tableau.add_row(row, cellLoc='center', fontsize=9, edgecolor="black", facecolor="white")

        tableau_ax.add_table(tableau)

    plt.title("Visualisation du Graphe avec les étapes de Dijkstra")
    plt.axis('off')

    # Animation du chemin optimal
    if chemin_optimal:
        def update(frame):
            # Effacer les anciennes arêtes mises en évidence
            ax.clear()
            for node in G.nodes:
                x, y = pos[node]
                ab = AnnotationBbox(OffsetImage(router_image, zoom=0.1), (x, y), frameon=False)
                ax.add_artist(ab)
            nx.draw_networkx_edges(G, pos, arrows=True, ax=ax)
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
            nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif', ax=ax)

            # Mettre en évidence les arêtes du chemin optimal jusqu'à l'étape actuelle
            edges_to_highlight = [(chemin_optimal[i].id, chemin_optimal[i+1].id) for i in range(frame)]
            nx.draw_networkx_edges(G, pos, edgelist=edges_to_highlight, edge_color='red', width=2, ax=ax)

        ani = FuncAnimation(fig, update, frames=len(chemin_optimal) + 1, interval=1000, repeat=False)
        plt.show()

    else:
        plt.show()

