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

def create_standar_top_level(title: str, main_label: str, height: int = 400) -> tk.Toplevel:
    new_window = tk.Toplevel()
    new_window.title(title)
    
    # Crear un Label para el título y ubicarlo centrado horizontalmente
    label = tk.Label(new_window, text=main_label, font=("Helvetica", 16, "bold"))
    label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")  # Centrado horizontal con sticky="ew"
    
    # Función para abrir la tabla
    def open_filterable_table():
        table_window = FilterableSortableTable(new_window, "Clientes Churn - Chile", "1200x600", 'Data/Clientes-Churn-Chile-Sky-22102024.xlsx') 

    button = tk.Button(new_window, text="Ver información", command=open_filterable_table)
    button.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    
    new_window.grid_columnconfigure(0, weight=1)
    new_window.grid_columnconfigure(1, weight=1)

    Utilities.center_window(new_window, 800, height)

    return new_window
