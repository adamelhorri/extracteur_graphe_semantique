# Contenu des fichiers

## gpt.py

```
import os
from pathlib import Path

# Définir les extensions de fichiers à lire
EXTENSIONS = {'.ts', '.css', '.html', '.py', '.json'}

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

## src\cache.py

```
class Cache:
    def __init__(self):
        self.relations_cachees = {}

    def obtenir_relation(self, cle):
        return self.relations_cachees.get(cle)

    def ajouter_relation(self, cle, relation):
        self.relations_cachees[cle] = relation

```

## src\desambiguiseur_lexical.py

```
import spacy

class DesambiguiseurLexical:
    def __init__(self):
        self.nlp = spacy.load("fr_core_news_md")

    def desambiguer(self, mot, contexte):
        # Désambiguïse le mot en fonction du contexte
        pass

```

## src\evaluateur_performance.py

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

## src\expression_composee.py

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

## src\gestionnaire_de_texte.py

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

## src\graphe_semantique.py

```
# graphe_semantique.py

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

```

## src\mot.py

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

## src\moteur_de_regles.py

```
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
                logging.warning(f"Aucun élément trouvé dans le document pour la fonction '{fonction}' avec '{source_lemma}'.")
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
                        logging.error(f"Attribut '{attr_name}' non trouvé pour la variable '${var}'")
                        return 'False'
                else:
                    return f'"{val.text.lower()}"' if hasattr(val, 'text') else f'"{str(val).lower()}"'
            else:
                logging.error(f"Variable '${var}' non trouvée dans le mapping")
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

                    # Ajouter ou mettre à jour la relation dans le CSV
                    self.ajouter_relation_csv(source_label, relation, cible_label)

                    # Si la relation n'était pas inversée (pas de -1), on ajoute l'inverse automatiquement
                    if not inverse_flag:
                        inverse_relation = f"{relation}-1"
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

## src\moteur_inference.py

```
class MoteurInference:
    def inferer_relations(self, graphe):
        # Tente de déduire des relations implicites
        pass

```

## src\noeud.py

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

## src\regle.py

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

## src\relation.py

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

## src\resolution_anaphore.py

```

```

## src\ressources_lexicales.py

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
            'chat': ['félin'],
            'animal': [],
            'jour': [],
            'nuit': [],
            'pain': [],
            'fromage': [],
            'souris': [],
            'chien': [],
            'mange': [],
            'succède': [],
            'dort': [],
            'endormi': [],
            'est': [],
            'sont': [],
            'délicieux': [],
            'lumineux': [],
            'sombre': []
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
            'jour': ['nuit'],
            'nuit': ['jour'],
            'animal': [],
            'chat': [],
            'chien': [],
            'pain': [],
            'fromage': [],
            'souris': [],
            'mange': [],
            'succède': [],
            'dort': [],
            'endormi': [],
            'est': [],
            'sont': [],
            'délicieux': [],
            'lumineux': [],
            'sombre': []
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
            'chat': ['animal'],
            'chien': ['animal'],
            'souris': ['animal'],
            'pain': [],
            'fromage': [],
            'jour': [],
            'nuit': []
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
            'animal': ['chat', 'chien', 'souris'],
            'jour': [],
            'nuit': [],
            'pain': [],
            'fromage': [],
            'mange': [],
            'succède': [],
            'dort': [],
            'endormi': [],
            'est': [],
            'sont': [],
            'délicieux': [],
            'lumineux': [],
            'sombre': []
        }
        for hypo in manual_hyponyms.get(mot, []):
            if hypo.lower() in self.mots_du_texte:
                hyponyms.add(hypo)
        return list(hyponyms)

```

## src\text_splitter.py

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

## src\traiter_csv.py

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

## src\type_relation.py

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

## src\visualisateur_graphe.py

```
class VisualisateurGraphe:
    def exporter_en_BRAT(self, graphe, chemin_fichier):
        # Exporte le graphe dans un format lisible par BRAT
        pass

```

## src\__init__.py

```

```


