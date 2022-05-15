from first_person_maze.command import Command
from first_person_maze.art import *
from first_person_maze.maze_math import *

import datetime

class Door:
    def __init__(self, open_provider = lambda: True):
        self.open_provider = open_provider

    def is_open(self):
        return self.open_provider()
    
    @staticmethod
    def closed_door():
        return Door(lambda: False) 


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
        return {
            "location": destination,
            "direction": direction,
            "interacting": status["interacting"],
            "explored": status["explored"] + [destination]
        }

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
            return {
                "location": status["location"],
                "direction": direction,
                "interacting": status["interacting"],
                "explored": status["explored"]
            }
    if command == Command.A:
        return dict(status, **{
            "interacting": not status["interacting"] and has_wall_in_front_of_player(status, maze)
        })
    return status       

def get_default_status():
    return {
        "location": (0, 0),
        "direction": N,
        "interacting": False,
        "explored": [(0, 0)]
    }

def lever(wire):
    return WallObject(translate(create_var(lambda: "O\n|\n|" if wire.is_on() else "\n\n|\n|\nO"), (4, 6)), wire)

def simple_door(start, end):
    return Door()

class WallObject:
    def __init__(self, art, wire = None):
        self.art = art
        self.wire = wire

    def get_art(self):
        return self.art

    def interact(self, command):
        if self.wire is not None and command in {Command.UP, Command.DOWN}:
            self.wire.status = command == Command.UP

class Wire:
    def __init__(self):
        self.status = False
    
    def is_on(self):
        return self.status

class Maze:
    def __init__(self, dimension, doors, wall_decors):
        self.dimension = dimension
        self.doors = doors
        self.wall_decors = wall_decors

def get_default_maze():
    door_locations = [{(3, 1), (2, 1)}, {(0, 1), (0, 0)}, {(3, 0), (2, 0)},
                    {(4, 2), (4, 3)}, {(0, 1), (1, 1)}, {(4, 4), (3, 4)}, {(3, 3), (4, 3)},
                    {(3, 2), (3, 1)}, {(1, 2), (0, 2)}, {(1, 4), (0, 4)}, {(1, 2), (1, 3)},
                    {(3, 4), (2, 4)}, {(2, 3), (2, 2)}, {(0, 3), (0, 2)}, {(4, 1), (4, 0)},
                    {(2, 0), (1, 0)}, {(2, 1), (2, 2)}, {(1, 2), (1, 1)}, {(3, 0), (3, 1)},
                    {(0, 3), (0, 4)}, {(4, 4), (4, 3)}, {(2, 3), (3, 3)}, {(3, 1), (4, 1)}
    ]
    doors = {frozenset(location): Door() for location in door_locations}
    wire_1 = Wire()
    wire_2 = Wire()
    doors.update({frozenset({(1, 0), (0, 0)}): Door(wire_1.is_on), frozenset({(1, 2), (1, 3)}): Door(wire_2.is_on)})
    return Maze(
        dimension = (5, 5),
        doors = doors,
        wall_decors = {
            ((1, 4), "East"): lever(wire_1),
            ((1, 2), "South"): lever(wire_2),
            ((2, 4), "East"): writing("Congrats!\n\nYou have found the exit."),
            ((2, 4), "West"): writing("Hope you enjoyed the trip!"),
            ((1, 4), "South"): writing("Sorry, this is a dead end :("),
            ((2, 0), "East"): wall_clock()
        }
        )
