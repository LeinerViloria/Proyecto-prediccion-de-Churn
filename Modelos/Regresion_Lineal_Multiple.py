import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from Utils import Utilities

def create_regresion_lineal_multiple_top_level():
    window = Utilities.create_standar_top_level(
        "Regresión Lineal Múltiple",
        "Modelo de Regresión Lineal Múltiple",
        600
    )

    # Cargar datos desde el archivo Excel
    try:
        df = pd.read_excel('Data/Clientes-Churn-Chile-Sky-22102024.xlsx')

        # Verificar columnas requeridas en el archivo Excel
        required_columns = [
            'Velocidad del Canal (Mbps)', 
            'Antigüedad (años)', 
            'Cantidad de Quejas', 
            'Mantenimientos Mensuales', 
            'Horas de Afectación'
        ]
        target_column = 'Probabilidad de Churn'
        
        if not all(col in df.columns for col in required_columns + [target_column]):
            raise KeyError(f"El archivo no contiene todas las columnas requeridas: {required_columns + [target_column]}")
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo de datos.", parent=window)
        return
    except KeyError as e:
        messagebox.showerror("Error", f"Error en los datos: {e}", parent=window)
        return

    # Preparar datos
    X = df[required_columns]
    y = df[target_column]

    # Dividir los datos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crear modelo
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predecir
    y_pred = model.predict(X_test)

    # Métricas del modelo
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Mostrar métricas en ventana
    metrics_label = ttk.Label(window, text=f"Error cuadrático medio (MSE): {mse:.2f}\nR²: {r2:.2f}")
    metrics_label.pack(pady=10)

    # Gráfico de predicciones vs reales
    def plot_results():
        plt.scatter(y_test, y_pred, alpha=0.7)
        plt.xlabel("Valores reales")
        plt.ylabel("Predicciones")
        plt.title("Predicciones vs Valores Reales")
        plt.grid(True)
        plt.show()

    plot_button = tk.Button(window, text="Mostrar Gráfico", command=plot_results)
    plot_button.pack(pady=10)

    # Ajustar ventana
    Utilities.center_window(window, 800, 600)


# Diccionario para incluir en el menú
REGRESION_LINEAL_MULTIPLE = {
    "label": "Usar el modelo de regresión lineal múltiple",
    "action": create_regresion_lineal_multiple_top_level
}
