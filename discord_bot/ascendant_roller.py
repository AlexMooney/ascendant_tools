from random import randint

class AscendantRoller:
    rv_table = {
        -9: [  0,   0,   0,   0, 100],
        -8: [  0,   0,   0,   1, 100],
        -7: [  0,   0,   1,   3, 100],
        -6: [  0,   1,   3,   7, 100],
        -5: [  0,   2,   6,   9, 100],
        -4: [  0,   3,   7,  12, 100],
        -3: [  0,   4,   9,  19, 100],
        -2: [  0,   6,  13,  25, 100],
        -1: [  0,   7,  19,  35, 100],
         0: [  1,  11,  26,  50, 100],
         1: [  2,  13,  33,  67, 100],
         2: [  3,  20,  50,  98, 100],
         3: [  9,  37,  79,  99, 100],
         4: [ 23,  55,  98,  99, 100],
         5: [ 47,  95,  98,  99, 100],
         6: [ 96,  97,  98,  99, 100],
         7: [100, 100, 100, 100, 100]
     }

    color_strings = [
        ':red_square: ' * 8,
        ':orange_square: ' * 4,
        ':yellow_square: ' * 2,
        ':green_square:',
        ':white_large_square:'
    ]

    def roll_attack(self, rv):
        dice = randint(1, 100)
        result = self._chart(dice, rv)
        return f"Attack roll of {dice} with RV {rv}.  Result: {self.color_strings[result]}"

    def roll_chart(self, rv):
        effective_rv = rv*2
        dice = randint(1, 100)
        result = self._chart(dice, effective_rv)
        return f"Challenge roll of {dice} with RV {rv}.  Result: {self.color_strings[result]}"

    def _chart(self, dice, rv):
        rv = max(min(7, rv), -9)
        for index, band in enumerate(self.rv_table[rv]):
            if dice <= band:
                return index
