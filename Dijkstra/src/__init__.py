# Ce fichier rend le dossier src un package Python.


from .graph import Graphe, Noeud
from .dijkstra import dijkstra
from .visualization import visualiser_chemin
from src import Graphe, dijkstra, visualiser_chemin
__version__ = "1.0.0"
# Configuration pour tout le package
CONFIG = {
    "default_weight": 1,
    "display_paths": True
}
