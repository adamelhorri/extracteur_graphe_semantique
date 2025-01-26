import logging
import json
from Tokenizer.MorphologicalAnalyzer import MorphologicalAnalyzer
from Tokenizer.Token_ import Token

class Disambiguator:
    POS_MAPPING = {
        "Adj": "ADJ",
        "Pre": "ADP",
        "Adv": "ADV",
        "Ver": "VERB",
        "Conj:Coord": "CCONJ",
        "Conj": "SCONJ",
        "Con": "SCONJ",
        "con": "SCONJ",
        "Det": "DET",
        "Int": "INTJ",
        "Nom": "NOUN",
        "Part": "PART",
        "Pro": "PRON",
        "Punct": "PUNCT",
        "Symbole": "SYM",
        "Unit": "VERB"
    }

    def __init__(self, json_file_path='struct_lemma.json'):
        """
        Initialize the Disambiguator with an optional JSON file for lemma replacements.
        """
        logging.info("Disambiguator initialized with hardcoded logic.")
        self.lemma_replacement_rules = self.load_json_rules(json_file_path)

    def load_json_rules(self, json_file_path):
        """
        Load JSON lemma replacement rules from the specified file.

        Parameters:
            json_file_path (str): Path to the JSON file containing replacement rules.

        Returns:
            dict: A dictionary with lemma replacement rules.
        """
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.debug(f"JSON file '{json_file_path}' not found.")
            return {}

    def map_pos_to_spacy(self, pos):
        """
        Map custom POS to spaCy POS tags.

        Parameters:
            pos (str): Custom POS tag.

        Returns:
            str: Mapped spaCy POS tag.
        """
        for key, value in self.POS_MAPPING.items():
            if pos.startswith(key):
                logging.debug(f"Mapping POS '{pos}' to '{value}'")
                return value
        logging.warning(f"POS '{pos}' not mapped, defaulting to 'X'")
        return "X"  # Default if no match found

    def disambiguate(self, tokens, morphological_analyzer, lexicon):
        """
        Disambiguate POS and lemmata for a list of tokens.

        Parameters:
            tokens (list): List of Token objects.
            morphological_analyzer (MorphologicalAnalyzer): Instance of the morphological analyzer.
            lexicon (Lexicon): Lexicon instance to use for morphology extraction.

        Returns:
            list: List of tokens with disambiguated POS and lemmata.
        """
        logging.info("Starting disambiguation process")
        prev_pos = 'BOS'  # Begin of sentence marker
        prev_token = None  # To keep track of the previous token
        prev_prev_token = None  # To keep track of the token before the previous token

        for i, token in enumerate(tokens):
            # Get the next token if available
            next_token = tokens[i + 1] if i + 1 < len(tokens) else None

            # Disambiguate POS
            pos_candidates = token.pos_candidates  # List of tuples (POS, score)
            logging.info(f"***** Disambiguation token: {token.text}")
            logging.debug(f"POS candidates for '{token.text}': {pos_candidates}")
            disamb_pos = self.disambiguate_pos(prev_pos, pos_candidates, next_token, morphological_analyzer, lexicon)

            # Map the selected POS to spaCy format
            spacy_pos = self.map_pos_to_spacy(disamb_pos)
            token.pos_ = spacy_pos
            logging.debug(f"Disambiguated POS for '{token.text}': {spacy_pos}")

            # Disambiguate Lemma
            lemma_candidates = sorted(token.lemma_candidates, key=lambda x: x[1], reverse=True)  # Sort by score
            disamb_lemma = self.disambiguate_lemma(spacy_pos, lemma_candidates, token, morphological_analyzer, lexicon)
            token.lemma_ = disamb_lemma
            logging.debug(f"Disambiguated Lemma for '{token.text}': {disamb_lemma}")

            # Check if it's an auxiliary verb and update POS accordingly
            auxiliary_verbs = ["être", "avoir"]
            if token.pos_ == "VERB" and token.lemma_ in auxiliary_verbs:
                token.pos_ = "AUX"
                logging.debug(f"Token '{token.text}' reclassified as AUX")

            # New condition: If a verb is preceded by an element that has 'Ver' in its pos_candidates
            # and 'être' or 'avoir' in its lemma_candidates, reclassify the preceding element as 'AUX'
            if token.pos_ == "VERB" and prev_token:
                # Check if 'Ver' is in prev_token.pos_candidates
                prev_has_ver = any(cand.startswith("Ver") for cand, _ in prev_token.pos_candidates)
                # Check if 'être' or 'avoir' is in prev_token.lemma_candidates
                prev_has_aux_lemma = any(lemma in auxiliary_verbs for lemma, _ in prev_token.lemma_candidates)
                if prev_has_ver and prev_has_aux_lemma:
                    original_pos = prev_token.pos_
                    prev_token.pos_ = "AUX"
                    logging.debug(f"Prev token '{prev_token.text}' reclassified from '{original_pos}' to 'AUX' based on new condition.")
            # New condition: If two NOUNs follow each other and the second has 'Ver' in pos_candidates
            if prev_token and prev_token.pos_ == "NOUN" and token.pos_ == "NOUN":
                # Check if the current token has 'Ver' in its pos_candidates
                current_has_ver = any(cand.startswith("Ver") for cand, _ in token.pos_candidates)
                if current_has_ver:
                    original_pos = token.pos_
                    token.pos_ = "VERB"
                    logging.debug(f"Token '{token.text}' reclassified from '{original_pos}' to 'VERB' based on new condition.")
                    
                    # Re-disambiguate lemma with the new POS
                    disamb_lemma = self.disambiguate_lemma(token.pos_, lemma_candidates, token, morphological_analyzer, lexicon)
                    token.lemma_ = disamb_lemma
                    logging.debug(f"Re-disambiguated Lemma for '{token.text}' after POS change: {disamb_lemma}")

            # Condition existante : Transformation du POS si deux tokens adjacents sont des NOUN et possèdent un candidat 'Adj'
            if prev_token and prev_token.pos_ == "NOUN" and token.pos_ == "NOUN":
                # Check if either token has 'Adj' in their pos_candidates
                prev_has_adj = any(cand.startswith("Adj") for cand, _ in prev_token.pos_candidates)
                current_has_adj = any(cand.startswith("Adj") for cand, _ in token.pos_candidates)

                if prev_has_adj or current_has_adj:
                    adj_tokens = []

                    if prev_has_adj:
                        # Get the highest score for 'Adj' candidate in prev_token
                        prev_adj_scores = [score for cand, score in prev_token.pos_candidates if cand.startswith("Adj")]
                        if prev_adj_scores:
                            prev_max_adj_score = max(prev_adj_scores)
                            adj_tokens.append((prev_token, prev_max_adj_score))

                    if current_has_adj:
                        # Get the highest score for 'Adj' candidate in token
                        current_adj_scores = [score for cand, score in token.pos_candidates if cand.startswith("Adj")]
                        if current_adj_scores:
                            current_max_adj_score = max(current_adj_scores)
                            adj_tokens.append((token, current_max_adj_score))

                    if adj_tokens:
                        # Select the token with the highest 'Adj' score
                        token_to_modify, _ = max(adj_tokens, key=lambda x: x[1])
                        original_pos = token_to_modify.pos_
                        token_to_modify.pos_ = "ADJ"
                        print(
                            f"Modified POS of token '{token_to_modify.text}' from '{original_pos}' to 'ADJ' "
                            f"due to adjacent NOUNs with 'Adj' candidates."
                        )
            # Nouvelle condition spécifique : ADJ + "et" + NOUN avec candidat 'Adj'
            if (
                prev_prev_token
                and prev_token
                and prev_prev_token.pos_ == "ADJ"
                and prev_token.text.lower() == "et" or "ou"  # Vérifier spécifiquement le mot "et" et ou
                
                and token.pos_ == "NOUN"
                and any(cand.startswith("Adj") for cand, _ in token.pos_candidates)
            ):
                # Transformer le POS en 'ADJ'
                original_pos = token.pos_
                #token.pos_ = "ADJ"
                logging.debug(
                    f"Modified POS of token '{token.text}' from '{original_pos}' to 'ADJ' "
                    f"due to pattern ADJ + 'et' + NOUN with 'Adj' candidate."
                )
            if token.text=="car":
                token.pos_="CCONJ"
            if token.text.lower() in {"ce","ces"}:
                token.pos_="DET"
            if token.text=="ne":
                token.pos_="ADV"
            if prev_token and prev_token.text=="ne":
                token.pos_="VERB"
            if token.text in {"leur","leurs","son","sa","ses","son","ta","ton","tes","ma","mon","mes","votre","vos"}:
                token.pos_="DET"
            if token.text in {"dessus","dessous"}:
                token.pos_="ADP"
        
            # Update the context POS and tokens for the next iteration
            prev_pos = disamb_pos if disamb_pos else 'BOS'
            prev_prev_token = prev_token
            prev_token = token

        logging.info("Disambiguation of lemmata and POS complete")
        return tokens

    def disambiguate_pos(self, prev_pos, pos_candidates, next_token=None, morphological_analyzer=None, lexicon=None):
        """
        Select the best POS candidate based on hardcoded logic, disambiguating the next token first if available.
        If the previous POS is 'DET' and current candidate is 'VERB', reclassify it as 'NOUN'.

        Parameters:
            prev_pos (str): POS of the previous token.
            pos_candidates (list): List of tuples (POS, score).
            next_token (Token): The next token, if available, to disambiguate before current token.
            morphological_analyzer (MorphologicalAnalyzer): Instance of the morphological analyzer.
            lexicon (Lexicon): Lexicon instance to use for morphology extraction.

        Returns:
            str: The selected POS tag or 'X' if no candidates are available.
        """
        if not pos_candidates:
            logging.warning(f"No POS candidates available for previous POS '{prev_pos}'. Assigning 'X' as default POS.")
            return 'X'  # Assign a default POS

        # Ensure prev_pos is a string
        if prev_pos is None:
            prev_pos = 'BOS'  # Begin of sentence marker

        # Disambiguate the next token first if available
        if next_token and not next_token.pos_:
            logging.info(f"Disambiguating the next token: {next_token.text}")
            next_pos_candidates = next_token.pos_candidates
            logging.info(f"POS candidates for next token '{next_token.text}': {next_pos_candidates}")
            next_pos = self.disambiguate_pos(prev_pos, next_pos_candidates, None, morphological_analyzer, lexicon)
            logging.info(f"Disambiguated POS for next token '{next_token.text}': {next_pos}")
            next_token.pos_ = self.map_pos_to_spacy(next_pos)

        logging.info(f"Previous token POS: {prev_pos}")

        # Special rule: If the previous POS is 'DET' and the current candidate is 'VERB', reclassify as 'NOUN'
        for candidate, score in pos_candidates:
            if candidate.startswith("Ver") and prev_pos.startswith("Det"):
                logging.info(f"Reclassifying 'VERB' as 'NOUN' since it's preceded by a 'DET'.")
                return "Nom"  # Map to 'NOUN' in the custom POS system

        # Special handling based on next token's POS
        if next_token and next_token.pos_:
            for candidate, score in pos_candidates:
                if candidate.startswith("Det") and next_token.pos_ in ['NOUN', 'PROPN']:
                    logging.info(f"Favoring 'DET' for candidate '{candidate}' based on next token POS '{next_token.pos_}'.")
                    return candidate
                if candidate.startswith("Pre") and next_token.pos_ in ['NOUN', 'PROPN', 'PRON']:
                    logging.info(f"Favoring 'ADP' for candidate '{candidate}' based on next token POS '{next_token.pos_}'.")
                    return candidate
                if candidate.startswith("Pro") and next_token.pos_ in ['VERB', 'ADP']:
                    logging.info(f"Favoring 'PRON' for candidate '{candidate}' based on next token POS '{next_token.pos_}'.")
                    return candidate

        # Define POS priority for tie-breaking (Adj has higher priority than Nom)
        pos_priority = ['Adj', 'Nom', 'Ver', 'Adv', 'Pro', 'Det', 'Punct', 'Pre']

        def get_pos_priority(pos, prev_pos=None):
            # Adjust priority based on context
            if prev_pos is not None:
                if pos.startswith('Adj') and prev_pos.startswith('Nom'):
                    # If current POS is 'Adj' and previous POS is 'Nom', prefer 'Adj'
                    return -1  # Highest priority
                if pos.startswith('Nom') and prev_pos.startswith('Det'):
                    # If current POS is 'Nom' and previous POS is 'Det', prefer 'Nom'
                    return -2  # Second highest priority
            # Default priority
            for idx, prefix in enumerate(pos_priority):
                if pos.startswith(prefix):
                    return idx
            return len(pos_priority)  # If not found, assign lowest priority

        # Default behavior: Select the candidate with the highest score and highest priority
        best_pos = max(pos_candidates, key=lambda x: (x[1], -get_pos_priority(x[0], prev_pos)))
        selected_pos = best_pos[0]
        logging.debug(f"Selected best POS '{selected_pos}' based on highest score and priority.")
        
        return selected_pos

    def disambiguate_lemma(self, pos, lemma_candidates, token, morphological_analyzer, lexicon, prev_pos=None):
        """
        Disambiguate the lemma for a token based on its POS and lemma candidates.

        Parameters:
            pos (str): The disambiguated POS tag of the token.
            lemma_candidates (list): List of tuples (lemma, score).
            token (Token): The token being processed.
            morphological_analyzer (MorphologicalAnalyzer): Instance of the morphological analyzer.
            lexicon (Lexicon): Lexicon instance to use for morphology extraction.
            prev_pos (str): POS of the previous token, if available.

        Returns:
            str: The selected lemma or None if no candidates are available.
        """
        if pos is None:
            logging.warning("POS is None, cannot disambiguate lemma.")
            return None

        if not lemma_candidates:
            logging.warning(f"No lemma candidates available for POS '{pos}'. Assigning the token itself as lemma.")
            return token.text.lower()  # Default to the lowercase form of the token itself

        # Step 1: If POS is 'VERB', prefer lemmas that have 'Ver:Inf' in their pos_candidates
        if pos == 'VERB':
            verb_inf_lemmas = []
            for lemma, score in lemma_candidates:
                temp_token = Token(lemma)
                # Analyze the temp_token to get its pos_candidates
                morphological_analyzer.analyze([temp_token], lexicon)
                # Check if 'Ver:Inf' is in temp_token.pos_candidates
                if any(cand.startswith('Ver:Inf') for cand, _ in temp_token.pos_candidates):
                    verb_inf_lemmas.append((lemma, score))
            if verb_inf_lemmas:
                # If we have verb infinitive lemmas, select the one with the highest score
                best_lemma = max(verb_inf_lemmas, key=lambda x: x[1])[0]
                logging.debug(f"Selected verb infinitive lemma: {best_lemma}")
                return best_lemma
            else:
                # No verb infinitive lemmas found, default to highest scoring lemma
                best_lemma = max(lemma_candidates, key=lambda x: x[1])[0]
                logging.debug(f"No infinitive verb lemmas found, selected best lemma: {best_lemma}")
                return best_lemma
        else:
            # Step 2: Evaluate each lemma candidate for POS matching
            pos_matched_lemmas = []
            for lemma, score in lemma_candidates:
                temp_token = Token(lemma)
                # Analyze temp_token to get its morphological features
                morphological_analyzer.analyze([temp_token], lexicon)
                # Map the first pos_candidate to spaCy POS
                temp_token.pos_ = self.map_pos_to_spacy(temp_token.pos_candidates[0][0]) if temp_token.pos_candidates else None
                if temp_token.pos_ == pos:
                    pos_matched_lemmas.append((temp_token, lemma, score))

            # Step 3: If no POS-matched lemmas, return the highest scoring lemma
            if not pos_matched_lemmas:
                best_lemma = max(lemma_candidates, key=lambda x: x[1])[0]
                logging.debug(f"No POS-matched lemmas found, selected best lemma: {best_lemma}")
                return best_lemma

            # Step 4: Among POS-matched lemmas, prefer singular candidates
            singular_lemmas = [lemma_info for lemma_info in pos_matched_lemmas if lemma_info[0].morph.get('Number') == 'Sing']
            if singular_lemmas:
                pos_matched_lemmas = singular_lemmas
                logging.debug(f"Filtered lemmas to prefer singular: {[lemma_info[1] for lemma_info in pos_matched_lemmas]}")

            # Step 5: Among remaining lemmas, prefer masculine lemmas
            masculine_lemmas = [lemma_info for lemma_info in pos_matched_lemmas if lemma_info[0].morph.get('Gender') == 'Mas']
            if masculine_lemmas:
                pos_matched_lemmas = masculine_lemmas
                logging.debug(f"Filtered lemmas to prefer masculine: {[lemma_info[1] for lemma_info in masculine_lemmas]}")

            # Step 6: Return the highest scoring lemma among the remaining filtered ones
            best_lemma = max(pos_matched_lemmas, key=lambda x: x[2])[1]
            logging.debug(f"Best lemma selected after preferences: {best_lemma}")

            # Step 7: Check if a rule from the JSON file applies (occurrences > 15)
            normalized_text = token.text.lower().strip()
            key = f"{normalized_text}_{pos}"

            logging.debug(f"Key being used for JSON lookup: {key}")

            if key in self.lemma_replacement_rules:
                rule = self.lemma_replacement_rules[key]
                logging.debug(f"Rule found for key: {key} with occurrences {rule['occurrences']}")
                if rule["occurrences"] > 15:
                    if best_lemma == rule["structure"]["system_lemma"]:
                        logging.info(f"Replacing '{best_lemma}' with spaCy lemma '{rule['structure']['spacy_lemma']}' due to occurrence threshold.")
                        best_lemma = rule['structure']['spacy_lemma']
                        return best_lemma
                    else:
                        logging.debug(f"Best lemma '{best_lemma}' does not match system lemma '{rule['structure']['system_lemma']}'")
                else:
                    logging.debug(f"Occurrences for key '{key}' are less than or equal to 15: {rule['occurrences']}")
            else:
                logging.debug(f"No rule found for key: {key}")

            return best_lemma

    def is_proper_noun(self, pos):
        """
        Determine if a POS tag corresponds to a proper noun.

        Parameters:
            pos (str): The POS tag.

        Returns:
            bool: True if POS corresponds to a proper noun, False otherwise.
        """
        proper_noun_pos_tags = ['NOUN', 'PROPN']  # PROPN is the tag for proper nouns
        return pos in proper_noun_pos_tags
