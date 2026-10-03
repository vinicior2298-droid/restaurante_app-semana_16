import tkinter as tk
from tkinter import messagebox
from ui.main_view import MainView
from pathlib import Path
from PIL import Image, ImageTk

class LoginView(tk.Tk):
    def __init__(self, servicio):
        super().__init__()
        self.servicio = servicio

        self.title("Acceso al Sistema - Restaurante")
        self.geometry("500x500")
        self.resizable(False, False)
        self.config(bg="#f4f6f7")

        self.logo_login = None 
        self._cargar_logo()

        self._crear_interfaz()

    def _crear_interfaz(self):
        if self.logo_login:
            lbl_logo = tk.Label(self, image=self.logo_login, bg="#f4f6f7")
            lbl_logo.pack(pady=(15, 5))

        lbl_titulo = tk.Label(
            self, text="SISTEMA DE RESTAURANTE", 
            font=("Arial", 14, "bold"), 
            bg="#f4f6f7", fg="#2c3e50"
        )
        lbl_titulo.pack(pady=(0, 2))

        lbl_sub = tk.Label(
            self, text="Ingrese sus credenciales para continuar", 
            font=("Arial", 9), 
            bg="#f4f6f7", fg="#7f8c8d"
        )
        lbl_sub.pack(pady=(0, 15))

        frm_campos = tk.Frame(self, bg="#f4f6f7")
        frm_campos.pack(pady=10)

        tk.Label(frm_campos, text="Usuario:", font=("Arial", 10), bg="#f4f6f7").grid(row=0, column=0, sticky="e", pady=8)
        self.ent_usuario = tk.Entry(frm_campos, font=("Arial", 10))
        self.ent_usuario.grid(row=0, column=1, pady=8, padx=5)

        tk.Label(frm_campos, text="Contraseña:", font=("Arial", 10), bg="#f4f6f7").grid(row=1, column=0, sticky="e", pady=8)
        self.ent_clave = tk.Entry(frm_campos, show="*", font=("Arial", 10))
        self.ent_clave.grid(row=1, column=1, pady=8, padx=5)

        btn_ingresar = tk.Button(
            self, text="INGRESAR", command=self._validar_login, 
            bg="#2980b9", fg="white", font=("Arial", 10, "bold"), width=15, height=1
        )
        btn_ingresar.pack(pady=20)

    def _validar_login(self):
        usr = self.ent_usuario.get().strip()
        clv = self.ent_clave.get().strip()

        if not usr or not clv:
            messagebox.showwarning("Atención", "Ingrese usuario y contraseña.")
            return

        usuario_valido = self.servicio.autenticar(usr, clv)
        if usuario_valido:
            self.destroy()
            app_principal = MainView(self.servicio, usuario_valido)
            app_principal.mainloop()
        else:
            messagebox.showerror("Error de Acceso", "Credenciales incorrectas.")

    def _cargar_logo(self):
        try:
            base_dir = Path(__file__).resolve().parent.parent
            assets_dir = base_dir / "assets"
            ruta_logo = assets_dir / "Sabor_de_casa.png"

            if ruta_logo.exists():
                img = Image.open(ruta_logo).resize((120, 120), Image.Resampling.LANCZOS)
                self.logo_login = ImageTk.PhotoImage(img) 
                print("¡Logo cargado correctamente en LoginView como self.logo_login!")
            else:
                self.logo_login = None
        except Exception as e:
            print(f"Error al cargar logo en Login: {e}")
            self.logo_login = None