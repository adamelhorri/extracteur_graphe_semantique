from noeud import Noeud
from type_relation import TypeRelation


class Relation:
    def __init__(self, type_relation: TypeRelation, poids: float, noeud_source: Noeud, noeud_cible: Noeud, est_negatif: bool = False):
        self.type_relation = type_relation
        self.poids = poids
        self.noeud_source = noeud_source
        self.noeud_cible = noeud_cible
        self.est_negatif = est_negatif

    def ajuster_poids(self, nouveau_poids: float):
        self.poids = nouveau_poids

    def marquer_negatif(self):
        self.est_negatif = True

    def afficher(self):
        negatif_str = "négatif" if self.est_negatif else "positif"
        return f"Relation {self.type_relation.value} entre {self.noeud_source.label} et {self.noeud_cible.label}, Poids: {self.poids}, {negatif_str}"

    def __repr__(self):
        return self.afficher()
