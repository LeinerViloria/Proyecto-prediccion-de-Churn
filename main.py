import tkinter as tk
from Modelos import MODELOS

def create_buttons(root, buttons_info):
    for button_info in buttons_info:
        button = tk.Button(root, text=button_info['label'], command=button_info['action'])
        button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ciencias de la computación")

    # Se deshabilita el Maximizar y el Resize
    root.resizable(False, False)
    
    # Añadir un título centrado
    title_label = tk.Label(root, text="Reducción del churn en servicios de conectividad por fibra óptica mediante modelos de aprendizaje automático", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=(20, 10))

    # Añadir una descripción centrada
    description_label = tk.Label(root, text="Se tiene como objetivo reducir la tasa de abandono de clientes (churn) en Sky Network, un proveedor de servicios de conectividad por fibra óptica.", font=("Helvetica", 12))
    description_label.pack(pady=(0, 20))

    create_buttons(root, MODELOS)

    # Para evitar que el ultimo boton se vea muy pegado al borde inferior
    padding_label = tk.Label(root, text="")
    padding_label.pack(pady=(0, 10))

    # Se establece el ancho fijo en píxeles y ajustar la altura automáticamente
    root.update_idletasks()  # Esto asegura que todos los widgets se hayan renderizado
    window_height = root.winfo_reqheight()
    window_width = 1200
    position_right = int(root.winfo_screenwidth()/2 - window_width/2)
    position_down = int(root.winfo_screenheight()/2 - window_height/2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

    root.mainloop()
