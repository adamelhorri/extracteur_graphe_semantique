import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

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
        """Visualise le graphe avec les nœuds et les relations, en évitant la superposition des arêtes et des étiquettes."""
        G = nx.DiGraph()

        # Ensemble des nœuds reliés
        noeuds_relies = set()

        # Dictionnaire pour stocker les relations entre deux nœuds (pour éviter la superposition)
        relations_counter = {}

        # Ajouter les relations filtrées (sans 'pos' et 'lemm') et compter les relations entre chaque paire de nœuds
        edges_colors = []
        for source, relation, cible in self.relations:
            if "pos" not in relation and "lemm" not in relation:
                G.add_edge(source, cible, label=relation)
                noeuds_relies.add(source)
                noeuds_relies.add(cible)

                # Si la relation contient "succ", ajouter la couleur verte, sinon noire
                if "succ" in relation:
                    edges_colors.append('green')
                else:
                    edges_colors.append('black')

                # Compter combien de relations existent entre chaque paire de nœuds
                if (source, cible) not in relations_counter:
                    relations_counter[(source, cible)] = []
                relations_counter[(source, cible)].append(relation)

        # Ajouter uniquement les nœuds qui sont reliés
        for noeud in noeuds_relies:
            G.add_node(noeud, label=self.noeuds[noeud])

        # Positionner les nœuds
        pos = nx.spring_layout(G)

        # Dessiner les nœuds
        nx.draw(G, pos, with_labels=True, node_color='lightblue', font_size=10, node_size=3000)

        # Dessiner les relations avec courbure pour éviter la superposition
        curved_edges = []
        straight_edges = []
        for (source, cible), relations in relations_counter.items():
            if len(relations) > 1:  # Plusieurs relations entre les mêmes nœuds
                curved_edges.append((source, cible))
            else:
                straight_edges.append((source, cible))

        # Tracer les arêtes courbées et droites
        arc_rad = 0.3  # Rayon de courbure pour les arêtes
        nx.draw_networkx_edges(G, pos, edgelist=straight_edges, edge_color=edges_colors)
        nx.draw_networkx_edges(G, pos, edgelist=curved_edges, connectionstyle=f'arc3, rad = {arc_rad}', edge_color=edges_colors)

        # Ajouter les étiquettes des relations en ajustant leur position pour éviter la superposition
        for (source, cible), relations in relations_counter.items():
            for i, relation in enumerate(relations):
                # Calculer la position au milieu de l'arête
                x_mid = (pos[source][0] + pos[cible][0]) / 2
                y_mid = (pos[source][1] + pos[cible][1]) / 2

                # Décaler verticalement l'étiquette pour chaque relation supplémentaire
                y_offset = 0.05 * (i - (len(relations) - 1) / 2)  # Ajustement dynamique

                # Ajouter l'étiquette à la position ajustée
                plt.text(x_mid, y_mid + y_offset, relation, fontsize=10, color='black', ha='center')

        # Afficher le graphe
        plt.show()

        # Réinitialiser le graphe après fermeture de la fenêtre de visualisation
        self.noeuds.clear()  # Vider les nœuds
        self.relations.clear()  # Vider les relations
