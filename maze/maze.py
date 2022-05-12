import art
from mazemath import edge

class Maze:

    def __init__(self, objects):
        self.objects = objects
        self.gates = dict()
        self.wall_objects = dict()
        for obj in objects:
            gate = obj.get_gate()
            if gate is not None:
                self.gates[gate.get_edge()] = self.gates.get(gate.get_edge(), []) + [gate]
            wall_object = obj.get_wall_object()
            if wall_object is not None:
                self.wall_objects[wall_object.get_placement()] = self.wall_objects.get(wall_object.get_placement(), []) + [wall_object]

    def can_pass(self, start, end):
        return any(map(lambda gate: gate.is_open(), self._get_gates(start, end)))

    def _get_gates(self, start, end):
        return self.gates.get(edge(start, end), [])

    def _get_wall_objects(self, location, direction):
        return self.wall_objects.get((location, direction), [])
