from datetime import datetime
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:

    def __init__(self):
        self.archivo = ArchivoServicio()

        self.productos = []
        self.usuarios = []
        self.ventas = []

        self.cargar_datos()

    def cargar_datos(self):
        productos_data = self.archivo.cargar_productos()
        usuarios_data = self.archivo.cargar_usuarios()
        ventas_data = self.archivo.cargar_ventas()

        self.productos = [
            Producto.from_dict(data)
            for data in productos_data
        ]

        self.usuarios = [
            Usuario.from_dict(data)
            for data in usuarios_data
        ]

        self.ventas = [
            Venta.from_dict(data)
            for data in ventas_data
        ]

    def autenticar_usuario(self, usuario, password):
        for user in self.usuarios:
            if (
                user.usuario == usuario
                and user.password == password
            ):
                return user

        return None

    def obtener_usuario(self, identificacion):
        for user in self.usuarios:
            if user.identificacion == identificacion:
                return user

        return None

    def obtener_usuarios(self):
        return self.usuarios

    def registrar_usuario(
        self,
        identificacion,
        nombre,
        usuario,
        password,
        rol
    ):
        identificacion = identificacion.strip()
        nombre = nombre.strip()
        usuario = usuario.strip()
        password = password.strip()

        if not identificacion:
            raise ValueError("La identificación es obligatoria")

        if not nombre:
            raise ValueError("El nombre es obligatorio")

        if not usuario:
            raise ValueError("El usuario es obligatorio")

        if not password:
            raise ValueError("La contraseña es obligatoria")

        if rol not in Usuario.ROLES:
            raise ValueError("El rol seleccionado no es válido")

        if self.obtener_usuario(identificacion):
            raise ValueError(
                "Ya existe un usuario con esa identificación"
            )

        for user in self.usuarios:
            if user.usuario.lower() == usuario.lower():
                raise ValueError(
                    "El nombre de usuario ya está registrado"
                )

        nuevo_usuario = Usuario(
            identificacion=identificacion,
            nombre=nombre,
            usuario=usuario,
            password=password,
            rol=rol
        )

        self.usuarios.append(nuevo_usuario)

        self.archivo.guardar_usuarios(
            [user.to_dict() for user in self.usuarios]
        )

        return nuevo_usuario

    def actualizar_usuario(
        self,
        identificacion,
        nombre,
        usuario,
        password,
        rol
    ):
        user = self.obtener_usuario(identificacion)

        if not user:
            raise ValueError(
                "No se encontró el usuario seleccionado"
            )

        nombre = nombre.strip()
        usuario = usuario.strip()
        password = password.strip()

        if not nombre:
            raise ValueError("El nombre es obligatorio")

        if not usuario:
            raise ValueError("El usuario es obligatorio")

        if not password:
            raise ValueError("La contraseña es obligatoria")

        if rol not in Usuario.ROLES:
            raise ValueError("El rol seleccionado no es válido")

        for otro in self.usuarios:
            if (
                otro is not user
                and otro.usuario.lower() == usuario.lower()
            ):
                raise ValueError(
                    "El nombre de usuario ya está registrado"
                )

        user.nombre = nombre
        user.usuario = usuario
        user.password = password
        user.rol = rol

        self.archivo.guardar_usuarios(
            [item.to_dict() for item in self.usuarios]
        )

        return user

    def eliminar_usuario(self, identificacion):
        user = self.obtener_usuario(identificacion)

        if not user:
            raise ValueError(
                "No se encontró el usuario seleccionado"
            )

        self.usuarios.remove(user)

        self.archivo.guardar_usuarios(
            [item.to_dict() for item in self.usuarios]
        )

    def es_administrador(self, usuario):
        return (
            usuario is not None
            and usuario.rol == "Administrador"
        )

    def obtener_producto(self, codigo):
        for producto in self.productos:
            if producto.codigo == codigo:
                return producto

        return None

    def obtener_productos(self):
        return self.productos

    def registrar_producto(
        self,
        codigo,
        nombre,
        categoria,
        precio,
        stock
    ):
        codigo = codigo.strip()
        nombre = nombre.strip()
        categoria = categoria.strip()

        if not codigo:
            raise ValueError("El código es obligatorio")

        if not nombre:
            raise ValueError("El nombre es obligatorio")

        if not categoria:
            raise ValueError("La categoría es obligatoria")

        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            raise ValueError(
                "Precio y stock deben ser valores numéricos"
            )

        if precio <= 0:
            raise ValueError(
                "El precio debe ser mayor que cero"
            )

        if stock < 0:
            raise ValueError(
                "El stock no puede ser negativo"
            )

        if self.obtener_producto(codigo):
            raise ValueError(
                "Ya existe un producto con ese código"
            )

        producto = Producto(
            codigo=codigo,
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            stock=stock,
            disponible=stock > 0
        )

        self.productos.append(producto)

        self.archivo.guardar_productos(
            [item.to_dict() for item in self.productos]
        )

        return producto

    def actualizar_producto(
        self,
        codigo,
        nombre,
        categoria,
        precio,
        stock
    ):
        producto = self.obtener_producto(codigo)

        if not producto:
            raise ValueError(
                "No se encontró el producto"
            )

        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            raise ValueError(
                "Precio y stock deben ser valores numéricos"
            )

        if precio <= 0:
            raise ValueError(
                "El precio debe ser mayor que cero"
            )

        if stock < 0:
            raise ValueError(
                "El stock no puede ser negativo"
            )

        producto.nombre = nombre.strip()
        producto.categoria = categoria.strip()
        producto.precio = precio
        producto.stock = stock
        producto.disponible = stock > 0

        self.archivo.guardar_productos(
            [item.to_dict() for item in self.productos]
        )

        return producto

    def registrar_venta(
        self,
        identificacion_usuario,
        codigo_producto,
        cantidad
    ):
        usuario = self.obtener_usuario(identificacion_usuario)

        if not usuario:
            raise ValueError(
                "El usuario no existe"
            )

        producto = self.obtener_producto(codigo_producto)

        if not producto:
            raise ValueError(
                "El producto no existe"
            )

        try:
            cantidad = int(cantidad)
        except ValueError:
            raise ValueError(
                "La cantidad debe ser un número entero"
            )

        if cantidad <= 0:
            raise ValueError(
                "La cantidad debe ser mayor que cero"
            )

        if producto.stock < cantidad:
            raise ValueError(
                "No existe suficiente stock"
            )

        producto.stock -= cantidad
        producto.disponible = producto.stock > 0

        codigo_venta = f"V{len(self.ventas) + 1:04d}"

        venta = Venta(
            codigo_venta=codigo_venta,
            identificacion_usuario=identificacion_usuario,
            codigo_producto=codigo_producto,
            cantidad=cantidad,
            precio_unitario=producto.precio,
            fecha=datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        self.ventas.append(venta)

        self.archivo.guardar_productos(
            [item.to_dict() for item in self.productos]
        )

        self.archivo.guardar_ventas(
            [item.to_dict() for item in self.ventas]
        )
        return venta

    def obtener_ventas(self):
        return self.ventas
