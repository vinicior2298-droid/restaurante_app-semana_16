class Usuario:
    def __init__(self, identificacion, nombre, username, contraseña, rol):
        self.identificacion = identificacion
        self.nombre = nombre
        self.username = username
        self.contraseña = contraseña
        self.rol = rol

    @staticmethod
    def validar_identificacion(identificacion: str) -> str:
        identificacion = str(identificacion).strip()
        if not identificacion:
            raise ValueError("La identificación no puede estar vacía.")
        return identificacion

    @staticmethod
    def validar_nombre(nombre: str) -> str:
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        return nombre.title()

    @staticmethod
    def validar_username(username: str) -> str:
        username = username.strip()
        if not username:
            raise ValueError("El nombre de usuario no puede estar vacío.")
        return username

    @staticmethod
    def validar_contraseña(contraseña: str) -> str:
        contraseña = contraseña.strip()
        if len(contraseña) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        if not any(c.isalpha() for c in contraseña):
            raise ValueError("La contraseña debe tener al menos una letra.")
        if not any(c.isdigit() for c in contraseña):
            raise ValueError("La contraseña debe tener al menos un número.")
        return contraseña

    @staticmethod
    def validar_rol(rol: str) -> str:
        roles_validos = ["Administrador", "Empleado", "Cliente"]
        if rol not in roles_validos:
            return "Cliente"
        return rol

    def to_dict(self) -> dict:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "username": self.username,
            "contraseña": self.contraseña,
            "rol": self.rol
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            identificacion=data.get("identificacion", ""),
            nombre=data.get("nombre", ""),
            username=data.get("username", ""),
            contraseña=data.get("contraseña", ""),
            rol=data.get("rol", "Cliente")
        )

    def mostrar_informacion(self) -> str:
        return (
            f"Identificación: {self.identificacion} | "
            f"Nombre: {self.nombre} | "
            f"Usuario: {self.username} | "
            f"Rol: {self.rol}"
        )

    def __str__(self) -> str:
        return self.mostrar_informacion()