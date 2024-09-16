# graphe_semantique.py

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
