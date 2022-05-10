from app import Key, Controllable

class Calculator:
    
    def __init__(self):
        self.content = "0"
        self.insert_mode = False
        self.operation = None
        self.memory = None
    
    def on_press(self, button):
        if button in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
            if self.insert_mode:
                self.content += button
            else:
                self.content = button
                self.insert_mode = True

        if button in {"+", "-", "*", "/"}:
            self.memory = self.get_content()
            self.insert_mode = False
            self.operation = button

        if button == ".":
            if self.insert_mode and "." not in self.content:
                self.content += "."
            elif not self.insert_mode:
                self.content = "0."
                self.insert_mode = True

        if button == "=":
            self.do_operation()
            self.insert_mode = False

    def do_operation(self):
        if self.operation is None:
            return
        op_function = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y
        }.get(self.operation)
        # TODO handle division by zero
        if self.memory is not None:
            self.content = str(op_function(float(self.memory), float(self.content)))
    
    def get_content(self):
        return self.content

class App(Controllable):
    
    def __init__(self):
        self.calculator = Calculator()
        self.selected_button = (1, 0)
        self.buttons = [[".", "0", "=", "/"], ["1", "2", "3", "*"], ["4", "5", "6", "-"], ["7", "8", "9", "+"]]
    
    def on_press(self, key):
        if key == Key.A:
            self.push_button()
        elif key == Key.RIGHT:
            self.move_selection((0, 1))
        elif key == Key.LEFT:
            self.move_selection((0, -1))
        elif key == Key.UP:
            self.move_selection((1, 0))
        elif key == Key.DOWN:
            self.move_selection((-1, 0))

    def push_button(self):
        button = self.get_selected()
        self.calculator.on_press(button)

    def get_selected(self):
        x, y = self.selected_button
        return self.buttons[x][y]

    def move_selection(self, vec):
        x = min(max(0, self.selected_button[0] + vec[0]), len(self.buttons) - 1)
        y = min(max(0, self.selected_button[1] + vec[1]), len(self.buttons[0]) - 1)
        self.selected_button = x, y

    def get_display(self):
        return self.calculator.get_content().rjust(15)

    def get_button(self, x, y):
        if (x, y) == self.selected_button:
            return "[" + self.buttons[x][y] + "]"
        return " " + self.buttons[x][y] + " "

    def show(self):
        return f""" _____________________
|  _________________  |
| | {self.get_display()} | |
| |_________________| |
|  ___ ___ ___   ___  |
| |{self.get_button(3, 0)}|{self.get_button(3, 1)}|{self.get_button(3, 2)}| |{self.get_button(3, 3)}| |
| |___|___|___| |___| |
| |{self.get_button(2, 0)}|{self.get_button(2, 1)}|{self.get_button(2, 2)}| |{self.get_button(2, 3)}| |
| |___|___|___| |___| |
| |{self.get_button(1, 0)}|{self.get_button(1, 1)}|{self.get_button(1, 2)}| |{self.get_button(1, 3)}| |
| |___|___|___| |___| |
| |{self.get_button(0, 0)}|{self.get_button(0, 1)}|{self.get_button(0, 2)}| |{self.get_button(0, 3)}| |
| |___|___|___| |___| |
|_____________________|"""
