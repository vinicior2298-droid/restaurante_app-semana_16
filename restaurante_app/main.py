import os
import sys
import tkinter as tk 

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView

def main():
    restaurante_servicio = RestauranteServicio()
    
    print("Usuarios cargados en el sistema")
    for u in restaurante_servicio.obtener_usuarios():
        print(f"-Usuario: {u.username} | Rol: {u.rol}")

    app = LoginView(restaurante_servicio)
    app.mainloop()

if __name__ == "__main__":
    main()