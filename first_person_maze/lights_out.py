from first_person_maze.command import Command
from first_person_maze.art import *
from first_person_maze.maze_math import *

SIZE = 5

default_start = [[0]*SIZE, [0]*SIZE, [0]*SIZE, [0]*SIZE, [0]*SIZE]

class LightsOut:
    def __init__(self, start_pos = default_start):
        self.position = start_pos
        self.selected = (0, 0)

    def get_art(self):
        def format_item(item):
            return "." if item == 0 else "#"
        selector = translate(create("[ ]"), (self.selected[0], self.selected[1] * 2 - 1))
        table = create("\n".join(" ".join(format_item(item) for item in row) for row in self.position))
        content = union([selector, table])
        return translate(content, (3, 12-2*SIZE))

    def is_solved(self):
        return all(map(lambda row: all(map(lambda item: item == 1, row)), self.position))

    def turn(self, x, y):
        if 0 <= x < SIZE and 0 <= y < SIZE:
            self.position[x][y] = 1 - self.position[x][y]

    def interact(self, command):
        if command == Command.B:
            x, y = self.selected
            self.turn(x, y)
            self.turn(x-1, y)
            self.turn(x+1, y)
            self.turn(x, y-1)
            self.turn(x, y+1)
        if command == Command.DOWN:
            self.selected = add_tuples(self.selected, (1, 0))
        if command == Command.UP:
            self.selected = add_tuples(self.selected, (-1, 0))
        if command == Command.RIGHT:
            self.selected = add_tuples(self.selected, (0, 1))
        if command == Command.LEFT:
            self.selected = add_tuples(self.selected, (0, -1))
        self.selected = within(self.selected, (0, 0), (SIZE-1, SIZE-1))
