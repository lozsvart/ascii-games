from mazeobjects import Gate as gate, WallObject as wall_object, MazeObject as maze_object
from mazemath import edge, Coord as coord, Direction
from maze import Maze as maze
from mazeart import writing

def standard_maze():
    gate_coords = [{(3, 1), (2, 1)}, {(3, 0), (2, 0)}, {(4, 2), (4, 3)}, {(0, 1), (1, 1)}, {(0, 1), (0, 0)},
                   {(4, 4), (3, 4)}, {(3, 3), (4, 3)}, {(3, 2), (3, 1)}, {(1, 2), (0, 2)}, {(1, 4), (0, 4)},
                   {(1, 2), (1, 3)}, {(3, 4), (2, 4)}, {(2, 3), (2, 2)}, {(0, 3), (0, 2)}, {(4, 1), (4, 0)},
                   {(2, 0), (1, 0)}, {(2, 1), (2, 2)}, {(1, 2), (1, 1)}, {(3, 0), (3, 1)}, {(1, 0), (0, 0)},
                   {(0, 3), (0, 4)}, {(4, 4), (4, 3)}, {(2, 3), (3, 3)}, {(3, 1), (4, 1)}]
    gates = [gate(edge(coord(*start), coord(*end))) for start, end in gate_coords]
    wall_objects = [
        wall_object((edge(0, 0), Direction.WEST), writing("I will instruct you and teach you in the way you should go; I will counsel you with my loving eye on you. Psalms 32,8"))
    ]
    objects = [maze_object(gate = gate) for gate in gates] +\
              [maze_object(wall_object = wall_object) for wall_object in wall_objects]
    return maze(objects)

maze = standard_maze()
