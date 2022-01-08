"""
Create all menus of the script
"""

list_menus = [
    ("home", "menu_home(menus, menus['home'])"),
    ("tournament",
     "menu_tournament(menus, menus['tournament'], menus['home'])"),
    ("player", "menu_player(menus, menus['player'], menus['home'])"),
    ("report", "menu_report(menus, menus['report'], menus['home'])"),
    (
        "all_players_alpha",
        "menu_report_all_players_alpha(menus, menus['all_players_alpha'],"
        " menus['report'])",
    ),
    (
        "all_players_rank",
        "menu_report_all_players_rank(menus, menus['all_players_rank'],"
        " menus['report'])",
    ),
    (
        "players_tournament_alpha",
        "menu_report_players_tournament_alpha(menus,"
        " menus['players_tournament_alpha'], menus['report'])",
    ),
    (
        "players_tournament_rank",
        "menu_report_players_tournament_rank(menus,"
        " menus['players_tournament_rank'], menus['report'])",
    ),
    (
        "all_tournaments",
        "menu_report_all_tournaments(menus,"
        " menus['all_tournaments'], menus['report'])",
    ),
    (
        "all_rounds",
        "menu_report_all_rounds(menus,"
        " menus['all_rounds'], menus['report'])",
    ),
    (
        "all_matchs",
        "menu_report_all_matchs(menus,"
        " menus['all_matchs'], menus['report'])",
    ),
    (
        "create_tournament",
        "menu_create_tournament(menus,"
        " menus['create_tournament'], menus['tournament'])",
    ),
    (
        "load_tournament",
        "menu_load_tournament(menus,"
        " menus['load_tournament'], menus['tournament'])",
    ),
    (
        "edit_tournament",
        "menu_edit_tournament(menus,"
        " menus['edit_tournament'], menus['tournament'])",
    ),
    (
        "delete_tournament",
        "menu_delete_tournament(menus,"
        " menus['delete_tournament'], menus['tournament'])",
    ),
    (
        "start_tournament",
        "menu_start_tournament(menus,"
        " menus['start_tournament'], menus['tournament'])",
    ),
    (
        "add_remove_player_tournament",
        "menu_add_remove_player_tournament(menus,"
        " menus['add_remove_player_tournament'], menus['tournament'])",
    ),
    (
        "create_player",
        "menu_create_player(menus, menus['create_player'], menus['player'])",
    ),
    ("load_player", "menu_load_player(menus,"
                    " menus['load_player'], menus['player'])"),
    ("edit_player", "menu_edit_player(menus,"
                    " menus['edit_player'], menus['player'])"),
    (
        "delete_player",
        "menu_delete_player(menus,"
        " menus['delete_player'], menus['player'])",
    ),
]


class Menu:
    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent
        self.path = str()
        self.choices = list()
        self.run = None

    def set_path(self):
        if self.parent:
            self.path = self.parent.path + "/" + self.name
        else:
            self.path = "/" + self.name

    def __repr__(self):
        return f"Menu   :{self.name} --- {self.path}\n"


def get_menus(menus):
    for menu in list_menus:
        menus.update({menu[0]: Menu()})
    for menu in list_menus:
        eval(menu[1])
    return menus


def menu_home(menus, menu):
    menu.name = "Accueil"
    menu.set_path()
    menu.choices = {
        "T": ("Menu Tournoi  [T]", menus["tournament"]),
        "P": ("Menu Joueur   [P]", menus["player"]),
        "R": ("Menu Rapports [R]", menus["report"]),
        "Q": ("Quitter       [Q]", "quit"),
    }
    menu.run = "self.run_home()"
    return menu


def menu_tournament(menus, menu, parent):
    menu.name = "tournoi"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "C": (f"{'Créer un nouveau tournoi':<45}[C]",
              menus["create_tournament"]),
        "L": (f"{'Charger un tournoi existant':<45}[L]",
              menus["load_tournament"]),
        "E": (f"{'Editer le tournoi sélectionné':<45}[E]",
              menus["edit_tournament"]),
        "D": (
            f"{'Supprimer le tournoi sélectionné':<45}[D]",
            menus["delete_tournament"],
        ),
        "S": (f"{'Gérer le tournoi':<45}[S]",
              menus["start_tournament"]),
        "A": (
            f"{'Ajouter ou retirer un joueur au tournoi':<45}[A]",
            menus["add_remove_player_tournament"],
        ),
        "H": (f"{'Menu accueil':<45}[H]", menus["home"]),
        "Q": (f"{'Quitter':<45}[Q]", "quit"),
    }
    menu.run = "self.run_tournament()"
    return menu


def menu_load_tournament(menus, menu, parent):
    menu.name = "charger un tournoi"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "S": (f"{'Gérer le tournoi':<45}[S]",
              menus["start_tournament"]),
        "E": (f"{'Editer le tournoi sélectionné':<45}[E]",
              menus["edit_tournament"]),
        "D": (
            f"{'Supprimer le tournoi sélectionné':<45}[D]",
            menus["delete_tournament"],
        ),
        "L": (f"{'Charger un tournoi existant':<45}[L]",
              menus["load_tournament"]),
        "C": (f"{'Créer un nouveau tournoi':<45}[C]",
              menus["create_tournament"]),
        "P": (f"{'Menu joueur':<45}[P]", menus["player"]),
        "A": (
            f"{'Ajouter ou retirer un joueur au tournoi':<45}[A]",
            menus["add_remove_player_tournament"],
        ),
        "H": (f"{'Menu accueil':<45}[H]", menus["home"]),
        "Q": (f"{'Quitter':<45}[Q]", "quit"),
    }
    menu.run = "self.run_load_tournament()"
    return menu


def menu_create_tournament(menus, menu, parent):
    menu.name = "créer un tournoi"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "S": (f"{'Gérer le tournoi':<45}[S]", menus["start_tournament"]),
        "A": (
            f"{'Ajouter ou retirer un joueur au tournoi':<45}[A]",
            menus["add_remove_player_tournament"],
        ),
        "P": (f"{'Menu joueur':<45}[P]", menus["player"]),
        "T": (f"{'Menu tournoi':<45}[T]", menus["tournament"]),
        "H": (f"{'Menu accueil':<45}[H]", menus["home"]),
        "Q": (f"{'Quitter':<45}[Q]", "quit"),
    }
    menu.run = "self.run_create_tournament()"
    return menu


def menu_edit_tournament(menus, menu, parent):
    menu.name = "éditer un tournoi"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "A": (
            f"{'Ajouter ou retirer un joueur au tournoi':<45}[A]",
            menus["add_remove_player_tournament"],
        ),
        "P": (f"{'Menu joueur':<45}[P]", menus["player"]),
        "T": (f"{'Menu tournoi':<45}[T]", menus["tournament"]),
        "H": (f"{'Menu accueil':<45}[H]", menus["home"]),
        "Q": (f"{'Quitter':<45}[Q]", "quit"),
    }
    menu.run = "self.run_edit_tournament()"
    return menu


def menu_delete_tournament(menus, menu, parent):
    menu.name = "supprimer un tournoi"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "P": (f"{'Menu joueur':<45}[P]", menus["player"]),
        "T": (f"{'Menu tournoi':<45}[T]", menus["tournament"]),
        "H": (f"{'Menu accueil':<45}[H]", menus["home"]),
        "Q": (f"{'Quitter':<45}[Q]", "quit"),
    }
    menu.run = "self.run_delete_tournament()"
    return menu


def menu_start_tournament(menus, menu, parent):
    menu.name = "gérer un tournoi"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "T": (f"{'Menu tournoi':<45}[T]", menus["tournament"]),
        "P": (f"{'Menu joueur':<45}[P]", menus["player"]),
        "A": (
            f"{'Ajouter ou retirer un joueur au tournoi':<45}[A]",
            menus["add_remove_player_tournament"],
        ),
        "H": (f"{'Menu accueil':<45}[H]", menus["home"]),
        "Q": (f"{'Quitter':<45}[Q]", "quit"),
    }
    menu.run = "self.run_start_tournament()"
    return menu


def menu_player(menus, menu, parent):
    menu.name = "joueur"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "C": (f"{'Créer un nouveau joueur':<45}[C]",
              menus["create_player"]),
        "L": (f"{'Charger un joueur existant':<45}[L]",
              menus["load_player"]),
        "E": (f"{'Editer le joueur sélectionné':<45}[E]",
              menus["edit_player"]),
        "D": (f"{'Supprimer le joueur sélectionné':<45}[D]",
              menus["delete_player"]),
        "A": (
            f"{'Ajouter ou retirer un joueur au tournoi':<45}[A]",
            menus["add_remove_player_tournament"],
        ),
        "T": (f"{'Menu tournoi':<45}[T]",
              menus["tournament"]),
        "S": (f"{'Gérer le tournoi':<45}[S]",
              menus["start_tournament"]),
        "H": (f"{'Menu accueil':<45}[H]",
              menus["home"]),
        "Q": (f"{'Quitter':<45}[Q]", "quit"),
    }
    menu.run = "self.run_player()"
    return menu


def menu_load_player(menus, menu, parent):
    menu.name = "charger un joueur"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "A": (
            f"{'Ajouter ou retirer un joueur au tournoi':<45}[A]",
            menus["add_remove_player_tournament"],
        ),
        "E": (f"{'Editer le joueur sélectionné':<45}[E]",
              menus["edit_player"]),
        "D": (f"{'Supprimer le joueur sélectionné':<45}[D]",
              menus["delete_player"]),
        "T": (f"{'Menu tournoi':<45}[T]", menus["tournament"]),
        "P": (f"{'Menu joueur':<45}[P]", menus["player"]),
        "H": (f"{'Menu accueil':<45}[H]", menus["home"]),
        "Q": (f"{'Quitter':<45}[Q]", "quit"),
    }
    menu.run = "self.run_load_player()"
    return menu


def menu_create_player(menus, menu, parent):
    menu.name = "créer un joueur"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "A": (
            f"{'Ajouter ou retirer un joueur au tournoi':<45}[A]",
            menus["add_remove_player_tournament"],
        ),
        "P": (f"{'Menu joueur':<45}[P]", menus["player"]),
        "T": (f"{'Menu tournoi':<45}[T]", menus["tournament"]),
        "H": (f"{'Menu accueil':<45}[H]", menus["home"]),
        "Q": (f"{'Quitter':<45}[Q]", "quit"),
    }
    menu.run = "self.run_create_player()"
    return menu


def menu_edit_player(menus, menu, parent):
    menu.name = "éditer un joueur"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "A": (
            f"{'Ajouter ou retirer un joueur au tournoi':<45}[A]",
            menus["add_remove_player_tournament"],
        ),
        "P": (f"{'Menu joueur':<45}[P]", menus["player"]),
        "T": (f"{'Menu tournoi':<45}[T]", menus["tournament"]),
        "H": (f"{'Menu accueil':<45}[H]", menus["home"]),
        "Q": (f"{'Quitter':<45}[Q]", "quit"),
    }
    menu.run = "self.run_edit_player()"
    return menu


def menu_delete_player(menus, menu, parent):
    menu.name = "supprimer un joueur"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "P": (f"{'Menu joueur':<45}[P]", menus["player"]),
        "T": (f"{'Menu tournoi':<45}[T]", menus["tournament"]),
        "H": (f"{'Menu accueil':<45}[H]", menus["home"]),
        "Q": (f"{'Quitter':<45}[Q]", "quit"),
    }
    menu.run = "self.run_delete_player()"
    return menu


def menu_add_remove_player_tournament(menus, menu, parent):
    menu.name = "ajouter-retirer un joueur au tournoi"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "S": (f"{'Gérer le tournoi':<45}[S]", menus["start_tournament"]),
        "P": (f"{'Menu joueur':<45}[P]", menus["player"]),
        "T": (f"{'Menu tournoi':<45}[T]", menus["tournament"]),
        "H": (f"{'Menu accueil':<45}[H]", menus["home"]),
        "Q": (f"{'Quitter':<45}[Q]", "quit"),
    }
    menu.run = "self.run_add_remove_player_tournament()"
    return menu


def menu_report(menus, menu, parent):
    menu.name = "rapports"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "1": (
            f"{'Afficher tous les joueurs par ordre alphabétique':<55}[1]",
            menus["all_players_alpha"],
        ),
        "2": (
            f"{'Afficher tous les joueurs par classement':<55}[2]",
            menus["all_players_rank"],
        ),
        "3": (
            f"{'Afficher les joueurs du tournoi par ordre alphabétique':<55}"
            f"[3]",
            menus["players_tournament_alpha"],
        ),
        "4": (
            f"{'Afficher les joueurs du tournoi par classement':<55}[4]",
            menus["players_tournament_rank"],
        ),
        "5": (
            f"{'Afficher la liste de tous les tournois':<55}[5]",
            menus["all_tournaments"],
        ),
        "6": (f"{'Afficher toutes les rondes du tournoi':<55}[6]",
              menus["all_rounds"]),
        "7": (f"{'Afficher tous les matchs du tournoi':<55}[7]",
              menus["all_matchs"]),
        "H": (f"{'Menu accueil':<55}[H]", menus["home"]),
        "Q": (f"{'Quitter':<55}[Q]", "quit"),
    }
    menu.run = "self.run_report()"
    return menu


def menu_report_all_players_alpha(menus, menu, parent):
    menu.name = "tous les joueurs par ordre alphabétique"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "2": (
            f"{'Afficher tous les joueurs par classement':<55}[2]",
            menus["all_players_rank"],
        ),
        "3": (
            f"{'Afficher les joueurs du tournoi par ordre alphabétique':<55}"
            f"[3]",
            menus["players_tournament_alpha"],
        ),
        "4": (
            f"{'Afficher les joueurs du tournoi par classement':<55}[4]",
            menus["players_tournament_rank"],
        ),
        "5": (
            f"{'Afficher la liste de tous les tournois':<55}[5]",
            menus["all_tournaments"],
        ),
        "6": (f"{'Afficher toutes les rondes du tournoi':<55}[6]",
              menus["all_rounds"]),
        "7": (f"{'Afficher tous les matchs du tournoi':<55}[7]",
              menus["all_matchs"]),
        "H": (f"{'Menu accueil':<55}[H]", menus["home"]),
        "Q": (f"{'Quitter':<55}[Q]", "quit"),
    }
    menu.run = "self.run_report_all_players_alpha()"
    return menu


def menu_report_all_players_rank(menus, menu, parent):
    menu.name = "tous les joueurs par classement"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "1": (
            f"{'Afficher tous les joueurs par ordre alphabétique':<55}[1]",
            menus["all_players_alpha"],
        ),
        "3": (
            f"{'Afficher les joueurs du tournoi par ordre alphabétique':<55}"
            f"[3]",
            menus["players_tournament_alpha"],
        ),
        "4": (
            f"{'Afficher les joueurs du tournoi par classement':<55}[4]",
            menus["players_tournament_rank"],
        ),
        "5": (
            f"{'Afficher la liste de tous les tournois':<55}[5]",
            menus["all_tournaments"],
        ),
        "6": (f"{'Afficher toutes les rondes du tournoi':<55}[6]",
              menus["all_rounds"]),
        "7": (f"{'Afficher tous les matchs du tournoi':<55}[7]",
              menus["all_matchs"]),
        "H": (f"{'Menu accueil':<55}[H]", menus["home"]),
        "Q": (f"{'Quitter':<55}[Q]", "quit"),
    }
    menu.run = "self.run_report_all_players_rank()"
    return menu


def menu_report_players_tournament_alpha(menus, menu, parent):
    menu.name = "tous les joueurs du tournoi par ordre alphabétique"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "1": (
            f"{'Afficher tous les joueurs par ordre alphabétique':<55}[1]",
            menus["all_players_alpha"],
        ),
        "2": (
            f"{'Afficher tous les joueurs par classement':<55}[2]",
            menus["all_players_rank"],
        ),
        "3": (
            f"{'Afficher les joueurs du tournoi par ordre alphabétique':<55}"
            f"[3]",
            menus["players_tournament_alpha"],
        ),
        "4": (
            f"{'Afficher les joueurs du tournoi par classement':<55}[4]",
            menus["players_tournament_rank"],
        ),
        "5": (
            f"{'Afficher la liste de tous les tournois':<55}[5]",
            menus["all_tournaments"],
        ),
        "6": (f"{'Afficher toutes les rondes du tournoi':<55}[6]",
              menus["all_rounds"]),
        "7": (f"{'Afficher tous les matchs du tournoi':<55}[7]",
              menus["all_matchs"]),
        "H": (f"{'Menu accueil':<55}[H]", menus["home"]),
        "Q": (f"{'Quitter':<55}[Q]", "quit"),
    }
    menu.run = "self.run_report_players_tournament_alpha()"
    return menu


def menu_report_players_tournament_rank(menus, menu, parent):
    menu.name = "tous les joueurs du tournoi par classement"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "1": (
            f"{'Afficher tous les joueurs par ordre alphabétique':<55}[1]",
            menus["all_players_alpha"],
        ),
        "2": (
            f"{'Afficher tous les joueurs par classement':<55}[2]",
            menus["all_players_rank"],
        ),
        "3": (
            f"{'Afficher les joueurs du tournoi par ordre alphabétique':<55}"
            f"[3]",
            menus["players_tournament_alpha"],
        ),
        "5": (
            f"{'Afficher la liste de tous les tournois':<55}[5]",
            menus["all_tournaments"],
        ),
        "6": (f"{'Afficher toutes les rondes du tournoi':<55}[6]",
              menus["all_rounds"]),
        "7": (f"{'Afficher tous les matchs du tournoi':<55}[7]",
              menus["all_matchs"]),
        "H": (f"{'Menu accueil':<55}[H]", menus["home"]),
        "Q": (f"{'Quitter':<55}[Q]", "quit"),
    }
    menu.run = "self.run_report_players_tournament_rank()"
    return menu


def menu_report_all_tournaments(menus, menu, parent):
    menu.name = "tous les tournois"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "1": (
            f"{'Afficher tous les joueurs par ordre alphabétique':<55}[1]",
            menus["all_players_alpha"],
        ),
        "2": (
            f"{'Afficher tous les joueurs par classement':<55}[2]",
            menus["all_players_rank"],
        ),
        "3": (
            f"{'Afficher les joueurs du tournoi par ordre alphabétique':<55}"
            f"[3]",
            menus["players_tournament_alpha"],
        ),
        "4": (
            f"{'Afficher les joueurs du tournoi par classement':<55}[4]",
            menus["players_tournament_rank"],
        ),
        "6": (f"{'Afficher toutes les rondes du tournoi':<55}[6]",
              menus["all_rounds"]),
        "7": (f"{'Afficher tous les matchs du tournoi':<55}[7]",
              menus["all_matchs"]),
        "H": (f"{'Menu accueil':<55}[H]", menus["home"]),
        "Q": (f"{'Quitter':<55}[Q]", "quit"),
    }
    menu.run = "self.run_report_all_tournaments()"
    return menu


def menu_report_all_rounds(menus, menu, parent):
    menu.name = "toutes les rondes d'un tournoi"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "1": (
            f"{'Afficher tous les joueurs par ordre alphabétique':<55}[1]",
            menus["all_players_alpha"],
        ),
        "2": (
            f"{'Afficher tous les joueurs par classement':<55}[2]",
            menus["all_players_rank"],
        ),
        "3": (
            f"{'Afficher les joueurs du tournoi par ordre alphabétique':<55}"
            f"[3]",
            menus["players_tournament_alpha"],
        ),
        "4": (
            f"{'Afficher les joueurs du tournoi par classement':<55}[4]",
            menus["players_tournament_rank"],
        ),
        "5": (
            f"{'Afficher la liste de tous les tournois':<55}[5]",
            menus["all_tournaments"],
        ),
        "7": (f"{'Afficher tous les matchs du tournoi':<55}[7]",
              menus["all_matchs"]),
        "H": (f"{'Menu accueil':<55}[H]", menus["home"]),
        "Q": (f"{'Quitter':<55}[Q]", "quit"),
    }
    menu.run = "self.run_report_all_rounds()"
    return menu


def menu_report_all_matchs(menus, menu, parent):
    menu.name = "tous les matchs d'un tournoi"
    menu.parent = parent
    menu.set_path()
    menu.choices = {
        "1": (
            f"{'Afficher tous les joueurs par ordre alphabétique':<55}[1]",
            menus["all_players_alpha"],
        ),
        "2": (
            f"{'Afficher tous les joueurs par classement':<55}[2]",
            menus["all_players_rank"],
        ),
        "3": (
            f"{'Afficher les joueurs du tournoi par ordre alphabétique':<55}"
            f"[3]",
            menus["players_tournament_alpha"],
        ),
        "4": (
            f"{'Afficher les joueurs du tournoi par classement':<55}[4]",
            menus["players_tournament_rank"],
        ),
        "5": (
            f"{'Afficher la liste de tous les tournois':<55}[5]",
            menus["all_tournaments"],
        ),
        "6": (f"{'Afficher toutes les rondes du tournoi':<55}[6]",
              menus["all_rounds"]),
        "H": (f"{'Menu accueil':<55}[H]", menus["home"]),
        "Q": (f"{'Quitter':<55}[Q]", "quit"),
    }
    menu.run = "self.run_report_all_matchs()"
    return menu
