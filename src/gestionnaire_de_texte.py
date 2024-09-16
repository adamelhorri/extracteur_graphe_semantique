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