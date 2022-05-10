from app import Key, Controllable

SIZE = 5
RODS = 3

class App(Controllable):

    def __init__(self):
        self.cursor = 0
        self.selected = 0
        self.tower = HanoiTower([0] * SIZE)

    def press(self, key):
        if key == Key.RIGHT:
            self.cursor += 1
            self.cursor %= RODS
        if key == Key.LEFT:
            self.cursor -= 1
            self.cursor %= RODS
        if self.selected == None:
            self.selected = self.cursor
        else:
            self.tower.move(self.selected, self.cursor)
            self.selected = None

    def show(self):
        dimension = get_picture_dimension(self.tower.size())
        return render_string_art(create_full_art(self.tower, self.cursor, self.selected), dimension)

class HanoiTower:
    def __init__(self, stones):
        self.stones = stones

    def size(self):
        return len(self.stones)
    
    def move(self, from_rod_index, to_rod_index):
        from_rod = self.get_rod_stones(from_rod_index)
        to_rod = self.get_rod_stones(to_rod_index)
        if len(from_rod) == 0:
            return
        moved_stone = from_rod[0]
        if (len(to_rod) == 0 or to_rod[0] > moved_stone):
            self.stones[moved_stone - 1] = to_rod_index

    def get_rod_stones(self, rod):
        return [i + 1 for i in range(len(self.stones))\
                if self.stones[i] == rod]

# ----------------------------------------

def get_gap():
    return 5

def get_tower_width(size):
    return 2 * size + 3

def get_tower_height(size):
    return size + 2

def get_tower_position(size, i):
    return i * (get_tower_width(size) + get_gap())

def get_tower_center(size, i):
    return get_tower_width(size) // 2 + get_tower_position(size, i)

def get_picture_height(size):
    return get_tower_height(size) + 4

def get_picture_width(size):
    return get_tower_width(size) * RODS + (RODS-1) * get_gap()

def get_picture_dimension(size):
    return (get_picture_height(size), get_picture_width(size))


#-------------------------------------

TRANSPARENT = ""

def empty_art():
   return lambda x, y: TRANSPARENT

def create_string_art(string):
  def result(x, y):
    if x == 0 and 0 <= y < len(string):
      return string[y]
    else:
      return TRANSPARENT
  return result
  
def translate(string_art, i, j):
  return lambda x, y: string_art(x - i, y - j)

def transpose(string_art):
  return lambda x, y: string_art(y, x)

def union(string_arts):
  def result(x, y):
    for art in string_arts:
      if art(x, y) != TRANSPARENT:
        return art(x, y)
    return TRANSPARENT
  return result

#-------------------------------------

def resolve_char(char):
  return " " if char == TRANSPARENT else char

def render_string_art(string_art, dimension):
  size_x, size_y = dimension
  lines = "\n".join("".join(resolve_char(string_art(i, j)) \
                            for j in range(size_y)) for i in range(size_x))
  return lines

#---------------------------------

def create_tower_base_and_stick(size, is_cursor, is_selected):
  height = get_tower_height(size)
  width = get_tower_width(size)
  stick = transpose(create_string_art("|" * height))
  stick = translate(stick, 0, width // 2)
  base = create_string_art("=" * width)
  base = translate(base, height - 1, 0)
  selection_symbol = "O" if is_selected else "^" if is_cursor else ""
  selection = translate(create_string_art(selection_symbol), size + 2, width // 2)
  return union([base, stick, selection])

def create_stone(size):
  stone_string = ("o" * size) + " " + ("o" * size)
  return translate(create_string_art(stone_string), 0, -size)

def create_tower_with_stones(size, stone_list, is_cursor, is_selected):
  tower_base_art = create_tower_base_and_stick(size, is_cursor, is_selected)
  stone_arts = []
  stone_height = size - len(stone_list) + 1
  center = size + 1
  for stone_size in stone_list:
    stone_art = translate(create_stone(stone_size), 0, center)
    stone_arts.append(translate(stone_art, stone_height, 0))
    stone_height += 1
  return union([tower_base_art] + stone_arts)

def create_art_for_tower(size, stone_list, i, is_cursor, is_selected):
  position = get_tower_position(size, i)
  tower_art = create_tower_with_stones(size, stone_list, is_cursor, is_selected)
  label_art = translate(create_string_art(get_tower_name(i)), 0, 0)
  return translate(union([label_art, tower_art]), 2, position)

def create_full_art(tower, cursor, selected):
  size = tower.size()
  tower_arts = [create_art_for_tower(size, tower.get_rod_stones(i), i, cursor == i, selected == i) \
                for i in range(RODS)]
  return union(tower_arts)

  
def get_tower_name(index):
    return "ABCDE"[index]
