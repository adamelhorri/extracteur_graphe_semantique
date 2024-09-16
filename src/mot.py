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
