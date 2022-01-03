import os
import datetime
from dateutil import parser


class View:
    def __init__(self):
        pass

    def home(self, player, tournament, menu):
        os.system("cls" if os.name == "nt" else "clear")
        print("*** Chess Manager : gestionnaire de tournois d'échecs ***\n")
        self.current_player_and_tournament(player, tournament, menu)

    @staticmethod
    def press_key():
        input("\nPressez une touche pour continuer\n")

    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def current_player_and_tournament(player, tournament, menu):
        print(menu)
        print(f"Joueur actuel : {'aucun' if not player else player}")
        print(f"Tournoi actuel : {'aucun' if not tournament else tournament}")
        print()

    @staticmethod
    def load_or_create_tournament():
        os.system("cls" if os.name == "nt" else "clear")
        print("Voulez-vous charger un tournoi existant [L]")
        print("Créer un nouveau tournoi                [C]")
        print("Revenir à l'accueil                     [H]")
        print("Quitter                                 [Q]")
        return input("-->  ")

    @staticmethod
    def display_all_players(players, tournament=None):
        if not tournament:
            t_players = []
        else:
            t_players = tournament.sort_players(tournament.players)
        print(f"Liste des joueurs existants\n")
        print(f"{'Nom':<12}{'Prénom':<10}{'Classement':<20}{'DN':<15}\n")
        for player in players.values():
            print(f"{player}", end="")
            if player not in t_players:
                print(f"[{player.ident}]")
            else:
                print()
        if tournament:
            print(f"\nJoueurs participant au tournoi {tournament.name} :\n")
            for player in tournament.players:
                print(f"{player} [{player.ident}]")
        print(
            "\nSaisissez le numéro du joueur à sélectionner [x] \n"
            "ou tapez [Y] pour passer à la suite"
        )
        return input("-->  ")

    @staticmethod
    def display_add_remove_players_tournament(players, tournament=None):
        if not tournament:
            t_players = []
        else:
            t_players = tournament.sort_players(tournament.players)
        print(f"Liste des joueurs existants\n")
        print(f"{'Nom':<12}{'Prénom':<10}{'Classement':<20}{'DN':<15}\n")
        for player in players.values():
            print(f"{player}", end="")
            if player not in t_players:
                print(f"[{player.ident}]")
            else:
                print()
        if tournament:
            print(f"\nJoueurs participant au tournoi {tournament.name} :\n")
            for player in tournament.players:
                print(f"{player} [{player.ident}]")
            print("\nSaisissez le numéro du joueur à ajouter/retirer au tournoi [x]")
            print("Tapez [C] pour retirer tous les joueurs du tournoi")
            print("Tapez [Y] pour valider et passer à la suite")

        else:
            print("\nAucun tournoi sélectionné \n")
        return input("-->  ")

    @staticmethod
    def display_all_tournaments(tournaments):
        print(f"Liste des tournois existants\n")
        print(f"{'Nom':<30}{'Ville':<20}{'Pays':<22}{'Début':<20}{'Statut'}\n")
        for tournament in tournaments.values():
            print(f"{tournament} [{tournament.ident}]")
        print("\nSaisissez le numéro du tournoi sélectionné")
        print("Tapez [C] si vous ne souhaitez pas sélectionner un tournoi")
        return input("-->  ")

    @staticmethod
    def display_editing_tournament(tournament, choices):
        for choice in choices.items():
            if isinstance(tournament.__getattribute__(choice[1]), datetime.datetime):
                print(
                    f"{tournament.get_translation_fr(choice[1]):<20}"
                    f"{tournament.__getattribute__(choice[1]).strftime('%Y-%m-%d'):<25} [{choice[0]}]"
                )
            else:
                print(
                    f"{tournament.get_translation_fr(choice[1]):<20}"
                    f"{tournament.__getattribute__(choice[1]):<25} [{choice[0]}]"
                )
        print("\nSaisissez le nombre [x] correspondant à la donnée à modifier")
        print("Tapez [N] pour quitter l'éditeur de tournoi")
        return input("-->  ")

    @staticmethod
    def display_editing_player(player, choices):
        for choice in choices.items():
            if isinstance(player.__getattribute__(choice[1]), datetime.datetime):
                print(
                    f"{player.get_translation_fr(choice[1]):<20}"
                    f"{player.__getattribute__(choice[1]).strftime('%Y-%m-%d'):<25} [{choice[0]}]"
                )
            else:
                print(
                    f"{player.get_translation_fr(choice[1]):<20}"
                    f"{player.__getattribute__(choice[1]):<25} [{choice[0]}]"
                )
        print("\nSaisissez le nombre [x] correspondant à la donnée à modifier")
        print("Tapez [N] pour quitter l'éditeur de joueur")
        return input("-->  ")

    def show_players_in_tournament(self, tournament, text=""):
        if tournament:
            print(f"Classement des joueurs du tournoi {tournament.name} {text}\n")
            if not tournament.players:
                self.no_player_in_tournament(tournament)
            else:
                print(
                    f"{'Nom':<12}{'Prénom':<10}{'Classement':<20}{'DN':<15}{'Score':<10}\n"
                )
                tournament.players = tournament.sort_players(tournament.players)
                for player in tournament.players:
                    if tournament.rounds:
                        print(
                            f"{player}{tournament.rounds[-1].scores[player.ident]:<10}"
                        )
                    else:
                        print(f"{player}{'0.0':<10}")
            print()

    @staticmethod
    def no_player_in_tournament(tournament):
        print(
            f"Il n'y a actuellement aucun participant pour le tournoi {tournament.name}.\n"
        )

    def not_enought_players_in_tournament(self, tournament):
        print(f"Il faut au moins 2 joueurs pour débuter le tournoi {tournament.name}")
        self.press_key()

    @staticmethod
    def load_or_create_player():
        os.system("cls" if os.name == "nt" else "clear")
        print("Voulez-vous charger un joueur existant [L]")
        print("Créer un nouveau joueur                [C]")
        print("Revenir à l'accueil                    [H]")
        print("Quitter                                [Q]")
        return input("-->  ")

    @staticmethod
    def add_another_player():
        return input("Voulez-vous ajouter d'autres joueurs au tournoi ([Y]/[N]) ?")

    @staticmethod
    def valid_or_cancel():
        up = "\033[1A"
        clrline = "\033[2K" + up

        def inline_input(msg):
            user_input = input(msg)
            print(up + clrline)
            return user_input

        return inline_input("Validation [Y]/[N] ?").upper()

    @staticmethod
    def resume_or_back_home():
        up = "\033[1A"
        clrline = "\033[2K" + up

        def inline_input(msg):
            user_input = input(msg)
            print(up + clrline)
            return user_input

        return inline_input("Poursuivre [Y] ou revenir à l'accueil [N] ?").upper()

    @staticmethod
    def show_matchs_of_the_round(tournament):
        os.system("cls" if os.name == "nt" else "clear")
        print(
            f"Matchs de la ronde : {len(tournament.rounds):<15} Début de la ronde : "
            f"{tournament.rounds[-1].start.strftime('%Y-%m-%d  %H:%M:%S')}\n"
        )
        for match in tournament.rounds[-1].matchs:
            if not match.data[1][0]:
                print(
                    f"\nMatch N° {match.ident[2]}{':':<10} {match.data[0][0]}"
                    f"  {tournament.rounds[-1].scores[match.data[0][0].ident]:<10}Joueur flottant"
                )
            else:
                print(
                    f"Match N° {match.ident[2]}{':':<10} {match.data[0][0]} "
                    f" {tournament.rounds[-1].scores[match.data[0][0].ident]:<10}{'vs':<10} {match.data[1][0]} "
                    f" {tournament.rounds[-1].scores[match.data[1][0].ident]:<10}",
                    end="",
                )
                if match.data[0][1] == 0 and match.data[1][1] == 0:
                    print(f"[{match.ident[2]}]")
                else:
                    print("")

        print("\nSaisissez le numéro du match pour entrer les résultats")
        print("Tapez [Y] pour valider ces résultats et passer à la suite")
        print("Tapez [N] pour revenir à l'accueil")
        return input("-->  ")

    @staticmethod
    def result_of_a_match(match):
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Résultat du {match}\n")
        print(
            f"Victoire de            : {match.data[0][0].firstname:>15}"
            f" {match.data[0][0].lastname:<15}  {'[':>10}{match.data[0][0].ident}]"
        )
        print(
            f"Victoire de            : {match.data[1][0].firstname:>15}"
            f" {match.data[1][0].lastname:<15}  {'[':>10}{match.data[1][0].ident}]"
        )
        print(f"Match nul              : {'[N]':>45}")
        print(f"Revenir aux matchs     : {'[C]':>45}")
        return input("--> ")

    def some_results_missing(self, tournament):
        print(
            f"Vous n'avez pas entré tous les résultats de la ronde {len(tournament.rounds)}"
        )
        print(f"Veuillez compléter vos saisies avant de lancer le tour suivant")
        self.press_key()

    @staticmethod
    def get_data_new_tournament():
        data = {
            "Nom": "Masterchess",
            "Ville": "New York",
            "Pays": "USA",
            "Date de début": datetime.datetime.today(),
            "Date de fin": datetime.datetime.today(),
            "Nombre de rondes": 4,
            "Type de partie": "rapid",
            "Système": "swiss",
            "Commentaires": "",
        }
        print("Veuillez saisir les informations du nouveau tournoi :")
        for item in data.items():
            if item[0] in ["Date de début", "Date de fin"]:
                date = input(f"{item[0]} : YYYY/mm/dd --> ")
                if date == "":
                    entry = item[1]
                else:
                    entry = parser.parse(date)
                data[item[0]] = entry
            else:
                entry = input(f"{item[0]} : {item[1]} --> ")
            if entry == "":
                pass
            else:
                data[item[0]] = entry
        return data

    @staticmethod
    def get_data_new_player():
        data = {
            "Nom": "Player",
            "Prénom": "x",
            "Classement": 1000,
            "Date de naissance": datetime.date.today(),
            "Sexe": "",
        }
        print("Veuillez saisir les informations du nouveau joueur :")
        for item in data.items():
            if item[0] in ["Date de naissance"]:
                date = input(f"{item[0]} : YYYY/mm/dd --> ")
                if date == "":
                    entry = item[1]
                else:
                    entry = parser.parse(date)
                data[item[0]] = entry
            else:
                entry = input(f"{item[0]} : {item[1]} --> ")
            if entry == "":
                pass
            else:
                data[item[0]] = entry
        return data

    def alert_creating_an_existing_tournament(self, name, town, country, date):
        print(
            f"ATTENTION ! Il existe déjà un tournoi {name} de {town} ({country})"
            f" et qui commence le {date} dans la base de données"
        )
        print("Veuillez modifier vos saisies pour distinguer les deux tournois")
        self.press_key()

    def alert_creating_an_existing_player(self, lastname, firstname, dob):
        print(
            f"ATTENTION ! Il existe déjà un joueur {firstname} {lastname}"
            f" né le {dob.strftime('%Y-%m-%d')} dans la base de données"
        )
        print("Veuillez modifier vos saisies pour distinguer les deux joueurs")
        self.press_key()

    def alert_tournament_permanently_delete(self, tournament):
        print(f"ATTENTION !! Le tournoi {tournament} sera définitivement supprimé")
        self.press_key()

    def alert_player_permanently_delete(self, player):
        print(f"ATTENTION !! Le joueur {player} sera définitivement supprimé")
        self.press_key()

    @staticmethod
    def tournament_ended(tournament):
        print(f"Le tournoi {tournament.name} est terminé.")

    @staticmethod
    def tournament_in_progress(tournament):
        print(f"Le tournoi {tournament.name} a déjà débuté.")

    def add_remove_player_tournament_disabled(self):
        print(f"Il n'est pas possible de modifier la liste des joueurs y participant.")
        self.press_key()

    def no_selected_tournament(self):
        print("Aucun tournoi sélectionné")
        self.press_key()

    def no_selected_player(self):
        print("Aucun joueur sélectionné")
        self.press_key()

    def not_swiss_system(self):
        print("L'application ne gère pas encore les tournois de sytème non suisse")
        self.press_key()

    @staticmethod
    def swiss_final_results(tournament):
        os.system("cls" if os.name == "nt" else "clear")
        print("Fin du tournoi")
        print("Score des joueurs du tournoi ")
        print(f"{'Nom':<10} {'Prénom':<15} {'Classement':<15} {'Score':<5}")
        for player in tournament.players:
            print(
                f"{player.lastname:<10} {player.firstname:<15} {player.rank:<15}"
                f" {tournament.rounds[-1].scores[player.ident]:<5}"
            )
        print(
            f"\n***** Victoire de {tournament.players[0].firstname} {tournament.players[0].lastname} *****\n"
        )
        print("Pressez une touche pour revenir à l'accueil")
        return input("--> ")

    @staticmethod
    def new_value_for_data(param, olddata):
        os.system("cls" if os.name == "nt" else "clear")
        print(
            f"Saisissez la nouvelle valeur de {param} en remplacement de {olddata} \n"
            f"[B] pour revenir à la liste des paramètres\n"
        )
        return input("-->  ")

    @staticmethod
    def confirm_new_value(olddata, newdata):
        return input(
            f"Veuillez confirmer que vous remplacez {olddata} par {newdata} : [Y] pour valider la modification : "
        )

    def modification_validated(self):
        print("La modification est validée")
        self.press_key()

    def modification_cancelled(self):
        print("La modification est annulée")
        self.press_key()

    @staticmethod
    def report_main_page():
        print("Saisissez le numéro du rapport que vous souhaitez afficher\n")

    @staticmethod
    def report_all_players(players):
        print(f"{'Nom':<12}{'Prénom':<10}{'Classement':<20}{'DN':<15}\n")
        for player in players:
            print(player)
        print()

    @staticmethod
    def report_all_tournaments(tournaments):
        print(f"{'Nom':<30}{'Ville':<20}{'Pays':<22}{'Début':<20}{'Statut'}\n")
        for tournament in tournaments:
            print(tournament)
        print()

    @staticmethod
    def report_players_in_tournament(players, tournament):
        print(f"Liste des participants au tournoi {tournament}\n")
        print(f"{'Nom':<12}{'Prénom':<10}{'Classement':<20}{'DN':<15}\n")
        for player in players:
            print(player)
        print()

    @staticmethod
    def report_rounds_in_tournament(tournament):
        for t_round in tournament.rounds:
            if isinstance(t_round.start, datetime.datetime):
                t_round.start = t_round.start.strftime("%Y-%m-%d %H:%M:%S")
            else:
                t_round.start = ""
            if isinstance(t_round.end, datetime.datetime):
                t_round.end = t_round.end.strftime("%Y-%m-%d  %H:%M:%S")
            else:
                t_round.end = ""
            print(
                f"Ronde N° {tournament.rounds.index(t_round)+1:<10} "
                f"Début: {t_round.start:<20} Fin: {t_round.end:<10}"
            )
            for match in t_round.matchs:
                if match.data[1][0]:
                    print(
                        f"Match N° {match.ident[2]}{':':<10}{match.data[0][0]}"
                        f"  {match.data[0][1]:<10}{'vs':<10} {match.data[1][0]}  {match.data[1][1]:<10}"
                    )
                else:
                    print(
                        f"Match N° {match.ident[2]}{':':<10}{match.data[0][0]}  {match.data[0][1]:<10}"
                    )
            print()

    @staticmethod
    def report_matchs_in_tournament(tournament):
        for t_round in tournament.rounds:
            for match in t_round.matchs:
                if match.data[1][0]:
                    print(
                        f"Match N° {match.ident[2]}{':':<10}{match.data[0][0]}"
                        f"  {match.data[0][1]:<10}{'vs':<10} {match.data[1][0]}  {match.data[1][1]:<10}"
                    )
                else:
                    print(
                        f"Match N° {match.ident[2]}{':':<10}{match.data[0][0]}  {match.data[0][1]:<10}"
                    )
            print()
