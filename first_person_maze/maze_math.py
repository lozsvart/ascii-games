from operator import add

def rotate_left(vector):
    return (-vector[1], vector[0])

def negate(vector):
    return (-vector[0], -vector[1])

def add_tuples(v1, v2):
  return tuple(map(add, v1, v2))

def create_edge(v1, v2):
  return frozenset({v1, v2})

def get_other_node(edge, node):
  for a_node in edge:
    if a_node != node:
      return a_node

def get_distance(coord, coords):
  def dist(first, second):
    return max(abs(first[0]-second[0]), abs(first[1]-second[1]))
  return min(map(lambda coor: dist(coord, coor), coords))

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

def get_relative_direction(start, end):
    start_index = [N, W, S, E].index(start)
    end_index = ["North", "West", "South", "East"].index(end)
    return ["front", "left", "back", "right"][(end_index - start_index) % 4]


def get_direction_name(location, neighbor):
    for direction in DIRECTIONS:
      if add_tuples(location, DIRECTIONS[direction]) == tuple(neighbor):
        return direction

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
        door = maze_edges.get(frozenset({middle, field}))
        if door is not None and door.is_open():
            result.append(junction)
            
    return set(result)
