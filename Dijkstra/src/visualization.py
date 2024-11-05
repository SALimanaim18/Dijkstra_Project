import matplotlib.pyplot as plt
import networkx as nx

def dessiner_graphe(graphe):
    G = nx.DiGraph()
    
    for noeud in graphe.noeuds:
        G.add_node(noeud.id)
    
    for lien in graphe.liens:
        G.add_edge(lien.source.id, lien.destination.id, weight=lien.calculer_cout())
    
    pos = nx.spring_layout(G)
    
    nx.draw_networkx_nodes(G, pos, node_size=700)
    
    edges = G.edges(data=True)
    nx.draw_networkx_edges(G, pos, arrows=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')
    
    plt.title("Visualisation du Graphe")
    plt.axis('off')
    plt.show()