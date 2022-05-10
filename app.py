from enum import Enum

class Key(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    A = 4
    B = 5

class Controllable:
    def on_press(self, key):
        pass
    
    def show(self):
        return ""
