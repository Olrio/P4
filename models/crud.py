"""
manage CRUD operations for following objects
Tournament
Player
Round
Match
"""

import datetime

from models.tournament import Tournament
from models.player import Player
from models.round import Round
from models.match import Match


class Crud:
    @staticmethod
    def create_tournament(data, tournaments):
        """create a new tournament from data"""
        t_ident = str(len(tournaments) + 1)
        tournaments[t_ident] = Tournament()
        tournaments[t_ident].ident = t_ident
        tournaments[t_ident].name = data["Nom"]
        tournaments[t_ident].town = data["Ville"]
        tournaments[t_ident].country = data["Pays"]
        tournaments[t_ident].date_start = data["Date de début"]
        tournaments[t_ident].date_end = data["Date de fin"]
        tournaments[t_ident].nb_rounds = int(data["Nombre de rondes"])
        tournaments[t_ident].control_time = data["Type de partie"]
        tournaments[t_ident].system = data["Système"]
        tournaments[t_ident].description = data["Commentaires"]
        tournaments[t_ident].status = "upcoming"
        tournaments[t_ident].rounds = list()
        tournaments[t_ident].players = list()
        tournaments[t_ident].singleton = list()
        return tournaments[t_ident]

    @staticmethod
    def retrieve_tournament(db_source):
        """retrieve a Tournament instance from serialized_tournament"""
        tournament = Tournament()
        for item in db_source.items():
            if item[0] == "rounds":
                for t_round in item[1]:
                    item[1][item[1].index(t_round)] = (t_round[0], t_round[1])
                    pass
                tournament.set_new_value(item[0], item[1])
            if item[0] in ["date_start", "date_end"]:
                tournament.set_new_value(
                    item[0], datetime.datetime.strptime(item[1], "%Y-%m-%d")
                )
            else:
                tournament.set_new_value(item[0], item[1])
        return tournament

    @staticmethod
    def update_tournament(tournament, parameter, value):
        tournament.set_new_value(parameter, value)

    @staticmethod
    def create_player(data, players):
        """create a new player from data"""
        p_ident = str(len(players) + 1)
        players[p_ident] = Player()
        players[p_ident].ident = p_ident
        players[p_ident].lastname = data["Nom"]
        players[p_ident].firstname = data["Prénom"]
        players[p_ident].rank = int(data["Classement"])
        players[p_ident].birthdate = data["Date de naissance"]
        players[p_ident].gender = data["Sexe"]
        return players[p_ident]

    @staticmethod
    def retrieve_player(db_source):
        """retrieve a Player instance from serialized_player"""
        player = Player()
        for item in db_source.items():
            if item[0] == "birthdate":
                player.set_new_value(
                    item[0], datetime.datetime.strptime(item[1], "%Y-%m-%d")
                )
            else:
                player.set_new_value(item[0], item[1])
        return player

    @staticmethod
    def update_player(player, parameter, value):
        player.set_new_value(parameter, value)

    @staticmethod
    def create_round(tournament, rounds):
        """create a new round from tournament given as an argument"""
        r_ident = (tournament.ident, str(len(tournament.rounds) + 1))
        rounds[r_ident] = Round()
        rounds[r_ident].ident = r_ident
        rounds[r_ident].name = "Round " + r_ident[1]
        rounds[r_ident].players = tournament.players
        rounds[r_ident].scores = dict()
        if len(tournament.rounds) == 0:
            for player in rounds[r_ident].players:
                rounds[r_ident].add_player_score(player.ident)
        else:
            for player in rounds[r_ident].players:
                rounds[r_ident].scores[player.ident] = \
                    tournament.rounds[-1].scores[
                    player.ident
                ]
        rounds[r_ident].matchs = list()
        rounds[r_ident].get_start_time()
        return rounds[r_ident]

    @staticmethod
    def retrieve_round(db_source):
        """retrieve a Round instance from serialized_round"""
        t_round = Round()
        for item in db_source.items():
            if item[0] == "ident":
                t_round.set_new_value(item[0], (item[1][0], item[1][1]))
            elif item[0] in ["start", "end"]:
                if item[1]:
                    t_round.set_new_value(
                        item[0],
                        datetime.datetime.strptime(item[1],
                                                   "%Y-%m-%d %H:%M:%S"),
                    )
                else:
                    t_round.set_new_value(item[0], item[1])
            elif item[0] == "matchs":
                tuples = [tuple(item) for item in item[1]]
                t_round.set_new_value(item[0], tuples)
            else:
                t_round.set_new_value(item[0], item[1])
        return t_round

    @staticmethod
    def create_match(matchs, player1, player2, tournament,
                     score1=0.0, score2=0.0):
        num_match = 1
        for t_round in tournament.rounds:
            num_match += len(t_round.matchs)
        m_ident = (
            tournament.rounds[-1].ident[0],
            tournament.rounds[-1].ident[1],
            str(num_match),
        )
        matchs[m_ident] = Match()
        matchs[m_ident].ident = m_ident
        matchs[m_ident].data = ([player1, score1], [player2, score2])
        return matchs[m_ident]

    @staticmethod
    def retrieve_match(db_source):
        """retrieve a Match instance from serialized_match"""
        match = Match()
        for item in db_source.items():
            if item[0] == "ident":
                match.set_new_value(item[0],
                                    (item[1][0], item[1][1], item[1][2]))
            else:
                match.set_new_value(item[0], tuple(item[1]))
        return match
