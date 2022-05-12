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
