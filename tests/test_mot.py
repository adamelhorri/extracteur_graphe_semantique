import sys
import os
import unittest

# Ajouter dynamiquement le chemin vers src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import de la classe Mot
from mot import Mot

class TestMot(unittest.TestCase):
    
    def test_creation_mot(self):
        mot = Mot(1, "chat", "chat", "nom")
        self.assertEqual(mot.texte, "chat")
        self.assertEqual(mot.lemme, "chat")
        self.assertEqual(mot.partie_du_discours, "nom")
        self.assertEqual(mot.sens, "")
    
    def test_afficher_mot(self):
        mot = Mot(1, "chat", "chat", "nom", "animal domestique")
        self.assertEqual(mot.afficher(), "Mot: chat, Lemme: chat, POS: nom, Sens: animal domestique")

if __name__ == '__main__':
    unittest.main()
