from app import Key, Controllable

class App(Controllable):
    
    def __init__(self):
        self.maze = Maze(
        dimension = (5, 5),
        doors = {frozenset({(3, 1), (2, 1)}), frozenset({(3, 0), (2, 0)}),
                frozenset({(4, 2), (4, 3)}), frozenset({(0, 1), (1, 1)}),
                frozenset({(0, 1), (0, 0)}), frozenset({(4, 4), (3, 4)}),
                frozenset({(3, 3), (4, 3)}), frozenset({(3, 2), (3, 1)}),
                frozenset({(1, 2), (0, 2)}), frozenset({(1, 4), (0, 4)}),
                frozenset({(1, 2), (1, 3)}), frozenset({(3, 4), (2, 4)}),
                frozenset({(2, 3), (2, 2)}), frozenset({(0, 3), (0, 2)}),
                frozenset({(4, 1), (4, 0)}), frozenset({(2, 0), (1, 0)}),
                frozenset({(2, 1), (2, 2)}), frozenset({(1, 2), (1, 1)}),
                frozenset({(3, 0), (3, 1)}), frozenset({(1, 0), (0, 0)}),
                frozenset({(0, 3), (0, 4)}), frozenset({(4, 4), (4, 3)}),
                frozenset({(2, 3), (3, 3)}), frozenset({(3, 1), (4, 1)})},
        wall_decors = {
            ((0, 0), "West"): to_writing("I will instruct you and teach you in the way you should go; I will counsel you with my loving eye on you. Psalms 32,8"),
            ((0, 0), "North"): to_writing("This is a wall.\n\nSome of them contain messages.\nEnjoy! :)"),
            ((2, 4), "East"): to_writing("Congrats!\n\nYou have found the exit."),
            ((2, 4), "West"): to_writing("Hope you enjoyed the trip!"),
            ((1, 4), "South"): to_writing("Sorry, this is a dead end :("),
            ((2, 1), "North"): to_writing("For where your treasure is, there your heart will be also.\n\nMt. 6, 21"),
            ((1, 3), "North"): to_writing("Do you not know? Have you not heard? The Lord is the everlasting God, the Creator of the ends of the earth."),
            ((1, 3), "East"): to_writing("He will not grow tired or weary, and his understand- ing no one can fathom."),
            ((1, 3), "South"): to_writing("He gives strength to the weary and increases the power of the weak.\n\nIs. 40, 28-29"),
            ((2, 0), "East"): wall_clock()
        }
        )
        self.status = get_default_status()
    
    def press(self, key):
        command = {
            Key.UP: 'w',
            Key.DOWN: 's',
            Key.LEFT: 'a',
            Key.RIGHT: 'd'
        }.get(key)
        if command is not None:
            self.status = get_new_status(command, self.status, self.maze)
    
    def show(self):
        maze_art = get_maze_art(self.maze, self.status)
        return render_status(self.maze, self.status, maze_art)

COMPACT_VIEW = True
RELATIVE_VIEW = True
FOG_OF_WAR_ENABLED = True
SHOW_MAP = False
START_LOCATION = (0, 0)

# ---------------------

import operator
import itertools
import json
import base64
import datetime
import sys

N = (-1, 0)
W = (0, -1)
S = (1, 0)
E = (0, 1)

FORWARD = lambda direction: direction
LEFT = lambda direction: (-direction[1], direction[0])
RIGHT = lambda direction: (direction[1], -direction[0])

DIRECTIONS = {
  "North": N,
  "South": S,
  "East": E,
  "West": W
}
  
def add_tuples(v1, v2):
  return tuple(map(operator.add, v1, v2))

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


def get_maze_symbol(row, column, doors):
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
    if create_edge(left_neighbor, right_neighbor) in doors:
      return EMPTY
    return OCCUPIED
  if is_hor_wall:
    up_neighbor = (row // 2, column // 2 - 1)
    down_neighbor = (row // 2, column // 2)
    if create_edge(up_neighbor, down_neighbor) in doors:
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
  symbol = {
      N: "^",
      W: "<",
      E: ">",
      S: "v"
  }.get(status["direction"])
  return translate(create(symbol), (1 + 2 * loc_x, 1 + 2 * loc_y))

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
  return translate(union([clock_frame, translate(clock, (1, 2))]), (3, 2))

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

def to_writing(message):
  return get_writing_art(split_text(message))

def get_wall_decoration(status, wall_decorations, direction):
    location = status["location"]
    return wall_decorations.get((location, direction), create_empty())

def get_relative_direction(start, end):
    while start != N:
        start = LEFT(start)
        end = LEFT(end)
    return {
        N: "front",
        W: "left",
        E: "right",
        S: "back"
    }.get(end)

def render_status(maze, status, maze_art):
    arts = {}
    arts["empty"] = create("")
    for direction in DIRECTIONS:
        junction = get_junction(status, maze.doors, direction)
        label = "" if RELATIVE_VIEW else direction
        first_person_art = create_first_person_art(junction, label,
                                                   get_wall_decoration(status, maze.wall_decors, direction))
        arts[direction] = first_person_art
        arts[get_relative_direction(status["direction"], DIRECTIONS[direction])] = first_person_art
    map_art = maze_art if SHOW_MAP else create("")
    
    up_art = arts["front" if RELATIVE_VIEW else "North"]
    down_art = arts["empty" if RELATIVE_VIEW else "South"]
    right_art = arts["right" if RELATIVE_VIEW else "East"]
    left_art = arts["left" if RELATIVE_VIEW else "West"]

    if COMPACT_VIEW:
        art = union([
                 translate(up_art, (0, 16)),
                 translate(down_art, (30, 16)),
                 translate(right_art, (15, 32)),
                 translate(left_art, (15, 0)),
                 translate(map_art, (16, 18))
        ])
        return render_art(art, (46, 49))
    else:
        first_person_view = union([
                 translate(up_art, (0, 0)),
                 translate(down_art, (15, 16)),
                 translate(right_art, (0, 16)),
                 translate(left_art, (15, 0))
        ])
        art = union([
            translate(first_person_view, (15, 0)),
            translate(map_art, (2, 9))
        ])
        return render_art(art, (46, 31))

def get_move_command(command):
    move_commands = {
        "s": lambda direction: direction,
        "w": FORWARD,
        "d": RIGHT,
        "a": LEFT
    }
    return move_commands[command]

def is_valid_move(location, destination, maze):
    return create_edge(location, destination) in maze.doors

def do_move_and_get_status(move_command, status, maze):
    location = status["location"]
    destination = location
    direction = move_command(status["direction"])
    if move_command == FORWARD:
        destination = add_tuples(direction, status["location"])
        if not is_valid_move(location, destination, maze):
            destination = location
    return {
        "location": destination,
        "direction": direction,
        "explored": status["explored"] + [destination]
    }

def get_new_status(command, status, maze):
    command = command.lower()
    if command in {"q"}:
        return None
    if command in {"w", "a", "s", "d"}:
        direction = get_move_command(command)
        return do_move_and_get_status(direction, status, maze)
    return status       

def get_default_status():
    return {
        "location": START_LOCATION,
        "direction": N,
        "explored": [START_LOCATION]
    }

class Maze:
    def __init__(self, dimension, doors, wall_decors):
        self.dimension = dimension
        self.doors = doors
        self.wall_decors = wall_decors
