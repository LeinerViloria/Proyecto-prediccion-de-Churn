import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import numpy as np

class Roc_Chart:
    def __init__(self, y_true, y_scores):
        """
        Inicializa la clase con los valores verdaderos (y_true) y las puntuaciones predichas (y_scores).

        :param y_true: Lista o array de los valores reales (0 o 1)
        :param y_scores: Lista o array de las probabilidades o puntuaciones predichas por el modelo
        """
        self.y_true = np.array(y_true)
        self.y_scores = np.array(y_scores)
        self.fpr = None  # False Positive Rate
        self.tpr = None  # True Positive Rate
        self.thresholds = None  # Umbrales de decisión
        self.roc_auc = None  # Área bajo la curva (AUC)

    def calculate_roc(self):
        """
        Calcula la curva ROC y el área bajo la curva (AUC).
        """
        self.fpr, self.tpr, self.thresholds = roc_curve(self.y_true, self.y_scores)
        self.roc_auc = auc(self.fpr, self.tpr)
        
    def plot_roc(self):
        """
        Genera la gráfica de la curva ROC y muestra el área bajo la curva (AUC).
        """
        if self.fpr is None or self.tpr is None:
            raise ValueError("Se debe calcular primero la curva ROC con 'calculate_roc()'.")

        plt.figure(figsize=(8, 6))
        plt.plot(self.fpr, self.tpr, color='darkorange', lw=2, label=f'Curva ROC (AUC = {self.roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')  # Línea diagonal
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Tasa de Falsos Positivos (FPR)')
        plt.ylabel('Tasa de Verdaderos Positivos (TPR)')
        plt.title('Curva ROC')
        plt.legend(loc="lower right")
        plt.grid(True)
        plt.show()