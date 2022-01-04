from tinydb import TinyDB, Query
from models.player import Player
from models.round import Round
from models.tournament import Tournament
from models.match import Match


class DataLoader:
    def __init__(self):
        pass

    @staticmethod
    def sorted_players_alpha(players):
        players = sorted(players, key=lambda x: x.lastname)
        return players

    @staticmethod
    def sorted_players_rank(players):
        players = sorted(players, key=lambda x: x.rank, reverse=True)
        return players

    @staticmethod
    def sorted_tournaments_date(tournaments):
        tournaments = sorted(tournaments, key=lambda x: x.date_start)
        return tournaments


class DBLoaderSaver:
    def __init__(self):
        self.db = TinyDB("data/db.json")
        self.query = Query()

    def save_db(self, data):
        """stores data in TinyDB as dicts"""
        if isinstance(data, Player):
            dict_player_to_save = data.__dict__.copy()
            dict_player_to_save["birthdate"] = data.birthdate.strftime("%Y-%m-%d")
            self.db.table("chess_players").insert(dict_player_to_save)
        elif isinstance(data, Tournament):
            dict_tournament_to_save = data.__dict__.copy()
            dict_tournament_to_save["date_start"] = data.date_start.strftime("%Y-%m-%d")
            dict_tournament_to_save["date_end"] = data.date_end.strftime("%Y-%m-%d")
            self.db.table("chess_tournaments").insert(dict_tournament_to_save)
        elif isinstance(data, Round):
            dict_round_to_save = data.__dict__.copy()
            dict_round_to_save["start"] = data.start.strftime("%Y-%m-%d %H:%M:%S")
            # replace player instance by player ident
            dict_round_to_save["players"] = [player.ident for player in data.players]
            if data.end:
                dict_round_to_save["end"] = data.end.strftime("%Y-%m-%d %H:%M:%S")
            self.db.table("chess_rounds").insert(dict_round_to_save)
        else:
            self.db.table("chess_matchs").insert(data.__dict__)

    def remove_db(self, data):
        """remove serialized object from database"""
        if isinstance(data, Player):
            data.birthdate = data.birthdate.strftime("%Y-%m-%d")
            self.db.table("chess_players").remove(self.query.ident == data.ident)
        elif isinstance(data, Tournament):
            data.date_start = data.date_start.strftime("%Y-%m-%d")
            data.date_end = data.date_end.strftime("%Y-%m-%d")
            self.db.table("chess_tournaments").remove(self.query.ident == data.ident)
        elif isinstance(data, Round):
            if data.start:
                data.start = data.start.strftime("%Y-%m-%d %H:%M:%S")
            if data.end:
                data.end = data.end.strftime("%Y-%m-%d %H:%M:%S")
            key_round = list(data.ident)
            self.db.table("chess_rounds").remove(self.query.ident == key_round)
        elif isinstance(data, Match):
            key_match = list(data.ident)
            self.db.table("chess_matchs").remove(self.query.ident == key_match)

    def update_db(self, data, param, value):
        new_value = value
        if isinstance(data, Player):
            if param == "birthdate":
                new_value = new_value.strftime("%Y-%m-%d")
            self.db.table("chess_players").update(
                {param: new_value}, self.query.ident == data.ident
            )
        elif isinstance(data, Tournament):
            if param in ["date_start", "date_end"]:
                new_value = new_value.strftime("%Y-%m-%d")
            self.db.table("chess_tournaments").update(
                {param: new_value}, self.query.ident == data.ident
            )
        elif isinstance(data, Round):
            if param in ["start", "end"]:
                new_value = new_value.strftime("%Y-%m-%d %H:%M:%S")
            self.db.table("chess_rounds").update(
                {param: new_value}, self.query.ident == list(data.ident)
            )
        else:
            self.db.table("chess_matchs").update(
                {param: new_value}, self.query.ident == list(data.ident)
            )

    def save_db_all(self, data):
        """stores all data in TinyDB"""
        players_table = self.db.table("chess_players")
        players_table.truncate()
        players_table.insert_multiple(data)

    def load_db(self):
        data = self.db.all()
        return data

    def load_db_all(self, table_name):
        data = self.db.table(table_name).all()
        return data
