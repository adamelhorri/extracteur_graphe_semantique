# src/Tokenizer.py

import re
from Tokenizer.Token_ import Token
import os
import logging

class Tokenizer:
    def __init__(self):
        # Définir les chemins
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, '..', 'data')
        mots_composes_path = os.path.join(data_dir, 'motsComposés.txt')
        
        # Charger les mots composés dans un ensemble
        self.mots_composes = self.load_mots_composes(mots_composes_path)
        logging.info(f"Loaded {len(self.mots_composes)} compound words.")

    def load_mots_composes(self, filepath):
        """
        Charger les mots composés depuis le fichier motsComposés.txt.
        """
        mots = set()
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split(';')
                    if len(parts) >= 2:
                        # Enlever les guillemets et ajouter au set
                        mot = parts[1].strip('"').lower()
                        mots.add(mot)
        except Exception as e:
            logging.error(f"Erreur lors du chargement de motsComposés.txt: {e}")
        return mots

    def normalize_text(self, text):
        """
        Normaliser les apostrophes et les guillemets typographiques.
        """
        # Remplacer les apostrophes typographiques par des apostrophes simples
        text = text.replace('’', "'")
        # Remplacer les guillemets français par des guillemets doubles
        text = text.replace('«', '"').replace('»', '"')
        return text

    def tokenize(self, text):
        """
        Tokenize the input text into a list of Token objects, assigning a unique token ID
        to each token and resetting the ID after each sentence-ending punctuation.
        """
        # Normalize the text
        text = self.normalize_text(text)

        tokens = []
        # Regular expression to match words, punctuation, and sentence-ending punctuation
        pattern = re.compile(r"\b\w+(?:-\w+)*\b|[.!?;\"()\[\]{}\-]", re.UNICODE)
        raw_tokens = pattern.findall(text)

        token_id = 0  # Initialize token ID
        token_pid = 0
        
        
        for raw_token in raw_tokens:
            if raw_token in ".!?":  # Punctuation marks that indicate the end of a sentence
                token = Token(raw_token)  # Create the token object for the punctuation
                token.token_id = token_id  # Assign the token ID to punctuation
                token.token_pid=token_pid
                token.token_primarykey=(token_pid,token_id)
                tokens.append(token)
                token_id += 1  # Increment ID for the punctuation (optional)
                token_id = 0  # Reset token ID for the next token after punctuation

                token_pid+=1
            else:
                if '-' in raw_token:
                    # Check if the full word is in compound words
                    if raw_token.lower() in self.mots_composes:
                        token = Token(raw_token)  # Create the token object
                        token.token_id = token_id  # Assign the token ID
                        token.token_pid=token_pid
                        token.token_primarykey=(token_pid,token_id)
                        tokens.append(token)
                        token_id += 1
                    else:
                        # Split the word by dashes and tokenize each part
                        split_tokens = re.split(r'(-)', raw_token)
                        for part in split_tokens:
                            if part == '-':
                                continue  # Skip dashes
                            token = Token(part)  # Create the token object
                            token.token_id = token_id  # Assign the token ID
                            token.token_pid=token_pid
                            token.token_primarykey=(token_pid,token_id)
                            tokens.append(token)
                            token_id += 1
                else:
                    token = Token(raw_token)  # Create the token object
                    token.token_id = token_id  # Assign the token ID
                    token.token_pid=token_pid
                    token.token_primarykey=(token_pid,token_id)
                    tokens.append(token)
                    token_id += 1

        return tokens
