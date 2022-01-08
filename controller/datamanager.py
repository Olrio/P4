from models.data import DataLoader, DBLoaderSaver
from models.crud import Crud


class DataManager:
    """Management of all data in the app"""

    def __init__(self):
        self.players = None
        self.matchs = None
        self.rounds = None
        self.tournaments = None
        self.crud = Crud()
        self.dataloader = DataLoader()
        self.db = DBLoaderSaver()

    def get_database(self):
        """loading players, matchs, rounds, tournaments from database"""
        self.players = dict()
        players_serialized = self.db.load_db_all("chess_players")
        for player_raw in players_serialized:
            player = self.crud.retrieve_player(player_raw)
            self.players[player.ident] = player
        self.matchs = dict()
        matchs_serialized = self.db.load_db_all("chess_matchs")
        for match_raw in matchs_serialized:
            match = self.crud.retrieve_match(match_raw)
            match.data[0][0] = self.players[match.data[0][0]]
            if match.data[1][0]:
                match.data[1][0] = self.players[match.data[1][0]]
            self.matchs.update({match.ident: match})
        self.rounds = dict()
        rounds_serialized = self.db.load_db_all("chess_rounds")
        for round_raw in rounds_serialized:
            t_round = self.crud.retrieve_round(round_raw)
            for match in t_round.matchs:
                match = tuple(match)
                t_round.matchs[t_round.matchs.index(match)] = \
                    self.matchs.get(match)
            for player in t_round.players:
                t_round.players[t_round.players.index(player)] = \
                    self.players.get(
                    player
                )
            self.rounds[t_round.ident] = t_round
        self.tournaments = dict()
        tournaments_serialized = self.db.load_db_all("chess_tournaments")
        for tournament_raw in tournaments_serialized:
            tournament = self.crud.retrieve_tournament(tournament_raw)
            for player in tournament.players:
                tournament.players[tournament.players.index(player)] = \
                    self.players[
                    player
                ]
            for player in tournament.singleton:
                tournament.singleton[tournament.singleton.index(player)] = \
                    self.players[
                    player
                ]
            for t_round in tournament.rounds:
                tournament.rounds[tournament.rounds.index(t_round)] = \
                    self.rounds[
                    t_round
                ]
            self.tournaments[tournament.ident] = tournament

    def create_tournament(self, data, tournaments):
        for tournament in tournaments.values():
            if (
                tournament.name == data["Nom"]
                and tournament.town == data["Ville"]
                and tournament.country == data["Pays"]
                and tournament.date_start.strftime("%Y-%m-%d")
                == data["Date de début"].strftime("%Y-%m-%d")
            ):
                return None
        tournament = self.crud.create_tournament(data, tournaments)
        self.db.save_db(tournament)
        return tournament

    def load_tournament(self, tournament_id):
        return self.tournaments[tournament_id]

    def update_tournament(self, tournament, param, value):
        self.db.update_db(tournament, param, value)
        self.crud.update_tournament(tournament, param, value)

    def delete_tournament(self, tournament):
        if tournament.rounds:
            for t_round in tournament.rounds:
                self.delete_round(t_round)
        self.db.remove_db(tournament)
        del self.tournaments[tournament.ident]

    def create_player(self, data, players):
        for player in players.values():
            if (
                player.lastname == data["Nom"]
                and player.firstname == data["Prénom"]
                and player.birthdate.strftime("%Y-%m-%d")
                == data["Date de naissance"].strftime("%Y-%m-%d")
            ):
                return None
        player = self.crud.create_player(data, players)
        self.db.save_db(player)
        return player

    def load_player(self, player_id):
        return self.players[player_id]

    def update_player(self, player, param, value):
        self.db.update_db(player, param, value)
        self.crud.update_player(player, param, value)

    def delete_player(self, player):
        self.db.remove_db(player)
        del self.players[player.ident]

    def create_round(self, tournament, rounds):
        t_round = self.crud.create_round(tournament, rounds)
        # a round has to be added to a tournament
        tournament.add_round(t_round)
        # add round to database
        self.db.save_db(t_round)
        # update tournament containing round in database
        # replace round instance by round ident
        save_db_tournament_rounds = [
            t_round.ident for t_round in tournament.rounds]
        self.db.update_db(tournament, "rounds", save_db_tournament_rounds)
        return tournament

    def update_round(self, t_round, param, value):
        self.db.update_db(t_round, param, value)

    def delete_round(self, t_round):
        if t_round.matchs:
            for match in t_round.matchs:
                self.delete_match(match)
        self.db.remove_db(t_round)
        del self.rounds[t_round.ident]

    def create_match(
        self, matchs, player1, player2, tournament, score1=0.0, score2=0.0
    ):
        match = self.crud.create_match(
            matchs, player1, player2, tournament, score1, score2
        )
        return match

    def save_match(self, tournament, match):
        # add match to database
        # replace player instance by player ident
        match.data[0][0] = match.data[0][0].ident
        if match.data[1][0]:
            match.data[1][0] = match.data[1][0].ident
        self.db.save_db(match)
        if match.data[1][0]:
            match.data = (
                [self.players[match.data[0][0]], match.data[0][1]],
                [self.players[match.data[1][0]], match.data[1][1]],
            )
        else:
            match.data = (
                [self.players[match.data[0][0]], match.data[0][1]],
                [match.data[1][0], match.data[1][1]],
            )
        # update tournament containing round in database
        # replace round instance by round ident
        save_db_rounds_matchs = [
            match.ident for match in tournament.rounds[-1].matchs]
        self.db.update_db(
            tournament.rounds[-1], "matchs", save_db_rounds_matchs)

    def update_match(self, match):
        match.data[0][0] = match.data[0][0].ident
        if match.data[1][0]:
            match.data[1][0] = match.data[1][0].ident
        self.db.update_db(match, "data", match.data)
        if match.data[1][0]:
            match.data = (
                [self.players[match.data[0][0]], match.data[0][1]],
                [self.players[match.data[1][0]], match.data[1][1]],
            )
        else:
            match.data = (
                [self.players[match.data[0][0]], match.data[0][1]],
                [match.data[1][0], match.data[1][1]],
            )

    def delete_match(self, match):
        self.db.remove_db(match)
        del self.matchs[match.ident]

    def create_matchs_swiss_first_round(self, tournament):
        # players are distributed in two halves
        halves = tournament.rounds[0].two_halves(
            tournament.rounds[0].players, tournament
        )
        # saving singletons in database
        self.db.update_db(
            tournament, "singleton", [
                player.ident for player in tournament.singleton]
        )
        # generating matchs of the first round
        for player1, player2 in zip(halves[0], halves[1]):
            match = self.create_match(
                self.matchs, player1, player2, tournament)
            tournament.rounds[0].add_match(match)
            self.save_match(tournament, match)
        # manage floating player if number of players is odd
        if len(tournament.rounds[0].players) % 2 != 0:
            match = self.create_match(
                self.matchs, tournament.singleton[-1], None, tournament
            )
            tournament.rounds[0].add_match(match)
            self.save_match(tournament, match)

    def create_matchs_swiss_following_round(self, tournament):
        self.create_round(tournament, self.rounds)
        matchs = []
        first_players = list(tournament.players)
        second_players = list(tournament.players)
        rev_i = -1
        if len(tournament.players) % 2 != 0:
            # if number of players is odd, a singleton is identified
            while tournament.players[rev_i] in tournament.singleton:
                rev_i -= 1
            tournament.singleton.append(tournament.players[rev_i])
            self.db.update_db(
                tournament,
                "singleton",
                [player.ident for player in tournament.singleton],
            )
            first_players.remove(tournament.singleton[-1])
            second_players.remove(tournament.singleton[-1])

        while first_players:
            second_players.remove(second_players[0])
            x = 0
            appairing = 0
            match = None

            # a player can't play twice against the same opponent
            while appairing == 0:
                flag = 0
                match = self.create_match(
                    self.matchs,
                    first_players[0],
                    second_players[x],
                    tournament
                )
                for t_round in tournament.rounds:
                    for past_match in t_round.matchs:
                        if (
                            match.data[0][0] == past_match.data[0][0]
                            and match.data[1][0] == past_match.data[1][0]
                            or match.data[0][0] == past_match.data[1][0]
                            and match.data[1][0] == past_match.data[0][0]
                        ):
                            if (
                                len(first_players) > 2
                            ):  # if no other possibility,
                                # player will play twice an opponent
                                x += 1
                                flag = 1
                                del self.matchs[match.ident]
                                break
                if flag == 0:
                    appairing = 1

            matchs.append(match)  # only when appairing is correct
            tournament.rounds[-1].add_match(match)
            self.save_match(tournament, match)
            first_players.remove(first_players[0])
            first_players.remove(second_players[x])
            second_players.remove(second_players[x])
        if len(tournament.players) % 2 != 0:  # adding a match with singleton
            match = self.create_match(
                self.matchs, tournament.singleton[-1], None, tournament
            )
            matchs.append(match)
            tournament.rounds[-1].add_match(match)
            self.save_match(tournament, match)

    def add_or_remove_a_player_to_tournament(self, player_ident, tournament):
        if self.players[player_ident] in tournament.players:
            tournament.remove_player(self.players[player_ident])
        else:
            tournament.add_player(self.players[player_ident])
        save_db_players = [player.ident for player in tournament.players]
        self.db.update_db(tournament, "players", save_db_players)

    def sorted_players_alpha(self, players):
        return self.dataloader.sorted_players_alpha(players)

    def sorted_players_rank(self, players):
        return self.dataloader.sorted_players_rank(players)

    def sorted_tournaments_date(self, tournaments):
        return self.dataloader.sorted_tournaments_date(tournaments)
