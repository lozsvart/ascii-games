from operator import add

def rotate_left(vector):
    return (-vector[1], vector[0])

def negate(vector):
    return (-vector[0], -vector[1])

def add_tuples(v1, v2):
  return tuple(map(add, v1, v2))

def create_edge(v1, v2):
  return frozenset({v1, v2})
