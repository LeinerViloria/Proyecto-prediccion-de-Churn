import tkinter as tk
from tkinter import messagebox

import pandas as pd
from Utils import Utilities
from Modelos.Algoritmos.Red_Neuronal_Perceptron import ChurnPredictionModel

def create_red_neuronal_top_level():
    window = Utilities.create_standar_top_level("Red neuronal", "Perceptron - Tipo de red neuronal artificial")
    
    df = pd.read_excel('Data/Clientes-Churn-Chile-Sky-22102024.xlsx')

    # Instancia de tu modelo de predicción
    model = ChurnPredictionModel(df)  # df es tu DataFrame
    model.preprocess_data()
    model.train_model()

    def create_entry(label_text, row_num):
        label = tk.Label(window, text=label_text)
        label.grid(row=row_num, column=0)
        entry = tk.Entry(window)
        entry.grid(row=row_num, column=1)
        return entry
    
    # Crear las entradas para las variables del modelo
    region_entry = create_entry('Region', 0)
    comuna_entry = create_entry('Comuna', 1)
    provincia_entry = create_entry('Provincia', 2)
    velocidad_entry = create_entry('Velocidad del Canal (Mb)', 3)
    antiguedad_entry = create_entry('Antigüedad (meses)', 4)
    quejas_entry = create_entry('Cantidad de Quejas', 5)
    tipo_queja_entry = create_entry('Tipo de Queja', 6)
    mantenimientos_entry = create_entry('Mantenimientos Mensuales', 7)
    tipo_mantenimiento_entry = create_entry('Tipo de Mantenimiento', 8)
    horas_entry = create_entry('Horas de Afectación', 9)

    # Función para hacer la predicción
    def predict_churn():
        try:
            # Obtener los valores de las entradas
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

            # Validación de los valores numéricos
            if velocidad_canal <= 0 or antiguedad < 0 or cantidad_quejas < 0 or mantenimientos_mensuales < 0 or horas_afectacion < 0:
                raise ValueError("Por favor ingrese valores válidos para los campos numéricos.")

            # Codificación de variables categóricas
            region = model.le.transform([region])[0]
            comuna = model.le.transform([comuna])[0]
            provincia = model.le.transform([provincia])[0]
            tipo_queja = model.le.transform([tipo_queja])[0]
            tipo_mantenimiento = model.le.transform([tipo_mantenimiento])[0]

            # Crear el vector de entrada para la predicción
            input_data = [
                region, comuna, provincia, velocidad_canal, antiguedad, cantidad_quejas,
                tipo_queja, mantenimientos_mensuales, tipo_mantenimiento, horas_afectacion
            ]
            
            result = model.predict_churn(input_data)
            
            # Mostrar el resultado
            messagebox.showinfo("Resultado de la Predicción", result)
        
        except ValueError as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error desconocido: {e}")

    predict_button = tk.Button(window, text="Predecir Churn", command=predict_churn)
    predict_button.grid(row=10, column=0, columnspan=2, pady=10)

    # Ajustar la posición de la ventana
    Utilities.center_window(window, 800, 400)



RED_NEURONAL = {"label": "Usar la red neuronal", "action": create_red_neuronal_top_level}