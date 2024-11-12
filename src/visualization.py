import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from graph import Graphe, Noeud, Lien
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import FancyArrowPatch

def dessiner_graphe(graphe, historique=None, chemin_optimal=None, distance_totale=None):
    G = nx.DiGraph()

    # Ajouter les noeuds
    for noeud in graphe.noeuds:
        G.add_node(noeud.id)

    # Ajouter les liens avec les poids
    for lien in graphe.liens:
        G.add_edge(lien.source.id, lien.destination.id, weight=lien.calculer_cout())

    # Positionnement des noeuds
    pos = nx.circular_layout(G)

    # Créer la figure et les axes
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [2, 1]})

    # Afficher les icônes de routeurs en premier
    router_image = plt.imread("src/1918.png")
    for node in G.nodes:
        x, y = pos[node]
        ab = AnnotationBbox(OffsetImage(router_image, zoom=0.07), (x, y), frameon=False)  # Taille réduite pour visibilité
        ax1.add_artist(ab)

    # Dessiner les arêtes en noir avec flèches pour les liens non-optimaux
    nx.draw_networkx_edges(G, pos, ax=ax1, edgelist=[(lien.source.id, lien.destination.id) for lien in graphe.liens],
                           arrows=False, edge_color="black")
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax1)

    # Ajouter des flèches pour chaque lien
    for (u, v, d) in G.edges(data=True):
        x_start, y_start = pos[u]
        x_end, y_end = pos[v]
        ax1.annotate(
            "", xy=(x_end, y_end), xytext=(x_start, y_start),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.5),
        )

    # Dessiner le chemin optimal en rouge, avec des flèches rouges
    if chemin_optimal:
        for i in range(len(chemin_optimal) - 1):
            u = chemin_optimal[i].id
            v = chemin_optimal[i + 1].id
            x_start, y_start = pos[u]
            x_end, y_end = pos[v]
            # Ligne rouge pour les liens du chemin optimal
            ax1.annotate(
                "", xy=(x_end, y_end), xytext=(x_start, y_start),
                arrowprops=dict(arrowstyle="->", color="red", lw=2.5),
            )

    # Afficher les étiquettes des noeuds
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif', ax=ax1)

    # Afficher le tableau des étapes de Dijkstra dans ax2
    if historique:
        historique_df = pd.DataFrame(historique)
        historique_df['Étape'] = range(1, len(historique_df) + 1)
        cols = ['Étape'] + [col for col in historique_df.columns if col != 'Étape']
        historique_df = historique_df[cols]

        # Positionner le titre du tableau
        ax2.text(0.5, 1.05, "Tableau de Dijkstra", ha='center', va='top', fontsize=14, fontweight='bold', color='red')

        # Afficher le tableau
        table = ax2.table(cellText=historique_df.values, colLabels=historique_df.columns, loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.5, 1.5)  # Augmenter l'échelle pour plus d'espace

        # Uniformiser la largeur des colonnes
        for j in range(len(historique_df.columns)):
            max_len = max(historique_df[historique_df.columns[j]].apply(lambda x: len(str(x))))
            table.auto_set_column_width([j])  # Ajuste la largeur de la colonne

        # Appliquer une largeur uniforme pour toutes les colonnes
        for j in range(len(historique_df.columns)):
            table.auto_set_column_width([j])  # Appliquer largeur égale à chaque colonne

        color = '#FFDDC1'
        for (i, j), cell in table.get_celld().items():
            if i == 0:
                cell.set_fontsize(12)
                cell.set_text_props(weight='bold')
                cell.set_facecolor(color)
            if j == len(historique_df.columns) - 1:
                cell.set_facecolor(color)

        ax2.axis('off')

    # Afficher le texte du chemin optimal et la distance en bas du tableau
    if chemin_optimal and distance_totale is not None:
        chemin_text = "Chemin optimal: " + " -> ".join([str(noeud.id) for noeud in chemin_optimal])
        distance_text = f"Distance totale: {distance_totale}"

        # Positionner le texte sous le tableau
        plt.text(1.05, -0.2, chemin_text + "\n" + distance_text, transform=ax1.transAxes, 
                 fontsize=12, verticalalignment='top', horizontalalignment='center', 
                 bbox=dict(boxstyle="round,pad=0.3", edgecolor="gray", facecolor="blue"))

    # Désactiver l'axe du graphe
    ax1.set_title("Visualisation du Graphe", fontsize=14, fontweight='bold', color='red')
    ax1.axis('off')

    # Ajuster l'espace pour éviter que le tableau et le texte ne chevauchent
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.25)  # Augmenter l'espace en bas pour éviter chevauchement

    plt.show()
