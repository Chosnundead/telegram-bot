import re


class Game:
    """
    1. create class obj:
    game = Game()


    2. use method start:
    game.start()
    """

    field = [[str(i + 3 * j) for i in range(1, 4)] for j in range(3)]

    def __init__(self):
        pass

    def show_field(self):
        print("-" * 9)
        for arr in self.field:
            for item in arr:
                print(f"|{item}|", end="")
            print("\n{}".format("-" * 9))
        pass

    def check(self):
        string = ""
        # row check
        for i in range(3):
            for j in range(3):
                string += self.field[i][j]
            if string == "OOO":
                return "O"
            elif string == "XXX":
                return "X"
            else:
                string = ""
        # column check
        for i in range(3):
            for j in range(3):
                string += self.field[j][i]
            if string == "OOO":
                return "O"
            elif string == "XXX":
                return "X"
            else:
                string = ""
        # diagonal check
        if (
            "{}{}{}".format(self.field[0][0], self.field[1][1], self.field[2][2])
            == "XXX"
        ):
            return "X"
        elif (
            "{}{}{}".format(self.field[0][0], self.field[1][1], self.field[2][2])
            == "OOO"
        ):
            return "O"
        elif (
            "{}{}{}".format(self.field[0][2], self.field[1][1], self.field[2][0])
            == "XXX"
        ):
            return "X"
        elif (
            "{}{}{}".format(self.field[0][2], self.field[1][1], self.field[2][0])
            == "OOO"
        ):
            return "O"
        else:
            return "-"

    def turn(self, stringOfPlayer):
        # !!!stringOfPlayer can be only "X" or "O"!!!
        self.show_field()
        print(
            f"{stringOfPlayer} player, press a number to put your symbol in cell: ",
            end="",
        )
        inputString = ""
        while True:
            inputString = input()
            if re.fullmatch(r"[1-9]{1,1}", inputString):
                break
            else:
                print("Please, use correct input: ", end="")
        for i in range(3):
            for j in range(3):
                if self.field[i][j] == inputString:
                    self.field[i][j] = stringOfPlayer
                    break
        pass

    def start(self):
        turn = 0
        while self.check() == "-" and turn < 9:
            self.turn("X" if turn % 2 == 0 else "O")
            turn += 1
        self.show_field()
        if self.check() == "X":
            print("X player win!")
        elif self.check() == "O":
            print("O player win!")
        else:
            print("Draw!")
        pass
