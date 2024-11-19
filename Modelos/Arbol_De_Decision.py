from tkinter import messagebox
import tkinter as tk
import pandas as pd
from tkinter import ttk
from Grid.FilterableSortableTable import FilterableSortableTable
from Utils import Utilities
from Modelos.Algoritmos.Arbol_De_Decision import ArbolDeDecisionChurnPredictionModel
from Data.Clientes_Churn_Chile import Clientes_Churn

# Función para analizar los clientes en riesgo usando el modelo Árbol de Decisión
def analyze_risk_clients_arbol(window: tk.Toplevel):
    df = pd.read_excel('Data/Clientes-Churn-Chile-Sky-22102024.xlsx')
    model = ArbolDeDecisionChurnPredictionModel(df)
    result = model.analyze_risk_clients()
    table_window = FilterableSortableTable(window, "Clientes en riesgo de abandono (Árbol de Decisión)", "1200x600", '', custom_data=result)

# Crear la ventana y los elementos gráficos para el modelo Árbol de Decisión
def create_arbol_de_decision_top_level():
    total_rows_in_standar_window = 2
    height = 500
    window = Utilities.create_standar_top_level(
        "Árbol de Decisión", 
        "Modelo Árbol de Decisión para predicción de Churn", 
        height,
        analyze_risk=True,
        analyze_risk_command=analyze_risk_clients_arbol
    )

    df = pd.read_excel('Data/Clientes-Churn-Chile-Sky-22102024.xlsx')

    def create_combobox(label_text, row_num, options):
        label = tk.Label(window, text=label_text)
        label.grid(row=row_num + total_rows_in_standar_window, column=0, padx=10, pady=5, sticky="w")
        
        combobox = ttk.Combobox(window, values=options, width=30)
        combobox.grid(row=row_num + total_rows_in_standar_window, column=1, padx=10, pady=5)
        return combobox
    
    def create_entry(label_text, row_num):
        label = tk.Label(window, text=label_text)
        label.grid(row=row_num + total_rows_in_standar_window, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(window, width=30)
        entry.grid(row=row_num + total_rows_in_standar_window, column=1, padx=10, pady=5)
        return entry
    
    region_entry = create_combobox(Clientes_Churn.Region, 0, df[Clientes_Churn.Region].unique().tolist())
    comuna_entry = create_combobox(Clientes_Churn.Comuna, 1, df[Clientes_Churn.Comuna].unique().tolist())
    provincia_entry = create_combobox(Clientes_Churn.Provincia, 2, df[Clientes_Churn.Provincia].unique().tolist())
    tipo_queja_entry = create_combobox(Clientes_Churn.Tipo_Queja, 6, df[Clientes_Churn.Tipo_Queja].unique().tolist())
    tipo_mantenimiento_entry = create_combobox(Clientes_Churn.Tipo_Mantenimiento, 8, df[Clientes_Churn.Tipo_Mantenimiento].unique().tolist())
    
    velocidad_entry = create_entry(Clientes_Churn.Velocidad_Canal, 3)
    antiguedad_entry = create_entry(Clientes_Churn.Antiguedad, 4)
    quejas_entry = create_entry(Clientes_Churn.Cantidad_Quejas, 5)
    mantenimientos_entry = create_entry(Clientes_Churn.Mantenimientos_Mensuales, 7)
    horas_entry = create_entry(Clientes_Churn.Horas_Afectacion, 9)

    model = ArbolDeDecisionChurnPredictionModel(df)
    model.preprocess_data()
    model.train_model()
    model.evaluate_model(window)

    def predict_churn_arbol():
        try:
            region = region_entry.get()
            comuna = comuna_entry.get()
            provincia = provincia_entry.get()
            velocidad_canal = float(velocidad_entry.get())
            antiguedad = int(antiguedad_entry.get())
            cantidad_quejas = int(quejas_entry.get())
            tipo_queja = tipo_queja_entry.get()
            mantenimientos_mensuales = int(mantenimientos_entry.get())
            tipo_mantenimiento = tipo_mantenimiento_entry.get()
            horas_afectacion = float(horas_entry.get())

            if velocidad_canal <= 0 or antiguedad < 0 or cantidad_quejas < 0 or mantenimientos_mensuales < 0 or horas_afectacion < 0:
                raise ValueError("Por favor ingrese valores válidos para los campos numéricos.")

            region = model.region_label_encoder.transform([region])[0]
            comuna = model.comuna_label_encoder.transform([comuna])[0]
            provincia = model.provincia_label_encoder.transform([provincia])[0]
            tipo_queja = model.tipo_queja_label_encoder.transform([tipo_queja])[0]
            tipo_mantenimiento = model.tipo_mantenimiento_label_encoder.transform([tipo_mantenimiento])[0]

            input_data = [
                region, comuna, provincia, velocidad_canal, antiguedad, cantidad_quejas,
                tipo_queja, mantenimientos_mensuales, tipo_mantenimiento, horas_afectacion
            ]
            
            result = model.predict_churn(input_data)
            messagebox.showinfo("Resultado de la Predicción (Árbol de Decisión)", result, parent=window)
            model.plot_roc_curve()
        
        except ValueError as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}", parent=window)
        except Exception as e:
            messagebox.showerror("Error", f"Error desconocido: {e}", parent=window)

    predict_button = tk.Button(window, text="Predecir Churn (Árbol de Decisión)", command=predict_churn_arbol)
    predict_button.grid(row=10 + total_rows_in_standar_window, column=0, columnspan=2, pady=5)

    Utilities.center_window(window, 800, height)

ARBOL_DE_DECISION = {"label": "Usar el modelo árbol de decisiones", "action": create_arbol_de_decision_top_level}
