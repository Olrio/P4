class Player:
    def __init__(self):
        """initialize a new player"""
        self.lastname = None
        self.firstname = None
        self.birthdate = None
        self.gender = None
        self.rank = None
        self.ident = None

    def __str__(self):
        return f"{self.lastname:<12}{self.firstname:<15}{self.rank:<10}{self.birthdate.strftime('%Y-%m-%d'):<20}"

    @staticmethod
    def get_translation_fr(item):
        fr = {
            "lastname": "Nom",
            "firstname": "Prénom",
            "rank": "Classement",
            "ident": "Identifiant",
            "birthdate": "Date de naissance",
            "gender": "Sexe",
        }
        return fr[item]

    def set_new_value(self, param, value):
        self.__setattr__(param, value)
