from app import Key, Controllable
from first_person_maze.game import Game, Command

class App(Controllable):

    def __init__(self):
        self.game = Game()

    def press(self, key):
        command = {
            Key.UP: Command.UP,
            Key.DOWN: Command.DOWN,
            Key.LEFT: Command.LEFT,
            Key.RIGHT: Command.RIGHT,
            Key.A: Command.A,
            Key.B: Command.B
        }.get(key)
        if command is not None:
            self.game.execute(command)
    
    def show(self):
        return self.game.render()
