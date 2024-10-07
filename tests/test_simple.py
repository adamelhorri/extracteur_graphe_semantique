# main.py

import logging
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from graphe_semantique import GrapheSemantique
from moteur_de_regles import MoteurDeRegles

def main():
    # Configurer le logging pour afficher les messages de débogage
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

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
    texte = "Les chats noirs dorment paisiblement sur leur canapé rouge.leur camion a mangé une moustache"
    moteur.appliquer_regles(texte)

    # Visualiser le graphe
    graphe.visualiser_graphe()

if __name__ == "__main__":
    main()