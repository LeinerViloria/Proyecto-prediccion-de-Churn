import tkinter as tk
from Grid.FilterableSortableTable import FilterableSortableTable
from Utils import Utilities

def center_window(root, width=400, height=200):
    # Obtiene el ancho y alto de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Se calculan las posiciones para centrar la ventana
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Establece el tamaño y la posición de la ventana
    root.geometry(f'{width}x{height}+{x}+{y}')

def create_standar_top_level(title: str, main_label: str) -> tk.Toplevel:
    new_window = tk.Toplevel()
    new_window.title(title)
    
    label = tk.Label(new_window, text=main_label, font=("Helvetica", 16, "bold"))
    label.pack(pady=10)

    def open_filterable_table():
        table_window = FilterableSortableTable(new_window, "Clientes Churn - Chile", "1200x600", 'Data/Clientes-Churn-Chile-Sky-22102024.xlsx') 

    button = tk.Button(new_window, text="Ver información", command=open_filterable_table)
    button.pack(pady=5)

    Utilities.center_window(new_window, 800, 400)

    return new_window
