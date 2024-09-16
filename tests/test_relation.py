import sys
import os
import unittest

# Ajouter dynamiquement le chemin vers src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import de la classe Relation, Mot, et TypeRelation
from relation import Relation
from mot import Mot
from relation import TypeRelation

class TestRelation(unittest.TestCase):

    def test_creation_relation(self):
        mot1 = Mot(1, "chat", "chat", "nom")
        mot2 = Mot(2, "boit", "boire", "verbe")
        relation = Relation(TypeRelation.r_succ, 1.0, mot1, mot2)
        
        self.assertEqual(relation.type_relation, TypeRelation.r_succ)
        self.assertEqual(relation.poids, 1.0)
        self.assertEqual(relation.noeud_source, mot1)
        self.assertEqual(relation.noeud_cible, mot2)
        self.assertFalse(relation.est_negatif)

    def test_ajuster_poids_relation(self):
        mot1 = Mot(1, "chat", "chat", "nom")
        mot2 = Mot(2, "boit", "boire", "verbe")
        relation = Relation(TypeRelation.r_succ, 1.0, mot1, mot2)
        relation.ajuster_poids(2.5)
        
        self.assertEqual(relation.poids, 2.5)

    def test_marquer_negatif_relation(self):
        mot1 = Mot(1, "chat", "chat", "nom")
        mot2 = Mot(2, "boit", "boire", "verbe")
        relation = Relation(TypeRelation.r_succ, 1.0, mot1, mot2)
        relation.marquer_negatif()
        
        self.assertTrue(relation.est_negatif)

    def test_afficher_relation(self):
        mot1 = Mot(1, "chat", "chat", "nom")
        mot2 = Mot(2, "boit", "boire", "verbe")
        relation = Relation(TypeRelation.r_succ, 1.0, mot1, mot2)
        self.assertEqual(relation.afficher(), "Relation succession entre chat et boit, Poids: 1.0, positif")

if __name__ == '__main__':
    unittest.main()
