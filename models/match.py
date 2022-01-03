"""
Gestion de la classe Match
correspondant à une partie entre deux joueurs
"""

import random


class Match:
    def __init__(self):
        """Partie entre deux joueurs"""
        self.data = None  # format = ([player1, score1], [player2, score2])
        self.ident = None

    @staticmethod
    def get_translation(lang):
        if lang == "fr":
            return {
                "data": "Informations sur le match",
                "ident": "Identifiant du match",
            }

    def __repr__(self):
        if self.data[1][0]:
            return (
                f"Match entre {self.data[0][0].firstname} {self.data[0][0].lastname}"
                f" et {self.data[1][0].firstname} {self.data[1][0].lastname}"
            )
        else:
            return f"Joueur flottant : {self.data[0][0].firstname} {self.data[0][0].lastname}"

    def set_new_value(self, param, value):
        self.__setattr__(param, value)

    def set_draw(self):
        self.data[0][1] += 0.5
        self.data[1][1] += 0.5

    def set_victory_1(self):
        self.data[0][1] += 1

    def set_victory_2(self):
        self.data[1][1] += 1

    def random_result(self):
        if not self.data[1][0]:
            print(
                f"Match N° {self.ident} : Le joueur flottant {self.data[0][0]} marque 1 point"
            )
            self.data[0][1] += 1
        else:
            print(f"Match N° {self.ident} : {self.data[0][0]} vs {self.data[1][0]}")
            ecart = abs(self.data[0][0].rank - self.data[1][0].rank)
            maxrank = 1000
            chance_draw = 0.33 - 0.66 * (ecart / (2 * maxrank))
            chance_win = 0.33 + 0.66 * (ecart / maxrank)
            seuil1 = int(1000 * chance_win)
            seuil2 = 1000 - int(1000 * chance_draw)
            result = random.randrange(1, 1000)
            if result <= seuil1:
                print(f"Victoire de {self.data[0][0]} \n")
                self.data[0][1] += 1
            elif result >= seuil2:
                print(f"Victoire de {self.data[1][0]} \n")
                self.data[1][1] += 1
            else:
                print(f"Match nul entre {self.data[0][0]} et {self.data[1][0]} \n")
                self.data[0][1] += 0.5
                self.data[1][1] += 0.5
