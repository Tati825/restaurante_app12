class Usuario:
    ROLES = ("Administrador", "Empleado", "Cliente")

    def __init__(
        self,
        identificacion,
        nombre,
        usuario,
        password,
        rol="Cliente"
    ):
        self.identificacion = identificacion
        self.nombre = nombre
        self.usuario = usuario
        self.password = password
        self.rol = rol

    def to_dict(self):
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "password": self.password,
            "rol": self.rol
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            identificacion=datos["identificacion"],
            nombre=datos["nombre"],
            usuario=datos["usuario"],
            password=datos["password"],
            rol=datos.get("rol", "Cliente")
        )

    def __str__(self):
        return f"{self.identificacion} - {self.nombre} - {self.rol}"
