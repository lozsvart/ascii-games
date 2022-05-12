
class Maze:

    def __init__(self, objects):
        self.objects = objects

    def can_pass(self, start, end):
        return any(map(lambda gate: gate.is_open(), self._get_gates(start, end)))

    def _get_gates(self, start, end):
        return []
    
    def _get_wall_objects(self, location, direction):
        return []

class MazeObject:
    def get_gate(self):
        return None

    def get_wall_object(self):
        return None

class Gate:
    def is_open(self):
        return True

    def get_edge(self):
        return (None, None)
