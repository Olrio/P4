"""
Management of a tournament
"""


class Tournament:
    def __init__(self):
        self.name = None
        self.town = None
        self.country = None
        self.ident = None
        self.date_start = None
        self.date_end = None
        self.status = None  # upcoming, in progress, ended
        self.control_time = None  # bullet, blitz or rapid
        self.description = None  # tournament director's comments
        self.system = None  # "swiss" by default
        self.nb_rounds = None  # number of rounds in the tournament  = 4 by default
        self.rounds = None  # list of round  instances
        self.players = None  # list of players instances
        self.singleton = None  # list of floating players when number of players is odd

    def __str__(self):
        return (
            f"{self.name:<30}{self.town:<20}{self.country:<20}"
            f"{self.date_start.strftime('%Y-%m-%d'):<20}  {self.status:<20}"
        )

    @staticmethod
    def get_translation_fr(item):
        fr = {
            "name": "Nom du tournoi",
            "town": "Ville",
            "country": "Pays",
            "ident": "ID",
            "date_start": "Date de début",
            "date_end": "Date de fin",
            "status": "Statut",
            "nb_rounds": "Nombre de rondes",
            "control_time": "Type de partie",
            "description": "Commentaires",
            "system": "Système",
            "scores": "Scores",
        }
        return fr[item]

    def set_new_value(self, param, value):
        self.__setattr__(param, value)

    def add_round(self, n_round):
        for t_round in self.rounds:
            if n_round.name == t_round.name:
                return
        self.rounds.append(n_round)

    def add_player(self, player):
        if player not in self.players:
            self.players.append(player)

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)

    def sort_players(self, players):
        s_players = sorted(players, key=lambda x: x.rank, reverse=True)  # by rank
        if self.rounds:
            s_players = sorted(
                s_players, key=lambda x: self.rounds[-1].scores[x.ident], reverse=True
            )
        return s_players
