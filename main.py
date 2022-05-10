from tkinter import ttk, Tk, Text
from app import Key
from menu import MenuApp

menu = MenuApp()

def on_press(event, text_area):
    keymap = {
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
    if event.keysym in keymap:
        menu.on_press(keymap[event.keysym])
    else:
        return
    text_area['state'] = 'normal'
    text_area.replace('1.0', '46.71', menu.show())
    text_area['state'] = 'disabled'

if __name__ == "__main__":
    root = Tk()
    
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    text_area = Text(frm, height = 46, width = 72, font = ("Courier", 14))
    text_area.insert('1.0', menu.show())
    text_area['state'] = 'disabled'
    text_area.grid(column=0, row=0)
    root.bind('<KeyPress>', lambda event: on_press(event, text_area))
    root.title("Widgets")
    root.mainloop()
