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
