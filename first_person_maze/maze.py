from first_person_maze.command import Command
from first_person_maze.art import *
from first_person_maze.maze_math import *

import datetime

class Door:
    def __init__(self, open_provider = lambda: True):
        self.open_provider = open_provider

    def is_open(self):
        return self.open_provider()

def wall_clock():
  clock = create_var(lambda: datetime.datetime.now().strftime("%H:%M"))
  return WallObject(translate(union([clock_frame, translate(clock, (1, 2))]), (3, 2)))

def writing(message):
  return WallObject(get_writing_art(split_text(message)))

def get_direction(command, original_direction):
    transformations = {
        Command.RIGHT: lambda coord: negate(rotate_left(coord)),
        Command.LEFT: rotate_left,
        Command.UP: lambda coord: coord
    }
    return transformations.get(command)(original_direction)

def is_valid_move(location, destination, maze):
    door = maze.doors.get(create_edge(location, destination))
    return door.is_open() if door is not None else False

def do_move_and_get_status(direction, status, maze):
    location = status["location"]
    destination = add_tuples(direction, location)
    if is_valid_move(location, destination, maze):
        return dict(status, **{
            "location": destination,
            "direction": direction,
            "explored": status["explored"] + [destination]
        })

    return status

def has_wall_in_front_of_player(status, maze):
    location = status["location"]
    direction = status["direction"]
    destination = add_tuples(direction, location)
    return not is_valid_move(location, destination, maze)

def do_interaction(status, maze, command):
    location = status["location"]
    direction = {
        N: "North",
        S: "South",
        W: "West",
        E: "East"
    }.get(status["direction"])
    obj = maze.wall_decors.get((location, direction))
    if obj is not None:
        obj.interact(command)
    return status

def get_new_status(command, status, maze):
    if status["interacting"] and command != Command.A:
        return do_interaction(status, maze, command)
    if command in {Command.UP, Command.RIGHT, Command.LEFT}:
        direction = get_direction(command, status["direction"])
        if command == Command.UP:
            return do_move_and_get_status(direction, status, maze)
        else:
            return dict(status, **{
                "direction": direction
            })
    if command == Command.A:
        return dict(status, **{
            "interacting": not status["interacting"] and has_wall_in_front_of_player(status, maze)
        })
    return status

class Lever:
    def __init__(self, on = False):
        self.on = on

    def get_art(self):
        return translate(create("\n\nO\n|\n|" if not self.is_on() else "|\n|\nO"), (4, 6))
    
    def is_on(self):
        return self.on

    def interact(self, command):
        if command in {Command.UP, Command.DOWN}:
            self.on = command == Command.UP

def simple_door(start, end):
    return Door()

class WallObject:
    def __init__(self, art):
        self.art = art

    def get_art(self):
        return self.art

    def interact(self, command):
        pass

class Safe:
    def __init__(self, solution):
        self.solution = list(map(int, solution))
        self.selected = 0
        self.counters = [0] * len(solution)

    def get_art(self):
        number = "".join(map(str, self.counters))
        selector = " " * self.selected + "^"
        return translate(create(number + "\n" + selector), (5, 6 - len(self.solution) // 2))

    def is_open(self):
        return self.counters == self.solution

    def interact(self, command):
        if command == Command.UP:
            self.counters[self.selected] += 1
        if command == Command.DOWN:
            self.counters[self.selected] -= 1
        if command == Command.RIGHT:
            self.selected += 1
        if command == Command.LEFT:
            self.selected -= 1

        for i in range(len(self.counters)):
            self.counters[i] %= 10
        self.selected %= len(self.counters)

class Maze:
    def __init__(self, dimension, doors, wall_decors):
        self.dimension = dimension
        self.doors = doors
        self.wall_decors = wall_decors

def get_default_status():
    return {
        "location": (0, 0),
        "direction": N,
        "interacting": False,
        "explored": [(0, 0)]
    }

def get_default_maze():
    safes = [Safe("404")]
    levers = [Lever(), Lever(True)]

    door_locations = [{(3, 1), (2, 1)}, {(0, 1), (0, 0)}, {(3, 0), (2, 0)},
                    {(4, 2), (4, 3)}, {(0, 1), (1, 1)}, {(4, 4), (3, 4)}, {(3, 3), (4, 3)},
                    {(3, 2), (3, 1)}, {(1, 2), (0, 2)}, {(1, 4), (0, 4)}, {(1, 2), (1, 3)},
                    {(3, 4), (2, 4)}, {(2, 3), (2, 2)}, {(0, 3), (0, 2)}, {(4, 1), (4, 0)},
                    {(2, 0), (1, 0)}, {(2, 1), (2, 2)}, {(1, 2), (1, 1)}, {(3, 0), (3, 1)},
                    {(0, 3), (0, 4)}, {(4, 4), (4, 3)}, {(2, 3), (3, 3)}, {(3, 1), (4, 1)}
    ]
    doors = {create_edge(*location): Door() for location in door_locations}
    doors.update({
        create_edge((1, 0), (0, 0)): Door(levers[0].is_on),
        create_edge((1, 2), (1, 3)): Door(levers[1].is_on),
        create_edge((4, 3), (4, 4)): Door(safes[0].is_open)
    })
    return Maze(
        dimension = (5, 5),
        doors = doors,
        wall_decors = {
            ((0, 0), "North"): writing("Controls: up, down, left, right and space"),
            ((0, 0), "West"): writing("Space switches between movement and interactive mode"),
            ((1, 4), "East"): levers[0],
            ((1, 3), "South"): levers[1],
            ((1, 3), "West"): writing("Hint:\nNOT FOUND"),
            ((3, 0), "South"): safes[0],
            ((2, 4), "North"): writing("Congrats!\n\nYou have found the exit"),
            ((1, 3), "North"): writing("Try pulling the lever"),
            ((2, 0), "East"): wall_clock()
        }
    )
