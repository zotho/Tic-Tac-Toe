r""" # Tic tac toe

Author: Alekseev Sviatoslav
Telegram: @zotho
E-mail: svjatoslavalekseef2@gmail.com

Using:
```
$ python3 tic_tac_toe.py play
$ python3 tic_tac_toe.py test
```

_|_|_
_|_|_
 | | 

1|2|3   x|2|3
4|5|6   o|x|6
7|8|9   7|8|9

x|_|o
_|x|o
o| |x

\|_|o
_|\|o
o| |\

"""

import itertools
import random
import sys

class Game:

    def __init__(self, x=3, y=3):
        if x < 1:
            raise ValueError(f"Invalid size of field: col={x}")
        if y < 1:
            raise ValueError(f"Invalid size of field: row={y}")
        self.x = x  # columns number
        self.y = y  # rows number
        self.field = [
            [
                "_" for _ in range(x)
            ] for _ in range(y)
        ]
        self.now_player = "x"
        self.winner = None

    def __str__(self):
        last_line = self.y - 1
        return "\n".join(
            [
                "|".join(
                    [
                        cell
                        if line_index < last_line or cell != "_"
                        else " "
                        for cell in line
                    ]
                ) for line_index, line in enumerate(self.field)
            ]
        )

    def help(self):
        if self.winner:
            return str(self)
        row_length = self.x
        cell_max_width = len(str(self.x * self.y))
        return "\n".join(
            [
                "|".join(
                    [
                        f"{cell:>{cell_max_width}}"
                        if cell != "_"
                        else f"{(row_index * row_length + col_index + 1):>{cell_max_width}}"
                        for col_index, cell in enumerate(line)
                    ]
                ) for row_index, line in enumerate(self.field)
            ]
        )

    def step(self, on_cell):
        if self.winner:
            raise Exception("Game already ended.")
        now = self.now_player
        cols = self.x
        rows = self.y
        row = (on_cell - 1) // cols
        col = (on_cell - 1) % cols
        if row + 1 > rows or on_cell < 1:
            raise ValueError("Index out of field!")
        cell = self.field[row][col]
        if cell != "_":
            raise ValueError(f"Invalid move. Cell already marked '{cell}'.")
        self.field[row][col] = now
        if self.check_winner():
            self.winner = now
        elif all([
                cell != "_"
                for row in self.field
                for cell in row
            ]):
            self.winner = "_"
        else:
            self.now_player = {"x":"o", "o":"x"}[now]

    def check_winner(self):
        field = self.field
        cols = self.x
        rows = self.y
        r"""
        - 1  0
        | 0  1
        \ 1  1
        / 1 -1
        """
        def check_line(line):
            return not any(map(lambda x: x != line[0] or x == "_", line))

        # Check rows
        for row_index, row in enumerate(field):
            if check_line(row):
                field[row_index] = ["-" for _ in range(cols)]
                return True

        # Check columns
        transponated_field = [
            [
                field[row_index][col_index]
                for row_index in range(rows)
            ]
            for col_index in range(cols)
        ]
        for col_index, col in enumerate(transponated_field):
            if check_line(col):
                for row_index in range(rows):
                    field[row_index][col_index] = "|"
                return True

        """Check diagonal.
        1 _ _
        4 2 _
        7 5 3 <-
        A 8 6 <-
        _ B 9
        _ _ C
        """
        start_row_index = cols - 1
        end_row = rows
        diagonal_field = [
            [
                field[row_index - col_index][col_index]
                for col_index in range(cols)
            ] for row_index in range(start_row_index, end_row)
        ]
        for row_index, row in enumerate(diagonal_field):
            if check_line(row):
                for col_index in range(cols):
                    field[start_row_index + row_index - col_index][col_index] = "/"
                return True

        """Check diagonal.
        _ _ 3
        _ 2 6
        1 5 9 <---
        4 8 C <---
        7 B _
        A _ _

        _ _ 3
        _ 2 6 <-x-
        1 5 _ <-x-
        4 _ _
        """
        start_row_index = 0
        end_row = rows - cols + 1
        diagonal_field = [
            [
                field[row_index + col_index][col_index]
                for col_index in range(cols)
            ] for row_index in range(start_row_index, end_row)
        ]
        for row_index, row in enumerate(diagonal_field):
            if check_line(row):
                for col_index in range(cols):
                    field[start_row_index + row_index + col_index][col_index] = "\\"
                return True
        return False

def test_game():
    game = Game()
    assert game.field == [["_", "_", "_"],
                          ["_", "_", "_"],
                          ["_", "_", "_"]], "Bad initial field"
    print(game)
    print()
    assert str(game) == "_|_|_\n"\
                        "_|_|_\n"\
                        " | | ", "Bad initial placement output"
    print(game.help())
    print()
    assert game.help() == "1|2|3\n"\
                          "4|5|6\n"\
                          "7|8|9", "Bad initial help output"
    game.step(1)
    print(game)
    print()
    print(game.help())
    print()
    assert game.field == [["x", "_", "_"],
                          ["_", "_", "_"],
                          ["_", "_", "_"]], "Bad first step field"
    assert str(game) == "x|_|_\n"\
                        "_|_|_\n"\
                        " | | ", "Bad first step placement output"
    game.step(4)
    print(game)
    print()
    print(game.help())
    print()
    assert game.help() == "x|2|3\n"\
                          "o|5|6\n"\
                          "7|8|9", "Bad second step help output"
    game.step(5)
    print(game)
    print()
    print(game.help())
    print()
    game.step(7)
    print(game)
    print()
    print(game.help())
    assert str(game) == "x|_|_\n"\
                        "o|x|_\n"\
                        "o| | ", "Bad prev step placement output"
    # X wins
    game.step(9)
    print()
    print(game)
    print()
    print(game.help())
    assert str(game) == "\\|_|_\n"\
                        "o|\\|_\n"\
                        "o| |\\", "Bad final placement output"
    assert game.help() == "\\|_|_\n"\
                          "o|\\|_\n"\
                          "o| |\\", "Bad final help output"

def play_game():
    x = None
    while x == None or x < 1:
        x = int(input("Select number of columns: "))
        if x < 1:
            print(f"Number of columns must be greater than zero: col={x}")
    y = None
    while y == None or y < 1:
        y = int(input("Select number of rows: "))
        if y < 1:
            print(f"Number of rows must be greater than zero: row={y}")
    print()

    game = Game(x=x, y=y)
    while not game.winner:
        game_strings = str(game).split(sep="\n")
        game_strings_max_len = max(map(len, game_strings))
        help_strings = game.help().split(sep="\n")
        print(
            "\n".join([
                "\t".join([left, right])
                for left, right in itertools.zip_longest(
                    game_strings,
                    help_strings,
                    fillvalue=" " * game_strings_max_len + "\t"
                )
            ]),
            end="\n\n"
        )
        if game.now_player == "x":
            while True:
                try:
                    game.step(int(input("Your turn: ")))
                    break
                except ValueError as error:
                    print(error, end="\n\n")
        else:
            game.step(random.choice([
                row_index * game.x + col_index + 1
                for row_index, row in enumerate(game.field)
                for col_index, cell in enumerate(row)
                if game.field[row_index][col_index] == "_"
            ]))
    print(game, end="\n\n")
    if game.winner == "_":
        print("Draw!", end="\n\n")
    else:
        print(f"'{game.winner.upper()}' wins!", end="\n\n")
    print("End of game. Bye!")


if __name__ == '__main__':
    argument = len(sys.argv) == 2 and sys.argv[1]
    try:
        {
            "test": test_game,
            "play": play_game,
        }[argument or "test"]()
    except KeyError:
        print(f"Invalid argument '{argument}'. Avaliable: 'test', 'play'")
