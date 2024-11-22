import tkinter as tk
from tkinter import messagebox
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import numpy as np
from Utils import Utilities


class ChurnPredictionModel:
    """Modelo de regresión lineal para predecir riesgo de abandono."""
    def __init__(self, data):
        self.data = data
        self.model = LinearRegression()
        self.label_encoders = {}

    def preprocess_data(self):
        """Preprocesa los datos y codifica las columnas categóricas."""
        categorical_columns = ['Region', 'Comuna', 'Provincia', 'Tipo de Queja', 'Tipo de Mantenimiento']
        for col in categorical_columns:
            le = LabelEncoder()
            self.data[col] = le.fit_transform(self.data[col])
            self.label_encoders[col] = le

    def decode_category(self, col, value):
        """Decodifica un valor categórico al texto original."""
        if col in self.label_encoders:
            return self.label_encoders[col].inverse_transform([value])[0]
        return value

    def train_model(self):
        """Entrena el modelo con los datos."""
        X = self.data[['Region', 'Comuna', 'Provincia', 'Velocidad del Canal (Mb)', 'Antigüedad (meses)',
                       'Cantidad de Quejas', 'Tipo de Queja', 'Mantenimientos Mensuales',
                       'Tipo de Mantenimiento', 'Horas de Afectación']]
        y = self.data['Churn']
        self.model.fit(X, y)
        self.feature_names = X.columns.tolist()  # Guardar nombres de características

    def predict(self, client_data):
        """Realiza la predicción del riesgo de abandono para un cliente."""
        client_df = pd.DataFrame(client_data, columns=self.feature_names)  # Convertir entrada a DataFrame
        return self.model.predict(client_df)[0]

    def explain_prediction(self, client_data):
        """Explica los factores más importantes que contribuyen a la predicción."""
        feature_importance = np.abs(self.model.coef_)
        explanation = sorted(
            zip(self.feature_names, feature_importance * client_data.flatten()),
            key=lambda x: -x[1]
        )
        return explanation


def create_regresion_lineal_top_level():
    """Crea la ventana para predecir el riesgo de abandono."""
    height = 500
    window = Utilities.create_standar_top_level(
        "Predicción de Churn",
        "Modelo de Regresión Lineal para Predicción de Riesgo de Abandono",
        height
    )

    try:
        df = pd.read_excel('Data/Clientes-Churn-Chile-Sky-22102024.xlsx')
        # Generar datos ficticios de churn si no existe la columna
        if 'Churn' not in df.columns:
            df['Churn'] = np.random.choice([0, 1], size=len(df))
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo de datos.", parent=window)
        return
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al cargar los datos: {e}", parent=window)
        return

    model = ChurnPredictionModel(df)
    model.preprocess_data()
    model.train_model()

    def predict_churn():
        try:
            # Obtener ID del cliente
            client_id = client_id_entry.get()
            client_row = df[df['ID'] == int(client_id)]

            if client_row.empty:
                raise ValueError("No se encontró un cliente con ese ID.")

            # Preparar los datos del cliente para predicción
            client_data = client_row[[
                'Region', 'Comuna', 'Provincia', 'Velocidad del Canal (Mb)', 'Antigüedad (meses)',
                'Cantidad de Quejas', 'Tipo de Queja', 'Mantenimientos Mensuales',
                'Tipo de Mantenimiento', 'Horas de Afectación'
            ]]
            client_data_np = client_data.iloc[0:1].to_numpy()

            churn_probability = model.predict(client_data_np)

            # Explicación de la predicción
            explanation = model.explain_prediction(client_data_np)
            explanation_text = "\n".join([f"{feature}: {impact:.2f}" for feature, impact in explanation[:3]])

            # Decodificar valores categóricos
            region_text = model.decode_category('Region', int(client_row.iloc[0]['Region']))
            tipo_queja_text = model.decode_category('Tipo de Queja', int(client_row.iloc[0]['Tipo de Queja']))
            tipo_mantenimiento_text = model.decode_category('Tipo de Mantenimiento', int(client_row.iloc[0]['Tipo de Mantenimiento']))

            # Crear texto con datos de entrada
            client_data_text = (
                f"ID: {int(client_row.iloc[0]['ID'])}\n"
                f"Región: {region_text}\n"
                f"Comuna: {model.decode_category('Comuna', int(client_row.iloc[0]['Comuna']))}\n"
                f"Provincia: {model.decode_category('Provincia', int(client_row.iloc[0]['Provincia']))}\n"
                f"Velocidad del Canal (Mb): {client_row.iloc[0]['Velocidad del Canal (Mb)']}\n"
                f"Antigüedad (meses): {client_row.iloc[0]['Antigüedad (meses)']}\n"
                f"Cantidad de Quejas: {client_row.iloc[0]['Cantidad de Quejas']}\n"
                f"Tipo de Queja: {tipo_queja_text}\n"
                f"Mantenimientos Mensuales: {client_row.iloc[0]['Mantenimientos Mensuales']}\n"
                f"Tipo de Mantenimiento: {tipo_mantenimiento_text}\n"
                f"Horas de Afectación: {client_row.iloc[0]['Horas de Afectación']}"
            )

            # Generar párrafo explicativo si el cliente tiene alto riesgo
            if churn_probability > 0.5:
                factors = [f"{feature}" for feature, impact in explanation[:3]]
                reasons_text = (
                    f"El cliente tiene un alto riesgo de abandono debido a los siguientes factores principales: "
                    f"{', '.join(factors)}. Estos factores sugieren problemas potenciales en el servicio ofrecido."
                )
            else:
                reasons_text = (
                    "El cliente no tiene un alto riesgo de abandono basado en los datos proporcionados. "
                    "Esto indica que el cliente probablemente esté satisfecho con el servicio."
                )

            # Agregar rango explicativo para la probabilidad
            range_explanation = (
                "\nInterpretación del rango de probabilidades:\n"
                "- 0.0 a 0.3: Bajo riesgo de abandono. Cliente satisfecho.\n"
                "- 0.3 a 0.6: Riesgo moderado. Se recomienda revisar el servicio.\n"
                "- 0.6 a 1.0: Alto riesgo de abandono. Atención prioritaria necesaria."
            )

            # Mostrar resultados
            messagebox.showinfo(
                "Resultado",
                f"Riesgo de Abandono: {'Sí' if churn_probability > 0.5 else 'No'}\n"
                f"Probabilidad: {churn_probability:.2f}\n\n"
                f"Factores principales:\n{explanation_text}\n\n"
                f"Datos de Entrada:\n{client_data_text}\n\n"
                f"{reasons_text}\n"
                f"{range_explanation}"
            )

        except ValueError as e:
            messagebox.showerror("Error de entrada", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error desconocido", f"Error: {e}")

    # Crear interfaz para ingresar ID del cliente
    client_id_label = tk.Label(window, text="Ingrese ID del Cliente:")
    client_id_label.grid(row=2, column=0, padx=10, pady=15, sticky="e")

    client_id_entry = tk.Entry(window, width=30)
    client_id_entry.grid(row=2, column=1, padx=10, pady=15, sticky="w")

    predict_button = tk.Button(window, text="Predecir Riesgo de Abandono", command=predict_churn)
    predict_button.grid(row=3, column=0, columnspan=2, pady=20)

    Utilities.center_window(window, 800, height)


# Registro del modelo para el menú
REGRESION_LINEAL = {"label": "Usar Algoritmo Regresion lineal", "action": create_regresion_lineal_top_level}
