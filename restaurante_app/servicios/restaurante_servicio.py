import json
import os
from pathlib import Path
from modelos.usuario import Usuario

class RestauranteServicio:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent
        self.archivo_usuarios = base_dir / "datos" / "usuarios.json"
        
        self.usuarios = []
        self.cargar_usuarios()

    def cargar_usuarios(self):
        if self.archivo_usuarios.exists():
            try:
                with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.usuarios = []
                    for u in data:
                        usuario_obj = Usuario(
                            identificacion=str(u.get("identificacion", "")),
                            nombre=str(u.get("nombre", "")),
                            username=str(u.get("username", "")),
                            contraseña=str(u.get("contraseña", "")),
                            rol=str(u.get("rol", ""))
                        )
                        self.usuarios.append(usuario_obj)
            except Exception as e:
                print(f"Error al cargar usuarios: {e}")
                self.usuarios = []
        else:
            self.usuarios = [Usuario("1", "Admin Principal", "admin", "Admin1234", "Administrador")]
            self.guardar_usuarios()

    def guardar_usuarios(self):
        self.archivo_usuarios.parent.mkdir(parents=True, exist_ok=True)
        with open(self.archivo_usuarios, "w", encoding="utf-8") as f:
            json.dump([u.to_dict() for u in self.usuarios], f, indent=4, ensure_ascii=False)
    def obtener_usuarios(self):
        return self.usuarios

    def registrar_usuario(self, identificacion, nombre, username, contraseña, rol):
        for u in self.usuarios:
            if str(u.identificacion) == str(identificacion):
                return False, "Ya existe un usuario con esa identificación."
        nuevo_usuario = Usuario(identificacion, nombre, username, contraseña, rol)
        self.usuarios.append(nuevo_usuario)
        self.guardar_usuarios()
        return True, "Usuario registrado correctamente."

    def actualizar_usuario(self, id_usuario, nombre, username, password, rol):
        for u in self.usuarios:
            if str(u.identificacion) == str(id_usuario):
                u.nombre = nombre
                u.username = username
                u.password = password
                u.rol = rol
                self.guardar_usuarios()
                return True, "Usuario actualizado correctamente."
        return False, "Usuario no encontrado."

    def eliminar_usuario(self, identificacion):
        for u in self.usuarios:
            if str(u.identificacion) == str(identificacion):
                self.usuarios.remove(u)
                self.guardar_usuarios()
                return True, "Usuario eliminado correctamente."
        return False, "Usuario no encontrado."

    def buscar_usuario_por_id(self, identificacion):
        id_buscado = str(identificacion).lstrip('0')
        for u in self.usuarios:
            id_actual = str(u.identificacion).lstrip('0')
            if id_actual == id_buscado:
                return u
        return None
    
    def autenticar(self, username, contraseña):
        print(f"-> Intentando login con: User='{username}' | Pass='{contraseña}'")
        for u in self.usuarios:
            print(f"-> Comparando con BD: User='{u.username}' | Pass='{u.contraseña}'")
            if u.username == username and u.contraseña == contraseña:
                print("¡Encontrado con éxito!")
                return u
        print("No se encontró coincidencia.")
        return None

    def listar_usuarios(self):
        return self.usuarios

    def listar_productos(self):
        ruta_productos = self.archivo_usuarios.parent / "productos.json"
        lista_productos = []
        if os.path.exists(ruta_productos):
            try:
                with open(ruta_productos, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    from modelos.producto import Producto  
                    for p in data:
                        prod_obj = Producto(
                            codigo=str(p.get("codigo", "")),
                            nombre=str(p.get("nombre", "")),
                            categoria=str(p.get("categoria", "")),
                            precio=float(p.get("precio", 0.0)),
                            stock=int(p.get("stock", 0))
                        )
                        lista_productos.append(prod_obj)
            except Exception as e:
                print(f"Error al listar productos: {e}")
                return []
        return lista_productos

    def registrar_producto(self, codigo, nombre, categoria, precio, stock=0):
        ruta_productos = self.archivo_usuarios.parent / "productos.json"
        lista_productos = []
        
        if os.path.exists(ruta_productos):
            try:
                with open(ruta_productos, "r", encoding="utf-8") as f:
                    lista_productos = json.load(f)
            except Exception as e:
                print(f"Error al leer productos: {e}")
        
        for p in lista_productos:
            if p.get("codigo") == codigo:
                return False, "Ya existe un producto con ese código."
        
        nuevo_prod = {
            "codigo": codigo,
            "nombre": nombre,
            "categoria": categoria,
            "precio": float(precio),
            "stock": int(stock)
        }
        
        lista_productos.append(nuevo_prod)
        
        try:
            with open(ruta_productos, "w", encoding="utf-8") as f:
                json.dump(lista_productos, f, indent=4, ensure_ascii=False)
            return True, "Producto registrado correctamente."
        except Exception as e:
            return False, f"Error al guardar el producto: {e}"

    def actualizar_producto(self, codigo, nombre, categoria, precio, stock=0):
        ruta_productos = self.archivo_usuarios.parent / "productos.json"
        if not os.path.exists(ruta_productos):
            return False, "No se encontró el archivo de productos."
        
        try:
            with open(ruta_productos, "r", encoding="utf-8") as f:
                lista_productos = json.load(f)
            
            encontrado = False
            for p in lista_productos:
                if p.get("codigo") == codigo:
                    p["nombre"] = nombre
                    p["categoria"] = categoria
                    p["precio"] = float(precio)
                    p["stock"] = int(stock)
                    encontrado = True
                    break
            
            if not encontrado:
                return False, "Producto no encontrado para actualizar."
            
            with open(ruta_productos, "w", encoding="utf-8") as f:
                json.dump(lista_productos, f, indent=4, ensure_ascii=False)
            return True, "Producto actualizado correctamente."
        except Exception as e:
            return False, f"Error al actualizar el producto: {e}"

    def eliminar_producto(self, codigo):
        ruta_productos = self.archivo_usuarios.parent / "productos.json"
        if not os.path.exists(ruta_productos):
            return False, "No se encontró el archivo de productos."
        
        try:
            with open(ruta_productos, "r", encoding="utf-8") as f:
                lista_productos = json.load(f)
            
            nueva_lista = [p for p in lista_productos if p.get("codigo") != codigo]
            
            if len(nueva_lista) == len(lista_productos):
                return False, "Producto no encontrado para eliminar."
            
            with open(ruta_productos, "w", encoding="utf-8") as f:
                json.dump(nueva_lista, f, indent=4, ensure_ascii=False)
            return True, "Producto eliminado correctamente."
        except Exception as e:
            return False, f"Error al eliminar el producto: {e}"

    def cargar_ventas(self):
        ruta_ventas = self.archivo_usuarios.parent / "ventas.json"
        
        class VentaObj:
            def __init__(self, id_usuario, id_producto, cantidad, total):
                self.id_usuario = str(id_usuario)
                self.id_producto = str(id_producto)
                self.cantidad = int(cantidad) if str(cantidad).isdigit() else 1
                self.total = float(total) if total is not None else 0.0

        lista_ventas_obj = []
        if os.path.exists(ruta_ventas):
            try:
                with open(ruta_ventas, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for v in data:
                        venta_obj = VentaObj(
                            id_usuario=v.get("id_usuario"),
                            id_producto=v.get("id_producto"),
                            cantidad=v.get("cantidad", 1),
                            total=v.get("total", 0.0)
                        )
                        lista_ventas_obj.append(venta_obj)
            except Exception as e:
                print(f"Error al cargar ventas: {e}")
                return []
        return lista_ventas_obj

    def registrar_venta(self, id_usuario, id_producto, cantidad):
        ruta_ventas = self.archivo_usuarios.parent / "ventas.json"
        ruta_productos = self.archivo_usuarios.parent / "productos.json"

        lista_productos = []
        if os.path.exists(ruta_productos):
            try:
                with open(ruta_productos, "r", encoding="utf-8") as f:
                    contenido_prod = f.read().strip()
                    lista_productos = json.loads(contenido_prod) if contenido_prod else []
            except Exception as e:
                return False, f"Error al leer productos: {e}"

        producto_encontrado = None
        for p in lista_productos:
            if str(p.get("codigo")) == str(id_producto):
                producto_encontrado = p
                break

        if not producto_encontrado:
            return False, "El producto seleccionado no existe."

        stock_actual = int(producto_encontrado.get("stock", 0))
        cant_pedida = int(cantidad)

        if stock_actual < cant_pedida:
            return False, f"Stock insuficiente. Disponible: {stock_actual}"

        producto_encontrado["stock"] = stock_actual - cant_pedida

        try:
            with open(ruta_productos, "w", encoding="utf-8") as f:
                json.dump(lista_productos, f, indent=4, ensure_ascii=False)
        except Exception as e:
            return False, f"Error al actualizar el stock: {e}"

        lista_ventas = []
        if ruta_ventas.exists():
            try:
                with open(ruta_ventas, "r", encoding="utf-8") as f:
                    contenido_ventas = f.read().strip()
                    lista_ventas = json.loads(contenido_ventas) if contenido_ventas else []
            except Exception:
                lista_ventas = []

        nueva_venta = {
            "id_usuario": str(id_usuario),
            "id_producto": str(id_producto),
            "cantidad": cant_pedida,
            "total": float(producto_encontrado.get("precio", 0.0)) * cant_pedida
        }

        lista_ventas.append(nueva_venta)
        
        try:
            with open(ruta_ventas, "w", encoding="utf-8") as f:
                json.dump(lista_ventas, f, indent=4, ensure_ascii=False)
            return True, "Venta registrada con éxito."
        except Exception as e:
            return False, f"Error al guardar la venta: {e}"

    def obtener_producto_por_id(self, codigo):
        ruta_productos = self.archivo_usuarios.parent / "productos.json"
        if os.path.exists(ruta_productos):
            try:
                with open(ruta_productos, "r", encoding="utf-8") as f:
                    lista_productos = json.load(f)
                    from modelos.producto import Producto
                    for p in lista_productos:
                        if str(p.get("codigo")) == str(codigo):
                            return Producto(
                                codigo=str(p.get("codigo", "")),
                                nombre=str(p.get("nombre", "")),
                                categoria=str(p.get("categoria", "")),
                                precio=float(p.get("precio", 0.0)),
                                stock=int(p.get("stock", 0))
                            )
            except Exception as e:
                print(f"Error al buscar producto por id: {e}")
        return None