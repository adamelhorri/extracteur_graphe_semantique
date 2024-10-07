# src/Lexicon.py

import os
import pickle
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Désactive les messages de log de niveau DEBUG et inférieur
logging.disable(logging.DEBUG)

class Lexicon:
    def __init__(self):
        """
        Initialize the Lexicon class by loading the indexes for lemma and POS extraction.
        """
        logging.info("Initializing Lexicon")
        
        # Définir les chemins relatifs à ce fichier
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir,'..', '..', 'data')
        
        # Chemins vers les fichiers de lemme et POS
        self.lemma_file_path = os.path.join(data_dir, 'lemma_clean_utf8.txt')
        self.pos_file_path = os.path.join(data_dir, 'pos_utf8.txt')

        # Chemins vers les fichiers d'index
        self.lemma_index_path = os.path.join(data_dir, 'lemma_index.pkl')
        self.pos_index_path = os.path.join(data_dir, 'pos_index.pkl')

        # Charger les index
        self.lemma_index = self.load_index(self.lemma_index_path, index_type='lemma')
        self.pos_index = self.load_index(self.pos_index_path, index_type='pos')

    def load_index(self, index_file_path, index_type='lemma'):
        """
        Load an index from a pickle file.

        Parameters:
            index_file_path (str): Path to the index pickle file.
            index_type (str): Type of index ('lemma' or 'pos') for logging purposes.

        Returns:
            dict: The loaded index.
        """
        logging.info(f"Loading {index_type} index from {index_file_path}")
        try:
            with open(index_file_path, 'rb') as f:
                index = pickle.load(f)
            logging.info(f"{index_type.capitalize()} index loaded successfully from {index_file_path}")
            return index
        except Exception as e:
            logging.error(f"Error loading {index_type} index: {e}")
            return {}

    def extract_lemmas(self, tokens: list) -> list:
        """
        Extracts all lemma candidates for a list of tokens and assigns them to each token.

        Parameters:
            tokens (list): List of Token objects.

        Returns:
            list: The list of tokens with all lemma candidates.
        """
        logging.info("Starting lemma extraction")
        target_words = [token.text.lower().lstrip('-').strip("-") for token in tokens]  # Supprimer les tirets initiaux et les apostrophes
        logging.debug(f"Target words for lemma extraction: {target_words}")

        results = self.search_lemmas_with_index(self.lemma_file_path, self.lemma_index, target_words)

        for token in tokens:
            # Nettoyer le mot
            word = token.text.lower().lstrip('-').strip("-")
            if word in results and results[word]:
                # Créer un dictionnaire pour conserver le score maximal de chaque lemme
                lemma_scores = {}
                for lemma, score in results[word]:
                    if lemma not in lemma_scores or score > lemma_scores[lemma]:
                        lemma_scores[lemma] = score
                # Convertir en liste de tuples et trier par score décroissant
                possible_lemmas_sorted = sorted(lemma_scores.items(), key=lambda x: x[1], reverse=True)
                logging.info(f"All lemmas for '{word}': {possible_lemmas_sorted}")
                # Assigner les lemmes uniques avec leurs scores au token
                token.lemma_candidates = possible_lemmas_sorted  # Liste de tuples (lemme, score)
                logging.info(f"Lemmas with scores assigned to token: {token.lemma_candidates}")
            else:
                # Si aucun lemme trouvé, assigner le mot lui-même comme lemme avec un score par défaut (0)
                token.lemma_candidates = [(word, 0)]
                logging.warning(f"No lemma found for '{word}', using the word itself with score 0")

        logging.info("Lemma extraction completed")
        return tokens

    def search_lemmas_with_index(self, txt_file_path, index, target_words):
        """
        Searches for lemmas in the file using the index for faster access.
        Ensures that the first column exactly matches the target word.

        Parameters:
            txt_file_path (str): Path to the lemma text file.
            index (dict): Lemma index mapping words to file positions.
            target_words (list): List of target words to extract lemmas for.

        Returns:
            dict: A dictionary mapping each word to a list of (lemma, score) tuples.
        """
        logging.info("Searching for lemmas using the index")
        results = {word: [] for word in target_words}

        try:
            with open(txt_file_path, 'r', encoding='utf-8') as file:
                for word in target_words:
                    if word in index:
                        positions = index[word]  # Récupérer les positions depuis l'index
                        for position in positions:
                            file.seek(position)  # Aller à la position dans le fichier
                            line = file.readline().strip()  # Lire la ligne
                            columns = [col.strip() for col in line.split(';')]  # Séparer les colonnes

                            while line:
                                logging.debug(f"Reading at position {position} for '{word}': {line}")

                                # Vérification stricte : le mot dans columns[0] doit correspondre exactement au mot cible
                                if columns[0].lower() != word or len(columns[0]) != len(word):
                                    logging.debug(f"Word mismatch at position {position}: '{columns[0].lower()}' != '{word}'")
                                    break  # Arrêter la lecture si le mot ne correspond plus

                                if len(columns) == 3 and columns[2].isdigit():
                                    lemma = columns[1].strip().lower()  # Convertir le lemme en minuscules
                                    score = int(columns[2].strip())
                                    if score > 0:  # Ne considérer que les scores positifs
                                        logging.debug(f"Lemma found at position {position}: '{lemma}', Score: {score}")
                                        results[word].append((lemma, score))

                                # Lire la ligne suivante pour vérifier d'autres lemmes pour le même mot
                                line = file.readline().strip()
                                if not line:
                                    break
                                columns = [col.strip() for col in line.split(';')]
        except Exception as e:
            logging.error(f"Error during lemma search: {e}")

        return results

    def extract_pos(self, tokens: list) -> list:
        """
        Extract POS candidates for a list of tokens and assigns them to each token.

        Parameters:
            tokens (list): List of Token objects.

        Returns:
            list: The list of tokens with all POS candidates.
        """
        logging.info("Starting POS extraction")

        for token in tokens:
            # Nettoyer le mot
            word = token.text.lower().lstrip('-').strip("-")
            if word in self.pos_index:
                positions = self.pos_index[word]  # Récupérer les positions depuis l'index
                pos_candidates = {}
                try:
                    with open(self.pos_file_path, 'rb') as file:
                        for pos_position in positions:
                            file.seek(pos_position)
                            line_bytes = file.readline()
                            try:
                                line = line_bytes.decode('utf-8').strip()
                            except UnicodeDecodeError:
                                logging.error(f"Unicode decode error at position {pos_position} for word '{word}'")
                                continue

                            columns = line.split(';')

                            if len(columns) > 3 and columns[3].isdigit():
                                score = int(columns[3])
                                if score > 0:
                                    pos_tag = columns[2].strip()
                                    # Conserver le score maximal pour chaque pos_tag
                                    if pos_tag not in pos_candidates or score > pos_candidates[pos_tag]:
                                        pos_candidates[pos_tag] = score
                                    logging.debug(f"Found POS: '{pos_tag}' with score: {score} for word: '{word}'")

                except Exception as e:
                    logging.error(f"Error extracting POS for '{word}': {e}")
                    pos_candidates = {}

                # Trier les POS candidates par score décroissant
                sorted_pos_candidates = sorted(pos_candidates.items(), key=lambda x: x[1], reverse=True)
                token.pos_candidates = sorted_pos_candidates
                logging.info(f"POS candidates for '{word}': {sorted_pos_candidates}")
            else:
                # Si aucun POS trouvé, assigner une liste vide
                token.pos_candidates = []
                logging.warning(f"No POS found for '{word}'")

        logging.info("POS extraction completed")
        return tokens
