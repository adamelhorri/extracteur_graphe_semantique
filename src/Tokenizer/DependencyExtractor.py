class DependencyExtractor:
    def __init__(self):
        pass

    def extract_dependencies(self, tokens):
        clauses = self.segment_into_clauses(tokens)
        for clause in clauses:
            self.process_clause(clause)
        return tokens

    def segment_into_clauses(self, tokens):
        clauses = []
        clause = []
        for token in tokens:
            clause.append(token)
            if token.pos_ == 'PUNCT' and token.text in ('.', '!', '?', ';'):
                clauses.append(clause)
                clause = []
        if clause:
            clauses.append(clause)
        return clauses

    def process_clause(self, clause_tokens):
        root_token = self.identify_root(clause_tokens)
        for token in clause_tokens:
            if token == root_token:
                token.dep_ = 'ROOT'
                token.head = token
            else:
                self.assign_dependencies(token, clause_tokens, root_token)
                # Ensure that dep_ and head are set
                if token.dep_ is None:
                    token.dep_ = 'dep'
                if token.head is None:
                    token.head = root_token

    def identify_root(self, tokens):
        # Priorité aux verbes finis qui ne sont pas auxiliaires
        for token in tokens:
            if token.pos_ == 'VERB' and token.morph.get('VerbForm') == 'Fin':
                return token
        # Identifier les constructions passives
        for idx, token in enumerate(tokens):
            if token.pos_ == 'AUX' and token.lemma_ == 'être':
                next_idx = idx + 1
                if next_idx < len(tokens):
                    next_token = tokens[next_idx]
                    if next_token.pos_ == 'VERB' and 'Part' in next_token.morph.get('VerbForm', ''):
                        return next_token  # Le participe passé est le ROOT
        # Ensuite tout verbe
        for token in tokens:
            if token.pos_ == 'VERB':
                return token
        # Ensuite les noms
        for token in tokens:
            if token.pos_ in ('NOUN', 'PROPN'):
                return token
        # Par défaut, le premier token
        return tokens[0]

    def assign_dependencies(self, token, tokens, root_token):
        if token.pos_ == 'DET':
            self.assign_det_dependency(token, tokens, root_token)
        elif token.pos_ in ('NOUN', 'PROPN'):
            self.assign_noun_dependencies(token, tokens, root_token)
        elif token.pos_ == 'PRON':
            if token.lemma_.lower() in ('qui', 'que', 'dont', 'où'):
                self.assign_relative_clause(token, tokens, root_token)
            else:
                self.assign_pron_dependency(token, tokens, root_token)
        elif token.pos_ == 'ADJ':
            self.assign_adj_dependency(token, tokens, root_token)
        elif token.pos_ == 'ADV':
            self.assign_adv_dependency(token, tokens, root_token)
        elif token.pos_ == 'VERB':
            self.assign_verb_dependency(token, tokens, root_token)
        elif token.pos_ == 'AUX':
            self.assign_aux_dependency(token, tokens, root_token)
        elif token.pos_ == 'ADP':
            self.assign_adp_dependency(token, tokens, root_token)
        elif token.pos_ == 'CCONJ':
            self.assign_cc_dependency(token, tokens, root_token)
        elif token.pos_ == 'SCONJ':
            self.assign_sconj_dependency(token, tokens, root_token)
        elif token.pos_ == 'PUNCT':
            token.dep_ = 'punct'
            token.head = root_token
        else:
            token.dep_ = 'dep'
            token.head = root_token

    def assign_det_dependency(self, token, tokens, root_token):
        head = self.find_next_token(token, tokens, ('NOUN', 'PROPN', 'ADJ'))
        if head:
            token.dep_ = 'det'
            token.head = head
        else:
            # Assign to root_token if no head is found
            token.dep_ = 'det'
            token.head = root_token

    def assign_noun_dependencies(self, token, tokens, root_token):
        idx = token.token_id
        # Vérifier si le nom est précédé d'une préposition
        if idx > 0 and tokens[idx - 1].pos_ == 'ADP':
            preposition = tokens[idx - 1]
            if preposition.text == 'par' and self.is_passive(root_token, tokens):
                # Agent dans une construction passive
                token.dep_ = 'obl:agent'
                token.head = root_token
                preposition.dep_ = 'case'
                preposition.head = token
            else:
                # Modificateur nominal ou oblique
                governing_noun = self.find_previous_token(preposition, tokens, ('NOUN', 'PROPN', 'PRON', 'ADJ'))
                if governing_noun:
                    # Modificateur nominal
                    token.dep_ = 'nmod'
                    token.head = governing_noun
                else:
                    # Modificateur oblique du verbe
                    token.dep_ = 'obl'
                    token.head = root_token
                preposition.dep_ = 'case'
                preposition.head = token
        elif self.is_coordinated(token, tokens):
            token.dep_ = 'conj'
            token.head = self.find_previous_noun(token, tokens) or root_token
        else:
            verb = root_token  # Utiliser le root_token comme verbe principal
            if self.is_subject(token, verb):
                token.dep_ = 'nsubj:pass' if self.is_passive(verb, tokens) else 'nsubj'
                token.head = verb
            else:
                token.dep_ = 'obj'
                token.head = verb

    def assign_adj_dependency(self, token, tokens, root_token):
        idx = token.token_id
        prev_token = tokens[idx - 1] if idx > 0 else None
        next_token = tokens[idx + 1] if idx + 1 < len(tokens) else None

        if next_token and next_token.pos_ in ('NOUN', 'PROPN', 'PRON'):
            token.dep_ = 'amod'
            token.head = next_token
        elif prev_token and prev_token.pos_ in ('NOUN', 'PROPN', 'PRON'):
            token.dep_ = 'amod'
            token.head = prev_token
        elif prev_token and prev_token.pos_ == 'AUX':
            token.dep_ = 'ROOT'
            token.head = token
        else:
            token.dep_ = 'dep'
            token.head = root_token

    def assign_adv_dependency(self, token, tokens, root_token):
        # Gérer les conjonctions subordonnées composées comme "tandis que"
        if token.text.lower() == 'tandis':
            token.dep_ = 'mark'
            token.head = self.find_next_verb(token, tokens) or root_token
            next_idx = token.token_id + 1
            if next_idx < len(tokens) and tokens[next_idx].text.lower() == 'que':
                tokens[next_idx].dep_ = 'fixed'
                tokens[next_idx].head = token
        else:
            head = self.find_previous_token(token, tokens, ('VERB', 'ADJ', 'ADV')) or root_token
            token.dep_ = 'advmod'
            token.head = head

    def assign_pron_dependency(self, token, tokens, root_token):
        verb = root_token  # Utiliser le root_token comme verbe principal
        if self.is_subject(token, verb):
            token.dep_ = 'nsubj'
        else:
            token.dep_ = 'obj'
        token.head = verb

    def assign_verb_dependency(self, token, tokens, root_token):
        if token == root_token:
            return
        if self.is_subordinated(token, tokens):
            token.dep_ = 'advcl'
            token.head = root_token
        elif self.is_coordinated(token, tokens):
            token.dep_ = 'conj'
            token.head = self.find_previous_token(token, tokens, ('VERB',)) or root_token
        else:
            token.dep_ = 'xcomp'
            token.head = root_token

    def assign_aux_dependency(self, token, tokens, root_token):
        if token.lemma_ == 'être' and root_token.pos_ == 'VERB' and 'Part' in root_token.morph.get('VerbForm', ''):
            token.dep_ = 'aux:pass'
            token.head = root_token
        else:
            token.dep_ = 'aux'
            token.head = root_token

    def assign_adp_dependency(self, token, tokens, root_token):
        idx = token.token_id
        next_idx = idx + 1
        while next_idx < len(tokens) and tokens[next_idx].pos_ == 'DET':
            next_idx += 1
        if next_idx < len(tokens) and tokens[next_idx].pos_ in ('NOUN', 'PROPN', 'PRON'):
            token.dep_ = 'case'
            token.head = tokens[next_idx]
        else:
            token.dep_ = 'mark'
            verb = self.find_next_token(token, tokens, ('VERB',))
            token.head = verb if verb else root_token

    def assign_cc_dependency(self, token, tokens, root_token):
        token.dep_ = 'cc'
        idx = token.token_id
        next_token = tokens[idx + 1] if idx + 1 < len(tokens) else None
        if next_token and next_token.pos_ in ('ADJ', 'NOUN', 'PROPN', 'VERB'):
            token.head = next_token
        else:
            token.head = self.find_previous_token(token, tokens, ('ADJ', 'NOUN', 'PROPN', 'VERB')) or root_token

    def assign_sconj_dependency(self, token, tokens, root_token):
        token.dep_ = 'mark'
        verb = self.find_next_verb(token, tokens)
        if verb:
            token.head = verb
        else:
            # Assign to root_token if no verb is found
            token.head = root_token

    def assign_relative_clause(self, token, tokens, root_token):
        antecedent = self.find_antecedent(token, tokens)
        verb_idx = self.find_next_token_idx(token.token_id, tokens, ('VERB', 'AUX'))
        if antecedent and verb_idx is not None:
            verb = tokens[verb_idx]
            # Vérifier si le verbe est un copule
            if verb.lemma_ == 'être' and verb.pos_ == 'AUX':
                pred_idx = self.find_next_token_idx(verb_idx, tokens, ('NOUN', 'ADJ', 'PRON', 'PROPN'))
                if pred_idx is not None:
                    predicate = tokens[pred_idx]
                    predicate.dep_ = 'acl:relcl'
                    predicate.head = antecedent
                    token.dep_ = 'nsubj'
                    token.head = predicate
                    verb.dep_ = 'cop'
                    verb.head = predicate
                    det = self.find_previous_token(predicate, tokens, ('DET',))
                    if det:
                        det.dep_ = 'det'
                        det.head = predicate
                else:
                    verb.dep_ = 'acl:relcl'
                    verb.head = antecedent
                    token.dep_ = 'nsubj'
                    token.head = verb
            else:
                verb.dep_ = 'acl:relcl'
                verb.head = antecedent
                token.dep_ = 'nsubj' if self.is_subject(token, verb) else 'obj'
                token.head = verb
        else:
            # Assign default dependencies if no antecedent or verb is found
            token.dep_ = 'dep'
            token.head = root_token

    # Méthodes utilitaires

    def is_subject(self, token, verb):
        return token.token_id < verb.token_id

    def is_passive(self, verb, tokens):
        idx = verb.token_id
        if 'Part' in verb.morph.get('VerbForm', '') or 'Part' in verb.morph.get('VerbForm', []):
            for i in range(idx - 1, -1, -1):
                aux = tokens[i]
                if aux.pos_ == 'AUX' and aux.lemma_ == 'être':
                    return True
        return False

    def is_coordinated(self, token, tokens):
        idx = token.token_id
        if idx > 0:
            prev_token = tokens[idx - 1]
            if prev_token.pos_ == 'CCONJ' or prev_token.text.lower() in ('et', 'ou', 'mais', 'ni', 'donc', 'or', 'car'):
                return True
        return False

    def is_subordinated(self, token, tokens):
        idx = token.token_id
        # Vérifier si précédé d'une conjonction subordonnée
        if idx > 0 and tokens[idx - 1].pos_ in ('SCONJ', 'PRON'):
            return True
        # Vérifier pour les conjonctions subordonnées composées
        if idx > 1 and tokens[idx - 2].text.lower() == 'tandis' and tokens[idx - 1].text.lower() == 'que':
            return True
        return False

    def find_previous_token(self, token, tokens, pos_tags):
        idx = token.token_id
        for i in range(idx - 1, -1, -1):
            if tokens[i].pos_ in pos_tags:
                return tokens[i]
        return None

    def find_next_token(self, token, tokens, pos_tags):
        idx = token.token_id
        for i in range(idx + 1, len(tokens)):
            if tokens[i].pos_ in pos_tags:
                return tokens[i]
        return None

    def find_next_token_idx(self, start_idx, tokens, pos_tags):
        for idx in range(start_idx + 1, len(tokens)):
            if tokens[idx].pos_ in pos_tags:
                return idx
        return None

    def find_previous_noun(self, token, tokens):
        for idx in range(token.token_id - 1, -1, -1):
            if tokens[idx].pos_ in ('NOUN', 'PROPN'):
                return tokens[idx]
        return None

    def find_previous_adj_or_noun(self, token, tokens):
        for idx in range(token.token_id - 1, -1, -1):
            if tokens[idx].pos_ in ('ADJ', 'NOUN', 'PROPN'):
                return tokens[idx]
        return None

    def find_antecedent(self, token, tokens):
        for idx in range(token.token_id - 1, -1, -1):
            if tokens[idx].pos_ in ('NOUN', 'PROPN', 'PRON'):
                return tokens[idx]
        return None

    def find_closest_verb(self, token, tokens, root_token):
        # Chercher en arrière
        for idx in range(token.token_id - 1, -1, -1):
            if tokens[idx].pos_ == 'VERB':
                return tokens[idx]
        # Sinon, utiliser le root_token s'il s'agit d'un verbe
        if root_token.pos_ == 'VERB':
            return root_token
        return None

    def find_next_verb(self, token, tokens):
        idx = token.token_id
        for i in range(idx + 1, len(tokens)):
            if tokens[i].pos_ == 'VERB':
                return tokens[i]
        return None
