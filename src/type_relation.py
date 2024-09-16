from enum import Enum

class TypeRelation(Enum):
    r_succ = "succession"
    r_associated = "association"
    r_raff_sem = "raffinement sémantique"
    r_pos = "partie du discours"
    r_syn = "synonyme"
    r_isa = "hyperonyme"
    r_anto = "antonyme"
    r_hypo = "hyponyme"
    r_agent = "agent"
    r_patient = "patient"
    r_lemma = "lemme"
