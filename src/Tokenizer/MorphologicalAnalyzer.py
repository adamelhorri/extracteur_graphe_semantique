# src/MorphologicalAnalyzer.py
#todo : reparer les genders et numbers mixtes  (extraction du det d'avant si le mot est multigender , sinon du mot qui viens après)
from Tokenizer.Lexicon import Lexicon
import re
import logging

class MorphologicalAnalyzer:
    def __init__(self, stop_words=None):
        """
        Initialize the MorphologicalAnalyzer class.

        Parameters:
            stop_words (set): A set of stop words. If None, a default set is used.
        """
        # Définir une liste de mots-vides (stop words). Vous pouvez la personnaliser selon vos besoins.
        if stop_words is None:
            self.stop_words = {'les', 'le', 'la', 'les', 'un', 'une', 'et', 'ou', 'mais', 'en', 'dans', 'de', 'du', 'des'}
        else:
            self.stop_words = stop_words

    def analyze(self, tokens: list, lexicon: Lexicon) -> list:
        """
        Perform morphological analysis on a list of tokens.

        Parameters:
            tokens (list): List of Token objects to analyze.
            lexicon (Lexicon): Instance of Lexicon to look up word forms.

        Returns:
            list: The list of tokens with added morphological information.
        """
        for token in tokens:
            # Définir si le token est alphabétique
            token.set_alpha(token.text.isalpha())

            # Définir la forme du token (majuscule, minuscule, etc.)
            token.set_shape(self.get_shape(token.text))
            if token.shape_ == "x" and token.text!="a" and token.text!="à" and token.text!="y":
            
                token.text += "'"

            # Définir si le token est un mot-vidage
            token.set_stop(token.text.lower() in self.stop_words)
            
            # Extraire les lemmes pour le token
            lexicon.extract_lemmas([token])

            # Extraire les POS candidates et les trier par score décroissant
            lexicon.extract_pos([token])
            pos_results_sorted = sorted(token.pos_candidates, key=lambda x: x[1], reverse=True)

            # Initialiser les caractéristiques morphologiques
            morphological_features = {}
            gender = None
            number = None

            # Parcourir tous les candidats POS pour extraire les caractéristiques morphologiques
            for pos, score in pos_results_sorted:
                # Extraction des caractéristiques morphologiques en fonction du POS
                if pos.startswith(('Det', 'Nom', 'Adj', 'Pro')):
                    gender_number = self.extract_gender_number(pos)
                    # Mettre à jour le genre si trouvé et non encore défini
                    if 'Gender' in gender_number and not gender:
                        gender = gender_number['Gender']
                        morphological_features['Gender'] = gender
                    # Mettre à jour le nombre si trouvé et non encore défini
                    if 'Number' in gender_number and not number:
                        number = gender_number['Number']
                        morphological_features['Number'] = number
                elif pos.startswith(('Number:', 'Gender:')):
                    gender_number = self.extract_gender_number(pos)
                    # Mettre à jour le genre si trouvé et non encore défini
                    if 'Gender' in gender_number and not gender:
                        gender = gender_number['Gender']
                        morphological_features['Gender'] = gender
                    # Mettre à jour le nombre si trouvé et non encore défini
                    if 'Number' in gender_number and not number:
                        number = gender_number['Number']
                        morphological_features['Number'] = number
                elif pos.startswith('Ver'):
                    verbal_features = self.extract_verbal_features(pos)
                    # Mettre à jour les caractéristiques verbales
                    for feature, value in verbal_features.items():
                        if feature not in morphological_features:
                            morphological_features[feature] = value

                # Continuer à parcourir tous les POS pour extraire toutes les caractéristiques disponibles

            # Assignation des caractéristiques morphologiques au token
            if gender:
                token.set_gender(gender)
            if number:
                token.set_number(number)

            # Assignation des autres caractéristiques morphologiques
            token.set_morphological_features(morphological_features)

            # **Ne pas définir l'entité nommée, les dépendances, etc. pour le moment**

        return tokens

    def extract_gender_number(self, pos_tag: str) -> dict:
        """
        Extract gender and number from the POS tag.

        Parameters:
            pos_tag (str): The POS tag string.

        Returns:
            dict: Dictionary with 'Gender' and 'Number' if found.
        """
        features = {}
        # Séparer le POS tag par ':' et '+'
        parts = re.split(r'[:+]', pos_tag)

        # Mapping des abréviations
        gender_map = {'Mas': 'Mas', 'Fem': 'Fem'}
        number_map = {'Sing': 'Sing', 'Plur': 'Plur', 'SG': 'Sing', 'SGN': 'Sing', 'PL': 'Plur'}

        for part in parts:
            if part in gender_map:
                features['Gender'] = gender_map[part]
            elif part in number_map:
                features['Number'] = number_map[part]

        logging.debug(f"Extracted features from POS tag '{pos_tag}': {features}")
        return features

    def extract_verbal_features(self, pos_tag: str) -> dict:
        """
        Extract verbal morphological features from the POS tag.

        Parameters:
            pos_tag (str): The POS tag string.

        Returns:
            dict: Dictionary with verbal morphological features.
        """
        features = {}
        verbal_time_match = re.search(r'VerbalTime:([^:]+)', pos_tag)
        verbal_mode_match = re.search(r'VerbalMode:([^:]+)', pos_tag)
        verbal_pers_match = re.search(r'VerbalPers:([^:]+)', pos_tag)
        verbal_number_match = re.search(r'VerbalNumber:([^:]+)', pos_tag)

        if verbal_time_match:
            features['VerbalTime'] = verbal_time_match.group(1)
        if verbal_mode_match:
            features['VerbalMode'] = verbal_mode_match.group(1)
        if verbal_pers_match:
            features['VerbalPers'] = verbal_pers_match.group(1)
        if verbal_number_match:
            # Gestion des abréviations pour le nombre verbal
            verbal_number = verbal_number_match.group(1)
            if verbal_number == 'PL':
                verbal_number = 'Plur'
            elif verbal_number == 'SG':
                verbal_number = 'Sing'
            features['VerbalNumber'] = verbal_number

        logging.debug(f"Extracted verbal features from POS tag '{pos_tag}': {features}")
        return features

    def get_shape(self, text: str) -> str:
        """
        Determine the shape of the token text, similar to SpaCy's shape_ attribute.

        Parameters:
            text (str): The token text.

        Returns:
            str: The shape string.
        """
        shape = ''
        for char in text:
            if char.isupper():
                shape += 'X'
            elif char.islower():
                shape += 'x'
            elif char.isdigit():
                shape += 'd'
            else:
                shape += char
        
        return shape
