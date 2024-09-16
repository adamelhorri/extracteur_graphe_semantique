import spacy

class DesambiguiseurLexical:
    def __init__(self):
        self.nlp = spacy.load("fr_core_news_md")

    def desambiguer(self, mot, contexte):
        # Désambiguïse le mot en fonction du contexte
        pass
