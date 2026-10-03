import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from PIL import Image, ImageTk

class MainView(tk.Tk):
    def __init__(self, servicio, usuario_encontrado):
        super().__init__()
        self.servicio = servicio
        self.usuario_actual = usuario_encontrado 

        self.title(f"Sistema Restaurante - Usuario: {self.usuario_actual.nombre}")
        self.geometry("950x580")
        self.minsize(850, 520)

        self.iconos = {}
        self._cargar_iconos()
        self._cargar_logo()

        self._crear_interfaz()

    def _cargar_iconos(self):
        self.iconos = {}
        try:
            base_dir = Path(__file__).resolve().parent.parent
            assets_dir = base_dir / "assets"

            nombres_iconos = ["home", "brunch_dining"]
            for nombre in nombres_iconos:
                ruta = assets_dir / f"{nombre}.png"
                if ruta.exists():
                    img = Image.open(ruta).resize((64, 64), Image.Resampling.LANCZOS)
                    self.iconos[nombre] = ImageTk.PhotoImage(img)

            ruta_logo = assets_dir / "Sabor_de_casa.png"
            if ruta_logo.exists():
                img_logo = Image.open(ruta_logo).resize((120, 120), Image.Resampling.LANCZOS)
                self.logo_contenido = ImageTk.PhotoImage(img_logo) 
                print("¡Logo cargado en self.logo_contenido con éxito!")
            else:
                self.logo_contenido = None

        except Exception as e:
            print(f"Aviso: No se pudieron cargar los iconos: {e}")
            self.logo_contenido = None

    def _cargar_logo(self):
        try:
            base_dir = Path(__file__).resolve().parent.parent
            assets_dir = base_dir / "assets"
            ruta_logo = assets_dir / "Sabor_de_casa.png"

            if ruta_logo.exists():
                img = Image.open(ruta_logo).resize((120, 120), Image.Resampling.LANCZOS)
                self.logo_main = ImageTk.PhotoImage(img) 
    
            else:
                self.logo_main = None
                print("No se encontró el logo.")
        except Exception as e:
            print(f"Error al cargar logo en MainView: {e}")
            self.logo_main = None

    def _crear_interfaz(self):
        self.frame_menu = tk.Frame(self, bg="#2c3e50", width=220)
        self.frame_menu.pack(side="left", fill="y")
        self.frame_menu.pack_propagate(False)

        self.frame_contenido = tk.Frame(self, bg="#ecf0f1")
        self.frame_contenido.pack(side="right", expand=True, fill="both")

        if hasattr(self, "logo_main") and self.logo_main:
            print("Mostrando logo en el contenido...")
            lbl_logo_main = tk.Label(
                self.frame_contenido,
                image=self.logo_main,
                bg="#ecf0f1"
            )
            lbl_logo_main.pack(pady=20)
        else:
            print("El logo_main no está disponible para mostrarse.")

        lbl_titulo = tk.Label(
            self.frame_menu, text="MENÚ", bg="#2c3e50", fg="white",
            font=("Arial", 14, "bold")
        )
        lbl_titulo.pack(pady=20)

        btn_productos = tk.Button(
            self.frame_menu, text="Gestión de Productos",
            command=self.mostrar_productos, width=20, bg="#34495e", fg="white",
            font=("Arial", 10), anchor="w", padx=10
        )
        btn_productos.pack(pady=10)

        btn_usuarios = tk.Button(
            self.frame_menu, text="Consulta de Usuarios",
            command=self.validar_y_mostrar_usuarios, width=20, bg="#34495e", fg="white",
            font=("Arial", 10), anchor="w", padx=10
        )
        btn_usuarios.pack(pady=10)

        btn_ventas = tk.Button(
            self.frame_menu, text="Gestión de Ventas",
            command=self.mostrar_ventas, width=20, bg="#34495e", fg="white",
            font=("Arial", 10), anchor="w", padx=10
        )
        btn_ventas.pack(pady=10)

        btn_salir = tk.Button(
            self.frame_menu, text="Cerrar Sesión",
            command=self.destroy, width=20, bg="#c0392b", fg="white",
            font=("Arial", 10), anchor="w", padx=10
        )
        btn_salir.pack(side="bottom", pady=20)

        self.mostrar_productos()

    def _limpiar_contenido(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

    # ===============================================
    #             SECCIÓN DE PRODUCTOS
    # ===============================================
    def mostrar_productos(self):
        self._limpiar_contenido()

        frm_header = tk.Frame(self.frame_contenido, bg="#ecf0f1")
        frm_header.pack(fill="x", padx=15, pady=10)

        tk.Label(
            frm_header, text="GESTIÓN DE PRODUCTOS",
            font=("Arial", 16, "bold"), bg="#ecf0f1"
        ).pack(side="left", pady=5)

        if "brunch_dining" in self.iconos:
            tk.Label(frm_header, image=self.iconos["brunch_dining"], bg="#ecf0f1").pack(side="right")

        frm_form = tk.LabelFrame(
            self.frame_contenido, text=" Datos del Producto ",
            font=("Arial", 11, "bold"), bg="#ecf0f1", padx=10, pady=10
        )
        frm_form.pack(fill="x", padx=15, pady=5)

        tk.Label(frm_form, text="Código:", bg="#ecf0f1").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.ent_id = tk.Entry(frm_form)
        self.ent_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frm_form, text="Nombre:", bg="#ecf0f1").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.ent_nombre = tk.Entry(frm_form)
        self.ent_nombre.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frm_form, text="Categoría:", bg="#ecf0f1").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.cmb_categoria = ttk.Combobox(
            frm_form, values=["Platos", "Bebidas", "Postres", "Entradas"], state="readonly"
        )
        self.cmb_categoria.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frm_form, text="Precio ($):", bg="#ecf0f1").grid(row=1, column=2, sticky="e", padx=5, pady=5)
        self.ent_precio = tk.Entry(frm_form)
        self.ent_precio.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(frm_form, text="Stock:", bg="#ecf0f1").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.ent_stock = tk.Entry(frm_form)
        self.ent_stock.grid(row=2, column=1, padx=5, pady=5)

        frm_botones = tk.Frame(self.frame_contenido, bg="#ecf0f1")
        frm_botones.pack(fill="x", padx=15, pady=5)

        tk.Button(
            frm_botones, text="Registrar", command=self._registrar_producto,
            bg="#2ecc71", fg="white", width=12
        ).pack(side="left", padx=5)

        tk.Button(
            frm_botones, text="Cargar/Buscar", command=self._consultar_producto,
            bg="#3498db", fg="white", width=12
        ).pack(side="left", padx=5)

        tk.Button(
            frm_botones, text="Actualizar", command=self._actualizar_producto,
            bg="#f39c12", fg="white", width=12
        ).pack(side="left", padx=5)

        tk.Button(
            frm_botones, text="Eliminar", command=self._eliminar_producto,
            bg="#e74c3c", fg="white", width=12
        ).pack(side="left", padx=5)

        tk.Button(
            frm_botones, text="Limpiar", command=self._limpiar_formulario,
            bg="#95a5a6", fg="white", width=10
        ).pack(side="right", padx=5)

        frm_tabla = tk.LabelFrame(
            self.frame_contenido, text=" Listado de Productos ",
            font=("Arial", 11, "bold"), bg="#ecf0f1", padx=5, pady=5
        )
        frm_tabla.pack(fill="both", expand=True, padx=15, pady=10)

        scroll = ttk.Scrollbar(frm_tabla, orient="vertical")
        scroll.pack(side="right", fill="y")

        self.tree_prod = ttk.Treeview(
            frm_tabla, columns=("codigo", "nombre", "categoria", "precio", "stock"),
            show="headings", yscrollcommand=scroll.set
        )
        scroll.config(command=self.tree_prod.yview)

        self.tree_prod.heading("codigo", text="Código")
        self.tree_prod.heading("nombre", text="Nombre")
        self.tree_prod.heading("categoria", text="Categoría")
        self.tree_prod.heading("precio", text="Precio ($)")
        self.tree_prod.heading("stock", text="Stock")

        self.tree_prod.column("codigo", width=80, anchor="center")
        self.tree_prod.column("nombre", width=180)
        self.tree_prod.column("categoria", width=100)
        self.tree_prod.column("precio", width=80, anchor="e")
        self.tree_prod.column("stock", width=60, anchor="center")

        self.tree_prod.pack(fill="both", expand=True)
        self.tree_prod.bind("<<TreeviewSelect>>", self._seleccionar_producto_tabla)
        self._cargar_tabla_productos()

    def _cargar_tabla_productos(self):
        for item in self.tree_prod.get_children():
            self.tree_prod.delete(item)

        productos = self.servicio.listar_productos()
        for p in productos:
            self.tree_prod.insert("", "end", values=(p.codigo, p.nombre, p.categoria, f"{p.precio:.2f}", p.stock))

    def _seleccionar_producto_tabla(self, event):
        seleccion = self.tree_prod.selection()
        if seleccion:
            item = self.tree_prod.item(seleccion)
            valores = item["values"]
            
            self.ent_id.delete(0, tk.END)
            self.ent_id.insert(0, valores[0])
            
            self.ent_nombre.delete(0, tk.END)
            self.ent_nombre.insert(0, valores[1])
            
            self.cmb_categoria.set(valores[2])
            
            self.ent_precio.delete(0, tk.END)
            self.ent_precio.insert(0, str(valores[3]).replace("$", "").strip())
            
            self.ent_stock.delete(0, tk.END)
            self.ent_stock.insert(0, str(valores[4]))

    def _limpiar_formulario(self):
        self.ent_id.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)
        self.cmb_categoria.set("")
        self.ent_precio.delete(0, tk.END)
        self.ent_stock.delete(0, tk.END)
        
    def _registrar_producto(self):
        id_p = self.ent_id.get().strip()
        nom = self.ent_nombre.get().strip()
        cat = self.cmb_categoria.get().strip()
        pre = self.ent_precio.get().strip()

        if not id_p or not nom or not cat or not pre:
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return

        try:
            precio_val = float(pre)
            exito, msj = self.servicio.registrar_producto(id_p, nom, cat, precio_val)
            if exito:
                messagebox.showinfo("Éxito", msj)
                self._limpiar_formulario()
                self._cargar_tabla_productos()
            else:
                messagebox.showerror("Error", msj)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido.")

    def _consultar_producto(self):
        id_p = self.ent_id.get().strip()
        if not id_p:
            messagebox.showwarning("Atención", "Ingrese el código del producto a consultar.")
            return

        prod = self.servicio.obtener_producto_por_id(id_p)
        if prod:
            self.ent_nombre.delete(0, tk.END)
            self.ent_nombre.insert(0, prod.nombre)
            self.cmb_categoria.set(prod.categoria)
            self.ent_precio.delete(0, tk.END)
            self.ent_precio.insert(0, str(prod.precio))
            messagebox.showinfo("Cargado", f"Producto '{prod.nombre}' cargado en el formulario.")
        else:
            messagebox.showerror("Error", "Producto no encontrado.")

    def _actualizar_producto(self):
        id_p = self.ent_id.get().strip()
        nom = self.ent_nombre.get().strip()
        cat = self.cmb_categoria.get().strip()
        pre = self.ent_precio.get().strip()
        sto = self.ent_stock.get().strip() 

        if not id_p or not nom or not cat or not pre or not sto: 
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return

        try:
            precio_val = float(pre)
            stock_val = int(sto) 
            exito, msj = self.servicio.actualizar_producto(id_p, nom, cat, precio_val, stock_val)
            
            if exito:
                messagebox.showinfo("Éxito", msj)
                self._limpiar_formulario()
                self._cargar_tabla_productos()
            else:
                messagebox.showerror("Error", msj)
        except ValueError:
            messagebox.showerror("Error", "El precio y el stock deben ser números válidos.")

    def _eliminar_producto(self):
        id_p = self.ent_id.get().strip()
        if not id_p:
            messagebox.showwarning("Atención", "Ingrese el código del producto a eliminar.")
            return

        if messagebox.askyesno("Confirmar", f"¿Desea eliminar el producto con código {id_p}?"):
            exito, msj = self.servicio.eliminar_producto(id_p)
            if exito:
                messagebox.showinfo("Éxito", msj)
                self._limpiar_formulario()
                self._cargar_tabla_productos()
            else:
                messagebox.showerror("Error", msj)

    # ===============================================
    #   SECCIÓN DE VALIDACIÓN Y CONTROL DE ACCESO
    # ===============================================
    def validar_y_mostrar_usuarios(self):
        if hasattr(self, 'usuario_actual') and self.usuario_actual:
            if self.usuario_actual.rol == "Administrador":
                self.mostrar_usuarios()
            else:
                from tkinter import messagebox
                messagebox.showerror("Acceso Denegado", "Solo los Administradores pueden acceder a la gestión de usuarios.")
        else:
            from tkinter import messagebox
            messagebox.showwarning("Atención", "No hay una sesión activa.")

    # ===============================================
    #             SECCIÓN DE USUARIOS
    # ===============================================
    def mostrar_usuarios(self):
        self._limpiar_contenido()

        frm_header = tk.Frame(self.frame_contenido, bg="#ecf0f1")
        frm_header.pack(fill="x", padx=15, pady=10)

        tk.Label(
            frm_header, text="GESTIÓN DE USUARIOS",
            font=("Arial", 16, "bold"), bg="#ecf0f1"
        ).pack(side="left", pady=5)

        frm_form = tk.LabelFrame(
            self.frame_contenido, text=" Datos del Usuario ",
            font=("Arial", 11, "bold"), bg="#ecf0f1", padx=10, pady=10
        )
        frm_form.pack(fill="x", padx=15, pady=5)

        tk.Label(frm_form, text="Identificación:", bg="#ecf0f1").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.ent_id_usu = tk.Entry(frm_form)
        self.ent_id_usu.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frm_form, text="Nombre:", bg="#ecf0f1").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.ent_nombre_usu = tk.Entry(frm_form)
        self.ent_nombre_usu.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frm_form, text="Username:", bg="#ecf0f1").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.ent_username = tk.Entry(frm_form)
        self.ent_username.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frm_form, text="Contraseña:", bg="#ecf0f1").grid(row=1, column=2, sticky="e", padx=5, pady=5)
        self.ent_password = tk.Entry(frm_form, show="*")
        self.ent_password.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(frm_form, text="Rol:", bg="#ecf0f1").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        from tkinter import ttk
        self.cmb_rol = ttk.Combobox(
            frm_form, values=["Administrador", "Empleado", "Cliente"], state= "readonly"
        )
        self.cmb_rol.grid(row=2, column=1, padx=5, pady=5)
        self.cmb_rol.current(1)

        self.ent_id_usu.bind("<Return>", lambda event: self._registrar_usuario_ui())
        self.ent_nombre_usu.bind("<Return>", lambda event: self._registrar_usuario_ui())
        self.ent_username.bind("<Return>", lambda event: self._registrar_usuario_ui())
        self.ent_password.bind("<Return>", lambda event: self._registrar_usuario_ui())

        self.ent_id_usu.bind("<Escape>", self._limpiar_formulario)
        self.ent_nombre_usu.bind("<Escape>", self._limpiar_formulario)
        self.ent_username.bind("<Escape>", self._limpiar_formulario)
        self.ent_password.bind("<Escape>", self._limpiar_formulario)

        frm_botones = tk.Frame(self.frame_contenido, bg="#ecf0f1")
        frm_botones.pack(fill="x", padx=15, pady=5)

        tk.Button(
            frm_botones, text="Registrar", command=self._registrar_usuario_ui,
            bg="#2ecc71", fg="white", width=12
        ).pack(side="left", padx=5)

        tk.Button(
            frm_botones, text="Cargar/Buscar", command=self._consultar_usuario_ui,
            bg="#3498db", fg="white", width=12
        ).pack(side="left", padx=5)

        tk.Button(
            frm_botones, text="Actualizar", command=self._actualizar_usuario_ui,
            bg="#f39c12", fg="white", width=12
        ).pack(side="left", padx=5)

        tk.Button(
            frm_botones, text="Eliminar", command=self._eliminar_usuario_ui,
            bg="#e74c3c", fg="white", width=12
        ).pack(side="left", padx=5)

        tk.Button(
            frm_botones, text="Limpiar", command=self._limpiar_formulario_usuario,
            bg="#95a5a6", fg="white", width=10
        ).pack(side="right", padx=5)

        frm_tabla = tk.LabelFrame(
            self.frame_contenido, text=" Listado de Usuarios ",
            font=("Arial", 11, "bold"), bg="#ecf0f1", padx=5, pady=5
        )
        frm_tabla.pack(fill="both", expand=True, padx=15, pady=10)

        scroll = ttk.Scrollbar(frm_tabla, orient="vertical")
        scroll.pack(side="right", fill="y")

        self.tree_usuarios = ttk.Treeview(
            frm_tabla, columns=("id", "nombre", "username", "rol"),
            show="headings", yscrollcommand=scroll.set
        )
        scroll.config(command=self.tree_usuarios.yview)

        self.tree_usuarios.heading("id", text="Identificación")
        self.tree_usuarios.heading("nombre", text="Nombre")
        self.tree_usuarios.heading("username", text="Username")
        self.tree_usuarios.heading("rol", text="Rol")

        self.tree_usuarios.column("id", width=100, anchor="center")
        self.tree_usuarios.column("nombre", width=180)
        self.tree_usuarios.column("username", width=120, anchor="center")
        self.tree_usuarios.column("rol", width=120, anchor="center")

        self.tree_usuarios.pack(fill="both", expand=True)
        self.tree_usuarios.bind("<<TreeviewSelect>>", self.seleccionar_usuario_tabla)
        self._cargar_tabla_usuarios()

    def _cargar_tabla_usuarios(self):
        for row in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(row)

        usuarios = self.servicio.obtener_usuarios()
        if usuarios:
            for u in usuarios:
                self.tree_usuarios.insert("", "end", values=(u.identificacion, u.nombre, u.username, u.rol))

    def _limpiar_formulario_usuario(self):
        self.ent_id_usu.delete(0, tk.END)
        self.ent_nombre_usu.delete(0, tk.END)
        self.ent_username.delete(0, tk.END)
        self.ent_password.delete(0, tk.END)
        self.cmb_rol.current(1)

    def _registrar_usuario_ui(self):
        id_u = self.ent_id_usu.get().strip()
        nombre = self.ent_nombre_usu.get().strip()
        user = self.ent_username.get().strip()
        pwd = self.ent_password.get().strip()
        rol = self.cmb_rol.get()

        if not id_u or not nombre or not user or not pwd:
            from tkinter import messagebox
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return

        exito, msj = self.servicio.registrar_usuario(id_u, nombre, user, pwd, rol)
        from tkinter import messagebox
        if exito:
            messagebox.showinfo("Éxito", msj)
            self._limpiar_formulario_usuario()
            self._cargar_tabla_usuarios()
        else:
            messagebox.showerror("Error", msj)

    def _consultar_usuario_ui(self):
        id_u = self.ent_id_usu.get().strip()
        if not id_u:
            from tkinter import messagebox
            messagebox.showwarning("Atención", "Ingrese la identificación del usuario a consultar.")
            return

        for u in self.servicio.listar_usuarios():
            if str(u.identificacion) == str(id_u):
                self._limpiar_formulario_usuario()
                self.ent_id_usu.insert(0, str(u.identificacion))
                self.ent_nombre_usu.insert(0, u.nombre)
                self.ent_username.insert(0, u.username)
                self.ent_password.insert(0, u.contraseña)
                self.cmb_rol.set(u.rol)
                from tkinter import messagebox
                messagebox.showinfo("Cargado", f"Usuario '{u.nombre}' cargado en el formulario.")
                return
        from tkinter import messagebox
        messagebox.showerror("Error", "Usuario no encontrado.")

    def _actualizar_usuario_ui(self):
        from tkinter import messagebox
        
        id_u = self.ent_id_usu.get().strip()
        nombre = self.ent_nombre_usu.get().strip()
        user = self.ent_username.get().strip()
        pwd = self.ent_password.get().strip()
        rol = self.cmb_rol.get()

        if not id_u or not nombre or not user or not pwd:
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return

        exito, msj = self.servicio.actualizar_usuario(id_u, nombre, user, pwd, rol)
        if exito:
            messagebox.showinfo("Éxito", msj)
            self._limpiar_formulario_usuario()
            self._cargar_tabla_usuarios()
        else:
            messagebox.showerror("Error", msj)

    def _eliminar_usuario_ui(self):
        id_u = self.ent_id_usu.get().strip()
        if not id_u:
            from tkinter import messagebox
            messagebox.showwarning("Atención", "Ingrese o cargue la identificación del usuario a eliminar.")
            return

        from tkinter import messagebox
        if messagebox.askyesno("Confirmar", f"¿Desea eliminar al usuario con ID {id_u}?"):
            exito, msj = self.servicio.eliminar_usuario(id_u)
            if exito:
                messagebox.showinfo("Éxito", msj)
                self._limpiar_formulario_usuario()
                self._cargar_tabla_usuarios()
            else:
                messagebox.showerror("Error", msj)

    def seleccionar_usuario_tabla(self, event):
        seleccion = self.tree_usuarios.selection()
        if seleccion:
            item = self.tree_usuarios.item(seleccion)
            valores = item['values']
            
            if valores:
                id_usuario = valores[0]
                print(f"ID seleccionado en la tabla: {id_usuario} (Tipo: {type(id_usuario)})")
                usuario = self.servicio.buscar_usuario_por_id(id_usuario)
                print(f"Resultado del servicio: {usuario}")
                
                if usuario:
                    self._limpiar_formulario_usuario()
                    self.ent_id_usu.insert(0, usuario.identificacion)
                    self.ent_nombre_usu.insert(0, usuario.nombre)
                    self.ent_username.insert(0, usuario.username)
                    self.cmb_rol.set(usuario.rol)

    def _limpiar_formulario_usuarios(self, event=None):
        self.ent_id_usu.delete(0, 'end')
        self.ent_nombre_usu.delete(0, 'end')
        self.ent_username.delete(0, 'end')
        self.ent_password.delete(0, 'end')
        self.cmb_rol.set('') 
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    # ===============================================
    #             SECCIÓN DE VENTAS
    # ===============================================
    def mostrar_ventas(self):
        self._limpiar_contenido()

        frm_header = tk.Frame(self.frame_contenido, bg="#ecf0f1")
        frm_header.pack(fill="x", padx=15, pady=10)

        tk.Label(
            frm_header, text="GESTIÓN DE VENTAS",
            font=("Arial", 16, "bold"), bg="#ecf0f1"
        ).pack(side="left", pady=5)

        if "brunch_dining" in self.iconos:
            tk.Label(frm_header, image=self.iconos["brunch_dining"], bg="#ecf0f1").pack(side="right")

        frm_form = tk.LabelFrame(
            self.frame_contenido, text=" Registrar Nueva Venta ",
            font=("Arial", 11, "bold"), bg="#ecf0f1", padx=10, pady=10
        )
        frm_form.pack(fill="x", padx=15, pady=5)

        tk.Label(frm_form, text="Usuario:", bg="#ecf0f1").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.cmb_usuario_venta = ttk.Combobox(frm_form, state="readonly", width=22)
        self.cmb_usuario_venta.grid(row=0, column=1, padx=5, pady=5)
        
        usuarios = self.servicio.listar_usuarios()
        self.mapa_usuarios = {f"{u.identificacion} - {u.nombre}": u.identificacion for u in usuarios}
        self.cmb_usuario_venta['values'] = list(self.mapa_usuarios.keys())

        tk.Label(frm_form, text="Producto:", bg="#ecf0f1").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.cmb_producto_venta = ttk.Combobox(frm_form, state="readonly", width=22)
        self.cmb_producto_venta.grid(row=0, column=3, padx=5, pady=5)
        
        productos = self.servicio.listar_productos()
        self.mapa_productos = {f"{p.codigo} - {p.nombre} (${p.precio})": p.codigo for p in productos}
        self.cmb_producto_venta['values'] = list(self.mapa_productos.keys())

        tk.Label(frm_form, text="Cantidad:", bg="#ecf0f1").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.ent_cantidad = tk.Entry(frm_form, width=10)
        self.ent_cantidad.insert(0, "1")
        self.ent_cantidad.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        tk.Button(
            frm_form, text="Registrar Venta", command=self._registrar_venta,
            bg="#2ecc71", fg="white", width=15
        ).grid(row=1, column=3, padx=5, pady=5, sticky="e")

        frm_tabla = tk.LabelFrame(
            self.frame_contenido, text=" Historial de Ventas ",
            font=("Arial", 11, "bold"), bg="#ecf0f1", padx=5, pady=5
        )
        frm_tabla.pack(fill="both", expand=True, padx=15, pady=10)

        scroll = ttk.Scrollbar(frm_tabla, orient="vertical")
        scroll.pack(side="right", fill="y")

        self.tree_ventas = ttk.Treeview(
            frm_tabla, columns=("usuario", "producto", "cantidad", "total"),
            show="headings", yscrollcommand=scroll.set
        )
        scroll.config(command=self.tree_ventas.yview)

        self.tree_ventas.heading("usuario", text="ID Usuario")
        self.tree_ventas.heading("producto", text="Código Producto")
        self.tree_ventas.heading("cantidad", text="Cantidad")
        self.tree_ventas.heading("total", text="Total ($)")

        self.tree_ventas.column("usuario", width=140, anchor="center")
        self.tree_ventas.column("producto", width=140, anchor="center")
        self.tree_ventas.column("cantidad", width=80, anchor="center")
        self.tree_ventas.column("total", width=90, anchor="e")

        self.tree_ventas.pack(fill="both", expand=True)
        self._cargar_tabla_ventas()

    def _cargar_tabla_ventas(self):
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)
        
        ventas = self.servicio.cargar_ventas()
        for v in ventas:
            prod = self.servicio.obtener_producto_por_id(v.id_producto)
            precio = prod.precio if prod else 0.0
            total = precio * getattr(v, 'cantidad', 1)
            
            self.tree_ventas.insert(
                "", "end", 
                values=(v.id_usuario, v.id_producto, getattr(v, 'cantidad', 1), f"{total:.2f}")
            )

    def _registrar_venta(self):
        sel_usr = self.cmb_usuario_venta.get()
        sel_prod = self.cmb_producto_venta.get()
        cant_str = self.ent_cantidad.get().strip()

        if not sel_usr or not sel_prod or not cant_str:
            messagebox.showwarning("Atención", "Debe seleccionar un usuario, un producto y especificar la cantidad.")
            return

        try:
            cantidad = int(cant_str)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0.")
            
            id_usuario = self.mapa_usuarios[sel_usr]
            id_producto = self.mapa_productos[sel_prod]

            exito, msj = self.servicio.registrar_venta(id_usuario, id_producto, cantidad)
            if exito:
                messagebox.showinfo("Éxito", msj)
                self.ent_cantidad.delete(0, tk.END)
                self.ent_cantidad.insert(0, "1")
                self.cmb_usuario_venta.set("")
                self.cmb_producto_venta.set("")
                self._cargar_tabla_ventas()
            else:
                messagebox.showerror("Error", msj)
        except ValueError as e:
            messagebox.showerror("Error", f"Cantidad inválida: {e}")