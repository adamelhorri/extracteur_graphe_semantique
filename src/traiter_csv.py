# scripts/traiter_csvs.py

import os
import csv
from collections import defaultdict

def traiter_csvs(data_dir):
    """
    Traite tous les fichiers CSV dans le répertoire data_dir pour ajouter une colonne 'recurrence'.
    Supprime les doublons et incrémente 'recurrence' en conséquence.
    """
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            csv_path = os.path.join(data_dir, filename)
            temp_path = os.path.join(data_dir, f"temp_{filename}")

            # Utiliser un dictionnaire pour compter les occurrences
            compteur = defaultdict(int)
            try:
                with open(csv_path, 'r', encoding='utf-8', newline='') as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=';')
                    for row in reader:
                        src = row['source']
                        tgt = row['target']
                        compteur[(src, tgt)] += 1
            except KeyError:
                # Si le fichier CSV n'a que 'source' et 'target', initialiser 'recurrence'
                compteur = defaultdict(int)
                with open(csv_path, 'r', encoding='utf-8', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=';')
                    headers = next(reader, None)
                    if headers and len(headers) == 2:
                        for row in reader:
                            src, tgt = row
                            compteur[(src, tgt)] += 1
                    else:
                        print(f"Format de fichier CSV non reconnu: {csv_path}")
                        continue

            # Réécrire le CSV avec la colonne 'recurrence'
            with open(temp_path, 'w', encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(['source', 'target', 'recurrence'])
                for (src, tgt), rec in compteur.items():
                    writer.writerow([src, tgt, rec])

            # Remplacer l'ancien fichier par le nouveau
            os.replace(temp_path, csv_path)
            print(f"Fichier traité: {filename}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(current_dir, '../data'))
    traiter_csvs(data_dir)
