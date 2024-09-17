import unittest
import os
import sys
import csv
import re

# Ajouter le chemin du répertoire 'src' pour importer les modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from moteur_de_regles import MoteurDeRegles
from graphe_semantique import GrapheSemantique
from text_splitter import TextSplitter

class TestMoteurDeRegles(unittest.TestCase):
    def setUp(self):
        # Initialiser le graphe sémantique et le moteur de règles
        self.graphe = GrapheSemantique()
        self.moteur_regles = MoteurDeRegles(self.graphe)
        
        # Initialiser l'instance de TextSplitter
        self.text_splitter = TextSplitter()

        # Définir le chemin complet vers 'relations.txt' dans le répertoire 'data'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.abspath(os.path.join(current_dir, '../data'))
        relations_path = os.path.join(data_dir, 'relations.txt')
        
        # Charger les règles depuis le chemin complet
        self.moteur_regles.charger_regles(relations_path)
        
        # Réinitialiser les fichiers CSV avant chaque test
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        for csv_file in csv_files:
            csv_path = os.path.join(data_dir, csv_file)
            with open(csv_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(['source', 'target', 'recurrence'])

    def verifier_csv(self, expected_relations):
        """
        Vérifie que les relations spécifiées existent avec les récurrences attendues.
        expected_relations : list of tuples
            Chaque tuple contient (relation_type, source, target, recurrence)
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.abspath(os.path.join(current_dir, '../data'))
        
        # Collecter toutes les relations existantes dans les CSV
        existing_relations = set()
        for csv_file in os.listdir(data_dir):
            if csv_file.endswith('.csv'):
                csv_path = os.path.join(data_dir, csv_file)
                relation_type = os.path.splitext(csv_file)[0]
                with open(csv_path, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=';')
                    for row in reader:
                        existing_relations.add((relation_type, row['source'], row['target'], int(row['recurrence'])))
        
        # Vérifier que chaque relation attendue est présente
        for relation in expected_relations:
            self.assertIn(relation, existing_relations,
                          f"La relation '{relation[1]} {relation[0]} {relation[2]}' avec 'recurrence'={relation[3]} n'a pas été trouvée.")

    def afficher_structure_spacy(self, phrase):
        """
        Affiche la structure des dépendances syntaxiques extraites par spaCy pour la phrase.
        """
        print(f"Structure syntaxique pour la phrase : '{phrase}'")
        doc = self.moteur_regles.nlp(phrase)  # Utilisation du modèle spaCy dans le moteur de règles
        for token in doc:
            print(f"Token: {token.text}, Dépendance: {token.dep_}, Tête: {token.head.text}, POS: {token.pos_}")

    def tester_relation(self, relation_name, phrases, expected_relations):
        """
        Méthode générique pour tester une relation donnée.
        relation_name: le nom de la relation à tester (ex: 'r_associated')
        phrases: une liste de phrases à tester
        expected_relations: une liste de relations attendues sous forme de tuples (relation, source, target, recurrence)
        """
        for phrase in phrases:
            print(f"Phrase en cours: {phrase}")
            self.afficher_structure_spacy(phrase)
            self.moteur_regles.appliquer_regles(phrase)
            self.graphe.visualiser_graphe()
        
        # Vérifier les relations dans les CSVs
        self.verifier_csv(expected_relations)

    def test_r_associated(self):
        phrases = [
            "La voiture rouge est rapide.",
            "Un homme intelligent et courageux a résolu le problème.",
            "Le chat noir et le chien blanc sont amis.",
            "La grande maison est magnifique.",
            "Les livres intéressants sont sur la table.",
            "Pierre est un homme sage et réfléchi.",
            "Marie et son amie sont très différentes."
        ]
        expected_relations = [
            ('r_associated', 'voiture', 'rouge', 1),
            ('r_associated', 'homme', 'intelligent', 1),
            ('r_associated', 'chat', 'noir', 1),
            ('r_associated', 'maison', 'grande', 1),
            ('r_associated', 'livres', 'intéressants', 1),
            ('r_associated', 'homme', 'sage', 1),
            ('r_associated', 'Marie', 'amie', 1)
        ]
        self.tester_relation('r_associated', phrases, expected_relations)

    def test_r_raff_sem(self):
        phrases = [
            "Le chat est un animal domestique.",
            "La pomme est un fruit.",
            "Un ordinateur puissant est nécessaire.",
            "L'avion est un moyen de transport rapide.",
            "Le lion est un animal dangereux.",
            "Les logiciels sont des outils indispensables.",
            "Le professeur est un expert en biologie."
        ]
        expected_relations = [
            ('r_raff_sem', 'animal', 'domestique', 1),
            ('r_raff_sem', 'pomme', 'fruit', 1),
            ('r_raff_sem', 'ordinateur', 'puissant', 1),
            ('r_raff_sem', 'avion', 'moyen', 1),
            ('r_raff_sem', 'lion', 'dangereux', 1),
            ('r_raff_sem', 'logiciels', 'indispensables', 1),
            ('r_raff_sem', 'professeur', 'expert', 1)
        ]
        self.tester_relation('r_raff_sem', phrases, expected_relations)

    def test_r_isa(self):
        phrases = [
            "Paul, un biologiste, adore les animaux.",
            "Marie est une enseignante.",
            "Jean, un expert, a résolu le problème.",
            "Le chien, un animal domestique, est fidèle.",
            "La Terre est une planète.",
            "La pomme, un fruit, est rouge.",
            "L'avion, un moyen de transport, est rapide."
        ]
        expected_relations = [
            ('r_isa', 'Paul', 'biologiste', 1),
            ('r_isa', 'Marie', 'enseignante', 1),
            ('r_isa', 'Jean', 'expert', 1),
            ('r_isa', 'chien', 'animal', 1),
            ('r_isa', 'Terre', 'planète', 1),
            ('r_isa', 'pomme', 'fruit', 1),
            ('r_isa', 'avion', 'moyen', 1)
        ]
        self.tester_relation('r_isa', phrases, expected_relations)

    # Ajouter les autres tests pour les relations suivantes :
    # 'r_syn', 'r_hypo', 'r_anto', 'r_agent', 'r_patient', 'r_has_magn', 'r_has_antimagn', 'r_family', 'r_lieu'
    
    # Exemple pour r_syn
    def test_r_syn(self):
        phrases = [
            "Paul est fort, puissant même.",
            "Jean est intelligent et brillant.",
            "Le chat est rusé ou astucieux.",
            "Le chien est grand et immense.",
            "La voiture est rapide ou véloce.",
            "Marie est jolie, belle même.",
            "L'enfant est sage ou obéissant."
        ]
        expected_relations = [
            ('r_syn', 'fort', 'puissant', 1),
            ('r_syn', 'intelligent', 'brillant', 1),
            ('r_syn', 'rusé', 'astucieux', 1),
            ('r_syn', 'grand', 'immense', 1),
            ('r_syn', 'rapide', 'véloce', 1),
            ('r_syn', 'jolie', 'belle', 1),
            ('r_syn', 'sage', 'obéissant', 1)
        ]
        self.tester_relation('r_syn', phrases, expected_relations)

if __name__ == '__main__':
    # Exécuter les tests spécifiques en fonction de la relation que vous souhaitez tester
    unittest.main()
    #tester:python -m unittest TestMoteurDeRegles.test_r_rel
