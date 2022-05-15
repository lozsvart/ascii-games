from tkinter import ttk, Tk, Text
from app import Key
from menu import MenuApp

MENU = MenuApp()

KEY_MAP = {
    'space': Key.A,
    'Return': Key.B,
    'plus': Key.B,
    'minus': Key.A,
    'Right': Key.RIGHT,
    'Left': Key.LEFT,
    'Up': Key.UP,
    'Down': Key.DOWN,
    'd': Key.RIGHT,
    'a': Key.LEFT,
    'w': Key.UP,
    's': Key.DOWN
}   

def update_view():
    text_area['state'] = 'normal'
    text_area.replace('1.0', '46.71', MENU.show())
    text_area['state'] = 'disabled'

def press(event, text_area):
    if event.keysym in KEY_MAP:
        MENU.press(KEY_MAP[event.keysym])
        update_view()

if __name__ == "__main__":
    root = Tk()
    
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    text_area = Text(frm, height = 30, width = 72, font = ("Courier", 14))
    text_area.grid(column=0, row=0)
    update_view()
    root.bind('<KeyPress>', lambda event: press(event, text_area))
    root.title("Widgets")
    root.mainloop()
