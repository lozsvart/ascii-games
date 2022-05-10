from app import Controllable, Key
from itertools import product
import random

class App(Controllable):

    def __init__(self):
        self.game = Minesweeper(8, 8, 10)
        self.cursor = (0, 0)

    def press(self, key):
        if key == Key.RIGHT:
            self.move_cursor((0, 1))
        elif key == Key.LEFT:
            self.move_cursor((0, -1))
        elif key == Key.UP:
            self.move_cursor((-1, 0))
        elif key == Key.DOWN:
            self.move_cursor((1, 0))
        elif key == Key.B:
            self.game.toggle_flag(self.cursor)
        elif key == Key.A:
            self.game.discover(self.cursor)

    def move_cursor(self, vec):
        max_width, max_height = self.game.dimension
        x = min(max(0, self.cursor[0] + vec[0]), max_width - 1)
        y = min(max(0, self.cursor[1] + vec[1]), max_height - 1)
        self.cursor = x, y

    def get_line(self, line_number):
        def get_symbol(column_number):
            coord = (line_number, column_number)
            return "[" + self.game.get_symbol(coord) + "]" if coord == self.cursor else " " + self.game.get_symbol(coord) + " "
        separator = "|"
        columns = self.game.dimension[1]
        return separator + separator.join(get_symbol(i) for i in range(columns)) + separator + "\n"

    def show(self):
        lines, columns = self.game.dimension
        separator = "+" + "---+" * columns + "\n"
        result = separator + separator.join(self.get_line(i) for i in range(lines)) + separator
        result += ("Undiscovered empty fields: " + str(self.game.get_undiscovered_empty_fields()) if self.game.mines_generated else "") + "\n"
        result += "You lost :(" if self.game.get_win_status() == "lost" else ""
        result += "You won!" if self.game.get_win_status() == "won" else ""
        return result

class Minesweeper:

    def __init__(self, width, height, mine_number):
        self.dimension = (width, height)
        self.mine_number = mine_number
        self.flagged = {coord: False for coord in product(range(width), range(height))}
        self.discovered = {coord: False for coord in product(range(width), range(height))}
        self.mines = {coord: False for coord in product(range(width), range(height))}
        self.mines_generated = False

    def toggle_flag(self, coord):
        if not self.discovered[coord]:
            self.flagged[coord] = not self.flagged[coord]

    def is_flagged(self, coord):
        return self.flagged[coord]
    
    def generate_mines(self, safe_coords):
        if self.mines_generated:
            return
        coords = set(product(*(range(size) for size in self.dimension))) - safe_coords
        mines = random.sample(coords, self.mine_number)
        for coord in mines:
            self.mines[coord] = True
        self.mines_generated = True

    def get_undiscovered_empty_fields(self):
        width, height = self.dimension
        return len(set(coord for coord in product(range(width), range(height)) if not self.discovered[coord] and not self.mines[coord]))

    def get_mines_found(self):
        width, height = self.dimension
        return len(set(coord for coord in product(range(width), range(height)) if self.discovered[coord] and self.mines[coord]))

    def get_win_status(self):
        if self.get_mines_found() > 0:
            return "lost"
        if self.get_undiscovered_empty_fields() == 0:
            return "won"
        return None

    def discover(self, coord):
        if self.get_win_status() == "won":
            return
        if not self.mines_generated:
            self.generate_mines({coord})
        if not self.is_flagged(coord):
            self.discovered[coord] = True
            if self.count_neighbor_mines(coord) == 0:
                for neighbor in neighbours(coord, self.dimension):
                    if not self.discovered[neighbor]:
                        self.discover(neighbor)

    def count_neighbor_mines(self, coord):
        return len(set(filter(lambda coord: self.mines[coord], neighbours(coord, self.dimension))))

    def get_symbol(self, coord):
        if self.is_flagged(coord):
            return "*"
        if self.discovered[coord]:
            if self.mines[coord]:
                return "!"
            else:
                if self.count_neighbor_mines(coord) > 0:
                    return str(self.count_neighbor_mines(coord))
                else:
                    return "."
        return " "

def neighbours(cell, sizes):
    for c in product(*(range(n-1, n+2) for n in cell)):
        if c != cell and all(0 <= n < sizes[i] for i, n in enumerate(c)):
            yield c
