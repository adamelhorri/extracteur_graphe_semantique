# src/moteur_de_regles.py

import itertools
import re
import os
import csv
import logging
from collections import defaultdict
from ressources_lexicales import RessourcesLexicales
from graphe_semantique import GrapheSemantique
from SyntaxicExtraction import SyntaxicExtraction

class MoteurDeRegles:
    def __init__(self, graphe):
        self.graphe = graphe
        self.regles = []
        self.relation_types = [
            'r_associated', 'r_raff_sem', 'r_pos',
            'r_syn', 'r_syn_syntaxique', 'r_isa',
            'r_hypo', 'r_anto', 'r_anto_syntaxique',
            'r_agent', 'r_patient', 'r_succ',
            'r_lemma', 'r_has_magn', 'r_has_antimagn',
            'r_family', 'r_lieu', 'r_carac'  # Ajout de r_carac
        ]
        self.relations_inverses = {
            'r_agent': 'r_agent-1',
            'r_patient': 'r_patient-1',
            'r_instr': 'r_instr-1',
            'r_domain': 'r_domain-1',
            'r_lieu': 'r_lieu-1',
            # Ajoutez ici toutes les autres relations et leurs inverses si nécessaire
        }

        self.initialiser_csv()
        self.word_counter = 0  # Compteur pour générer des identifiants uniques
        self.token_to_word_id = {}  # Mapping des token_primarykey aux word_ids

    def initialiser_csv(self):
        """Créer les fichiers CSV pour chaque type de relation avec les en-têtes s'ils n'existent pas."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, '..', 'data')
        data_dir = os.path.abspath(data_dir)

        if not os.path.exists(data_dir):
            try:
                os.makedirs(data_dir)
                logging.warning(f"Dossier 'data' créé à {data_dir}")
            except Exception as e:
                logging.error(f"Erreur lors de la création du dossier 'data' à {data_dir}: {e}")

        for rel in self.relation_types:
            csv_filename = f"{rel}.csv"
            csv_path = os.path.join(data_dir, csv_filename)
            if not os.path.exists(csv_path):
                try:
                    with open(csv_path, 'w', encoding='utf-8', newline='') as csvfile:
                        writer = csv.writer(csvfile, delimiter=';')
                        writer.writerow(['source', 'target', 'recurrence'])
                except Exception as e:
                    logging.error(f"Erreur lors de la création du fichier CSV '{csv_filename}': {e}")

    def charger_regles(self, fichier):
        """Charger les règles depuis un fichier texte."""
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                for ligne in f:
                    ligne = ligne.strip()
                    if ligne and not ligne.startswith("#") and ligne.lower() != "relations:":
                        self.regles.append(ligne)
        except FileNotFoundError:
            logging.error(f"Le fichier de règles '{fichier}' est introuvable.")
        except Exception as e:
            logging.error(f"Erreur lors du chargement des règles: {e}")

    def appliquer_regles(self, texte):
        """Appliquer les règles après analyse du texte."""
        try:
            self.ressources = RessourcesLexicales(texte)
            syntaxic_extraction = SyntaxicExtraction(texte)
            tokens = syntaxic_extraction.tokens

            self.appliquer_relations(tokens)
            for regle in self.regles:
                self.appliquer_regle(regle, tokens)
            # Les relations sont déjà enregistrées au fur et à mesure
        except Exception as e:
            logging.error(f"Erreur lors de l'application des règles: {e}")

    def appliquer_relations(self, tokens):
        """Appliquer les relations prédéfinies entre les tokens."""
        previous_word_id = None

        for mot in tokens:
            self.word_counter += 1
            word_id = f"word_{self.word_counter}"
            pos_id = f"pos_{self.word_counter}"
            lemma_id = f"lemma_{self.word_counter}"

            mot_lemma = mot.lemma_.lower()
            mot_pos = mot.pos_.lower()

            try:
                # Ajouter le nœud central du mot avec un identifiant unique
                self.graphe.ajouter_noeud(word_id, 'word', mot.text)

                # Mapper le token_primarykey à word_id
                if mot.token_primarykey:
                    self.token_to_word_id[mot.token_primarykey] = word_id
                    logging.debug(f"Mapping {mot.token_primarykey} -> {word_id}")
                else:
                    logging.error(f"Token '{mot.text}' n'a pas de token_primarykey.")

                # Ajouter le nœud pos unique pour ce mot
                self.graphe.ajouter_noeud(pos_id, 'pos', mot_pos)
                self.graphe.ajouter_relation(word_id, "r_pos", pos_id)
                self.ajouter_relation_csv(word_id, "r_pos", pos_id)

                # Ajouter le nœud lemma unique pour ce mot
                self.graphe.ajouter_noeud(lemma_id, 'lemma', mot_lemma)
                self.graphe.ajouter_relation(word_id, "r_lemma", lemma_id)
                self.ajouter_relation_csv(word_id, "r_lemma", lemma_id)
            except Exception as e:
                logging.error(f"Erreur lors de l'ajout des nœuds pour le mot '{mot.text}': {e}")

            # Gérer la relation r_succ avec le mot précédent
            if previous_word_id:
                try:
                    if not self.graphe.existe_relation(previous_word_id, "r_succ", word_id):
                        self.graphe.ajouter_relation(previous_word_id, "r_succ", word_id)
                        self.ajouter_relation_csv(previous_word_id, "r_succ", word_id)
                except Exception as e:
                    logging.error(f"Erreur lors de l'ajout de la relation 'r_succ' entre '{previous_word_id}' et '{word_id}': {e}")

            previous_word_id = word_id

    def appliquer_regle(self, regle, tokens):
        """Appliquer une règle spécifique aux tokens."""
        try:
            if "⇒" not in regle:
                logging.error(f"Règle mal formée (manque '⇒') : {regle}")
                return

            conditions, actions = regle.split("⇒")
            conditions = conditions.strip()
            actions = actions.strip()
            variables = self.extraire_variables(conditions + ' ' + actions)
            combinations, variable_names = self.generer_combinations(variables, tokens)

            if not combinations:
                logging.warning(f"Règle ignorée '{regle}' en raison de variables manquantes.")
                return

            for tokens_combination in combinations:
                variable_mapping = dict(zip(variable_names, tokens_combination))
                if self.verifier_conditions(conditions, variable_mapping):
                    self.executer_actions(actions, variable_mapping)
        except ValueError:
            logging.error(f"Erreur dans la syntaxe de la règle : {regle}")
        except Exception as e:
            logging.error(f"Erreur lors de l'application de la règle '{regle}': {e}")

    def extraire_variables(self, texte):
        """Extrait les variables du texte."""
        variables = re.findall(r'\$(\w+)', texte)
        return set(variables)

    def generer_combinations(self, variable_names, tokens):
        """Génère toutes les combinaisons possibles de tokens pour les variables."""
        variable_tokens = {}
        for var in variable_names:
            if var == 'cc':
                tokens_var = [token for token in tokens if token.dep_ == 'cc']
            elif var == 'cop':
                tokens_var = [token for token in tokens if token.dep_ == 'cop']
            else:
                tokens_var = [token for token in tokens if token.pos_.upper() != 'PUNCT']

            if tokens_var:
                variable_tokens[var] = tokens_var
            else:
                variable_tokens[var] = [None]
                logging.warning(f"Aucun token trouvé pour la variable '${var}'. La règle peut ne pas s'appliquer correctement.")

        combinations = itertools.product(*[variable_tokens[var] for var in variable_names])
        return combinations, variable_names

    def verifier_conditions(self, conditions, variable_mapping):
        """Vérifie si les conditions sont satisfaites pour un mapping de variables donné."""
        try:
            # Remplacer les opérateurs logiques
            condition_evaluated = conditions.replace('&', 'and').replace('|', 'or')

            def replace_var(match):
                var = match.group(1)
                attr = match.group(2)
                if var in variable_mapping:
                    val = variable_mapping[var]
                    if val is None:
                        return 'False'
                    if attr:
                        attr_name = attr
                        # Utiliser les attributs du token
                        if attr_name == 'text':
                            return f'"{val.text.lower()}"'
                        elif attr_name == 'text.lower':
                            return f'"{val.text.lower()}"'
                        elif attr_name == 'lemma_':
                            return f'"{val.lemma_.lower()}"'
                        elif attr_name == 'dep_':
                            return f'"{val.dep_}"'
                        elif attr_name == 'pos_':
                            return f'"{val.pos_.lower()}"'
                        elif attr_name == 'head.i':
                            if hasattr(val, 'head') and val.head and val.head.token_primarykey in self.token_to_word_id:
                                return f'"{self.token_to_word_id[val.head.token_primarykey]}"'
                            else:
                                return 'False'
                        elif attr_name == 'head.pos_':
                            if hasattr(val, 'head') and hasattr(val.head, 'pos_'):
                                return f'"{val.head.pos_.lower()}"'
                            else:
                                return 'False'
                        elif attr_name == 'i':
                            if val.token_primarykey in self.token_to_word_id:
                                return f'"{self.token_to_word_id[val.token_primarykey]}"'
                            else:
                                return 'False'
                        else:
                            logging.error(f"Attribut '{attr_name}' non pris en charge pour la variable '${var}'")
                            return 'False'
                    else:
                        return f'"{val.text.lower()}"'
                else:
                    logging.error(f"Variable '${var}' non trouvée dans le mapping")
                    return 'False'

            pattern = re.compile(r'\$(\w+)(?:\.([a-zA-Z_.]+))?')
            condition_evaluated = pattern.sub(replace_var, condition_evaluated)

            # Sécuriser l'évaluation
            return eval(condition_evaluated, {}, {})
        except Exception as e:
            logging.error(f"Erreur lors de l'évaluation de la condition '{conditions}': {e}")
            return False

    def executer_actions(self, actions, variable_mapping):
        """Exécute les actions en remplaçant les variables par les tokens correspondants."""
        for action in actions.split('&'):
            action = action.strip()
            if action.startswith('pour chaque'):
                self.executer_boucle(action, variable_mapping)
            else:
                self.executer_action_simple(action, variable_mapping)

    def executer_boucle(self, action, variable_mapping):
        """Exécute une boucle définie dans une action."""
        pattern = r'pour chaque\s+\$(\w+)\s+dans\s+(\w+)\(\s*\$(\w+)(?:\.text)?\s*\):\s*(.*)'
        match = re.match(pattern, action)
        if match:
            var_elem, fonction, var_source, action_interne = match.groups()
            source_token = variable_mapping.get(var_source)
            if not source_token:
                logging.error(f"Source token pour la variable '${var_source}' est manquant.")
                return

            # Obtenir le lemme du source_token
            if isinstance(source_token, str):
                source_lemma = source_token.lower()
            elif hasattr(source_token, 'lemma_') and source_token.lemma_:
                source_lemma = source_token.lemma_.lower()
            else:
                source_lemma = str(source_token).lower()

            try:
                # Récupérer les éléments via la fonction lexicale
                elements = getattr(self.ressources, fonction)(source_lemma)
            except AttributeError:
                logging.error(f"La fonction '{fonction}' n'existe pas dans RessourcesLexicales.")
                return

            # Filtrer les éléments pour ne garder que ceux présents dans le graphe (lemmes)
            elements_present = [elem for elem in elements if self.get_word_id_by_lemma(elem.lower())]
            if not elements_present:
                logging.warning(f"Aucun élément trouvé pour la fonction '{fonction}' avec le lemme '{source_lemma}'.")

            for elem in elements_present:
                elem_lemma = elem.lower()
                word_id = self.get_word_id_by_lemma(elem_lemma)
                if not word_id:
                    logging.warning(f"Nœud pour le lemme '{elem_lemma}' non trouvé dans le graphe.")
                    continue

                # Si des conditions supplémentaires sont nécessaires, les appliquer ici
                # Exemple : vérifier si $s.pos_ == $x.pos_
                # Récupérer le word_id de $x (supposé être une variable dans le mapping)
                x_word_id = variable_mapping.get('x')  # Assurez-vous que 'x' est une variable pertinente
                if x_word_id and self.graphe.existe_noeud(x_word_id):
                    x_pos = self.graphe.get_pos_of_word(x_word_id)
                    s_pos = self.graphe.get_pos_of_word(word_id)
                    if x_pos != s_pos:
                        continue  # Filtrer les synonymes qui ne partagent pas la même catégorie grammaticale

                # Map variable to word_id
                local_mapping = variable_mapping.copy()
                local_mapping[var_elem] = word_id
                self.executer_action_simple(action_interne, local_mapping)
        else:
            logging.error(f"Format de boucle non reconnu : {action}")

    def executer_action_simple(self, action, variable_mapping):
        """Exécute une action simple en remplaçant les variables par les valeurs correspondantes, avec gestion des relations inversées."""
        pattern = re.compile(r'\$(\w+)(?:\.([a-zA-Z_.]+))?')

        def replace_var(match):
            var = match.group(1)
            attr = match.group(2)
            if var in variable_mapping:
                val = variable_mapping[var]
                if val is None:
                    return 'None'
                if attr:
                    attr_name = attr
                    if hasattr(val, attr_name):
                        attr_value = getattr(val, attr_name)
                        if isinstance(attr_value, str):
                            return f'"{attr_value.lower()}"'
                        else:
                            return str(attr_value)
                    else:
                        return 'False'
                else:
                    # Remplacer par le word_id
                    if isinstance(val, str):
                        # Si val est déjà un word_id
                        return f'"{val}"'
                    elif hasattr(val, 'token_primarykey') and val.token_primarykey in self.token_to_word_id:
                        return f'"{self.token_to_word_id[val.token_primarykey]}"'
                    else:
                        logging.error(f"word_id pour le token '{val.text}' n'existe pas dans le graphe.")
                        return 'False'
            else:
                return 'False'

        try:
            # Remplacer les variables dans l'action par leur valeur
            action_evaluated = pattern.sub(replace_var, action)

            # Regex pour identifier la relation (avec ou sans -1)
            # Exemple: "word_1" r_carac "word_2" ou "word_1" r_carac-1 "word_2"
            match = re.match(r'"([^"]+)"\s+(r_\w+)(-1)?\s+"([^"]+)"', action_evaluated)
            if match:
                source_label, relation, inverse_flag, cible_label = match.groups()

                # Si la relation est inversée (-1), on inverse les labels source et cible
                if inverse_flag:
                    relation = relation[:-2]  # Enlever le '-1'
                    source_label, cible_label = cible_label, source_label

                # Vérifier que la relation commence par 'r_'
                if not relation.startswith('r_'):
                    logging.warning(f"Ignorant la relation '{relation}' car elle ne commence pas par 'r_'.")
                    return

                if 'None' in [source_label, cible_label]:
                    logging.warning("Relation invalide détectée, sources ou cibles sont None. Relation ignorée.")
                    return

                # Mettre les labels en minuscules
                source_label = source_label.lower()
                cible_label = cible_label.lower()

                try:
                    # Vérifier que les nœuds existent dans le graphe
                    if not self.graphe.existe_noeud(source_label):
                        logging.warning(f"Nœud source '{source_label}' n'existe pas dans le graphe.")
                        return
                    if not self.graphe.existe_noeud(cible_label):
                        logging.warning(f"Nœud cible '{cible_label}' n'existe pas dans le graphe.")
                        return

                    # Ajouter la relation dans le graphe
                    if not self.graphe.existe_relation(source_label, relation, cible_label):
                        self.graphe.ajouter_relation(source_label, relation, cible_label)
                        self.ajouter_relation_csv(source_label, relation, cible_label)

                    # Ajouter l'inverse si défini
                    inverse_relation = self.relations_inverses.get(relation)
                    if inverse_relation:
                        if not self.graphe.existe_relation(cible_label, inverse_relation, source_label):
                            self.graphe.ajouter_relation(cible_label, inverse_relation, source_label)
                            self.ajouter_relation_csv(cible_label, inverse_relation, source_label)
                except Exception as e:
                    logging.error(f"Erreur lors de l'ajout de la relation '{relation}' entre '{source_label}' et '{cible_label}': {e}")
            else:
                # Si la relation n'est pas sous la forme "source" r_relation "target", essayer la forme $x r_relation $y
                match = re.match(r'\$(\w+)\s+(r_\w+)\s+\$(\w+)', action_evaluated)
                if match:
                    source_var, relation, cible_var = match.groups()

                    # Obtenir les word_ids correspondants
                    source_word_id = variable_mapping.get(source_var)
                    cible_word_id = variable_mapping.get(cible_var)

                    if not source_word_id or not cible_word_id:
                        logging.warning(f"Relation ignorée car l'un des nœuds ('{source_var}' ou '{cible_var}') n'existe pas.")
                        return

                    # Ajouter la relation dans le graphe
                    if not self.graphe.existe_relation(source_word_id, relation, cible_word_id):
                        self.graphe.ajouter_relation(source_word_id, relation, cible_word_id)
                        self.ajouter_relation_csv(source_word_id, relation, cible_word_id)

                    # Ajouter l'inverse si défini
                    inverse_relation = self.relations_inverses.get(relation)
                    if inverse_relation:
                        if not self.graphe.existe_relation(cible_word_id, inverse_relation, source_word_id):
                            self.graphe.ajouter_relation(cible_word_id, inverse_relation, source_word_id)
                            self.ajouter_relation_csv(cible_word_id, inverse_relation, source_word_id)
                else:
                    logging.error(f"Action non reconnue ou mal formée : {action_evaluated}")
        except Exception as e:
            logging.error(f"Erreur lors de l'exécution de l'action '{action}': {e}")

    def ajouter_relation_csv(self, source, relation, cible):
        """Ajouter ou mettre à jour une relation dans le fichier CSV correspondant."""
        # Vérifier si source et cible sont identiques, si oui, ignorer la relation
        if source == cible:
            return  # Ne pas ajouter cette relation

        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, '..', 'data')
        data_dir = os.path.abspath(data_dir)
        csv_filename = f"{relation}.csv"
        csv_path = os.path.join(data_dir, csv_filename)

        try:
            # Lire le CSV et compter les occurrences
            relations = defaultdict(int)
            if os.path.exists(csv_path):
                with open(csv_path, 'r', encoding='utf-8', newline='') as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=';')
                    for row in reader:
                        key = (row['source'], row['target'])
                        relations[key] = int(row['recurrence'])

            # Mettre à jour ou ajouter la relation
            key = (source, cible)
            relations[key] += 1

            # Réécrire le CSV avec les relations mises à jour
            with open(csv_path, 'w', encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(['source', 'target', 'recurrence'])
                for (src, tgt), rec in relations.items():
                    writer.writerow([src, tgt, rec])
            logging.debug(f"Relation '{relation}' mise à jour dans '{csv_filename}': {source} -> {cible} ({relations[key]} fois)")
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout ou de la mise à jour de la relation '{relation}' dans '{csv_path}': {e}")

    def get_word_id_by_lemma(self, lemma):
        """Retourne le word_id correspondant au lemme donné."""
        for token_primarykey, word_id in self.token_to_word_id.items():
            if self.graphe.existe_noeud(word_id):
                node_data = self.graphe.G.nodes[word_id]
                if node_data['type'] == 'word' and node_data['valeur'].lower() == lemma:
                    return word_id
        return None

    def get_word_text_by_lemma(self, lemma):
        """Retourne le word_id correspondant au lemme donné."""
        return self.get_word_id_by_lemma(lemma.lower())

    def get_word_id_by_label(self, label):
        """Retourne le word_id correspondant au label donné."""
        label = label.lower()
        # Rechercher le word_id par le label
        for node, data in self.graphe.G.nodes(data=True):
            if data['type'] == 'word' and data['valeur'].lower() == label:
                return node
        return None

    def enregistrer_relations(self):
        """Cette méthode est désormais obsolète car les CSV sont remplis en temps réel."""
        pass
