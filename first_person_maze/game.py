from first_person_maze.old_maze import *
from first_person_maze.command import Command

class Game:
    def __init__(self):
        self.maze = get_default_maze()
        self.status = get_default_status()

    def execute(self, command):
        self.status = get_new_status(command, self.status, self.maze)

    def render(self):
        return render_status(self.maze, self.status, get_maze_art(self.maze, self.status))

