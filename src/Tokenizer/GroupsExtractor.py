class GroupExtractor:
    def __init__(self):
        pass

    def extract_groups(self, tokens):
        """
        Extrait les groupes nominaux (GN) et les groupes verbaux (GV) des tokens.
        Met à jour chaque token avec les intervalles des groupes auxquels il appartient.
        """
        # Extraction des groupes nominaux
        noun_phrases = self.extract_noun_phrases(tokens)
        # Extraction des groupes verbaux
        verb_phrases = self.extract_verb_phrases(tokens)

        # Mise à jour des tokens avec les groupes nominaux
        for np in noun_phrases:
            for token in tokens:
                if token.token_primarykey >= np['start'] and token.token_primarykey <= np['end']:
                    if token.groupe is None:
                        token.groupe = []
                    token.groupe.append({'type': 'GN', 'range': (np['start'], np['end'])})

        # Mise à jour des tokens avec les groupes verbaux
        for vp in verb_phrases:
            for token in tokens:
                if token.token_primarykey >= vp['start'] and token.token_primarykey <= vp['end']:
                    if token.groupe is None:
                        token.groupe = []
                    token.groupe.append({'type': 'GV', 'range': (vp['start'], vp['end'])})

        return tokens

    def extract_noun_phrases(self, tokens):
        """
        Identifie les groupes nominaux dans la liste de tokens.
        Retourne une liste de dictionnaires avec les clés 'start' et 'end' représentant les intervalles des GN.
        """
        noun_phrases = []
        for token in tokens:
            if token.pos_ in ('NOUN', 'PROPN'):
                np = self.build_noun_phrase(token, tokens)
                if np not in noun_phrases:
                    noun_phrases.append(np)
        return noun_phrases

    def build_noun_phrase(self, token, tokens):
        """
        Construit un groupe nominal à partir d'un nom donné.
        Retourne un dictionnaire avec les clés 'start' et 'end'.
        """
        start = token.token_primarykey
        end = token.token_primarykey

        # Inclure les modificateurs à gauche (déterminants, adjectifs, etc.)
        current = token
        while True:
            lefts = [t for t in tokens if t.head == current and t.dep_ in ('det', 'amod', 'nmod') and t.token_primarykey < current.token_primarykey]
            if not lefts:
                break
            left = min(lefts, key=lambda x: x.token_primarykey)
            start = left.token_primarykey
            current = left

        # Inclure les modificateurs à droite (prépositions, compléments du nom)
        current = token
        while True:
            rights = [t for t in tokens if t.head == current and t.dep_ in ('amod', 'nmod', 'case') and t.token_primarykey > current.token_primarykey]
            if not rights:
                break
            right = max(rights, key=lambda x: x.token_primarykey)
            end = right.token_primarykey
            current = right

        # Extraire les GN internes (e.g., "du gentil fermier")
        internal_nps = []
        for t in tokens:
            if t.token_primarykey >= start and t.token_primarykey <= end and t.pos_ in ('NOUN', 'PROPN') and t != token:
                internal_np = self.build_noun_phrase(t, tokens)
                internal_nps.append(internal_np)

        # Ajouter les GN internes s'il y en a
        noun_phrase = {'start': start, 'end': end}
        if internal_nps:
            noun_phrase['internal'] = internal_nps

        return noun_phrase

    def extract_verb_phrases(self, tokens):
        """
        Identifie les groupes verbaux dans la liste de tokens.
        Retourne une liste de dictionnaires avec les clés 'start' et 'end' représentant les intervalles des GV.
        """
        verb_phrases = []
        for token in tokens:
            if token.pos_ == 'VERB' and token.dep_ == 'ROOT':
                vp = self.build_verb_phrase(token, tokens)
                if vp not in verb_phrases:
                    verb_phrases.append(vp)
        return verb_phrases

    def build_verb_phrase(self, token, tokens):
        """
        Construit un groupe verbal à partir d'un verbe donné.
        Retourne un dictionnaire avec les clés 'start' et 'end'.
        """
        start = token.token_primarykey
        end = token.token_primarykey

        # Inclure les auxiliaires et les modificateurs à gauche
        current = token
        while True:
            lefts = [t for t in tokens if t.head == current and t.dep_ in ('aux', 'aux:pass', 'neg') and t.token_primarykey < current.token_primarykey]
            if not lefts:
                break
            left = min(lefts, key=lambda x: x.token_primarykey)
            start = left.token_primarykey
            current = left

        # Inclure les objets et les modificateurs à droite
        rights = [t for t in tokens if t.head == token and t.dep_ in ('obj', 'iobj', 'obl', 'xcomp', 'advmod', 'advcl', 'ccomp')]
        for right in rights:
            end = max(end, right.token_primarykey)
            # Inclure les modificateurs de l'objet
            if right.pos_ in ('NOUN', 'PRON', 'PROPN'):
                np = self.build_noun_phrase(right, tokens)
                end = max(end, np['end'])

        verb_phrase = {'start': start, 'end': end}
        return verb_phrase
