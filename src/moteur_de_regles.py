# src/moteur_de_regles.py

import itertools
import re
import spacy
import os
import csv
import logging
from collections import defaultdict
from ressources_lexicales import RessourcesLexicales
from graphe_semantique import GrapheSemantique

# Configuration du logging pour n'afficher que les avertissements et les erreurs
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

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
            'r_family','r_lieu'
        ]
        # Ajout de la correspondance entre les relations et leurs inverses
        self.relations_inverses = {
            'r_agent': 'r_agent-1',
            'r_patient': 'r_patient-1',
            'r_instr': 'r_instr-1',
            'r_domain': 'r_domain-1',
            'r_lieu': 'r_lieu-1',
            # Ajoutez ici toutes les autres relations et leurs inverses si nécessaire
        }


        try:
            self.nlp = spacy.load('fr_core_news_md')
            logging.warning("Modèle spaCy chargé avec succès.")
        except Exception as e:
            logging.error(f"Impossible de charger le modèle spaCy: {e}")
            self.nlp = None
        self.initialiser_csv()

    def initialiser_csv(self):
        """Créer les fichiers CSV pour chaque type de relation avec les en-têtes si ils n'existent pas."""
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
        if not self.nlp:
            logging.error("Le modèle spaCy n'est pas chargé.")
            return
        try:
            self.ressources = RessourcesLexicales(texte)
            doc = self.nlp(texte)
            self.appliquer_relations(doc)
            for regle in self.regles:
                self.appliquer_regle(regle, doc)
            # Les relations sont déjà enregistrées au fur et à mesure
        except Exception as e:
            logging.error(f"Erreur lors de l'application des règles: {e}")

    def appliquer_relations(self, doc):
        """Appliquer les relations prédéfinies entre les tokens."""
        for i in range(len(doc)):
            mot = doc[i]
            mot_lemma = mot.lemma_.lower()
            mot_pos = mot.pos_.lower()
            try:
                # Ajouter la relation r_lemma
                self.graphe.ajouter_relation(mot.text, "r_lemma", mot_lemma)
                self.ajouter_relation_csv(mot.text, "r_lemma", mot_lemma)

                # Ajouter le noeud dans le graphe
                self.graphe.ajouter_noeud(mot_lemma, mot_pos)
            except Exception as e:
                logging.error(f"Erreur lors de l'ajout du lemme '{mot_lemma}' avec POS '{mot_pos}': {e}")

            # Gérer la relation r_succ
            if i < len(doc) - 1:
                mot_suivant = doc[i + 1]
                mot_suivant_lemma = mot_suivant.lemma_.lower()
                mot_suivant_pos = mot_suivant.pos_.lower()
                try:
                    if not self.graphe.existe_relation(mot_lemma, "r_succ", mot_suivant_lemma):
                        self.graphe.ajouter_relation(mot_lemma, "r_succ", mot_suivant_lemma)
                        self.ajouter_relation_csv(mot_lemma, "r_succ", mot_suivant_lemma)
                except Exception as e:
                    logging.error(f"Erreur lors de l'ajout de la relation ('{mot_lemma}', 'r_succ', '{mot_suivant_lemma}'): {e}")

    def appliquer_regle(self, regle, doc):
        """Appliquer une règle spécifique au document."""
        try:
            conditions, actions = regle.split("⇒")
            conditions = conditions.strip()
            actions = actions.strip()
            variables = self.extraire_variables(conditions + ' ' + actions)
            combinations, variable_names = self.generer_combinations(variables, doc)

            if not combinations:
                logging.warning(f"Règle ignorée '{regle}' en raison de variables manquantes.")
                return

            for tokens in combinations:
                variable_mapping = dict(zip(variable_names, tokens))
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

    def generer_combinations(self, variable_names, doc):
        """Génère toutes les combinaisons possibles de tokens pour les variables."""
        variable_tokens = {}
        for var in variable_names:
            if var == 'cc':
                tokens = [token for token in doc if token.dep_ == 'cc']
            elif var == 'cop':
                tokens = [token for token in doc if token.dep_ == 'cop']
            else:
                tokens = [token for token in doc if not token.is_punct]

            if tokens:
                variable_tokens[var] = tokens
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
                        if attr_name == 'text':
                            return f'"{val.text}"'  # Utilisation de guillemets doubles
                        elif attr_name == 'text.lower':
                            return f'"{val.text.lower()}"'
                        elif attr_name == 'dep_':
                            return f'"{val.dep_}"'
                        elif attr_name == 'pos_':
                            return f'"{val.pos_.lower()}"'  # Convertir POS en minuscules
                        elif attr_name == 'head.i':
                            if hasattr(val, 'head') and val.head:  # Vérification que le head existe
                                return str(val.head.i)
                            else:
                                return 'False'
                        elif attr_name == 'head.pos_':
                            if hasattr(val, 'head') and hasattr(val.head, 'pos_'):  # Vérification que le head et pos_ existent
                                return f'"{val.head.pos_.lower()}"'
                            else:
                                return 'False'
                        elif attr_name == 'i':
                            return str(val.i)
                        else:
                            logging.error(f"Attribut '{attr_name}' non pris en charge pour la variable '${var}'")
                            return 'False'
                    else:
                        return f'"{val.text}"'
                else:
                    logging.error(f"Variable '${var}' non trouvée dans le mapping")
                    return 'False'

            pattern = re.compile(r'\$(\w+)(?:\.([a-zA-Z_.]+))?')
            condition_evaluated = pattern.sub(replace_var, condition_evaluated)

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
            source_token = variable_mapping[var_source]
            if isinstance(source_token, str):
                source_lemma = source_token.lower()
            elif hasattr(source_token, 'lemma_'):
                source_lemma = source_token.lemma_.lower()
            else:
                source_lemma = str(source_token).lower()
            try:
                elements = getattr(self.ressources, fonction)(source_lemma)
            except AttributeError:
                logging.error(f"La fonction '{fonction}' n'existe pas dans RessourcesLexicales.")
                return
            # Filtrer les éléments pour ne garder que ceux présents dans le document (lemmes)
            elements_present = [elem for elem in elements if self.graphe.existe_noeud(elem.lower())]
            if not elements_present:
               # logging.warning(f"Aucun élément trouvé dans le document pour la fonction '{fonction}' avec '{source_lemma}'.")
               pass
            for elem in elements_present:
                elem_lemma = elem.lower()
                try:
                    if not self.graphe.existe_noeud(elem_lemma):
                        self.graphe.ajouter_noeud(elem_lemma, pos='noun')  # POS par défaut
                except Exception as e:
                    logging.error(f"Erreur lors de l'ajout du noeud '{elem_lemma}': {e}")
                local_mapping = variable_mapping.copy()
                local_mapping[var_elem] = elem_lemma  # elem is a string (lemma)
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
                            return f'"{attr_value}"'
                        else:
                            return str(attr_value)
                    else:
                        return 'False'
                else:
                    return f'"{val.text.lower()}"' if hasattr(val, 'text') else f'"{str(val).lower()}"'
            else:
                return 'False'

        try:
            # On remplace les variables dans l'action par leur valeur
            action_evaluated = pattern.sub(replace_var, action)

            # Regex pour identifier la relation (avec ou sans -1)
            match = re.match(r'"([^"]+)"\s+(r_\w+)(-1)?\s+"([^"]+)"', action_evaluated)
            if match:
                source_label, relation, inverse_flag, cible_label = match.groups()

                # Si la relation est inversée (-1), on inverse les labels source et cible
                if inverse_flag:
                    source_label, cible_label = cible_label, source_label

                # Vérifier que la relation commence par 'r_'
                if not relation.startswith('r_'):
                    logging.warning(f"Ignoring relation '{relation}' as it does not start with 'r_'")
                    return

                if 'None' in [source_label, cible_label]:
                    logging.warning("Relation invalide détectée, sources ou cibles sont None. Relation ignorée.")
                    return

                # Mettre les labels en minuscules
                source_label = source_label.lower()
                cible_label = cible_label.lower()

                try:
                    # Si les noeuds n'existent pas dans le graphe, on les ajoute
                    if not self.graphe.existe_noeud(source_label):
                        self.graphe.ajouter_noeud(source_label, pos='noun')
                    if not self.graphe.existe_noeud(cible_label):
                        self.graphe.ajouter_noeud(cible_label, pos='noun')

                    # Ajouter la relation dans le graphe
                    if not self.graphe.existe_relation(source_label, relation, cible_label):
                        self.graphe.ajouter_relation(source_label, relation, cible_label)

                    # Ajouter ou mettre à jour la relation dans le CSV
                    self.ajouter_relation_csv(source_label, relation, cible_label)

                    # Si la relation n'était pas inversée (pas de -1), on ajoute l'inverse automatiquement
                    if not inverse_flag:
                        inverse_relation = f"{relation}-1"
                        if not self.graphe.existe_relation(cible_label, inverse_relation, source_label):
                            self.graphe.ajouter_relation(cible_label, inverse_relation, source_label)
                        self.ajouter_relation_csv(cible_label, inverse_relation, source_label)
                except Exception as e:
                    logging.error(f"Erreur lors de l'ajout du noeud ou de la relation: {e}")
            else:
                logging.error(f"Action non reconnue après substitution : {action_evaluated}")
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
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout ou de la mise à jour de la relation '{relation}' dans '{csv_path}': {e}")

    def enregistrer_relations(self):
        """Cette méthode est désormais obsolète car les CSV sont remplis en temps réel."""
        pass
