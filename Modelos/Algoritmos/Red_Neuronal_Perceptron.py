import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from Data.Clientes_Churn_Chile import Clientes_Churn

class ChurnPredictionModel:
    def __init__(self, data):
        self.df = data
        self.model = None
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
        self.categorias = None

    def preprocess_data(self):
        self.df[Clientes_Churn.Region] = self.region_label_encoder.fit_transform(self.df[Clientes_Churn.Region])
        self.df[Clientes_Churn.Comuna] = self.comuna_label_encoder.fit_transform(self.df[Clientes_Churn.Comuna])
        self.df[Clientes_Churn.Provincia] = self.provincia_label_encoder.fit_transform(self.df[Clientes_Churn.Provincia])
        self.df[Clientes_Churn.Tipo_Queja] = self.tipo_queja_label_encoder.fit_transform(self.df[Clientes_Churn.Tipo_Queja])
        self.df[Clientes_Churn.Tipo_Mantenimiento] = self.tipo_mantenimiento_label_encoder.fit_transform(self.df[Clientes_Churn.Tipo_Mantenimiento])

        umbral_quejas = self.df[Clientes_Churn.Cantidad_Quejas].quantile(0.75)  # Percentil 75
        umbral_mantenimientos = self.df[Clientes_Churn.Mantenimientos_Mensuales].quantile(0.75) # Percentil 75
        
        # Se define la variable objetivo 'Churn' basándonos en la cantidad de quejas y mantenimientos mensuales
        self.df['Churn'] = ((self.df[Clientes_Churn.Cantidad_Quejas] > umbral_quejas) | (self.df[Clientes_Churn.Mantenimientos_Mensuales] > umbral_mantenimientos)).astype(int)
        
        # Variables independientes y dependientes
        X = self.df[[Clientes_Churn.Region, Clientes_Churn.Comuna, Clientes_Churn.Provincia, Clientes_Churn.Velocidad_Canal, 
                     Clientes_Churn.Antiguedad, Clientes_Churn.Tipo_Mantenimiento, Clientes_Churn.Tipo_Queja, 
                     Clientes_Churn.Mantenimientos_Mensuales, Clientes_Churn.Tipo_Mantenimiento, Clientes_Churn.Horas_Afectacion]]
        y = self.df['Churn']
        
        # Dividir en conjunto de entrenamiento y prueba
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # Estandarizar los datos
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)

    def train_model(self):
        # Crear y entrenar el modelo
        self.model = MLPClassifier(hidden_layer_sizes=(5,), max_iter=1000, random_state=42)
        self.model.fit(self.X_train, self.y_train)
    
    def evaluate_model(self):
        # Predicción y evaluación
        y_pred = self.model.predict(self.X_test)
        print("Reporte de clasificación:\n", classification_report(self.y_test, y_pred))
        print("Matriz de confusión:\n", confusion_matrix(self.y_test, y_pred))

    def predict_churn(self, new_data):
        # Predicción para un nuevo cliente
        new_data = np.array([new_data])  # Los datos deben ser una lista de listas
        new_data = self.scaler.transform(new_data)
        prediccion_churn = self.model.predict(new_data)
        
        return "El cliente está en riesgo de abandono (Churn)." if prediccion_churn[0] == 1 else "El cliente no está en riesgo de abandono (Churn)."