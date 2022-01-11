"""
>>> a = 2+2
>>> a
5
"""

import datetime

from models.menu import get_menus
from view.view import View
from controller.datamanager import DataManager
from dateutil import parser


class MainController:
    """
    Global management of the app
    MainController interacts with Menu objects
    """
    def __init__(self):
        # instance menus
        self.menus = dict()
        self.current_menu = None
        self.dm = DataManager()
        self.player = None  # current player
        self.tournament = None  # current tournament
        self.view = View()

    def setup(self):
        self.dm.get_database()
        get_menus(self.menus)
        # launching program
        self.current_menu = self.menus["home"]
        self.run()

    def run(self):
        while True:
            choice = ""
            while choice not in self.current_menu.choices.keys():
                eval(self.current_menu.run)
                for valid_choice in self.current_menu.choices.items():
                    print(valid_choice[1][0])
                choice = self.view.main_choice()
            if choice == "Q":
                exit()
            else:
                self.current_menu = self.current_menu.choices[choice][1]

    def run_home(self):
        self.view.home(self.player, self.tournament, self.current_menu)
        self.view.show_players_in_tournament(self.tournament)

    def run_tournament(self):
        self.view.clear()
        self.view.current_player_and_tournament(
            self.player, self.tournament, self.current_menu
        )
        self.view.show_players_in_tournament(self.tournament)

    def run_load_tournament(self):
        valid_choice = ["C"]
        t_choice = ""
        for tournament in self.dm.tournaments.values():
            valid_choice.append(tournament.ident)
        while t_choice.upper() not in valid_choice:
            self.view.clear()
            self.view.current_player_and_tournament(
                self.player, self.tournament, self.current_menu
            )
            t_choice = self.view.display_all_tournaments(self.dm.tournaments)
        if t_choice.upper() == "C":
            pass
        else:
            self.tournament = self.dm.load_tournament(t_choice)
            self.view.clear()
            self.view.current_player_and_tournament(
                self.player, self.tournament, self.current_menu
            )
            self.view.show_players_in_tournament(self.tournament)

    def run_start_tournament(self):
        self.view.clear()
        self.view.current_player_and_tournament(
            self.player, self.tournament, self.current_menu
        )
        if not self.tournament:
            self.view.no_selected_tournament()
            self.current_menu = self.menus["tournament"]
            self.view.clear()
            self.view.current_player_and_tournament(
                self.player, self.tournament, self.current_menu
            )
            self.view.show_players_in_tournament(self.tournament)
        # if not enough player in tournament, add some
        elif len(self.tournament.players) < 2:
            self.view.show_players_in_tournament(self.tournament)
            self.view.not_enought_players_in_tournament(self.tournament)
        else:
            if self.tournament.system != "swiss":
                self.view.not_swiss_system()
            else:
                # the program verify if the tournament has already started
                # and resume at current round
                if self.tournament.status == "ended":
                    self.view.tournament_ended(self.tournament)
                    self.view.press_key()
                    self.current_menu = self.menus["tournament"]
                    self.run()
                elif len(self.tournament.rounds) <= 1:
                    self.run_swiss_first_round(self.tournament)
                else:
                    self.run_swiss_following_rounds(self.tournament)
                self.view.swiss_final_results(self.tournament)
                self.dm.update_tournament(self.tournament, "status", "ended")
                self.current_menu = self.menus["home"]
                self.view.clear()
                self.view.current_player_and_tournament(
                    self.player, self.tournament, self.current_menu
                )
                self.view.show_players_in_tournament(self.tournament)

    def run_swiss_first_round(self, tournament):
        # create a first round if needed
        if len(tournament.rounds) == 0:
            self.dm.create_round(tournament, self.dm.rounds)
            # change tournament status
            self.dm.update_tournament(tournament, "status", "in progress")
        # display players participating in the tournament
        # players are sorted by score then by rank
        self.show_players_in_tournament(tournament)
        self.resume_or_back_home(tournament)
        # creating matchs for the first round
        if len(tournament.rounds) == 1 \
                and len(tournament.rounds[-1].matchs) == 0:
            self.dm.create_matchs_swiss_first_round(tournament)
        # manage matchs of the first round
        for match in tournament.rounds[-1].matchs:
            if match.data[0][1] == 0 and match.data[1][1] == 0:
                self.matchs_of_the_round(tournament)
        # display ranking at the end of the round
        self.show_players_in_tournament(tournament)
        self.resume_or_back_home(tournament)
        # other rounds
        self.run_swiss_following_rounds(tournament)

    def matchs_of_the_round(self, tournament):
        t_round = tournament.rounds[-1]
        choice = ""
        valid_choice = ["N", "Y", "E"]
        for match in t_round.matchs:
            if match.data[1][0]:
                valid_choice.append(match.ident[2])
        while choice.upper() not in valid_choice:
            choice = self.view.show_matchs_of_the_round(tournament)
        if choice.upper() == "N":
            for match in t_round.matchs:
                if match.data[0][1] == 0 and match.data[1][1] == 0:
                    self.current_menu = self.menus["home"]
                    self.run()
            t_round.get_end_time()
            self.dm.update_round(
                t_round, "end", t_round.end
            )
            self.current_menu = self.menus["home"]
            self.run()
        elif choice.upper() == "E":
            self.change_player_rank_during_tournament(tournament)
        elif choice.upper() == "Y":
            # check if a result for every match exists
            for match in t_round.matchs:
                if match.data[0][1] == 0.0 and match.data[1][0] is None:
                    match.data[0][1] = 1.0  # singleton marks 1 point
                    t_round.scores[match.data[0][0].ident] += 1
                    self.dm.update_match(match)
                    self.dm.update_round(
                        t_round, "scores", t_round.scores
                    )
                if match.data[0][1] == 0.0 and match.data[1][1] == 0.0:
                    self.view.some_results_missing(tournament)
                    self.matchs_of_the_round(tournament)
            t_round.get_end_time()
            self.dm.update_round(
                t_round, "end", t_round.end
            )
        for match in t_round.matchs:
            if match.ident[2] == choice:
                self.result_of_a_match(match, tournament)

    def change_player_rank_during_tournament(self, tournament):
        self.view.clear()
        choice = ""
        valid_choices = ["C"]
        valid_choices.extend(player.ident for player in tournament.players)
        while choice.upper() not in valid_choices:
            choice = self.view.change_player_rank_during_tournament(tournament)
        if choice.upper() == "C":
            pass
        else:
            self.player = self.dm.players[choice]
            self.run_edit_player()
        return

    def result_of_a_match(self, match, tournament):
        choice = ""
        while choice.upper() not in [
            "C",
            "N",
            match.data[0][0].ident,
            match.data[1][0].ident,
        ]:
            choice = self.view.result_of_a_match(match)
        if choice.upper() == "C":
            self.matchs_of_the_round(tournament)
            return
        # check if a result has already been entered for this match.
        # If yes, reset scores
        if match.data[0][1] != 0 or match.data[1][1] != 0:
            tournament.rounds[-1].scores_reset(match)
        if choice.upper() == "N":
            match.set_draw()
        elif choice.upper() == match.data[0][0].ident:
            match.set_victory_1()
        elif choice.upper() == match.data[1][0].ident:
            match.set_victory_2()
        tournament.rounds[-1].scores_update(match)
        self.dm.update_match(match)
        self.dm.update_round(
            tournament.rounds[-1], "scores", tournament.rounds[-1].scores
        )
        self.matchs_of_the_round(tournament)

    def show_players_in_tournament(self, tournament):
        t_round = tournament.rounds[-1]
        text = f"pour la ronde {t_round.name}"
        for match in t_round.matchs:
            # check if round not ended
            if match.data[0][1] == 0 and match.data[1][1] == 0:
                text = f"pour la ronde {t_round.name}"
                break
            if isinstance(t_round.end, datetime.datetime):
                text = (
                    f"à l'issue de la ronde {t_round.name}"
                    f" - Fin de la ronde :"
                    f"{t_round.end.strftime('%Y-%m-%d  %H:%M:%S')}"
                )
            else:
                text = (
                    f"à l'issue de la ronde {t_round.name}"
                    f" - Fin de la ronde :{t_round.end}"
                )
        t_round.players = tournament.rounds[0].sort_players(
            tournament.rounds[-1].players
        )
        tournament.players = t_round.sort_players(tournament.players)
        self.view.show_players_in_tournament(tournament, text)

    def resume_or_back_home(self, tournament):
        choice = ""
        while choice not in ["Y", "N", "E"]:
            choice = self.view.resume_or_back_home()
        if choice == "N":
            self.current_menu = self.menus["home"]
            self.run()
        elif choice.upper() == "E":
            self.change_player_rank_during_tournament(tournament)

    def run_swiss_following_rounds(self, tournament):
        round_status = ""
        while len(tournament.rounds) <= tournament.nb_rounds:
            for match in tournament.rounds[-1].matchs:
                if match.data[0][1] == 0 and match.data[1][1] == 0:
                    round_status = "in progress"
                    break
                else:
                    round_status = "ended"
            if round_status == "ended" and not tournament.rounds[-1].end:
                tournament.rounds[-1].get_end_time()
            if (
                round_status == "ended"
                and len(tournament.rounds) < tournament.nb_rounds
            ):
                self.dm.create_matchs_swiss_following_round(tournament)
                round_status = "in progress"
            if round_status == "in progress":
                self.matchs_of_the_round(tournament)
            self.show_players_in_tournament(tournament)
            self.resume_or_back_home(tournament)
            if len(tournament.rounds) == tournament.nb_rounds and\
                    round_status == "ended":
                if not tournament.rounds[-1].end:
                    tournament.rounds[-1].get_end_time()
                break

    def run_create_tournament(self):
        self.view.clear()
        self.view.current_player_and_tournament(
            self.player, self.tournament, self.current_menu
        )
        data = self.view.get_data_new_tournament()
        valid_choice = ["Y", "N"]
        choice = ""
        while choice.upper() not in valid_choice:
            choice = self.view.valid_or_cancel()
        if choice.upper() == "N":
            pass
        elif choice.upper() == "Y":
            new_tournament = \
                self.dm.create_tournament(data, self.dm.tournaments)
            if new_tournament is None:
                self.view.alert_creating_an_existing_tournament(
                    data["Nom"], data["Ville"],
                    data["Pays"], data["Date de début"]
                )
            else:
                self.tournament = new_tournament
        self.current_menu = self.menus["tournament"]
        self.view.clear()
        self.view.current_player_and_tournament(
            self.player, self.tournament, self.current_menu
        )
        self.view.show_players_in_tournament(self.tournament)

    def run_edit_tournament(self):
        if not self.tournament:
            self.view.no_selected_tournament()
            self.current_menu = self.menus["tournament"]
            self.view.clear()
            self.view.current_player_and_tournament(
                self.player, self.tournament, self.current_menu
            )
            self.view.show_players_in_tournament(self.tournament)
        else:
            self.view.clear()
            self.view.current_player_and_tournament(
                self.player, self.tournament, self.current_menu
            )
            choice = ""
            valid_choices = ["N"]
            param_choices = {}
            for param, index in zip(
                self.tournament.__dict__, range(len(self.tournament.__dict__))
            ):
                if param in [
                    "scores",
                    "ident",
                    "rounds",
                    "players",
                    "first_half",
                    "second_half",
                    "translation",
                    "singleton",
                ]:
                    pass
                else:
                    param_choices[str(index)] = param
                    valid_choices.append(str(index))
            while choice.upper() not in valid_choices:
                choice = self.view.display_editing_tournament(
                    self.tournament, param_choices
                )
            if choice.upper() == "N":
                self.current_menu = self.menus["tournament"]
                self.view.clear()
                self.view.current_player_and_tournament(
                    self.player, self.tournament, self.current_menu
                )
                self.view.show_players_in_tournament(self.tournament)
            else:
                # Determination of the attribute to modify
                parameter = param_choices[choice]
                old_value = self.tournament.__getattribute__(parameter)
                new_value = self.view.new_value_for_data(
                    self.tournament.get_translation_fr(parameter), old_value
                )
                if new_value.upper() == "B":
                    self.run_edit_tournament()
                if self.view.confirm_new_value(old_value, new_value) == "Y":
                    if parameter in ["date_start", "date_end"]:
                        try:
                            new_value = parser.parse(new_value)
                        except ValueError:
                            print(
                                "Veuillez entrer une date de naissance "
                                "au format jj/mm/aaaa ou yyyy/mm/dd"
                            )
                            self.view.modification_cancelled()
                            new_value = old_value
                            self.run_edit_tournament()
                    elif parameter == "nb_rounds":
                        new_value = int(new_value)
                    elif parameter == "status":
                        if new_value not in ["upcoming",
                                             "in progress", "ended"]:
                            print(
                                "Le statut du tournoi doit être : "
                                "'upcoming', 'in progress' ou 'ended'"
                            )
                            self.view.modification_cancelled()
                            new_value = old_value
                            self.run_edit_tournament()
                    if new_value != old_value:
                        self.view.modification_validated()
                    self.dm.update_tournament(
                        self.tournament, parameter, new_value)
                    self.run_edit_tournament()
                else:
                    self.view.modification_cancelled()
                    self.run_edit_tournament()

    def run_delete_tournament(self):
        self.view.clear()
        self.view.current_player_and_tournament(
            self.player, self.tournament, self.current_menu
        )
        self.view.show_players_in_tournament(self.tournament)
        if not self.tournament:
            self.view.no_selected_tournament()
        else:
            self.view.alert_tournament_permanently_delete(self.tournament)
            choice = ""
            while choice not in ["Y", "N"]:
                choice = self.view.valid_or_cancel()
            if choice == "N":
                pass
            else:
                self.dm.delete_tournament(self.tournament)
                self.tournament = None
        self.current_menu = self.menus["tournament"]
        self.view.clear()
        self.view.current_player_and_tournament(
            self.player, self.tournament, self.current_menu
        )
        self.view.show_players_in_tournament(self.tournament)

    def run_player(self):
        self.view.clear()
        self.view.current_player_and_tournament(
            self.player, self.tournament, self.current_menu
        )

    def run_load_player(self):
        valid_choice = ["Y"]
        p_choice = ""
        for player in self.dm.players.values():
            valid_choice.append(player.ident)
        while p_choice.upper() not in valid_choice:
            self.view.clear()
            self.view.current_player_and_tournament(
                self.player, self.tournament, self.current_menu
            )
            p_choice = \
                self.view.display_all_players(self.dm.players, self.tournament)
        if p_choice.upper() == "Y":
            pass
        else:
            self.player = self.dm.load_player(p_choice)
            self.run_load_player()
        self.view.clear()
        self.view.current_player_and_tournament(
            self.player, self.tournament, self.current_menu
        )

    def run_create_player(self):
        self.view.clear()
        self.view.current_player_and_tournament(
            self.player, self.tournament, self.current_menu
        )
        data = self.view.get_data_new_player()
        valid_choice = ["Y", "N"]
        choice = ""
        while choice.upper() not in valid_choice:
            choice = self.view.valid_or_cancel()
        if choice.upper() == "N":
            pass
        elif choice.upper() == "Y":
            new_player = self.dm.create_player(data, self.dm.players)
            if new_player is None:
                self.view.alert_creating_an_existing_player(
                    data["Nom"], data["Prénom"], data["Date de naissance"]
                )
            elif new_player == "rank_incorrect":
                self.view.rank_incorrect()
                self.view.press_key()
            else:
                self.player = new_player
        self.view.clear()
        self.current_menu = self.menus["player"]
        self.view.current_player_and_tournament(
            self.player, self.tournament, self.current_menu
        )

    def run_edit_player(self):
        # not possible if none player is selected
        if not self.player:
            self.view.no_selected_player()
            self.current_menu = self.menus["player"]
            self.view.clear()
            self.view.current_player_and_tournament(
                self.player, self.tournament, self.current_menu
            )
        else:
            self.view.clear()
            self.view.current_player_and_tournament(
                self.player, self.tournament, self.current_menu
            )
            choice = ""
            valid_choices = ["N"]
            param_choices = {}
            for param, index in zip(
                self.player.__dict__, range(len(self.player.__dict__))
            ):
                if param in ["ident"]:
                    pass
                else:
                    param_choices[str(index)] = param
                    valid_choices.append(str(index))
            while choice.upper() not in valid_choices:
                choice = self.view.display_editing_player(
                    self.player, param_choices)
            if choice.upper() == "N":
                self.current_menu = self.menus["player"]
                self.view.clear()
                self.view.current_player_and_tournament(
                    self.player, self.tournament, self.current_menu
                )
            else:
                # Determination of the attribute to modify
                parameter = param_choices[choice]
                old_value = self.player.__getattribute__(parameter)
                new_value = self.view.new_value_for_data(
                    self.player.get_translation_fr(parameter), old_value
                )
                if new_value.upper() == "B":
                    self.run_edit_player()
                if self.view.confirm_new_value(old_value, new_value) == "Y":
                    if parameter == "birthdate":
                        try:
                            new_value = parser.parse(new_value)
                        except ValueError:
                            print(
                                "Veuillez entrer une date de naissance "
                                "au format jj/mm/aaaa ou yyyy/mm/dd"
                            )
                            self.view.modification_cancelled()
                            new_value = old_value
                            self.run_edit_player()
                    elif parameter == "rank":
                        new_value = int(new_value)
                    if new_value != old_value:
                        self.view.modification_validated()
                    self.dm.update_player(self.player, parameter, new_value)
                    self.run_edit_player()
                else:
                    self.view.modification_cancelled()
                    self.run_edit_player()

    def run_delete_player(self):
        if not self.player:
            self.view.no_selected_player()
            self.current_menu = self.menus["player"]
            self.view.clear()
            self.view.current_player_and_tournament(
                self.player, self.tournament, self.current_menu
            )
        else:
            self.view.clear()
            self.view.current_player_and_tournament(
                self.player, self.tournament, self.current_menu
            )
            self.view.alert_player_permanently_delete(self.player)
            choice = ""
            while choice not in ["Y", "N"]:
                choice = self.view.valid_or_cancel()
            if choice == "N":
                pass
            else:
                self.dm.delete_player(self.player)
                self.player = None
            self.current_menu = self.menus["player"]
            self.view.clear()
            self.view.current_player_and_tournament(
                self.player, self.tournament, self.current_menu
            )

    def run_add_remove_player_tournament(self):
        self.view.clear()
        self.view.current_player_and_tournament(
            self.player, self.tournament, self.current_menu
        )
        if not self.tournament:
            self.view.no_selected_tournament()
            self.current_menu = self.menus["tournament"]
            self.view.current_player_and_tournament(
                self.player, self.tournament, self.current_menu
            )
        elif self.tournament.status == "ended":
            self.view.tournament_ended(self.tournament)
            self.view.add_remove_player_tournament_disabled()
            self.current_menu = self.menus["tournament"]
            self.view.current_player_and_tournament(
                self.player, self.tournament, self.current_menu
            )
        elif self.tournament.status == "in progress":
            self.view.tournament_in_progress(self.tournament)
            self.view.add_remove_player_tournament_disabled()
            self.current_menu = self.menus["tournament"]
            self.view.clear()
            self.view.current_player_and_tournament(
                self.player, self.tournament, self.current_menu
            )
            self.view.show_players_in_tournament(self.tournament)
        else:
            valid_choice = ["C", "Y"]
            p_choice = ""
            for player in self.dm.players.values():
                valid_choice.append(player.ident)
            while p_choice.upper() not in valid_choice:
                self.view.current_player_and_tournament(
                    self.player, self.tournament, self.current_menu
                )
                p_choice = self.view.display_add_remove_players_tournament(
                    self.dm.players, self.tournament
                )
            if p_choice.upper() == "C":
                if self.tournament.status == "upcoming":
                    while self.tournament.players:
                        self.dm.add_or_remove_a_player_to_tournament(
                            self.tournament.players[-1].ident, self.tournament
                        )
                    self.run_add_remove_player_tournament()
            elif p_choice.upper() == "Y":
                pass
            else:
                self.dm.add_or_remove_a_player_to_tournament(
                    p_choice, self.tournament)
                self.run_add_remove_player_tournament()

    def run_report(self):
        self.view.clear()
        self.view.current_player_and_tournament(
            self.player, self.tournament, self.current_menu
        )
        self.view.report_main_page()

    def run_report_all_players_alpha(self):
        self.view.clear()
        self.view.current_player_and_tournament(
            self.player, self.tournament, self.current_menu
        )
        players = self.dm.sorted_players_alpha(self.dm.players.values())
        self.view.report_all_players(players)

    def run_report_all_players_rank(self):
        self.view.clear()
        self.view.current_player_and_tournament(
            self.player, self.tournament, self.current_menu
        )
        players = self.dm.sorted_players_rank(self.dm.players.values())
        self.view.report_all_players(players)

    def run_report_players_tournament_alpha(self):
        self.view.clear()
        self.view.current_player_and_tournament(
            self.player, self.tournament, self.current_menu
        )
        if not self.tournament:
            self.view.no_selected_tournament()
            valid_choice = ["C"]
            t_choice = ""
            for tournament in self.dm.tournaments.values():
                valid_choice.append(tournament.ident)
            while t_choice.upper() not in valid_choice:
                self.view.clear()
                self.view.current_player_and_tournament(
                    self.player, self.tournament, self.current_menu
                )
                t_choice = self.view.display_all_tournaments(
                    self.dm.tournaments)
            if t_choice.upper() == "C":
                self.view.clear()
                self.view.current_player_and_tournament(
                    self.player, self.tournament, self.current_menu
                )
            else:
                self.tournament = self.dm.load_tournament(t_choice)
                players = self.dm.sorted_players_alpha(self.tournament.players)
                self.view.clear()
                self.view.current_player_and_tournament(
                    self.player, self.tournament, self.current_menu
                )
                self.view.report_players_in_tournament(
                    players, self.tournament)
        else:
            players = self.dm.sorted_players_alpha(self.tournament.players)
            self.view.report_players_in_tournament(players, self.tournament)

    def run_report_players_tournament_rank(self):
        self.view.clear()
        self.view.current_player_and_tournament(
            self.player, self.tournament, self.current_menu
        )
        if not self.tournament:
            self.view.no_selected_tournament()
            valid_choice = ["C"]
            t_choice = ""
            for tournament in self.dm.tournaments.values():
                valid_choice.append(tournament.ident)
            while t_choice.upper() not in valid_choice:
                self.view.clear()
                self.view.current_player_and_tournament(
                    self.player, self.tournament, self.current_menu
                )
                t_choice = self.view.display_all_tournaments(
                    self.dm.tournaments)
            if t_choice.upper() == "C":
                self.view.clear()
                self.view.current_player_and_tournament(
                    self.player, self.tournament, self.current_menu
                )
            else:
                self.tournament = self.dm.load_tournament(t_choice)
                players = self.dm.sorted_players_rank(self.tournament.players)
                self.view.report_players_in_tournament(
                    players, self.tournament)
        else:
            players = self.dm.sorted_players_rank(self.tournament.players)
            self.view.report_players_in_tournament(players, self.tournament)

    def run_report_all_tournaments(self):
        self.view.clear()
        self.view.current_player_and_tournament(
            self.player, self.tournament, self.current_menu
        )
        tournaments = self.dm.sorted_tournaments_date(
            self.dm.tournaments.values())
        self.view.report_all_tournaments(tournaments)

    def run_report_all_rounds(self):
        self.view.clear()
        self.view.current_player_and_tournament(
            self.player, self.tournament, self.current_menu
        )
        if not self.tournament:
            self.view.no_selected_tournament()
            valid_choice = ["C"]
            t_choice = ""
            for tournament in self.dm.tournaments.values():
                valid_choice.append(tournament.ident)
            while t_choice.upper() not in valid_choice:
                self.view.clear()
                self.view.current_player_and_tournament(
                    self.player, self.tournament, self.current_menu
                )
                t_choice = self.view.display_all_tournaments(
                    self.dm.tournaments)
            if t_choice.upper() == "C":
                self.view.clear()
                self.view.current_player_and_tournament(
                    self.player, self.tournament, self.current_menu
                )
            else:
                self.tournament = self.dm.load_tournament(t_choice)
                self.view.clear()
                self.view.current_player_and_tournament(
                    self.player, self.tournament, self.current_menu
                )
                self.view.report_rounds_in_tournament(self.tournament)
        else:
            self.view.clear()
            self.view.current_player_and_tournament(
                self.player, self.tournament, self.current_menu
            )
            self.view.report_rounds_in_tournament(self.tournament)

    def run_report_all_matchs(self):
        self.view.clear()
        self.view.current_player_and_tournament(
            self.player, self.tournament, self.current_menu
        )
        if not self.tournament:
            self.view.no_selected_tournament()
            valid_choice = ["C"]
            t_choice = ""
            for tournament in self.dm.tournaments.values():
                valid_choice.append(tournament.ident)
            while t_choice.upper() not in valid_choice:
                self.view.clear()
                self.view.current_player_and_tournament(
                    self.player, self.tournament, self.current_menu
                )
                t_choice = self.view.display_all_tournaments(
                    self.dm.tournaments)
            if t_choice.upper() == "C":
                self.view.clear()
                self.view.current_player_and_tournament(
                    self.player, self.tournament, self.current_menu
                )
            else:
                self.tournament = self.dm.load_tournament(t_choice)
                self.view.clear()
                self.view.current_player_and_tournament(
                    self.player, self.tournament, self.current_menu
                )
                self.view.report_matchs_in_tournament(self.tournament)
        else:
            self.view.clear()
            self.view.current_player_and_tournament(
                self.player, self.tournament, self.current_menu
            )
            self.view.report_matchs_in_tournament(self.tournament)
