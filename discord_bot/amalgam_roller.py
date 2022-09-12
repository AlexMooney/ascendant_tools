from random import randint


class AmalgamRoller:
    rv_table = {
        -31: [0, 0, 0, 0, 100],
        -30: [0, 0, 0, 1, 100],
        -29: [0, 0, 0, 1, 100],
        -28: [0, 0, 0, 1, 100],
        -27: [0, 0, 0, 1, 100],
        -26: [0, 0, 0, 1, 100],
        -25: [0, 0, 0, 1, 100],
        -24: [0, 0, 0, 2, 100],
        -23: [0, 0, 0, 2, 100],
        -22: [0, 0, 0, 2, 100],
        -21: [0, 0, 0, 3, 100],
        -20: [0, 0, 0, 3, 100],
        -19: [0, 0, 1, 3, 100],
        -18: [0, 0, 1, 3, 100],
        -17: [0, 0, 1, 4, 100],
        -16: [0, 0, 2, 4, 100],
        -15: [0, 0, 2, 5, 100],
        -14: [0, 0, 3, 6, 100],
        -13: [0, 0, 3, 8, 100],
        -12: [0, 1, 3, 8, 100],
        -11: [0, 1, 4, 9, 100],
        -10: [0, 1, 6, 10, 100],
        -9: [0, 2, 6, 11, 100],
        -8: [0, 3, 7, 12, 100],
        -7: [0, 3, 8, 16, 100],
        -6: [0, 4, 9, 18, 100],
        -5: [0, 5, 11, 21, 100],
        -4: [0, 6, 13, 25, 100],
        -3: [0, 7, 16, 29, 100],
        -2: [0, 8, 19, 36, 100],
        -1: [0, 10, 21, 43, 100],
        0: [1, 11, 24, 50, 100],
        1: [1, 13, 29, 60, 100],
        2: [2, 15, 34, 69, 100],
        3: [2, 17, 42, 84, 100],
        4: [3, 20, 51, 97, 100],
        5: [5, 27, 66, 98, 100],
        6: [8, 37, 78, 99, 100],
        7: [15, 46, 85, 99, 100],
        8: [24, 57, 91, 99, 100],
        9: [34, 73, 95, 99, 100],
        10: [46, 93, 97, 99, 100],
        11: [70, 97, 99, 100, 100],
        12: [100, 100, 100, 100, 100],
    }

    color_strings = [
        ":red_square: " * 8,
        ":orange_square: " * 4,
        ":yellow_square: " * 2,
        ":green_square:",
        ":white_large_square:",
    ]

    def roll_opposed(self, rv):
        dice = randint(1, 100)
        result = self._chart(dice, rv)
        return f"Opposed roll of {dice} with RV {rv}.  Result: {self.color_strings[result]}"

    def roll_check(self, rv):
        effective_rv = rv * 2
        dice = randint(1, 100)
        result = self._chart(dice, effective_rv)
        return (
            f"Check roll of {dice} with RV {rv}.  Result: {self.color_strings[result]}"
        )

    def _chart(self, dice, rv):
        rv = max(min(12, rv), -31)
        for index, band in enumerate(self.rv_table[rv]):
            if dice <= band:
                return index
