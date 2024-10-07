# src/Token.py

class Token:
    def __init__(self, text):
        self.text = text #texte de base
        self.lemma_candidates = [] #candidats de lemmes
        self.pos_candidates = [] #candidats de pos 
        self.pos_ = None # pos gagnant (peut etre X)
        self.lemma_ = None #lemme gagnant (peut etre token.text si aucun lemme trouvé)
        self.gender = None #genre du mot (peut etre none)
        self.number = None #nombre du mot (peut etre none)
        self.shape_ = None #format exemple Adam.shape_ = Xxxx
        self.is_alpha = None # si token est un alpha (boolean)
        self.is_stop = None # si c'est un stop word
        self.morph = {} # morphlogie du mot , diffère d'un pos à l'autre niveau format
        self.dep_ = None #TODO type de dependance syntaxique
        self.head = None #TODO mot dont le token depends 
        self.token_id = None #id du token se reinitialise à 0 au debut de chaque phrase
        self.token_pid= None #id de la phrase s'incremente à partir de chaque 
        self.token_primarykey=None#clé primaire unique de chaque token
        self.groupe=None

    # Méthodes pour définir les attributs
    def set_alpha(self, is_alpha):
        self.is_alpha = is_alpha

    def set_shape(self, shape):
        self.shape_ = shape

    def set_stop(self, is_stop):
        self.is_stop = is_stop

    def set_gender(self, gender):
        self.gender = gender

    def set_number(self, number):
        self.number = number

    def set_morphological_features(self, features):
        self.morph = features

    def set_dep_(self, dep):
        self.dep_ = dep

    def set_head(self, head):
        self.head = head
    def set_pid(self, pid):
        self.token_pid = pid

    def __repr__(self):
        # Afficher uniquement le texte de la tête pour éviter la récursion
        head_text = self.head.text if isinstance(self.head, Token) else self.head
        return f"\nTid:[{self.token_primarykey}]\n        [\n        text : '{self.text}',\n        pos_cand : {self.pos_candidates} \n        pos_ : '{self.pos_}' \n        lemmas_cand : {self.lemma_candidates} \n        lemma_ : '{self.lemma_}' \n        gender|number : '{self.gender}|{self.number}' \n        morphological features : '{self.morph}' \n        shape : '{self.shape_}' \n        dep_ : '{self.dep_}'\n        head : '{head_text}' \n        groups: '{self.groupe}'        ]"
