class Producto:
    def __init__(
        self,
        codigo,
        nombre,
        categoria,
        precio,
        disponible=True,
        stock=0
    ):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = float(precio)
        self.disponible = disponible
        self.stock = int(stock)

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "disponible": self.disponible,
            "stock": self.stock
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            codigo=datos["codigo"],
            nombre=datos["nombre"],
            categoria=datos["categoria"],
            precio=datos["precio"],
            disponible=datos.get("disponible", True),
            stock=datos.get("stock", 0)
        )

    def __str__(self):
        return f"{self.codigo} - {self.nombre} - ${self.precio:.2f}"
