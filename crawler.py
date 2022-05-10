from app import Key, Controllable

class App(Controllable):
    
    def __init__(self):
        self.max_path_length = 5
        self.path = [(5, 5), (5, 6), (5, 7)]
        self.selected_leg_index = 0
    
    def press(self, key):
        #if key == Key.B:
        #    self.selected_leg_index = -1 - self.selected_leg_index
        if key == Key.UP:
            self.path = [(self.path[0][0]-1, self.path[0][1])] + self.path

    def show(self):
        def art(x, y):
            if (x, y) in self.path[1:-1]:
                return "O"
            if (x, y) in {self.path[0], self.path[-1]}:
                return "X"
            return " "
        return render_string_art(art, (10, 10))


class Crawler:
    pass

#-------------------------------------
TRANSPARENT = ""

def resolve_char(char):
  return " " if char == TRANSPARENT else char

def render_string_art(string_art, dimension):
  size_x, size_y = dimension
  lines = "\n".join("".join(resolve_char(string_art(i, j)) \
                            for j in range(size_y)) for i in range(size_x))
  return lines
