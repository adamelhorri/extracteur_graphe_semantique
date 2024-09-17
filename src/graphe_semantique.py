import networkx as nx
import matplotlib.pyplot as plt

class GrapheSemantique:
    def __init__(self):
        # Dictionnaire pour stocker les nœuds et leurs attributs
        self.noeuds = {}  # clé: nom du nœud, valeur: POS
        # Liste pour stocker les relations sous forme de tuples (source, relation, cible)
        self.relations = []

    def ajouter_noeud(self, nom, pos):
        """Ajouter un nœud avec son POS au graphe."""
        if nom not in self.noeuds:
            self.noeuds[nom] = pos

    def existe_noeud(self, nom):
        """Vérifie si un nœud existe dans le graphe."""
        return nom in self.noeuds

    def ajouter_relation(self, source, relation, cible):
        """Ajouter une relation au graphe."""
        if not self.existe_relation(source, relation, cible):
            self.relations.append((source, relation, cible))

    def existe_relation(self, source, relation, cible):
        """Vérifie si une relation existe déjà dans le graphe."""
        return (source, relation, cible) in self.relations

    def get_toutes_relations(self):
        """Retourne toutes les relations du graphe."""
        return self.relations

    def visualiser_graphe(self):
        """Visualise le graphe avec les nœuds et les relations."""
        G = nx.DiGraph()

        # Ajouter les nœuds
        for noeud, pos in self.noeuds.items():
            G.add_node(noeud, label=pos)

        # Ajouter les relations (edges)
        for source, relation, cible in self.relations:
            G.add_edge(source, cible, label=relation)

        # Positionner les nœuds
        pos = nx.spring_layout(G)

        # Dessiner les nœuds et les relations
        nx.draw(G, pos, with_labels=True, node_color='lightblue', font_size=10, node_size=3000)

        # Ajouter les étiquettes de relation
        edge_labels = {(source, cible): relation for source, relation, cible in self.relations}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        # Afficher le graphe
        plt.show()
