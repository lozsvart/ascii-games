
class MazeObject:
    def __init__(self, gate = None, wall_object = None):
        self.gate = gate
        self.wall_object = wall_object

    def get_gate(self):
        return self.gate

    def get_wall_object(self):
        return self.wall_object

class WallObject:
    def __init__(self, placement, art):
        self.placement = placement
        self.art = art

    def get_placement(self):
        return self.placement

    def get_art(self):
        return self.art

class Gate:
    def __init__(self, edge, open_func = lambda: True):
        self.open_func = open_func
        self.edge = edge

    def is_open(self):
        return self.open_func()

    def get_edge(self):
        return self.edge
