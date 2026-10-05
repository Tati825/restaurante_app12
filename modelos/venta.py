class Venta:
    def __init__(
        self,
        codigo_venta,
        identificacion_usuario,
        codigo_producto,
        cantidad,
        precio_unitario,
        total=None,
        fecha=""
    ):
        self.codigo_venta = codigo_venta
        self.identificacion_usuario = identificacion_usuario
        self.codigo_producto = codigo_producto
        self.cantidad = int(cantidad)
        self.precio_unitario = float(precio_unitario)

        if total is None:
            self.total = self.cantidad * self.precio_unitario
        else:
            self.total = float(total)

        self.fecha = fecha

    def to_dict(self):
        return {
            "codigo_venta": self.codigo_venta,
            "identificacion_usuario": self.identificacion_usuario,
            "codigo_producto": self.codigo_producto,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "total": self.total,
            "fecha": self.fecha
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            codigo_venta=datos["codigo_venta"],
            identificacion_usuario=datos["identificacion_usuario"],
            codigo_producto=datos["codigo_producto"],
            cantidad=datos["cantidad"],
            precio_unitario=datos["precio_unitario"],
            total=datos.get("total"),
            fecha=datos.get("fecha", "")
        )
