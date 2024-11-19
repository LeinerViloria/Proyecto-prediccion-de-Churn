from tkinter import messagebox
import tkinter as tk
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from Charts.Roc_Chart import Roc_Chart
from Data.Clientes_Churn_Chile import Clientes_Churn

class KNNChurnPredictionModel:
    def __init__(self, data, n_neighbors=5):
        self.df = data
        self.model = None
        self.n_neighbors = n_neighbors
        self.scaler = StandardScaler()
        self.region_label_encoder = LabelEncoder()
        self.comuna_label_encoder = LabelEncoder()
        self.provincia_label_encoder = LabelEncoder()
        self.tipo_queja_label_encoder = LabelEncoder()
        self.tipo_mantenimiento_label_encoder = LabelEncoder()
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def preprocess_data(self):
        self.df[Clientes_Churn.Region] = self.region_label_encoder.fit_transform(self.df[Clientes_Churn.Region])
        self.df[Clientes_Churn.Comuna] = self.comuna_label_encoder.fit_transform(self.df[Clientes_Churn.Comuna])
        self.df[Clientes_Churn.Provincia] = self.provincia_label_encoder.fit_transform(self.df[Clientes_Churn.Provincia])
        self.df[Clientes_Churn.Tipo_Queja] = self.tipo_queja_label_encoder.fit_transform(self.df[Clientes_Churn.Tipo_Queja])
        self.df[Clientes_Churn.Tipo_Mantenimiento] = self.tipo_mantenimiento_label_encoder.fit_transform(self.df[Clientes_Churn.Tipo_Mantenimiento])

        umbral_quejas = self.df[Clientes_Churn.Cantidad_Quejas].quantile(0.75)
        umbral_mantenimientos = self.df[Clientes_Churn.Mantenimientos_Mensuales].quantile(0.75)
        
        self.df['Churn'] = ((self.df[Clientes_Churn.Cantidad_Quejas] > umbral_quejas) | (self.df[Clientes_Churn.Mantenimientos_Mensuales] > umbral_mantenimientos)).astype(int)
        
        X = self.df[[Clientes_Churn.Region, Clientes_Churn.Comuna, Clientes_Churn.Provincia, Clientes_Churn.Velocidad_Canal, 
                     Clientes_Churn.Antiguedad, Clientes_Churn.Tipo_Mantenimiento, Clientes_Churn.Tipo_Queja, 
                     Clientes_Churn.Mantenimientos_Mensuales, Clientes_Churn.Tipo_Mantenimiento, Clientes_Churn.Horas_Afectacion]]
        y = self.df['Churn']
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)

    def train_model(self):
        self.model = KNeighborsClassifier(n_neighbors=self.n_neighbors)
        self.model.fit(self.X_train, self.y_train)
    
    def evaluate_model(self, window: tk.Toplevel):
        y_pred = self.model.predict(self.X_test)
        messagebox.showinfo("Resultado de la Predicción", classification_report(self.y_test, y_pred), parent=window)
        messagebox.showinfo("Matriz de confusión", f'Matriz de confusión:\n{confusion_matrix(self.y_test, y_pred).tolist()}', parent=window)

    def predict_churn(self, new_data):
        new_data = np.array([new_data])
        new_data = self.scaler.transform(new_data)
        prediccion_churn = self.model.predict(new_data)
        
        return "El cliente está en riesgo de abandono (Churn)." if prediccion_churn[0] == 1 else "El cliente no está en riesgo de abandono (Churn)."
    
    def plot_roc_curve(self):
        y_prob = self.model.predict_proba(self.X_test)[:, 1]
        roc_analyzer = Roc_Chart(self.y_test, y_prob)

        roc_analyzer.calculate_roc()
        roc_analyzer.plot_roc()

    def analyze_risk_clients(self):
        self.preprocess_data()
        self.train_model()

        X_all = self.df[[Clientes_Churn.Region, Clientes_Churn.Comuna, Clientes_Churn.Provincia, Clientes_Churn.Velocidad_Canal, 
                         Clientes_Churn.Antiguedad, Clientes_Churn.Tipo_Mantenimiento, Clientes_Churn.Tipo_Queja, 
                         Clientes_Churn.Mantenimientos_Mensuales, Clientes_Churn.Tipo_Mantenimiento, Clientes_Churn.Horas_Afectacion]]
        X_all_scaled = self.scaler.transform(X_all)
        self.df['Churn_Pred'] = self.model.predict(X_all_scaled)

        max_quejas = self.df[Clientes_Churn.Cantidad_Quejas].max()
        max_horas_afectacion = self.df[Clientes_Churn.Horas_Afectacion].max()

        self.df[Clientes_Churn.Satisfaccion] = 1 - (self.df[Clientes_Churn.Horas_Afectacion] / max_horas_afectacion)
        self.df[Clientes_Churn.Insatisfaccion] = self.df[Clientes_Churn.Cantidad_Quejas] / max_quejas

        clientes_en_riesgo = self.df[self.df['Churn_Pred'] == 1]
        return clientes_en_riesgo[[Clientes_Churn.Id, Clientes_Churn.Velocidad_Canal, Clientes_Churn.Antiguedad, Clientes_Churn.Cantidad_Quejas, Clientes_Churn.Mantenimientos_Mensuales, Clientes_Churn.Satisfaccion, Clientes_Churn.Insatisfaccion]]
