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
