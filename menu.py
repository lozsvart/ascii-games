from app import Key, Controllable
import importlib

APPS = [line.strip() for line in open('plugins.txt', 'r').readlines()]

class MenuApp(Controllable):

    def __init__(self):
        self.app = None
        self.selected = 0

    def on_press(self, key):
        if self.app is None:
            if key in {Key.A, Key.B}:
                self.app = importlib.import_module(APPS[self.selected], '.').App()
            if key == Key.DOWN:
                self.selected += 1
            if key == Key.UP:
                self.selected -= 1
            self.selected = max(0, min(len(APPS) - 1, self.selected))
        else:
            self.app.on_press(key)

    def render(self):
        return "Available games:\n" +\
            "\n".join(("  " if self.selected != i else " >") + app_name for i, app_name in enumerate(APPS))

    def show(self):
        if self.app is None:
            return self.render()
        else:
            return self.app.show()
