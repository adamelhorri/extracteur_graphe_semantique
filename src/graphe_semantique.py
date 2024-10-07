# src/graphe_semantique.py

import networkx as nx
import matplotlib.pyplot as plt
import re
import logging
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from collections import defaultdict

class GrapheSemantique:
    def __init__(self):
        # Utilisation de NetworkX pour gérer le graphe
        self.G = nx.DiGraph()
        # Color map pour les relations sémantiques
        self.relation_colors = {}
        self.next_color = 0
        self.colors = [
            'red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink',
            'gray', 'olive', 'cyan', 'magenta', 'yellow', 'lime', 'teal'
        ]

    def obtenir_couleur_relation(self, relation):
        """Assigne une couleur unique à chaque type de relation sémantique."""
        if relation not in self.relation_colors:
            if self.next_color < len(self.colors):
                self.relation_colors[relation] = self.colors[self.next_color]
                self.next_color += 1
            else:
                # Génère une couleur aléatoire si les couleurs prédéfinies sont épuisées
                import random
                r = lambda: random.randint(0,255)
                self.relation_colors[relation] = '#%02X%02X%02X' % (r(), r(), r())
        return self.relation_colors[relation]

    def ajouter_noeud(self, nom, type_noeud, valeur):
        """Ajouter un nœud avec son type et sa valeur au graphe."""
        if not self.G.has_node(nom):
            self.G.add_node(nom, type=type_noeud, valeur=valeur)
            logging.debug(f"Ajout du nœud: {nom}, type: {type_noeud}, valeur: {valeur}")
        else:
            logging.debug(f"Nœud déjà existant: {nom}")

    def existe_noeud(self, nom):
        """Vérifie si un nœud existe dans le graphe."""
        return self.G.has_node(nom)

    def ajouter_relation(self, source, relation, cible):
        """Ajouter une relation au graphe."""
        if not self.existe_relation(source, relation, cible):
            self.G.add_edge(source, cible, relation=relation)
            logging.debug(f"Ajout de la relation: {source} -[{relation}]-> {cible}")

    def existe_relation(self, source, relation, cible):
        """Vérifie si une relation existe déjà dans le graphe."""
        return self.G.has_edge(source, cible) and self.G[source][cible].get('relation') == relation

    def get_toutes_relations(self):
        """Retourne toutes les relations du graphe."""
        return list(self.G.edges(data=True))

    def visualiser_graphe(self):
        """Visualise le graphe avec les nœuds et les relations de manière organisée."""
        plt.figure(figsize=(15, 10))  # Adjust figure size
        pos = {}
        labels = {}

        # Separate nodes by type
        word_nodes = [node for node, data in self.G.nodes(data=True) if data['type'] == 'word']
        pos_nodes = [node for node, data in self.G.nodes(data=True) if data['type'] == 'pos']
        lemma_nodes = [node for node, data in self.G.nodes(data=True) if data['type'] == 'lemma']
        other_nodes = [node for node, data in self.G.nodes(data=True) if data['type'] not in ['word', 'pos', 'lemma']]

        # Sort word_nodes by their number to maintain word order
        word_nodes_sorted = sorted(word_nodes, key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)

        # Position word_nodes linearly
        x_spacing = 5
        y_word = 0
        y_pos = 1
        y_lemma = -1

        for idx, word in enumerate(word_nodes_sorted):
            x = idx * x_spacing
            pos[word] = (x, y_word)
            labels[word] = self.G.nodes[word]['valeur']
            logging.debug(f"Positioned {word} at ({x}, {y_word})")

            # Find POS and lemma nodes related to this word
            for neighbor in self.G.neighbors(word):
                relation = self.G[word][neighbor]['relation']
                if relation == 'r_pos':
                    pos[neighbor] = (x, y_pos)
                    labels[neighbor] = self.G.nodes[neighbor]['valeur']
                    logging.debug(f"Positioned {neighbor} at ({x}, {y_pos})")
                elif relation == 'r_lemma':
                    pos[neighbor] = (x, y_lemma)
                    labels[neighbor] = self.G.nodes[neighbor]['valeur']
                    logging.debug(f"Positioned {neighbor} at ({x}, {y_lemma})")

        # Position other nodes separately
        for idx, node in enumerate(other_nodes):
            pos[node] = (len(word_nodes_sorted) * x_spacing + idx * x_spacing, y_word)
            labels[node] = self.G.nodes[node]['valeur']
            logging.debug(f"Positioned {node} at ({len(word_nodes_sorted) * x_spacing + idx * x_spacing}, {y_word})")

        # Create node list in position order
        node_list = list(pos.keys())

        # Assign colors and sizes based on node type
        couleurs = []
        node_sizes = []
        for node in node_list:
            node_type = self.G.nodes[node]['type']
            if node_type == 'word':
                couleurs.append('lightblue')
                node_sizes.append(800)  # Smaller nodes
            elif node_type == 'pos':
                couleurs.append('lightgreen')
                node_sizes.append(600)  # Smaller nodes
            elif node_type == 'lemma':
                couleurs.append('lightcoral')
                node_sizes.append(600)  # Smaller nodes
            else:
                couleurs.append('gray')
                node_sizes.append(600)

        # Draw nodes
        nx.draw_networkx_nodes(self.G, pos, nodelist=node_list, node_color=couleurs, node_size=node_sizes)

        # Draw node labels
        nx.draw_networkx_labels(self.G, pos, labels, font_size=10, font_weight='bold')

        # Define relations
        # r_succ relations between words
        succ_edges = [(u, v) for u, v, d in self.G.edges(data=True) if d['relation'] == 'r_succ']
        # r_pos and r_lemma attribute relations
        attr_edges = [(u, v) for u, v, d in self.G.edges(data=True) if d['relation'] in ['r_pos', 'r_lemma']]
        # Other semantic relations
        semantic_relations = [rel for rel in self.G.edges(data=True) if rel[2]['relation'] not in ['r_succ', 'r_pos', 'r_lemma']]
        semantic_edges = [(u, v, d['relation']) for u, v, d in semantic_relations]

        # Draw r_succ relations with black arrows
        nx.draw_networkx_edges(
            self.G,
            pos,
            edgelist=succ_edges,
            edge_color='black',
            arrows=True,
            arrowsize=20,
            connectionstyle='arc3,rad=0.1'
        )

        # Draw r_pos and r_lemma relations with dashed gray lines
        nx.draw_networkx_edges(
            self.G,
            pos,
            edgelist=attr_edges,
            edge_color='gray',
            style='dashed',
            arrows=False
        )

        # Draw semantic relations with colored, curved arrows (no labels)
        for u, v, relation in semantic_edges:
            color = self.obtenir_couleur_relation(relation)
            nx.draw_networkx_edges(
                self.G,
                pos,
                edgelist=[(u, v)],
                edge_color=color,
                style='solid',
                arrows=True,  # Directed arrows for all relations
                arrowstyle='->',  # Arrow style
                arrowsize=30,  # Arrow size for better visibility
                connectionstyle='arc3,rad=0.3'  # Increase edge curvature
            )

        # Remove relation labels (no edge labels)

        # Add legend for color coding
        legend_handles = [
            mpatches.Patch(color='lightblue', label='Word'),
            mpatches.Patch(color='lightgreen', label='POS'),
            mpatches.Patch(color='lightcoral', label='Lemma'),
            mpatches.Patch(color='gray', linestyle='dashed', label='Relations attributaires'),
            mpatches.Patch(color='black', label='r_succ'),
        ]

        # Add patches for semantic relations
        for relation, color in self.relation_colors.items():
            legend_handles.append(mpatches.Patch(color=color, label=relation))

        plt.legend(handles=legend_handles, loc='upper right', fontsize='small')

        # Display the graph
        plt.axis('off')
        plt.tight_layout()
        plt.show()
