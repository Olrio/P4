"""
Gestion de la classe Round
correspondant à un tour dans un tournoi d'échecs
Un round comprend plusieurs matchs opposant tous les joueurs deux à deux
"""
import datetime


class Round:
    def __init__(self, name=None, ident=None):
        """ensemble des parties jouées durant une ronde"""
        self.name = name
        self.scores = None  # dict of identifiants of the players in the round and their score in the round
        self.players = None
        self.matchs = None
        self.ident = ident
        self.start = None
        self.end = None

    @staticmethod
    def get_translation(lang):
        if lang == "fr":
            return {
                "name": "Nom",
                "scores": "Scores des joueurs",
                "sorted_players": "Liste triée des joueurs",
                "matchs": "Liste des matchs",
                "ident": "Identifiant",
            }

    def set_new_value(self, param, value):
        self.__setattr__(param, value)

    def add_player_score(self, player):
        if player not in self.scores:
            self.scores[player] = 0.0

    def add_match(self, match):
        if match not in self.matchs:
            self.matchs.append(match)

    def sort_players(self, players):
        s_players = sorted(players, key=lambda x: x.rank, reverse=True)  # by rank
        s_players = sorted(s_players, key=lambda x: self.scores[x.ident], reverse=True)
        return s_players

    @staticmethod
    def two_halves(players, tournament):
        # distribute players in best half and lowest half
        first_half = players.copy()
        second_half = []

        # verify if number of players is odd number
        # player with the lowest score/rank is singleton for this round
        # player can be singleton only once
        rev_i = -1
        if len(players) % 2 != 0:
            while players[rev_i] in tournament.singleton:
                rev_i -= 1
            tournament.singleton.append(players[rev_i])
            first_half.remove(players[rev_i])

        while len(first_half) > len(second_half):
            second_half.append(first_half.pop())
        # players of the latest group are sorted by rank
        second_half.sort(key=lambda x: x.rank, reverse = True)
        return first_half, second_half

    def scores_update(self, match):
        self.scores[match.data[0][0].ident] += match.data[0][1]
        if match.data[1][0]:
            self.scores[match.data[1][0].ident] += match.data[1][1]

    def scores_reset(self, match):
        self.scores[match.data[0][0].ident] -= match.data[0][1]
        if match.data[1][0]:
            self.scores[match.data[1][0].ident] -= match.data[1][1]
        match.data[0][1] = 0.0
        match.data[1][1] = 0.0

    def get_start_time(self):
        self.start = datetime.datetime.now()

    def get_end_time(self):
        self.end = datetime.datetime.now()
