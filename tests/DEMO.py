# main.py

import logging
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from graphe_semantique import GrapheSemantique
from moteur_de_regles import MoteurDeRegles

def main():
    # Configurer le logging pour afficher les messages de débogage
    

    # Initialiser le graphe
    graphe = GrapheSemantique()

    # Initialiser le moteur de règles avec le graphe
    moteur = MoteurDeRegles(graphe)
    # Définir le chemin complet vers 'relations.txt' dans le répertoire 'data'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(current_dir, '../data'))
    relations_path = os.path.join(data_dir, 'relations.txt')
        
    # Charger les règles depuis un fichier (assurez-vous que le chemin est correct)
    moteur.charger_regles(relations_path)

    # Appliquer les règles sur un texte donné
    #Exemple simple
    texte = "le chat boit du lait de chèvre"
    # Resolution d'ambiguité ADJ <-> NOUN +Test avec negation
    #texte = "le petit chat ne préfère pas le lait de chèvre"
    # Test pour r_lieu
    #texte = "Le poisson rouge est perdu dans l'ocean atlantique"
    #texte = "L'homme d'affaires vit à paris , paris se trouve en France"
    #texte = "le garçon rouge sur la table"
    #texte ="la chèvre est dans l'écurie."
    # Test Ambiguité Verbe Nom
    #texte = "le chat lèche sa queue"
    #texte = "la frégate sombre rapidement"
    #texte = "la frégate a attrapé un poisson"
    #texte = "la frégate vole un poisson au pêcheur nageur"
    #texte = "le chat du voisin a pissé sur le paillasson "
    #Test Hyponimie
    #texte = "la fusée a explosé au décollage"
    #texte = "l'enfant lèche la glace avec délice"
    #texte = "le garçon regarde sa voisine avec un télescope"
    # Test Anaphore + structures de phrases relativement complexes 
    texte = "le chien tomba dans le puits. Il a pleuré toute la nuit."
    texte = "le chien tombe brusquement dans la rive. Elle est profonde et le récupérer sera compliqué."
    texte = "la religieuse croyante rentre dans la pâtisserie. Elle achète une délicieuse religieuse"
    #texte = "les cafards mangent les chairs de cadavres"
    #texte = "les corbeaux embellissent les cadavres exquis"
    #texte = "la voisine vient s'excuser"
 
    moteur.appliquer_regles(texte)

    # Visualiser le graphe
    graphe.visualiser_graphe()

if __name__ == "__main__":
    main()