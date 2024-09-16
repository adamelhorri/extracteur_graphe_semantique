class Cache:
    def __init__(self):
        self.relations_cachees = {}

    def obtenir_relation(self, cle):
        return self.relations_cachees.get(cle)

    def ajouter_relation(self, cle, relation):
        self.relations_cachees[cle] = relation
