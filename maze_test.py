from first_person_maze.game import Game, Command
import unittest

U = Command.UP
D = Command.DOWN
L = Command.LEFT
R = Command.RIGHT
A = Command.A

class MazeTest(unittest.TestCase):

    def test_solution(self):
        game = Game()
        commands = [R, U, R, U, L, U, L, U, R, U, U, R, U, L, A, U, A,
                    L, U, L, U, U, L, U, R, U, R, U, L, U,
                    L, U, U, U, A, U, U, U, U, L, U, U, U, U, A, L, U, L, U, R, U, U, R, U, U, L, U, L, U, U]
        for command in commands:
            game.execute(command)
        self.assertIn('Congrat', game.render())

if __name__ == "__main__":
    unittest.main()
