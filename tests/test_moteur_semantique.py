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

    def test_long_text_with_multiple_sentences(self):
        # Exemple de texte long contenant plusieurs phrases
        texte = """
Paul, un célèbre biologiste, adore observer les comportements des animaux. Son chien Max est un compagnon fidèle, toujours à ses côtés pendant ses recherches. Max est un chien intelligent, souvent attentif aux petits détails que Paul néglige parfois. Ensemble, ils passent de longues heures dans la forêt à observer les oiseaux. Les oiseaux colorés, tels que les perroquets, fascinent Paul par leur beauté et leurs chants mélodieux.

Lors d'une de ses explorations, Paul a rencontré Marie, une amie de longue date qui partage sa passion pour la nature. Elle est une botaniste talentueuse, et elle passe beaucoup de temps à étudier les plantes rares. Paul et Marie discutent souvent des similarités entre le comportement des plantes et des animaux, et ils débattent sur la question de savoir si les plantes ressentent des émotions.

Marie utilise un microscope pour examiner en détail les cellules végétales, tandis que Paul préfère utiliser une caméra pour filmer les interactions des animaux dans leur habitat naturel. Ensemble, ils ont découvert une espèce d'oiseau qui, selon eux, pourrait être une variation rare du perroquet. Ils ont nommé cet oiseau "Perroquet de cristal", en raison de la transparence de ses plumes.

La forêt où ils travaillent est un lieu rempli de merveilles. Les arbres majestueux, hauts de plusieurs mètres, semblent toucher le ciel. Paul est souvent émerveillé par la robustesse des chênes et la douceur des saules pleureurs qui bordent les rivières. Max, lui, adore courir dans les clairières et se rouler dans les feuilles.

Un jour, alors qu'ils exploraient une nouvelle zone de la forêt, Paul et Marie ont trouvé un insecte géant qui ressemblait à une libellule, mais en beaucoup plus grand. Ils ont pris des échantillons pour les étudier dans leurs laboratoires respectifs. Paul pense que cet insecte pourrait avoir des propriétés intéressantes pour la recherche médicale.

Max, toujours curieux, s'est approché d'un nid d'oiseaux pour l'observer de plus près. Marie a averti Paul que Max pourrait déranger les oiseaux, mais Paul lui a répondu que Max était suffisamment prudent pour ne pas causer de problème.

La collaboration entre Paul et Marie est fructueuse. Ensemble, ils ont présenté leurs recherches à plusieurs conférences internationales, où ils ont reçu des éloges pour leur travail novateur. Leurs découvertes ont suscité l'intérêt de nombreux chercheurs, et ils ont été invités à rejoindre un projet de recherche mondial sur la biodiversité.

Marie habite à Paris, une ville qu'elle adore. Chaque matin, elle prend son café dans la cuisine, un endroit calme à côté du salon. Sur la table, elle dispose un vase au-dessus du journal. De temps en temps, elle regarde par la fenêtre pour observer ce qui se passe devant la maison.

Derrière le jardin, il y a un grand parc où les enfants aiment jouer. L’été, elle passe souvent ses soirées à la plage avec ses amis. Elle préfère s'asseoir en-dessous du parasol pour se protéger du soleil.

Le week-end, Marie aime rendre visite chez ses parents qui vivent à la campagne. Dans la cour de la ferme, il y a un vieux puits à côté duquel les enfants jouent souvent.

Lorsqu'elle est fatiguée, elle se repose sur le canapé dans le salon. Elle passe parfois des heures devant la télévision à regarder des films. À la montagne, où elle aime faire des randonnées, les paysages sont magnifiques, avec des sentiers qui montent au-dessus des vallées.

        """

        # Diviser le texte en phrases
        phrases = self.text_splitter.split_text_into_sentences(texte)

        # Liste des relations attendues pour les phrases (mettre à jour avec les nouvelles relations)
        expected_relations = [
            ('r_agent', 'Paul', 'enseigner', 1),
            ('r_pos', 'Paul', 'noun', 1),
            ('r_pos', 'enseigné', 'verb', 1),
            ('r_isa', 'physique', 'sujet', 1),
            ('r_has_magn', 'passionné', 'grande', 1),
            ('r_instr-1', 'Max', 'accompagner', 1),
            ('r_domain-1', 'jardin', 'fleur', 1),
            ('r_lemma', 'Paul', 'professeur', 1),
            ('r_patient', 'physique', 'enseigner', 1),
            ('r_lieu-1', 'université', 'Paul', 1),
        ]

        # Appliquer les règles pour chaque phrase individuellement
        for phrase in phrases:
            self.moteur_regles.appliquer_regles(phrase)

        # Vérifier les relations dans les CSVs
        self.verifier_csv(expected_relations)


if __name__ == '__main__':
    unittest.main()
