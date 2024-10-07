
# Analyseur Sémantique - Extraction de Relations Sémantiques
## avant tout
Il faut telecharger et inserer le dossier data dans le même repo que src 
https://drive.google.com/file/d/1hQV05fKsB3PN8jqewcAcSz7sl3gaWnEr/view?usp=drive_link
## Description

Ce projet consiste à développer un analyseur sémantique capable d'extraire des relations sémantiques à partir de textes en langue française. Le système est structuré en Python, avec une approche orientée objet, et utilise des fichiers textuels pour extraire des informations, notamment des expressions composées. Ces données sont ensuite organisées sous forme de graphes sémantiques où chaque nœud représente une entité et chaque relation capture une association sémantique spécifique.

## Objectifs

- **Extraction de relations sémantiques** à partir de textes.
- **Modélisation des mots et expressions composées** sous forme de graphes sémantiques.
- **Utilisation de fichiers textuels volumineux** pour extraire des expressions composées, avec gestion efficace de la mémoire.

## Structure du projet

Le projet est organisé avec une architecture modulaire dans un environnement Python, et inclut des tests unitaires pour assurer la robustesse du système.

### Arborescence du projet

```
analyseur_semantique/
├── src/
│   ├── __init__.py
|   ├──Tokenizer
|   |  └── TOkenizer(creation de token syntaxique)
│   ├── noeud.py
│   ├── mot.py
│   ├── expression_composee.py
│   ├── relation.py
│   ├── graphe_semantique.py
│   └── ...
├── tests/
│   ├── __init__.py
│   ├── test_mot.py
│   ├── test_expression_composee.py
│   └── ...
├── data/
│   └── motsComposes.txt   # Fichier texte volumineux contenant les expressions composées
├── README.md              # Ce fichier
└── requirements.txt
```

## Fonctionnalités principales

### 1. Gestion des Mots et des Expressions Composées

- **Mot (`mot.py`)** : Représente un mot avec ses attributs (`texte`, `lemme`, `partie du discours`, etc.).
- **Expression Composée (`expression_composee.py`)** : Représente une expression composée, qui est un groupe de mots. Les expressions peuvent être extraites d'un fichier texte.

### 2. Lecture des Fichiers Volumineux

Le fichier `motsComposes.txt` contient des expressions composées dans une structure formatée (`id;"expression";`). Nous avons implémenté une méthode robuste dans la classe `ExpressionComposee` pour lire et extraire ces données à partir d'un fichier texte volumineux (50 Mo) contenant des millions de lignes.

### 3. Tests Unitaires

Les tests ont été mis en place avec la bibliothèque `unittest` pour s'assurer du bon fonctionnement des différentes classes.

- **Tests pour la classe `Mot`** : Vérification de la création et de l'affichage des mots.
- **Tests pour la classe `ExpressionComposee`** : Vérification de la création d'expressions composées à partir de chaînes de caractères et extraction depuis un fichier volumineux.

### 4. Optimisation pour les fichiers volumineux

Le fichier `motsComposes.txt` étant volumineux, nous avons pris soin d'optimiser la méthode de lecture pour qu'elle puisse traiter un grand nombre de lignes sans surcharge mémoire. Nous avons également adapté les tests pour vérifier un sous-ensemble d'expressions spécifiques.

## Installation

### Prérequis

- Python 3.8 ou supérieur
- Installer les dépendances :

```bash
pip install -r requirements.txt
```

### Structure du fichier `motsComposes.txt`

Le fichier `motsComposes.txt` contient des expressions composées sous le format suivant :

```
9;"avant toute chose";
15;"sir Sacheverell Sitwell";
16;"Maria Callas";
21;"Marcel Gotlieb Gotlib";
23;"art et architecture catalans";
...
```

Chaque ligne est composée d'un identifiant (`id`) suivi d'une expression composée entre guillemets et se terminant par un point-virgule.

### Exécution des tests

Pour exécuter les tests, assurez-vous que vous êtes dans le répertoire racine du projet, puis utilisez la commande suivante pour exécuter tous les tests :

```bash
python -m unittest discover tests
```

## Avancement

- Création des classes de base (`Mot`, `ExpressionComposee`, `Relation`).
- Gestion des fichiers volumineux avec extraction des expressions composées.
- Tests unitaires robustes pour valider les fonctionnalités.
- Gestion optimisée de la mémoire lors de la lecture des fichiers.

## Étapes futures

- **Développement du graphe sémantique** : Implémenter la classe `GrapheSemantique` pour organiser les mots et relations sous forme de graphes.
- **Extraction des relations sémantiques** : Extraire les relations entre les nœuds du graphe à partir des textes fournis.
- **Visualisation des graphes** : Créer des outils de visualisation pour inspecter les graphes sémantiques extraits.
