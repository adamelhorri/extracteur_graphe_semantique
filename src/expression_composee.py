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
