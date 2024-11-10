import tkinter as tk
from Modelos.Knn import KNN
from Modelos.Arbol_De_Desicion import ARBOL_DE_DESICION
from Modelos.Regresion_Lineal import REGRESION_LINEAL
from Modelos.Regresion_Lineal_Multiple import REGRESION_LINEAL_MULTIPLE

def center_window(root, width=300, height=200):
    # Obtiene el ancho y alto de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Se calculan las posiciones para centrar la ventana
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Establece el tamaño y la posición de la ventana
    root.geometry(f'{width}x{height}+{x}+{y}')

def create_buttons(root, buttons_info):
    for button_info in buttons_info:
        button = tk.Button(root, text=button_info['label'], command=button_info['action'])
        button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Proyecto de predicción de Churn")

    buttons_info = [
        KNN,
        ARBOL_DE_DESICION,
        REGRESION_LINEAL,
        REGRESION_LINEAL_MULTIPLE
    ]

    create_buttons(root, buttons_info)
    center_window(root, 400, 200)
    root.mainloop()
