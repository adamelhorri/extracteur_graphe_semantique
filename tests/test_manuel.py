# test_manuel.py

from graphe_semantique import GrapheSemantique
from moteur_de_regles import MoteurDeRegles

if __name__ == "__main__":
    graphe = GrapheSemantique()
    moteur = MoteurDeRegles(graphe)
    moteur.charger_regles('relations.txt')  # Assurez-vous que le chemin est correct
    moteur.appliquer_regles("Le chat mange la souris.")

    # Vérifier manuellement les relations
    assert graphe.existe_relation("chat", "mange", "r_agent"), "Relation r_agent non trouvée."
    assert graphe.existe_relation("souris", "mange", "r_patient"), "Relation r_patient non trouvée."
    print("Toutes les assertions sont passées.")
