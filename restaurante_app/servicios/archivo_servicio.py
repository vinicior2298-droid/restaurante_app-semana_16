import json
from pathlib import Path
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class ArchivoServicio:

  def __init__(self, carpeta_datos: str = "datos") -> None:
    base_dir = Path(__file__).resolve().parent.parent
    self.carpeta = base_dir / carpeta_datos

    self.carpeta.mkdir(parents=True, exist_ok=True)

    self.archivo_productos = self.carpeta / "productos.json"
    self.archivo_usuarios = self.carpeta / "usuarios.json"
    self.archivo_ventas = self.carpeta / "ventas.json"

  def cargar_usuarios(self) -> list[Usuario]:
    if not self.archivo_usuarios.exists():
      return []

    try:
      with self.archivo_usuarios.open("r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

      usuarios = []
      for registro in datos:
        try:
          usuario = Usuario.from_dict(registro)
          usuarios.append(usuario)
        except (KeyError, ValueError):
          continue
      return usuarios
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
      return []

  def cargar_productos(self) -> list[Producto]:
    if not self.archivo_productos.exists():
      return []

    try:
      with self.archivo_productos.open("r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

      productos = []
      for reg in datos:
        try:
          prod = Producto(
              reg["codigo"],
              reg["nombre"],
              reg["categoria"],
              float(reg["precio"]),
              int(reg["stock"]),
          )
          productos.append(prod)
        except (KeyError, ValueError):
          continue
      return productos
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
      return []

  def cargar_ventas(self) -> list[Venta]:
    if not self.archivo_ventas.exists():
      return []

    try:
      with self.archivo_ventas.open("r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

      ventas = []
      for reg in datos:
        try:
          v = Venta(
              reg["id_usuario"], reg["id_producto"], int(reg["cantidad"])
          )
          ventas.append(v)
        except (KeyError, ValueError):
          continue
      return ventas
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
      return []

  def guardar_usuarios(self, usuarios: list[Usuario]) -> None:
    datos = [u.to_dict() for u in usuarios]
    with self.archivo_usuarios.open("w", encoding="utf-8") as archivo:
      json.dump(datos, archivo, indent=4, ensure_ascii=False)

  def guardar_productos(self, productos: list[Producto]) -> None:
    datos = [p.to_dict() for p in productos]
    with self.archivo_productos.open("w", encoding="utf-8") as archivo:
      json.dump(datos, archivo, indent=4, ensure_ascii=False)

  def guardar_ventas(self, ventas: list[Venta]) -> None:
    datos = [v.to_dict() for v in ventas]
    with self.archivo_ventas.open("w", encoding="utf-8") as archivo:
      json.dump(datos, archivo, indent=4, ensure_ascii=False)

  def validar_acceso(
      self, identificacion: str, contraseña: str
  ) -> Usuario | None:
    usuarios = self.cargar_usuarios()
    for u in usuarios:
      if u.identificacion == identificacion and u.contraseña == contraseña:
        return u
    return None