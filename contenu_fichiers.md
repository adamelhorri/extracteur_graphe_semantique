# Contenu des fichiers

## gpt.py

```
import os
from pathlib import Path

# Définir les extensions de fichiers à lire
EXTENSIONS = {'.ts', '.css', '.html', '.py'}

def get_file_content(file_path):
    """Lit le contenu d'un fichier et le renvoie sous forme de chaîne."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_markdown_file(file_name, content):
    """Écrit le contenu dans un fichier Markdown."""
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)

def generate_markdown_for_directory(root_dir):
    """Génère un fichier Markdown avec le contenu de tous les fichiers spécifiés."""
    markdown_content = "# Contenu des fichiers\n\n"
    
    print(f"Démarrage de l'analyse du répertoire : {root_dir}")
    
    # Parcourir les répertoires et fichiers
    for root, dirs, files in os.walk(root_dir):
        print(f"Analyse du répertoire : {root}")
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix in EXTENSIONS:
                print(f"Lecture du fichier : {file_path}")
                # Ajouter le nom du fichier dans le Markdown
                markdown_content += f"## {file_path.relative_to(root_dir)}\n\n"
                # Ajouter le contenu du fichier dans le Markdown
                try:
                    file_content = get_file_content(file_path)
                    markdown_content += f"```\n{file_content}\n```\n\n"
                except Exception as e:
                    markdown_content += f"Erreur lors de la lecture du fichier {file_path}: {e}\n\n"
                    print(f"Erreur lors de la lecture du fichier {file_path}: {e}")

    return markdown_content

if __name__ == "__main__":
    root_directory = Path(__file__).parent  # Le répertoire contenant ce script
    print(f"Répertoire racine : {root_directory}")
    markdown_file_path = root_directory / 'contenu_fichiers.md'
    print(f"Fichier Markdown sera généré ici : {markdown_file_path}")
    markdown_content = generate_markdown_for_directory(root_directory)
    write_markdown_file(markdown_file_path, markdown_content)
    print("Le fichier Markdown a été généré avec succès.")

```

## main.py

```
import nltk
nltk.download('omw-1.4')
nltk.download('wordnet')

```

## src/ressources_lexicales.py

```
# src/ressources_lexicales.py

import nltk
from nltk.corpus import wordnet

# Assurez-vous d'avoir téléchargé WordNet et les données pour le français
# Exécutez cette commande une seule fois
# nltk.download('wordnet')
# nltk.download('omw-1.4')

class RessourcesLexicales:
    def __init__(self, texte):
        # Convertir le texte en une liste de mots pour le filtrage
        self.mots_du_texte = set(word.lower() for word in texte.split())

    def synonymes(self, mot):
        synonyms = set()
        for syn in wordnet.synsets(mot, lang='fra'):
            for lemma in syn.lemmas('fra'):
                synonym = lemma.name().replace('_', ' ')
                if synonym.lower() in self.mots_du_texte:
                    synonyms.add(synonym)
        # Ajouter des synonymes manuellement si nécessaire, mais uniquement s'ils sont dans le texte
        manual_synonyms = {

        }
        for syn in manual_synonyms.get(mot, []):
            if syn.lower() in self.mots_du_texte:
                synonyms.add(syn)
        return list(synonyms)

    def antonymes(self, mot):
        antonyms = set()
        for syn in wordnet.synsets(mot, lang='fra'):
            for lemma in syn.lemmas('fra'):
                if lemma.antonyms():
                    for ant in lemma.antonyms():
                        antonym = ant.name().replace('_', ' ')
                        if antonym.lower() in self.mots_du_texte:
                            antonyms.add(antonym)
        # Ajouter des antonymes manuellement si nécessaire, mais uniquement s'ils sont dans le texte
        manual_antonyms = {

        }
        for ant in manual_antonyms.get(mot, []):
            if ant.lower() in self.mots_du_texte:
                antonyms.add(ant)
        return list(antonyms)

    def hyperonymes(self, mot):
        hyperonyms = set()
        for syn in wordnet.synsets(mot, lang='fra'):
            for hyper in syn.hypernyms():
                for lemma in hyper.lemmas('fra'):
                    hyperonym = lemma.name().replace('_', ' ')
                    if hyperonym.lower() in self.mots_du_texte:
                        hyperonyms.add(hyperonym)
        # Ajouter des hyperonymes manuellement si nécessaire, mais uniquement s'ils sont dans le texte
        manual_hyperonyms = {

        }
        for hyper in manual_hyperonyms.get(mot, []):
            if hyper.lower() in self.mots_du_texte:
                hyperonyms.add(hyper)
                print(list(hyperonyms))
        return list(hyperonyms)

    def hyponymes(self, mot):
        hyponyms = set()
        for syn in wordnet.synsets(mot, lang='fra'):
            for hypo in syn.hyponyms():
                for lemma in hypo.lemmas('fra'):
                    hyponym = lemma.name().replace('_', ' ')
                    if hyponym.lower() in self.mots_du_texte:
                        hyponyms.add(hyponym)
        # Ajouter des hyponyms manuellement si nécessaire, mais uniquement s'ils sont dans le texte
        manual_hyponyms = {

        }
        for hypo in manual_hyponyms.get(mot, []):
            if hypo.lower() in self.mots_du_texte:
                hyponyms.add(hypo)
        return list(hyponyms)

```

## src/noeud.py

```
from abc import ABC, abstractmethod

class Noeud(ABC):
    def __init__(self, id: int, label: str):
        self.id = id
        self.label = label

    @abstractmethod
    def afficher(self):
        pass

```

## src/mot.py

```
from noeud import Noeud


class Mot(Noeud):
    def __init__(self, id: int, texte: str, lemme: str, partie_du_discours: str, sens: str = ""):
        super().__init__(id, texte)
        self.texte = texte
        self.lemme = lemme
        self.partie_du_discours = partie_du_discours
        self.sens = sens

    def afficher(self):
        return f"Mot: {self.texte}, Lemme: {self.lemme}, POS: {self.partie_du_discours}, Sens: {self.sens}"

    def __repr__(self):
        return self.afficher()

```

## src/graphe_semantique.py

```
import networkx as nx
import matplotlib.pyplot as plt

class GrapheSemantique:
    def __init__(self):
        # Dictionnaire pour stocker les nœuds et leurs attributs
        self.noeuds = {}  # clé: nom du nœud, valeur: POS
        # Liste pour stocker les relations sous forme de tuples (source, relation, cible)
        self.relations = []

    def ajouter_noeud(self, nom, pos):
        """Ajouter un nœud avec son POS au graphe."""
        if nom not in self.noeuds:
            self.noeuds[nom] = pos

    def existe_noeud(self, nom):
        """Vérifie si un nœud existe dans le graphe."""
        return nom in self.noeuds

    def ajouter_relation(self, source, relation, cible):
        """Ajouter une relation au graphe."""
        if not self.existe_relation(source, relation, cible):
            self.relations.append((source, relation, cible))

    def existe_relation(self, source, relation, cible):
        """Vérifie si une relation existe déjà dans le graphe."""
        return (source, relation, cible) in self.relations

    def get_toutes_relations(self):
        """Retourne toutes les relations du graphe."""
        return self.relations

    def visualiser_graphe(self):
        """Visualise le graphe avec les nœuds et les relations."""
        G = nx.DiGraph()

        # Ajouter les nœuds
        for noeud, pos in self.noeuds.items():
            G.add_node(noeud, label=pos)

        # Ajouter les relations (edges)
        for source, relation, cible in self.relations:
            G.add_edge(source, cible, label=relation)

        # Positionner les nœuds
        pos = nx.spring_layout(G)

        # Dessiner les nœuds et les relations
        nx.draw(G, pos, with_labels=True, node_color='lightblue', font_size=10, node_size=3000)

        # Ajouter les étiquettes de relation
        edge_labels = {(source, cible): relation for source, relation, cible in self.relations}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        # Afficher le graphe
        plt.show()

```

## src/type_relation.py

```
from enum import Enum

class TypeRelation(Enum):
    r_succ = "succession"
    r_associated = "association"
    r_raff_sem = "raffinement sémantique"
    r_pos = "partie du discours"
    r_syn = "synonyme"
    r_isa = "hyperonyme"
    r_anto = "antonyme"
    r_hypo = "hyponyme"
    r_agent = "agent"
    r_patient = "patient"
    r_lemma = "lemme"

```

## src/moteur_de_regles.py

```
# src/moteur_de_regles.py

import itertools
import re
import os
import csv
import logging
#logging.basicConfig(level=logging.CRITICAL)
from collections import defaultdict
from ressources_lexicales import RessourcesLexicales
from graphe_semantique import GrapheSemantique

# Import your custom NLP pipeline components
from SyntaxicExtraction import SyntaxicExtraction

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

        # Remove spaCy model loading
        self.nlp = None  # No need to load spaCy
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
        try:
            self.ressources = RessourcesLexicales(texte)
            # Use your custom SyntaxicExtraction pipeline
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
        for i in range(len(tokens)):
            mot = tokens[i]
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
            if i < len(tokens) - 1:
                mot_suivant = tokens[i + 1]
                mot_suivant_lemma = mot_suivant.lemma_.lower()
                mot_suivant_pos = mot_suivant.pos_.lower()
                try:
                    if not self.graphe.existe_relation(mot_lemma, "r_succ", mot_suivant_lemma):
                        self.graphe.ajouter_relation(mot_lemma, "r_succ", mot_suivant_lemma)
                        self.ajouter_relation_csv(mot_lemma, "r_succ", mot_suivant_lemma)
                except Exception as e:
                    logging.error(f"Erreur lors de l'ajout de la relation ('{mot_lemma}', 'r_succ', '{mot_suivant_lemma}'): {e}")

    def appliquer_regle(self, regle, tokens):
        """Appliquer une règle spécifique aux tokens."""
        try:
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
                tokens_var = [token for token in tokens if not token.pos_ == 'PUNCT']

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
                        if attr_name == 'text':
                            return f'"{val.text}"'
                        elif attr_name == 'text.lower':
                            return f'"{val.text.lower()}"'
                        elif attr_name == 'lemma_':
                            return f'"{val.lemma_.lower()}"'
                        elif attr_name == 'dep_':
                            return f'"{val.dep_}"'
                        elif attr_name == 'pos_':
                            return f'"{val.pos_.lower()}"'
                        elif attr_name == 'head.i':
                            if hasattr(val, 'head') and val.head:
                                return str(val.head.token_id)
                            else:
                                return 'False'
                        elif attr_name == 'head.pos_':
                            if hasattr(val, 'head') and hasattr(val.head, 'pos_'):
                                return f'"{val.head.pos_.lower()}"'
                            else:
                                return 'False'
                        elif attr_name == 'i':
                            return str(val.token_id)
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

```

## src/relation.py

```
from noeud import Noeud
from type_relation import TypeRelation


class Relation:
    def __init__(self, type_relation: TypeRelation, poids: float, noeud_source: Noeud, noeud_cible: Noeud, est_negatif: bool = False):
        self.type_relation = type_relation
        self.poids = poids
        self.noeud_source = noeud_source
        self.noeud_cible = noeud_cible
        self.est_negatif = est_negatif

    def ajuster_poids(self, nouveau_poids: float):
        self.poids = nouveau_poids

    def marquer_negatif(self):
        self.est_negatif = True

    def afficher(self):
        negatif_str = "négatif" if self.est_negatif else "positif"
        return f"Relation {self.type_relation.value} entre {self.noeud_source.label} et {self.noeud_cible.label}, Poids: {self.poids}, {negatif_str}"

    def __repr__(self):
        return self.afficher()

```

## src/desambiguiseur_lexical.py

```
import spacy

class DesambiguiseurLexical:
    def __init__(self):
        self.nlp = spacy.load("fr_core_news_md")

    def desambiguer(self, mot, contexte):
        # Désambiguïse le mot en fonction du contexte
        pass

```

## src/SyntaxicExtraction.py

```
from Tokenizer.DependencyExtractor import DependencyExtractor
from Tokenizer.Disambiguator import Disambiguator
from Tokenizer.GroupsExtractor import GroupExtractor
from Tokenizer.Lexicon import Lexicon
from Tokenizer.MorphologicalAnalyzer import MorphologicalAnalyzer
from Tokenizer.Tokenizer import Tokenizer


class SyntaxicExtraction:
    def __init__(self, text):
        # Initialize the components of the NLP pipeline
        self.tokenizer = Tokenizer()
        self.lexicon = Lexicon()
        self.morph_analyzer = MorphologicalAnalyzer()
        self.disambiguator = Disambiguator()
        self.dependency_extractor = DependencyExtractor()
        self.group_extractor = GroupExtractor()
        
        # Process the text through the pipeline
        tokens = self.tokenizer.tokenize(text)
        tokens = self.lexicon.extract_lemmas(tokens)
        tokens = self.lexicon.extract_pos(tokens)
        tokens = self.morph_analyzer.analyze(tokens, self.lexicon)
        tokens = self.disambiguator.disambiguate(tokens, self.morph_analyzer, self.lexicon)
        tokens = self.dependency_extractor.extract_dependencies(tokens)
        tokens = self.group_extractor.extract_groups(tokens)
        
        # Store the processed tokens
        self.tokens = tokens

```

## src/resolution_anaphore.py

```

```

## src/expression_composee.py

```
from noeud import Noeud

class ExpressionComposee(Noeud):
    def __init__(self, id: int, label: str):
        super().__init__(id, label)

    def afficher(self):
        return f"Expression composée: {self.label}"

    @classmethod
    def from_file(cls, file_path: str):
        expressions = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Supprimer les espaces et les retours à la ligne inutiles
                line = line.strip()
                # Diviser la ligne en deux parties séparées par le point-virgule
                if line:
                    parts = line.split(';"')
                    if len(parts) == 2:
                        try:
                            # Extraction de l'id et de l'expression
                            id_str, phrase = parts
                            id_ = int(id_str)
                            phrase = phrase.rstrip('";')  # Supprimer les guillemets et point-virgule de la fin
                            expressions.append(cls(id_, phrase))
                        except ValueError:
                            print(f"Erreur de conversion dans la ligne : {line}")
        return expressions

```

## src/moteur_inference.py

```
class MoteurInference:
    def inferer_relations(self, graphe):
        # Tente de déduire des relations implicites
        pass

```

## src/visualisateur_graphe.py

```
class VisualisateurGraphe:
    def exporter_en_BRAT(self, graphe, chemin_fichier):
        # Exporte le graphe dans un format lisible par BRAT
        pass

```

## src/evaluateur_performance.py

```
class EvaluateurPerformance:
    def mesurer_temps_execution(self):
        # Mesure le temps d'exécution du système
        pass

    def calculer_precision(self):
        # Calcule la précision du système
        pass

    def calculer_rappel(self):
        # Calcule le rappel du système
        pass

```

## src/__init__.py

```

```

## src/graphe_semantique_evo.py

```
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class GrapheSemantique:
    def __init__(self):
        # Dictionnaire pour stocker les nœuds et leurs attributs
        self.noeuds = {}  # clé: nom du nœud, valeur: POS
        # Liste pour stocker les relations sous forme de tuples (source, relation, cible)
        self.relations = []

    def ajouter_noeud(self, nom, pos):
        """Ajouter un nœud avec son POS au graphe."""
        if nom not in self.noeuds:
            self.noeuds[nom] = pos

    def existe_noeud(self, nom):
        """Vérifie si un nœud existe dans le graphe."""
        return nom in self.noeuds

    def ajouter_relation(self, source, relation, cible):
        """Ajouter une relation au graphe."""
        if not self.existe_relation(source, relation, cible):
            self.relations.append((source, relation, cible))

    def existe_relation(self, source, relation, cible):
        """Vérifie si une relation existe déjà dans le graphe."""
        return (source, relation, cible) in self.relations

    def get_toutes_relations(self):
        """Retourne toutes les relations du graphe."""
        return self.relations

    def visualiser_graphe(self):
        """Visualise le graphe avec les nœuds et les relations, en évitant la superposition des arêtes et des étiquettes."""
        G = nx.DiGraph()

        # Ensemble des nœuds reliés
        noeuds_relies = set()

        # Dictionnaire pour stocker les relations entre deux nœuds (pour éviter la superposition)
        relations_counter = {}

        # Ajouter les relations filtrées (sans 'pos' et 'lemm') et compter les relations entre chaque paire de nœuds
        edges_colors = []
        for source, relation, cible in self.relations:
            if "pos" not in relation and "lemm" not in relation:
                G.add_edge(source, cible, label=relation)
                noeuds_relies.add(source)
                noeuds_relies.add(cible)

                # Si la relation contient "succ", ajouter la couleur verte, sinon noire
                if "succ" in relation:
                    edges_colors.append('green')
                else:
                    edges_colors.append('black')

                # Compter combien de relations existent entre chaque paire de nœuds
                if (source, cible) not in relations_counter:
                    relations_counter[(source, cible)] = []
                relations_counter[(source, cible)].append(relation)

        # Ajouter uniquement les nœuds qui sont reliés
        for noeud in noeuds_relies:
            G.add_node(noeud, label=self.noeuds[noeud])

        # Positionner les nœuds
        pos = nx.spring_layout(G)

        # Dessiner les nœuds
        nx.draw(G, pos, with_labels=True, node_color='lightblue', font_size=10, node_size=3000)

        # Dessiner les relations avec courbure pour éviter la superposition
        curved_edges = []
        straight_edges = []
        for (source, cible), relations in relations_counter.items():
            if len(relations) > 1:  # Plusieurs relations entre les mêmes nœuds
                curved_edges.append((source, cible))
            else:
                straight_edges.append((source, cible))

        # Tracer les arêtes courbées et droites
        arc_rad = 0.3  # Rayon de courbure pour les arêtes
        nx.draw_networkx_edges(G, pos, edgelist=straight_edges, edge_color=edges_colors)
        nx.draw_networkx_edges(G, pos, edgelist=curved_edges, connectionstyle=f'arc3, rad = {arc_rad}', edge_color=edges_colors)

        # Ajouter les étiquettes des relations en ajustant leur position pour éviter la superposition
        for (source, cible), relations in relations_counter.items():
            for i, relation in enumerate(relations):
                # Calculer la position au milieu de l'arête
                x_mid = (pos[source][0] + pos[cible][0]) / 2
                y_mid = (pos[source][1] + pos[cible][1]) / 2

                # Décaler verticalement l'étiquette pour chaque relation supplémentaire
                y_offset = 0.05 * (i - (len(relations) - 1) / 2)  # Ajustement dynamique

                # Ajouter l'étiquette à la position ajustée
                plt.text(x_mid, y_mid + y_offset, relation, fontsize=10, color='black', ha='center')

        # Afficher le graphe
        plt.show()

        # Réinitialiser le graphe après fermeture de la fenêtre de visualisation
        self.noeuds.clear()  # Vider les nœuds
        self.relations.clear()  # Vider les relations

```

## src/traiter_csv.py

```
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

```

## src/text_splitter.py

```
import re

class TextSplitter:
    def __init__(self):
        pass
    
    def split_text_into_sentences(self, texte):
        """
        Divise un texte complet en phrases, tout en conservant les virgules à l'intérieur des phrases.
        
        :param texte: str, le texte à diviser
        :return: list, une liste de phrases
        """
        # Utiliser une expression régulière pour diviser en phrases par les ponctuations finales (., !, ?)
        phrase_endings = re.compile(r'(?<=[.!?])\s+')
        phrases = phrase_endings.split(texte.strip())
        
        # Retourner les phrases après suppression des espaces superflus
        return [phrase.strip() for phrase in phrases if phrase]

# Exemple d'utilisation
texte = """
Le chat dort sur le canapé, il est fatigué. Marie mange une pomme rouge, tout en regardant la télévision. 
Le pilote contrôle l'avion avec précision, et tout se passe bien !
"""

# Initialiser l'instance de TextSplitter
splitter = TextSplitter()

# Diviser le texte en phrases
phrases = splitter.split_text_into_sentences(texte)

# Afficher les phrases divisées
for i, phrase in enumerate(phrases, 1):
    print(f"Phrase {i}: {phrase}")

```

## src/regle.py

```
class Regle:
    def __init__(self, conditions, actions):
        self.conditions = conditions
        self.actions = actions

    def est_applicable(self, graphe):
        # Vérifie si la condition est remplie dans le graphe
        pass

    def appliquer(self, graphe):
        # Applique les actions si applicable
        pass

```

## src/cache.py

```
class Cache:
    def __init__(self):
        self.relations_cachees = {}

    def obtenir_relation(self, cle):
        return self.relations_cachees.get(cle)

    def ajouter_relation(self, cle, relation):
        self.relations_cachees[cle] = relation

```

## src/gestionnaire_de_texte.py

```
from expression_composee import ExpressionComposee


class GestionnaireDeTexte:
    def importer_texte(self, chemin_fichier):
        with open(chemin_fichier, "r", encoding="utf-8") as file:
            return file.read()

    def segmenter_texte(self, texte):
        # Segmente le texte en mots
        pass

    def identifier_expressions_composees(self, mots):
        # Identifie les expressions composées dans une liste de mots
        pass
    @staticmethod
    def importer_expressions_composees(file_path: str):
        return ExpressionComposee.from_file(file_path)
```

## src/Tokenizer/Disambiguator.py

```
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

            # Condition existante : Transformation du POS si deux tokens adjacents sont des NOUN et possèdent un candidat 'Adj'
            if prev_token and prev_token.pos_ == "NOUN" and token.pos_ == "NOUN":
                # Vérifier si l'un des deux tokens a un candidat POS qui commence par 'Adj'
                prev_has_adj = any(cand.startswith("Adj") for cand, _ in prev_token.pos_candidates)
                current_has_adj = any(cand.startswith("Adj") for cand, _ in token.pos_candidates)

                if prev_has_adj and current_has_adj:
                    adj_tokens = []

                    if prev_has_adj:
                        # Obtenir le score le plus élevé pour un candidat POS commençant par 'Adj' dans le token précédent
                        prev_adj_scores = [score for cand, score in prev_token.pos_candidates if cand.startswith("Adj")]
                        if prev_adj_scores:
                            prev_max_adj_score = max(prev_adj_scores)
                            adj_tokens.append((prev_token, prev_max_adj_score))

                    if current_has_adj:
                        # Obtenir le score le plus élevé pour un candidat POS commençant par 'Adj' dans le token actuel
                        current_adj_scores = [score for cand, score in token.pos_candidates if cand.startswith("Adj")]
                        if current_adj_scores:
                            current_max_adj_score = max(current_adj_scores)
                            adj_tokens.append((token, current_max_adj_score))

                    if adj_tokens:
                        # Sélectionner le token avec le score 'Adj' le plus élevé
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
        Select the best lemma candidate by ensuring POS matches, then preferring singular and gender-matched lemmas,
        and finally preferring masculine lemmas among those. If the token is a verb and one of the lemma candidates 
        contains 'Ver:Inf', that candidate is chosen.

        If the POS is 'VERB' or 'AUX' and the previous POS is 'DET', reclassify as 'NOUN'.

        If a rule is found in the loaded JSON file with an occurrence > 20, replace the best lemma with spaCy's lemma.

        Parameters:
            pos (str): The disambiguated POS tag.
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

        # Step 1: Special rule - Reclassify 'VERB' or 'AUX' to 'NOUN' if previous POS is 'DET'
        if pos in ['VERB', 'AUX'] and prev_pos == 'DET':
            logging.info(f"Reclassifying POS 'VERB' or 'AUX' to 'NOUN' because previous POS is 'DET'.")
            pos = 'NOUN'

        pos_matched_lemmas = []
        best_lemma = None

        # Step 2: Evaluate each lemma candidate for POS matching
        for lemma, score in lemma_candidates:
            temp_token = Token(lemma)
            temp_token.pos_candidates = token.pos_candidates
            temp_token.pos_ = self.disambiguate_pos(None, temp_token.pos_candidates)
            temp_token.pos_ = self.map_pos_to_spacy(temp_token.pos_)
            morphological_analyzer.analyze([temp_token], lexicon)

            if temp_token.pos_ == pos:
                pos_matched_lemmas.append((temp_token, lemma, score))

        # Step 3: If no POS-matched lemmas, return the first lemma
        if not pos_matched_lemmas:
            return lemma_candidates[0][0]

        # Step 4: Among POS-matched lemmas, prefer singular candidates
        singular_lemmas = [lemma_info for lemma_info in pos_matched_lemmas if lemma_info[0].morph.get('Number') == 'Sing']
        if singular_lemmas:
            pos_matched_lemmas = singular_lemmas
            logging.debug(f"Filtered lemmas to prefer singular: {[lemma[1] for lemma in pos_matched_lemmas]}")

        # Step 5: Among remaining lemmas, prefer masculine lemmas
        masculine_lemmas = [lemma_info for lemma_info in pos_matched_lemmas if lemma_info[0].morph.get('Gender') == 'Mas' and token.pos_ != 'NOUN']
        if masculine_lemmas:
            pos_matched_lemmas = masculine_lemmas
            logging.debug(f"Filtered lemmas to prefer masculine: {[lemma[1] for lemma in masculine_lemmas]}")

        # Step 6: Return the highest scoring lemma among the remaining filtered ones
        best_lemma = max(pos_matched_lemmas, key=lambda x: x[2])[1]
        logging.debug(f"Best lemma selected after preferences: {best_lemma}")

        # Step 7: Check if a rule from the JSON file applies (occurrences > 15)
        normalized_text = token.text.lower().strip()  # Ensure the text matches the format in the JSON
        key = f"{normalized_text}_{pos}"

        logging.debug(f"Key being used for JSON lookup: {key}")

        if key in self.lemma_replacement_rules:
            rule = self.lemma_replacement_rules[key]
            logging.debug(f"Rule found for key: {key} with occurrences {rule['occurrences']}")
            if rule["occurrences"] > 15:
                if best_lemma == rule["structure"]["system_lemma"]:
                    logging.info(f"Replacing '{best_lemma}' with spaCy lemma '{rule['structure']['spacy_lemma']}' due to occurrence threshold.")
                    best_lemma = rule['structure']['spacy_lemma']
                    return rule["structure"]["spacy_lemma"]
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

```

## src/Tokenizer/DependencyExtractor.py

```
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

```

## src/Tokenizer/Tokenizer.py

```
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

```

## src/Tokenizer/test.py

```

import logging

# Adjust the import path if necessary
# Import your modules
logging.basicConfig(level=logging.CRITICAL)

from SyntaxicExtraction import SyntaxicExtraction

# Now you can use the SyntaxicExtraction class
if __name__ == "__main__":
    text = "les chats mangent la souris"
    nlp = SyntaxicExtraction(text)
    tokens = nlp.tokens

    # Process the tokens as needed
    for token in tokens:
        print(token)
```

## src/Tokenizer/Token_.py

```
# src/Token.py

class Token:
    def __init__(self, text):
        self.text = text #texte de base
        self.lemma_candidates = [] #candidats de lemmes
        self.pos_candidates = [] #candidats de pos 
        self.pos_ = None # pos gagnant (peut etre X)
        self.lemma_ = None #lemme gagnant (peut etre token.text si aucun lemme trouvé)
        self.gender = None #genre du mot (peut etre none)
        self.number = None #nombre du mot (peut etre none)
        self.shape_ = None #format exemple Adam.shape_ = Xxxx
        self.is_alpha = None # si token est un alpha (boolean)
        self.is_stop = None # si c'est un stop word
        self.morph = {} # morphlogie du mot , diffère d'un pos à l'autre niveau format
        self.dep_ = None #TODO type de dependance syntaxique
        self.head = None #TODO mot dont le token depends 
        self.token_id = None #id du token se reinitialise à 0 au debut de chaque phrase
        self.token_pid= None #id de la phrase s'incremente à partir de chaque 
        self.token_primarykey=None#clé primaire unique de chaque token
        self.groupe=None

    # Méthodes pour définir les attributs
    def set_alpha(self, is_alpha):
        self.is_alpha = is_alpha

    def set_shape(self, shape):
        self.shape_ = shape

    def set_stop(self, is_stop):
        self.is_stop = is_stop

    def set_gender(self, gender):
        self.gender = gender

    def set_number(self, number):
        self.number = number

    def set_morphological_features(self, features):
        self.morph = features

    def set_dep_(self, dep):
        self.dep_ = dep

    def set_head(self, head):
        self.head = head
    def set_pid(self, pid):
        self.token_pid = pid

    def __repr__(self):
        # Afficher uniquement le texte de la tête pour éviter la récursion
        head_text = self.head.text if isinstance(self.head, Token) else self.head
        return f"\nTid:[{self.token_primarykey}]\n        [\n        text : '{self.text}',\n        pos_cand : {self.pos_candidates} \n        pos_ : '{self.pos_}' \n        lemmas_cand : {self.lemma_candidates} \n        lemma_ : '{self.lemma_}' \n        gender|number : '{self.gender}|{self.number}' \n        morphological features : '{self.morph}' \n        shape : '{self.shape_}' \n        dep_ : '{self.dep_}'\n        head : '{head_text}' \n        groups: '{self.groupe}'        ]"

```

## src/Tokenizer/Lexicon.py

```
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

```

## src/Tokenizer/GroupsExtractor.py

```
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

```

## src/Tokenizer/MorphologicalAnalyzer.py

```
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

```

## tests/test_mot.py

```
import sys
import os
import unittest

# Ajouter dynamiquement le chemin vers src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import de la classe Mot
from mot import Mot

class TestMot(unittest.TestCase):
    
    def test_creation_mot(self):
        mot = Mot(1, "chat", "chat", "nom")
        self.assertEqual(mot.texte, "chat")
        self.assertEqual(mot.lemme, "chat")
        self.assertEqual(mot.partie_du_discours, "nom")
        self.assertEqual(mot.sens, "")
    
    def test_afficher_mot(self):
        mot = Mot(1, "chat", "chat", "nom", "animal domestique")
        self.assertEqual(mot.afficher(), "Mot: chat, Lemme: chat, POS: nom, Sens: animal domestique")

if __name__ == '__main__':
    unittest.main()

```

## tests/test_analyseur_semantique.py

```
import sys
import os
import unittest

# Ajouter dynamiquement le chemin vers src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import de la classe Relation, Mot, et TypeRelation
from relation import Relation
from mot import Mot
from relation import TypeRelation

class TestRelation(unittest.TestCase):

    def test_creation_relation(self):
        mot1 = Mot(1, "chat", "chat", "nom")
        mot2 = Mot(2, "boit", "boire", "verbe")
        relation = Relation(TypeRelation.r_succ, 1.0, mot1, mot2)
        
        self.assertEqual(relation.type_relation, TypeRelation.r_succ)
        self.assertEqual(relation.poids, 1.0)
        self.assertEqual(relation.noeud_source, mot1)
        self.assertEqual(relation.noeud_cible, mot2)
        self.assertFalse(relation.est_negatif)

    def test_ajuster_poids_relation(self):
        mot1 = Mot(1, "chat", "chat", "nom")
        mot2 = Mot(2, "boit", "boire", "verbe")
        relation = Relation(TypeRelation.r_succ, 1.0, mot1, mot2)
        relation.ajuster_poids(2.5)
        
        self.assertEqual(relation.poids, 2.5)

    def test_marquer_negatif_relation(self):
        mot1 = Mot(1, "chat", "chat", "nom")
        mot2 = Mot(2, "boit", "boire", "verbe")
        relation = Relation(TypeRelation.r_succ, 1.0, mot1, mot2)
        relation.marquer_negatif()
        
        self.assertTrue(relation.est_negatif)

    def test_afficher_relation(self):
        mot1 = Mot(1, "chat", "chat", "nom")
        mot2 = Mot(2, "boit", "boire", "verbe")
        relation = Relation(TypeRelation.r_succ, 1.0, mot1, mot2)
        self.assertEqual(relation.afficher(), "Relation succession entre chat et boit, Poids: 1.0, positif")

if __name__ == '__main__':
    unittest.main()

```

## tests/test_graphe_semantique.py

```
import sys
import os
import unittest

# Ajouter dynamiquement le chemin vers src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Importer les classes nécessaires
from graphe_semantique import GrapheSemantique

class TestGrapheSemantique(unittest.TestCase):

    def setUp(self):
        """Initialiser un graphe pour chaque test."""
        self.graphe = GrapheSemantique()

    def test_extraction_relations_et_application_regles(self):
        """Test de l'extraction des relations d'un texte et application des règles."""
        # Exemple de phrase simple
        texte = "le chat mange la souris"
        self.graphe.extraire_relations_du_texte(texte)

        # Vérification des relations initiales (succession)
        self.assertEqual(len(self.graphe.graph.edges), 4)

        # Chemin du fichier de règles
        fichier_regles = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/relations.txt'))

        # Appliquer les règles
        self.graphe.appliquer_regles(fichier_regles)

        # Vérification que les nouvelles relations ont été ajoutées
        # Cela dépendra des règles dans relations.txt
        self.assertGreaterEqual(len(self.graphe.graph.edges), 4)

        # Afficher le graphe pour voir les relations ajoutées
        self.graphe.afficher_graphe()

if __name__ == '__main__':
    unittest.main()

```

## tests/test_relation.py

```
import sys
import os
import unittest

# Ajouter dynamiquement le chemin vers src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import de la classe Relation, Mot, et TypeRelation
from relation import Relation
from mot import Mot
from relation import TypeRelation

class TestRelation(unittest.TestCase):

    def test_creation_relation(self):
        mot1 = Mot(1, "chat", "chat", "nom")
        mot2 = Mot(2, "boit", "boire", "verbe")
        relation = Relation(TypeRelation.r_succ, 1.0, mot1, mot2)
        
        self.assertEqual(relation.type_relation, TypeRelation.r_succ)
        self.assertEqual(relation.poids, 1.0)
        self.assertEqual(relation.noeud_source, mot1)
        self.assertEqual(relation.noeud_cible, mot2)
        self.assertFalse(relation.est_negatif)

    def test_ajuster_poids_relation(self):
        mot1 = Mot(1, "chat", "chat", "nom")
        mot2 = Mot(2, "boit", "boire", "verbe")
        relation = Relation(TypeRelation.r_succ, 1.0, mot1, mot2)
        relation.ajuster_poids(2.5)
        
        self.assertEqual(relation.poids, 2.5)

    def test_marquer_negatif_relation(self):
        mot1 = Mot(1, "chat", "chat", "nom")
        mot2 = Mot(2, "boit", "boire", "verbe")
        relation = Relation(TypeRelation.r_succ, 1.0, mot1, mot2)
        relation.marquer_negatif()
        
        self.assertTrue(relation.est_negatif)

    def test_afficher_relation(self):
        mot1 = Mot(1, "chat", "chat", "nom")
        mot2 = Mot(2, "boit", "boire", "verbe")
        relation = Relation(TypeRelation.r_succ, 1.0, mot1, mot2)
        self.assertEqual(relation.afficher(), "Relation succession entre chat et boit, Poids: 1.0, positif")

if __name__ == '__main__':
    unittest.main()

```

## tests/test_expression_composee.py

```
import sys
import os
import unittest

# Ajouter dynamiquement le chemin vers src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import de la classe ExpressionComposee
from expression_composee import ExpressionComposee

class TestExpressionComposee(unittest.TestCase):

    def test_creation_expression_composee(self):
        expr = ExpressionComposee(1, "avant toute chose")
        self.assertEqual(expr.label, "avant toute chose")

    def test_afficher_expression_composee(self):
        expr = ExpressionComposee(1, "avant toute chose")
        self.assertEqual(expr.afficher(), "Expression composée: avant toute chose")

    def test_extraction_fichier(self):
        # Chemin du fichier motsComposes.txt dans le dossier data
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/motsComposes.txt'))
        
        expressions = ExpressionComposee.from_file(file_path)
        
        # Vérifier qu'il y a au moins 1 million d'expressions
        self.assertGreater(len(expressions), 1000000)  # Adaptez ce nombre en fonction de la taille réelle du fichier
        
        # Vérifier certaines expressions spécifiques
        self.assertEqual(expressions[0].id, 9)
        self.assertEqual(expressions[0].label, "avant toute chose")
        self.assertEqual(expressions[10].label, "Moshe Ben Maimon")

if __name__ == '__main__':
    unittest.main()

```

## tests/test_extraction_relation.py

```
import sys
import os
import unittest

# Ajouter dynamiquement le chemin vers src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Importer les classes nécessaires
from graphe_semantique import GrapheSemantique
from mot import Mot
from relation import TypeRelation

class TestExtractionRelations(unittest.TestCase):

    def setUp(self):
        """Initialiser un graphe pour chaque test."""
        self.graphe = GrapheSemantique()

    def test_extraction_relations_simple(self):
        """Test de l'extraction automatique des relations dans une phrase simple."""
        texte = "le chat boit du lait"
        self.graphe.extraire_relations_du_texte(texte)

        # Vérifier que les 5 nœuds (mots) sont bien ajoutés
        self.assertEqual(len(self.graphe.graph.nodes), 5)

        # Vérifier que 4 relations (r_succ) sont bien créées
        self.assertEqual(len(self.graphe.graph.edges), 4)

        # Vérifier une relation particulière entre "chat" et "boit"
        rel = self.graphe.trouver_relation(1, 2)
        self.assertIsNotNone(rel)
        self.assertEqual(rel['type'], TypeRelation.r_succ)
        self.assertEqual(rel['poids'], 1.0)

        # Afficher le graphe visuellement
        self.graphe.afficher_graphe()

    def test_extraction_relations_complexe(self):
        """Test de l'extraction des relations dans une phrase plus complexe."""
        texte = "le chat noir boit du lait frais"
        self.graphe.extraire_relations_du_texte(texte)

        # Vérifier que 7 nœuds sont ajoutés
        self.assertEqual(len(self.graphe.graph.nodes), 7)

        # Vérifier que 6 relations de succession sont ajoutées
        self.assertEqual(len(self.graphe.graph.edges), 6)

        # Vérifier la relation entre "boit" et "du"
        rel = self.graphe.trouver_relation(3, 4)
        self.assertIsNotNone(rel)
        self.assertEqual(rel['type'], TypeRelation.r_succ)
        self.assertEqual(rel['poids'], 1.0)

        # Afficher le graphe visuellement
        self.graphe.afficher_graphe()

if __name__ == '__main__':
    unittest.main()

```

## tests/test_moteur_semantique.py

```
import logging
import unittest
import os
import sys
import csv
import re

# Ajouter le chemin du répertoire 'src' pour importer les modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from moteur_de_regles import MoteurDeRegles
from graphe_semantique_evo import GrapheSemantique
# Remove import of TextSplitter if not needed
# from text_splitter import TextSplitter

# Import your custom SyntaxicExtraction class
from SyntaxicExtraction import SyntaxicExtraction
#logging.basicConfig(level=logging.CRITICAL)

class TestMoteurDeRegles(unittest.TestCase):
    def setUp(self):
        # Initialiser le graphe sémantique et le moteur de règles
        self.graphe = GrapheSemantique()
        self.moteur_regles = MoteurDeRegles(self.graphe)
        
        # Définir le chemin complet vers 'relations.txt' dans le répertoire 'data'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.abspath(os.path.join(current_dir, '../data'))
        relations_path = os.path.join(data_dir, 'relations.txt')
        
        # Charger les règles depuis le chemin complet
        self.moteur_regles.charger_regles(relations_path)
        
        # Réinitialiser les fichiers CSV avant chaque test
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        for csv_file in csv_files:
            csv_path = os.path.join(data_dir, csv_file)
            with open(csv_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(['source', 'target', 'recurrence'])

    def verifier_csv(self, expected_relations):
        """
        Vérifie que les relations spécifiées existent avec les récurrences attendues.
        expected_relations : list of tuples
            Chaque tuple contient (relation_type, source, target, recurrence)
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.abspath(os.path.join(current_dir, '../data'))
        
        # Collecter toutes les relations existantes dans les CSV
        existing_relations = set()
        for csv_file in os.listdir(data_dir):
            if csv_file.endswith('.csv'):
                csv_path = os.path.join(data_dir, csv_file)
                relation_type = os.path.splitext(csv_file)[0]
                with open(csv_path, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=';')
                    for row in reader:
                        existing_relations.add((relation_type, row['source'], row['target'], int(row['recurrence'])))
        
        # Vérifier que chaque relation attendue est présente
        for relation in expected_relations:
            self.assertIn(relation, existing_relations,
                          f"La relation '{relation[1]} {relation[0]} {relation[2]}' avec 'recurrence'={relation[3]} n'a pas été trouvée.")

    def afficher_structure(self, phrase):
        """
        Affiche la structure des dépendances syntaxiques extraites par SyntaxicExtraction pour la phrase.
        """
        print(f"Structure syntaxique pour la phrase : '{phrase}'")
        syntaxic_extraction = SyntaxicExtraction(phrase)
        tokens = syntaxic_extraction.tokens
        for token in tokens:
            print(f"Token: {token.text}, Dépendance: {token.dep_}, Tête: {token.head.text}, POS: {token.pos_}")

    def tester_relation(self, relation_name, phrases, expected_relations):
        """
        Méthode générique pour tester une relation donnée.
        relation_name: le nom de la relation à tester (ex: 'r_associated')
        phrases: une liste de phrases à tester
        expected_relations: une liste de relations attendues sous forme de tuples (relation, source, target, recurrence)
        """
        for phrase in phrases:
            print(f"Phrase en cours: {phrase}")
            self.afficher_structure(phrase)
            self.moteur_regles.appliquer_regles(phrase)
            # Optionally visualize the graph if needed
            self.graphe.visualiser_graphe()
        
        # Vérifier les relations dans les CSVs
        self.verifier_csv(expected_relations)

    def test_r_associated(self):
        phrases = [
            "La voiture rouge est rapide.",
            "Un homme intelligent et courageux a résolu le problème.",
            "Le chat noir et le chien blanc sont amis.",
            "La grande maison est magnifique.",
            "Les livres intéressants sont sur la table.",
            "Pierre est un homme sage et réfléchi.",
            "Marie et son amie sont très différentes."
        ]
        expected_relations = [
            ('r_associated', 'voiture', 'rouge', 1),
            ('r_associated', 'homme', 'intelligent', 1),
            ('r_associated', 'chat', 'noir', 1),
            ('r_associated', 'maison', 'grande', 1),
            ('r_associated', 'livres', 'intéressants', 1),
            ('r_associated', 'homme', 'sage', 1),
            ('r_associated', 'marie', 'amie', 1)
        ]
        self.tester_relation('r_associated', phrases, expected_relations)

    # Continue adapting other test methods as needed
    # For example:

    def test_r_raff_sem(self):
        phrases = [
            "Le chat est un animal domestique.",
            "La pomme est un fruit.",
            "Un ordinateur puissant est nécessaire.",
            "L'avion est un moyen de transport rapide.",
            "Le lion est un animal dangereux.",
            "Les logiciels sont des outils indispensables.",
            "Le professeur est un expert en biologie."
        ]
        expected_relations = [
            ('r_raff_sem', 'animal', 'domestique', 1),
            ('r_raff_sem', 'pomme', 'fruit', 1),
            ('r_raff_sem', 'ordinateur', 'puissant', 1),
            ('r_raff_sem', 'avion', 'moyen', 1),
            ('r_raff_sem', 'lion', 'dangereux', 1),
            ('r_raff_sem', 'logiciels', 'indispensables', 1),
            ('r_raff_sem', 'professeur', 'expert', 1)
        ]
        self.tester_relation('r_raff_sem', phrases, expected_relations)

    def test_r_isa(self):
        phrases = [
            "Paul, un biologiste, adore les animaux.",
            "Marie est une enseignante.",
            "Jean, un expert, a résolu le problème.",
            "Le chien, un animal domestique, est fidèle.",
            "La Terre est une planète.",
            "La pomme, un fruit, est rouge.",
            "L'avion, un moyen de transport, est rapide."
        ]
        expected_relations = [
            ('r_isa', 'paul', 'biologiste', 1),
            ('r_isa', 'marie', 'enseignante', 1),
            ('r_isa', 'jean', 'expert', 1),
            ('r_isa', 'chien', 'animal', 1),
            ('r_isa', 'terre', 'planète', 1),
            ('r_isa', 'pomme', 'fruit', 1),
            ('r_isa', 'avion', 'moyen', 1)
        ]
        self.tester_relation('r_isa', phrases, expected_relations)

if __name__ == '__main__':
    # Exécuter tous les tests
    unittest.main()
    # Pour exécuter un test spécifique:
    # python3 -m unittest test_moteur_semantique.TestMoteurDeRegles.test_r_isa

```

## tests/test_manuel.py

```
# test_manuel.py

from graphe_semantique import GrapheSemantique
from moteur_de_regles import MoteurDeRegles

if __name__ == "__main__":
    graphe = GrapheSemantique()
    moteur = MoteurDeRegles(graphe)
    moteur.charger_regles('relations.txt')  # Assurez-vous que le chemin est correct
    moteur.appliquer_regles("Le chat mange la souris.")

    # Vérifier manuellement les relations
    assert graphe.existe_relation("chat", "mange", "r_agent"), "Relation r_agent non trouvée."
    assert graphe.existe_relation("souris", "mange", "r_patient"), "Relation r_patient non trouvée."
    print("Toutes les assertions sont passées.")

```

## tests/__init__.py

```

```

