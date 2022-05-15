from first_person_maze.maze_math import *

FOG_OF_WAR_ENABLED = True
SHOW_MAP = True

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

def create_frame(size_x, size_y, standard = True): # TODO use a more expressive name instead of standard
  x_range = range(size_x)
  y_range = range(size_y)
  x_inside = range(1, size_x - 1)
  y_inside = range(1, size_y - 1)
  def result(coord):
    x, y = coord
    if (x not in x_range) or (y not in y_range):
      return TRANSPARENT
    if (x not in x_inside) and (y not in y_inside):
      return "+" if standard else "O"
    if x not in x_inside:
      return "-" if standard else "="
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
close_wall_interacting = create_frame(14, 15, False)
clock_frame = create_frame(3, 9)

def get_writing_art(writing):
    lines = len(writing.split('\n'))
    return translate(create(writing), (6 - lines // 2, 1))

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
  direction = status["direction"]
  player_symbol = {
      N: "^",
      S: "v",
      E: ">",
      W: "<"
  }.get(direction)
  return translate(create(player_symbol), (1 + 2 * loc_x, 1 + 2 * loc_y))

def get_maze_art(maze, status):
    size_x, size_y = maze.dimension
    return frame_art(union([create_fog_of_war(status),
                                 create_maze_art(maze.doors),
                                 create_player_art(status)]), (2 * size_x + 1, 2 * size_y + 1))

def create_maze_art(doors):
  def result(coord):
    row, column = coord
    return get_maze_symbol(row, column, doors)
  return result

def get_maze_symbol(row, column, doors):
    is_field = row % 2 == 1 and column % 2 == 1
    is_vert_wall = row % 2 == 0 and column % 2 == 1
    is_hor_wall = row % 2 == 1 and column % 2 == 0
    EMPTY = TRANSPARENT
    OCCUPIED = "#"
    if is_field:
        return EMPTY
    if not is_vert_wall and not is_hor_wall:
        return OCCUPIED
    if is_vert_wall:
        left_neighbor = (row // 2 - 1, column // 2)
        right_neighbor = (row // 2, column // 2)
        door = doors.get(create_edge(left_neighbor, right_neighbor))

    if is_hor_wall:
        up_neighbor = (row // 2, column // 2 - 1)
        down_neighbor = (row // 2, column // 2)
        door = doors.get(create_edge(up_neighbor, down_neighbor))

    return EMPTY if door is not None and door.is_open() else OCCUPIED

def render_status(maze, status, maze_art):
    arts = {}
    for direction in DIRECTIONS:
        relative_direction = get_relative_direction(status["direction"], direction)
        junction = get_junction(status, maze.doors, direction)
        is_interacting = status["interacting"] and relative_direction == "front"
        first_person_art = create_first_person_art(junction,
                                                   get_wall_decoration(status, maze.wall_decors, direction), is_interacting)
        arts[direction] = first_person_art
        arts[relative_direction] = first_person_art
    map_art = maze_art if SHOW_MAP else create("")

    art = union([
             translate(arts["front"], (0, 16)),
             translate(arts["right"], (15, 32)),
             translate(arts["left"], (15, 0)),
             translate(map_art, (16, 18))
    ])
    return render_art(art, (46, 49))

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

def create_first_person_art(junction, wall_decoration, is_interacting):
    if 'back' not in junction:
        wall = close_wall_interacting if is_interacting else close_wall
        result = union([wall, translate(wall_decoration, (1, 1))])
    else:
        parts = [open_adjacent_door]
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

def get_wall_decoration(status, wall_decorations, direction):
    location = status["location"]
    wall_decor = wall_decorations.get((location, direction))
    return wall_decor.get_art() if wall_decor != None else create_empty()

