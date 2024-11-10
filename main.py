import tkinter as tk
from Modelos import MODELOS
from Utils import Utilities

def create_buttons(root, buttons_info):
    for button_info in buttons_info:
        button = tk.Button(root, text=button_info['label'], command=button_info['action'])
        button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Proyecto de predicción de Churn")

    create_buttons(root, MODELOS)
    Utilities.center_window(root, 400, 200)
    root.mainloop()
