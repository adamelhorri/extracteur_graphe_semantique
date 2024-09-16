import sys
import os
import unittest

# Ajouter dynamiquement le chemin vers src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Importer les classes nécessaires
from graphe_semantique import GrapheSemantique
from mot import Mot
from relation import TypeRelation

class TestExtractionRelations(unittest.TestCase):

    def setUp(self):
        """Initialiser un graphe pour chaque test."""
        self.graphe = GrapheSemantique()

    def test_extraction_relations_simple(self):
        """Test de l'extraction automatique des relations dans une phrase simple."""
        texte = "le chat boit du lait"
        self.graphe.extraire_relations_du_texte(texte)

        # Vérifier que les 5 nœuds (mots) sont bien ajoutés
        self.assertEqual(len(self.graphe.graph.nodes), 5)

        # Vérifier que 4 relations (r_succ) sont bien créées
        self.assertEqual(len(self.graphe.graph.edges), 4)

        # Vérifier une relation particulière entre "chat" et "boit"
        rel = self.graphe.trouver_relation(1, 2)
        self.assertIsNotNone(rel)
        self.assertEqual(rel['type'], TypeRelation.r_succ)
        self.assertEqual(rel['poids'], 1.0)

        # Afficher le graphe visuellement
        self.graphe.afficher_graphe()

    def test_extraction_relations_complexe(self):
        """Test de l'extraction des relations dans une phrase plus complexe."""
        texte = "le chat noir boit du lait frais"
        self.graphe.extraire_relations_du_texte(texte)

        # Vérifier que 7 nœuds sont ajoutés
        self.assertEqual(len(self.graphe.graph.nodes), 7)

        # Vérifier que 6 relations de succession sont ajoutées
        self.assertEqual(len(self.graphe.graph.edges), 6)

        # Vérifier la relation entre "boit" et "du"
        rel = self.graphe.trouver_relation(3, 4)
        self.assertIsNotNone(rel)
        self.assertEqual(rel['type'], TypeRelation.r_succ)
        self.assertEqual(rel['poids'], 1.0)

        # Afficher le graphe visuellement
        self.graphe.afficher_graphe()

if __name__ == '__main__':
    unittest.main()
