from enum import Enum
from first_person_maze.command import Command
from first_person_maze.refactor_utils import transform_param

COMPACT_VIEW = True
FOG_OF_WAR_ENABLED = True
SHOW_MAP = True
START_LOCATION = (0, 0)

# ---------------------

from operator import add
import itertools
import datetime

N = (-1, 0)
W = (0, -1)
S = (1, 0)
E = (0, 1)

DIRECTIONS = {
  "North": N,
  "South": S,
  "East": E,
  "West": W
}
  
def add_tuples(v1, v2):
  return tuple(map(add, v1, v2))

def create_edge(v1, v2):
  return frozenset({v1, v2})

TRANSPARENT = ""

def space_to_transparent(char):
  return TRANSPARENT if char == " " else char

def create_empty():
  return lambda coord: TRANSPARENT

def create(string):
  lines = string.split("\n")
  def result(coord):
    x, y = coord
    if 0 <= x < len(lines):
      if 0 <= y < len(lines[x]):
        return space_to_transparent(lines[x][y])
    return TRANSPARENT
  return result

def create_var(string_provider):
  def result(coord):
    lines = string_provider().split("\n")
    x, y = coord
    if 0 <= x < len(lines):
      if 0 <= y < len(lines[x]):
        return space_to_transparent(lines[x][y])
    return TRANSPARENT
  return result

def translate(string_art, vect):
  return lambda coord: string_art((coord[0] - vect[0], coord[1] - vect[1]))

def union(string_arts):
  def result(coord):
    x, y = coord
    for art in string_arts:
      if art(coord) != TRANSPARENT:
        return art(coord)
    return TRANSPARENT
  return result
  
def frame_art(art, dimension):
  size_x, size_y = dimension
  x_range = range(size_x)
  y_range = range(size_y)
  def result(coord):
    x, y = coord
    if (x not in x_range) or (y not in y_range):
      return TRANSPARENT
    return art(coord)
  return result

def create_frame(size_x, size_y):
  x_range = range(size_x)
  y_range = range(size_y)
  x_inside = range(1, size_x - 1)
  y_inside = range(1, size_y - 1)
  def result(coord):
    x, y = coord
    if (x not in x_range) or (y not in y_range):
      return TRANSPARENT
    if (x not in x_inside) and (y not in y_inside):
      return "+"
    if x not in x_inside:
      return "-"
    if y not in y_inside:
      return "|"
    return TRANSPARENT
  return result


def resolve_char(char):
  return  " " if char == TRANSPARENT else char

def render_art(string_art, dimension):
  size_x, size_y = dimension
  result = []
  for i in range(size_x):
    result.append("".join([resolve_char(string_art((i, j))) for j in range(size_y)]))
  return "\n".join(result)

class Door:
    def __init__(self, open_provider = lambda: True):
        self.open_provider = open_provider

    def is_open(self):
        return self.open_provider()
    
    @staticmethod
    def closed_door():
        return Door(lambda: False)

def get_maze_symbol(row, column, doors):
    closed_door = Door.closed_door()
    is_field = row % 2 == 1 and column % 2 == 1
    is_vert_wall = row % 2 == 0 and column % 2 == 1
    is_hor_wall = row % 2 == 1 and column % 2 == 0
    EMPTY = TRANSPARENT
    OCCUPIED = "#"
    if is_field:
        return EMPTY
    if is_vert_wall:
        left_neighbor = (row // 2 - 1, column // 2)
        right_neighbor = (row // 2, column // 2)
        if doors.get(create_edge(left_neighbor, right_neighbor), closed_door).is_open():
          return EMPTY
        return OCCUPIED
    if is_hor_wall:
        up_neighbor = (row // 2, column // 2 - 1)
        down_neighbor = (row // 2, column // 2)
        if doors.get(create_edge(up_neighbor, down_neighbor), closed_door).is_open():
          return EMPTY
        return OCCUPIED
    return OCCUPIED

def create_maze_art(doors):
  def result(coord):
    row, column = coord
    return get_maze_symbol(row, column, doors)
  return result

def get_distance(coord, coords):
  def dist(first, second):
    return max(abs(first[0]-second[0]), abs(first[1]-second[1]))
  return min(map(lambda coor: dist(coord, coor), coords))

def create_fog_of_war(status):
  if not FOG_OF_WAR_ENABLED:
      return create_empty()
  explored = list(map(lambda coord: (2*coord[0]+1, 2*coord[1]+1), status["explored"]))
  def result(coord):
    distance = get_distance(coord, explored)
    return TRANSPARENT if distance <= 2 else "."
  return result

def create_player_art(status):
  loc_x, loc_y = status["location"]
  return translate(create("X"), (1 + 2 * loc_x, 1 + 2 * loc_y))

def get_maze_art(maze, status):
    size_x, size_y = maze.dimension
    return frame_art(union([create_fog_of_war(status),
                                 create_maze_art(maze.doors),
                                 create_player_art(status)]), (2 * size_x + 1, 2 * size_y + 1))
    

def create_status(choice):
    return {
        "explored": choice["explored"],
        "location": choice["location"]
    }


def get_direction_name(location, neighbor):
    for direction in DIRECTIONS:
      if add_tuples(location, DIRECTIONS[direction]) == tuple(neighbor):
        return direction

def get_other_node(edge, node):
  for a_node in edge:
    if a_node != node:
      return a_node

open_adjacent_door = create(
r"""
\             /
 \           /
  \         / 
              
              
              
              
              
           
       
     
  /         \ 
 /           \
/             \
"""[1:])

long_corridor = translate(create(r"""
\   /    
 \_/     
 / \     
/   \    
"""[1:]), (5, 5))

short_corridor = translate(create("""
___   
              
              
              
___    
"""[1:]), (4, 6))

short_corridor_right_extension = translate(create("""
_  
              
              
              
_    
"""[1:]), (4, 9))

short_corridor_left_extension = translate(create("""
_   
              
              
              
_    
"""[1:]), (4, 5))


short_corridor_right_wall = translate(create("""
|    
|    
|    
|   
"""[1:]), (5, 9))

short_corridor_left_wall = translate(create("""
|      
|       
|       
|   
"""[1:]), (5, 5))


left_wall = translate(create(r"""
\   
 \  

     
     
     
 /
/ 
"""[1:]), (3, 3))

right_wall = translate(create(r"""
 /
/

     

     
\
 \
"""[1:]), (3, 10))

right_corridor = translate(create("""
 |  
_|  
 |  
 |  
 |  
_|  
 |  
 |          
"""[1:]), (3, 10))

left_corridor = translate(create("""
|  
|_  
|  
|  
|  
|_  
|  
|          
"""[1:]), (3, 3))

close_wall = create_frame(14, 15)
clock_frame = create_frame(3, 9)

def wall_clock():
  clock = create_var(lambda: datetime.datetime.now().strftime("%H:%M"))
  return WallObject(translate(union([clock_frame, translate(clock, (1, 2))]), (3, 2)))

def split_text(text, max_width = 11):
    def split_paragraph(paragraph, max_width):
      words = paragraph.split()
      line_length = 0
      result = ""
      for word in words:
          if line_length > 0:
              line_length += 1 + len(word)
              if line_length > max_width:
                  line_length = len(word)
                  result += "\n" + word
              else:
                  result += " " + word
            
          else:
              result += word
              line_length += len(word)
      return result

    paragraphs = text.split("\n")
    return "\n".join(map(lambda paragraph: split_paragraph(paragraph, max_width), paragraphs))

def get_short_corridor(goes_left, goes_right):
    parts = [short_corridor]
    if not goes_left:
        parts.append(short_corridor_left_wall)
    else:
        parts.append(short_corridor_left_extension)

    if not goes_right:
        parts.append(short_corridor_right_wall)
    else:
        parts.append(short_corridor_right_extension)

    return union(parts)

def create_first_person_art(junction, label, wall_decoration):
    label_art = translate(create(label), (0, 7 - (len(label) - 1) // 2))
    if 'back' not in junction:
        result = union([label_art, close_wall,
                      translate(wall_decoration, (1, 1))])
    else:
        parts = [label_art, open_adjacent_door]
        goes_left = 'left' in junction
        goes_right = 'right' in junction

        if 'forward' in junction:
            parts.append(long_corridor)
        else:
            parts.append(get_short_corridor(goes_left, goes_right))

        parts.append(left_corridor if goes_left else left_wall)
        parts.append(right_corridor if goes_right else right_wall)
        
        result = union(parts)

    return frame_art(result, (14, 15))


def rotate_left(vector):
    return (-vector[1], vector[0])

def negate(vector):
    return (-vector[0], -vector[1])

def get_junction(status, maze_edges, direction):
    dir_vector = DIRECTIONS[direction]
    left_vector = rotate_left(dir_vector)
    
    back = status["location"]
    middle = add_tuples(back, dir_vector)
    forward = add_tuples(middle, dir_vector)
    left = add_tuples(middle, left_vector)
    right = add_tuples(middle, negate(left_vector))

    result = []
    for junction, field in zip(('forward', 'left', 'right', 'back'),
                               (forward, left, right, back)):
        if frozenset({middle, field}) in maze_edges:
            result.append(junction)
            
    return set(result)

def get_writing_art(writing):
    lines = len(writing.split('\n'))
    return translate(create(writing), (6 - lines // 2, 1))

def writing(message):
  return WallObject(get_writing_art(split_text(message)))

def get_wall_decoration(status, wall_decorations, direction):
    location = status["location"]
    wall_decor = wall_decorations.get((location, direction))
    return wall_decor.get_art() if wall_decor != None else create_empty()

def render_status(maze, status, maze_art):
    arts = {}
    for direction in DIRECTIONS:
        junction = get_junction(status, maze.doors, direction)
        first_person_art = create_first_person_art(junction, direction,
                                                   get_wall_decoration(status, maze.wall_decors, direction))
        arts[direction] = first_person_art
    map_art = maze_art if SHOW_MAP else create("")

    if COMPACT_VIEW:
        art = union([
                 translate(arts["North"], (0, 16)),
                 translate(arts["South"], (30, 16)),
                 translate(arts["East"], (15, 32)),
                 translate(arts["West"], (15, 0)),
                 translate(map_art, (16, 18))
        ])
        return render_art(art, (46, 49))
    else:
        first_person_view = union([
                 translate(arts["North"], (0, 0)),
                 translate(arts["South"], (15, 16)),
                 translate(arts["East"], (0, 16)),
                 translate(arts["West"], (15, 0))
        ])
        art = union([
            translate(first_person_view, (15, 0)),
            translate(map_art, (2, 9))
        ])
        return render_art(art, (46, 31))

def get_direction(command, original_direction):
    command_directions = {
        Command.DOWN: S,
        Command.UP: N,
        Command.RIGHT: E,
        Command.LEFT: W
    }
    return command_directions[command]
    
def is_valid_move(location, destination, maze):
    door = maze.doors.get(create_edge(location, destination))
    return door.is_open() if door is not None else False

def do_move_and_get_status(direction, status, maze):
    location = status["location"]
    destination = add_tuples(direction, status["location"])
    if is_valid_move(location, destination, maze):
        return {
            "location": destination,
            "direction": direction,
            "explored": status["explored"] + [destination]
        }
        
    return status

def do_interaction(status, maze):
    location = status["location"]
    direction = {
        N: "North",
        S: "Sourh",
        W: "West",
        E: "East"
    }.get(status["direction"])
    maze.wall_decors.get((location, direction)).interact()
    return status

def get_new_status(command, status, maze):
    if command in {Command.UP, Command.RIGHT, Command.LEFT}:
        direction = get_direction(command, status["direction"])
        return do_move_and_get_status(direction, status, maze)
    if command in {Command.A}:
        return do_interaction(status, maze)
    return status       

def get_default_status():
    return {
        "location": START_LOCATION,
        "direction": N,
        "explored": [START_LOCATION]
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
    
    def interact(self):
        self.wire.status = not self.wire.status

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
    door_locations = [{(3, 1), (2, 1)}, 
            {(3, 0), (2, 0)},
            {(4, 2), (4, 3)}, 
            {(0, 1), (1, 1)},
            {(4, 4), (3, 4)},
            {(3, 3), (4, 3)}, 
            {(3, 2), (3, 1)},
            {(1, 2), (0, 2)}, 
            {(1, 4), (0, 4)},
            {(1, 2), (1, 3)}, 
            {(3, 4), (2, 4)},
            {(2, 3), (2, 2)}, 
            {(0, 3), (0, 2)},
            {(4, 1), (4, 0)}, 
            {(2, 0), (1, 0)},
            {(2, 1), (2, 2)}, 
            {(1, 2), (1, 1)},
            {(3, 0), (3, 1)}, 
            {(1, 0), (0, 0)},
            {(0, 3), (0, 4)}, 
            {(4, 4), (4, 3)},
            {(2, 3), (3, 3)}, 
            {(3, 1), (4, 1)}]
    doors = {frozenset(location): Door() for location in door_locations}
    wire = Wire()
    doors.update({frozenset({(0, 1), (0, 0)}): Door(wire.is_on)})
    return Maze(
        dimension = (5, 5),
        doors = doors,
        wall_decors = {
            ((0, 0), "North"): lever(wire),
            ((2, 4), "East"): writing("Congrats!\n\nYou have found the exit."),
            ((2, 4), "West"): writing("Hope you enjoyed the trip!"),
            ((1, 4), "South"): writing("Sorry, this is a dead end :("),
            ((2, 1), "North"): writing("For where your treasure is, there your heart will be also.\n\nMt. 6, 21"),
            ((1, 3), "North"): writing("Do you not know? Have you not heard? The Lord is the everlasting God, the Creator of the ends of the earth."),
            ((1, 3), "East"): writing("He will not grow tired or weary, and his understand- ing no one can fathom."),
            ((1, 3), "South"): writing("He gives strength to the weary and increases the power of the weak.\n\nIs. 40, 28-29"),
            ((2, 0), "East"): wall_clock()
        }
        )
