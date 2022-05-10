from app import Key, Controllable

class App(Controllable):

    def __init__(self):
        self.text = "World!    "
        self.prefix = "Hello "
        self.cursor = 0
        
    def press(self, key):
        if key == Key.RIGHT:
            self.cursor += 1
            self.cursor = min(10, self.cursor)
        if key == Key.LEFT:
            self.cursor -= 1
            self.cursor = max(0, self.cursor)
        if key == Key.UP:
            self.change_char(1)
        if key == Key.DOWN:
            self.change_char(-1)
        if key == Key.A:
            self.set_char(' ')
    
    def show(self):
        return self.prefix + self.text + "\n" + (" " * (self.cursor + len(self.prefix))) + "^"
    
    def change_char(self, amount):
        allowed_chars = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!?."
        index = allowed_chars.find(self.text[self.cursor])
        new_char = allowed_chars[(index + amount) % len(allowed_chars)]
        self.set_char(new_char)
        
    def set_char(self, new_char):
        self.text = self.text[:self.cursor] + new_char + self.text[self.cursor+1:]
