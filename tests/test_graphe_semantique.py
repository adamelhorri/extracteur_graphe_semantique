import sys
import os
import unittest

# Ajouter dynamiquement le chemin vers src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Importer les classes nécessaires
from graphe_semantique import GrapheSemantique

class TestGrapheSemantique(unittest.TestCase):

    def setUp(self):
        """Initialiser un graphe pour chaque test."""
        self.graphe = GrapheSemantique()

    def test_extraction_relations_et_application_regles(self):
        """Test de l'extraction des relations d'un texte et application des règles."""
        # Exemple de phrase simple
        texte = "le chat mange la souris"
        self.graphe.extraire_relations_du_texte(texte)

        # Vérification des relations initiales (succession)
        self.assertEqual(len(self.graphe.graph.edges), 4)

        # Chemin du fichier de règles
        fichier_regles = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/relations.txt'))

        # Appliquer les règles
        self.graphe.appliquer_regles(fichier_regles)

        # Vérification que les nouvelles relations ont été ajoutées
        # Cela dépendra des règles dans relations.txt
        self.assertGreaterEqual(len(self.graphe.graph.edges), 4)

        # Afficher le graphe pour voir les relations ajoutées
        self.graphe.afficher_graphe()

if __name__ == '__main__':
    unittest.main()
