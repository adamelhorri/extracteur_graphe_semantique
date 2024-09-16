from abc import ABC, abstractmethod

class Noeud(ABC):
    def __init__(self, id: int, label: str):
        self.id = id
        self.label = label

    @abstractmethod
    def afficher(self):
        pass
