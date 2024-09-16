import sys
import os
import unittest

# Ajouter dynamiquement le chemin vers src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import de la classe ExpressionComposee
from expression_composee import ExpressionComposee

class TestExpressionComposee(unittest.TestCase):

    def test_creation_expression_composee(self):
        expr = ExpressionComposee(1, "avant toute chose")
        self.assertEqual(expr.label, "avant toute chose")

    def test_afficher_expression_composee(self):
        expr = ExpressionComposee(1, "avant toute chose")
        self.assertEqual(expr.afficher(), "Expression composée: avant toute chose")

    def test_extraction_fichier(self):
        # Chemin du fichier motsComposes.txt dans le dossier data
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/motsComposes.txt'))
        
        expressions = ExpressionComposee.from_file(file_path)
        
        # Vérifier qu'il y a au moins 1 million d'expressions
        self.assertGreater(len(expressions), 1000000)  # Adaptez ce nombre en fonction de la taille réelle du fichier
        
        # Vérifier certaines expressions spécifiques
        self.assertEqual(expressions[0].id, 9)
        self.assertEqual(expressions[0].label, "avant toute chose")
        self.assertEqual(expressions[10].label, "Moshe Ben Maimon")

if __name__ == '__main__':
    unittest.main()
