import pandas as pd
from tkinter import messagebox
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

class LinearRegressionModel:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.model = LinearRegression()
        self.feature_columns = []  # Se establecerán más adelante
        self.target_column = ""
        self.x_train = self.x_test = self.y_train = self.y_test = None

    def preprocess_data(self, features, target):
        """
        Preprocesa los datos dividiéndolos en conjuntos de entrenamiento y prueba.
        Las columnas son mapeadas a los nombres reales del archivo cargado.
        """
        # Renombrar las columnas del DataFrame a nombres estándar
        column_mapping = {
            "Velocidad del Canal (Mbps)": "Velocidad_Canal",
            "Antigüedad (años)": "Antiguedad",
            "Cantidad de Quejas": "Cantidad_Quejas",
            "Mantenimientos (mensuales)": "Mantenimientos_Mensuales",
            "Horas de Afectación (mensuales)": "Horas_Afectacion",
            "Probabilidad de Churn": "Churn"
        }
        self.dataframe.rename(columns=column_mapping, inplace=True)

        # Mostrar las columnas actuales para depuración
        print("Columnas actuales del DataFrame:", self.dataframe.columns)

        # Verificar que las columnas de características y objetivo existan en el DataFrame
        missing_features = [feature for feature in features if feature not in self.dataframe.columns]
        missing_target = target if target not in self.dataframe.columns else None

        if missing_features or missing_target:
            raise KeyError(f"Faltan columnas: {missing_features} o columna objetivo: {missing_target}")

        # Mapear las características y el objetivo
        mapped_features = [column_mapping[feature] for feature in features]
        mapped_target = column_mapping[target]

        self.feature_columns = mapped_features
        self.target_column = mapped_target

        X = self.dataframe[mapped_features]
        y = self.dataframe[mapped_target]

        # Dividir los datos en conjuntos de entrenamiento y prueba
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

    def train_model(self):
        """Entrena el modelo de regresión lineal."""
        self.model.fit(self.x_train, self.y_train)

    def evaluate_model(self, window=None):
        """
        Evalúa el modelo utilizando los datos de prueba.
        Muestra los resultados en un mensaje de Tkinter si se proporciona una ventana.
        """
        y_pred = self.model.predict(self.x_test)
        mse = mean_squared_error(self.y_test, y_pred)
        r2 = r2_score(self.y_test, y_pred)

        message = f"Error Cuadrático Medio (MSE): {mse:.2f}\nR^2 Score: {r2:.2f}"
        if window:
            messagebox.showinfo("Evaluación del Modelo", message, parent=window)
        else:
            print(message)

    def predict(self, input_data):
        """
        Realiza una predicción utilizando el modelo entrenado.

        Args:
            input_data (list): Lista de valores para las características de entrada.

        Returns:
            float: Predicción del modelo.
        """
        return self.model.predict([input_data])[0]
