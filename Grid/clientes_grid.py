import tkinter as tk
from tkinter import ttk
import pandas as pd

class CustomersFilterableSortableTable(tk.Toplevel): 
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Clientes Churn - Chile")
        self.geometry("1200x600")

        # Leer el archivo Excel
        self.df = pd.read_excel('Data/Clientes-Churn-Chile-Sky-22102024.xlsx')

        # Obtener las columnas desde el DataFrame
        columns = list(self.df.columns)

        # Crear un frame para los filtros
        filter_frame = tk.Frame(self)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        self.filters = {}
        self.filter_vars = {}

        # Añadir etiquetas y entradas para el filtrado, con salto de línea cada 3 inputs
        for i, col in enumerate(columns):
            # Determinar fila y columna (ahora cada 3 inputs por línea)
            row = i // 3  # Salto de línea cada 3 inputs
            col_in_row = i % 3  # Columna dentro de esa fila

            label = tk.Label(filter_frame, text=f"Filtrar por {col}")
            label.grid(row=row, column=col_in_row*2, padx=5, pady=5, sticky="w")  # Etiqueta en una columna
            self.filter_vars[col] = tk.StringVar()
            filter_entry = tk.Entry(filter_frame, textvariable=self.filter_vars[col])
            filter_entry.grid(row=row, column=col_in_row*2 + 1, padx=5, pady=5)  # Input en la columna siguiente
            filter_entry.bind('<KeyRelease>', self.filter_table)
            self.filters[col] = filter_entry

        # Crear un frame para la tabla y las barras de desplazamiento
        table_frame = tk.Frame(self)
        table_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

        # Crear la tabla con scrollbars
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        # Añadir barras de desplazamiento
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        self.tree.pack(expand=True, fill=tk.BOTH)

        # Calcular el ancho máximo de cada columna basado en el contenido
        column_widths = {}
        for col in columns:
            max_width = max(self.df[col].astype(str).apply(len).max(), len(col))  # Máxima longitud de las celdas
            column_widths[col] = max_width * 10  # Multiplicar por un factor para hacer el ancho más grande si es necesario

        # Establecer las columnas y su ancho
        for col in columns:
            self.tree.heading(col, text=col, command=lambda _col=col: self.sort_by_column(_col, False))
            self.tree.column(col, width=column_widths[col])

        # Cargar los datos del DataFrame en la tabla
        for row in self.df.values:
            self.tree.insert('', tk.END, values=tuple(row))

    def filter_table(self, event=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        filtered_data = self.df
        for col in self.filter_vars:
            val = self.filter_vars[col].get()
            if val:
                filtered_data = filtered_data[filtered_data[col].astype(str).str.contains(val, case=False, na=False)]

        for row in filtered_data.values:
            self.tree.insert('', tk.END, values=tuple(row))

    def sort_by_column(self, col, descending):
        data = []
        for child in self.tree.get_children(''):
            value = self.tree.set(child, col)  # Obtener el valor de la celda
            # Intentar convertir a número si es posible (int o float)
            try:
                value = float(value) if '.' in value else int(value)
            except ValueError:
                pass  # Si no se puede convertir a número, mantenerlo como cadena
            data.append((value, child))

        # Ordenar los datos por el valor de la columna (considerando números y texto)
        data.sort(key=lambda x: x[0], reverse=descending)

        # Reorganizar las filas según el orden
        for ix, item in enumerate(data):
            self.tree.move(item[1], '', ix)

        # Cambiar la función de ordenación para alternar entre ascendente y descendente
        self.tree.heading(col, command=lambda col=col: self.sort_by_column(col, not descending))
