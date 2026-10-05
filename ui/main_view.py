import tkinter as tk
from tkinter import ttk, messagebox

class MainView(ttk.Frame):
    def __init__(
        self,
        parent,
        servicio,
        usuario_actual,
        on_logout
    ):
        super().__init__(parent)

        self.parent = parent
        self.servicio = servicio
        self.usuario_actual = usuario_actual
        self.on_logout = on_logout

        self.crear_interfaz()

    def crear_interfaz(self):

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.crear_encabezado()
        self.crear_navegacion()
        self.crear_contenido()

        self.mostrar_productos()

    def crear_encabezado(self):

        encabezado = ttk.Frame(
            self,
            padding=10
        )
        encabezado.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        encabezado.columnconfigure(0, weight=1)

        titulo = ttk.Label(
            encabezado,
            text="RESTAURANTE APP",
            font=("Arial", 18, "bold")
        )
        titulo.grid(
            row=0,
            column=0,
            sticky="w"
        )

        usuario_texto = (
            f"Usuario: {self.usuario_actual.nombre} | "
            f"Rol: {self.usuario_actual.rol}"
        )

        ttk.Label(
            encabezado,
            text=usuario_texto
        ).grid(
            row=0,
            column=1,
            sticky="e",
            padx=10
        )

        ttk.Button(
            encabezado,
            text="Cerrar sesión",
            command=self.cerrar_sesion
        ).grid(
            row=0,
            column=2
        )

    def crear_navegacion(self):

        navegacion = ttk.Frame(
            self,
            padding=(10, 0, 10, 10)
        )

        navegacion.grid(
            row=1,
            column=0,
            sticky="n"
        )

        ttk.Button(
            navegacion,
            text="Productos",
            command=self.mostrar_productos
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            navegacion,
            text="Ventas",
            command=self.mostrar_ventas
        ).pack(
            side="left",
            padx=5
        )

        if self.servicio.es_administrador(
            self.usuario_actual
        ):
            ttk.Button(
                navegacion,
                text="Usuarios",
                command=self.mostrar_usuarios
            ).pack(
                side="left",
                padx=5
            )

    def crear_contenido(self):

        self.contenido = ttk.Frame(
            self,
            padding=10
        )

        self.contenido.grid(
            row=2,
            column=0,
            sticky="nsew"
        )

        self.contenido.grid_rowconfigure(
            0,
            weight=1
        )

        self.contenido.grid_columnconfigure(
            0,
            weight=1
        )

    def limpiar_contenido(self):

        for widget in self.contenido.winfo_children():
            widget.destroy()

    def mostrar_productos(self):

        self.limpiar_contenido()

        titulo = ttk.Label(
            self.contenido,
            text="Gestión de productos",
            font=("Arial", 16, "bold")
        )
        titulo.pack(
            pady=(0, 10)
        )

        tabla = ttk.Treeview(
            self.contenido,
            columns=(
                "codigo",
                "nombre",
                "categoria",
                "precio",
                "stock"
            ),
            show="headings",
            height=15
        )

        columnas = {
            "codigo": "Código",
            "nombre": "Nombre",
            "categoria": "Categoría",
            "precio": "Precio",
            "stock": "Stock"
        }

        for columna, texto in columnas.items():
            tabla.heading(
                columna,
                text=texto
            )

        tabla.pack(
            fill="both",
            expand=True
        )

        for producto in self.servicio.obtener_productos():

            tabla.insert(
                "",
                "end",
                values=(
                    producto.codigo,
                    producto.nombre,
                    producto.categoria,
                    f"${producto.precio:.2f}",
                    producto.stock
                )
            )

    def mostrar_ventas(self):

        self.limpiar_contenido()

        titulo = ttk.Label(
            self.contenido,
            text="Gestión de ventas",
            font=("Arial", 16, "bold")
        )
        titulo.pack(
            pady=(0, 10)
        )

        formulario = ttk.Frame(
            self.contenido
        )
        formulario.pack(
            fill="x",
            pady=10
        )

        ttk.Label(
            formulario,
            text="Producto:"
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        self.producto_venta = ttk.Combobox(
            formulario,
            state="readonly",
            width=30
        )
        self.producto_venta.grid(
            row=0,
            column=1,
            padx=5
        )

        productos = self.servicio.obtener_productos()

        self.productos_venta_dict = {
            f"{p.codigo} - {p.nombre}": p.codigo
            for p in productos
        }

        self.producto_venta["values"] = list(
            self.productos_venta_dict.keys()
        )

        ttk.Label(
            formulario,
            text="Cantidad:"
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        self.cantidad_venta = ttk.Entry(
            formulario,
            width=10
        )
        self.cantidad_venta.grid(
            row=0,
            column=3,
            padx=5
        )

        ttk.Button(
            formulario,
            text="Registrar venta",
            command=self.registrar_venta
        ).grid(
            row=0,
            column=4,
            padx=10
        )

        tabla = ttk.Treeview(
            self.contenido,
            columns=(
                "codigo",
                "usuario",
                "producto",
                "cantidad",
                "total",
                "fecha"
            ),
            show="headings",
            height=12
        )

        columnas = {
            "codigo": "Venta",
            "usuario": "Usuario",
            "producto": "Producto",
            "cantidad": "Cantidad",
            "total": "Total",
            "fecha": "Fecha"
        }

        for columna, texto in columnas.items():
            tabla.heading(
                columna,
                text=texto
            )

        tabla.pack(
            fill="both",
            expand=True
        )

        for venta in self.servicio.obtener_ventas():

            tabla.insert(
                "",
                "end",
                values=(
                    venta.codigo_venta,
                    venta.identificacion_usuario,
                    venta.codigo_producto,
                    venta.cantidad,
                    f"${venta.total:.2f}",
                    venta.fecha
                )
            )

    def registrar_venta(self):

        seleccion = self.producto_venta.get()
        cantidad = self.cantidad_venta.get()

        if not seleccion:
            messagebox.showwarning(
                "Advertencia",
                "Seleccione un producto."
            )
            return

        codigo_producto = self.productos_venta_dict[
            seleccion
        ]

        try:
            venta = self.servicio.registrar_venta(
                self.usuario_actual.identificacion,
                codigo_producto,
                cantidad
            )

            messagebox.showinfo(
                "Venta registrada",
                f"Venta {venta.codigo_venta} registrada"
            )

            self.mostrar_ventas()

        except ValueError as error:
            messagebox.showerror(
                "Error",
                str(error)
            )

    def mostrar_usuarios(self):

        if not self.servicio.es_administrador(
            self.usuario_actual
        ):
            messagebox.showerror(
                "Acceso denegado",
                "Solo un Administrador puede gestionar usuarios"
            )
            return

        self.limpiar_contenido()

        titulo = ttk.Label(
            self.contenido,
            text="Gestión administrativa de usuarios",
            font=("Arial", 16, "bold")
        )
        titulo.pack(
            pady=(0, 10)
        )

        contenedor = ttk.Frame(
            self.contenido
        )
        contenedor.pack(
            fill="both",
            expand=True
        )

        contenedor.columnconfigure(
            1,
            weight=1
        )

        contenedor.rowconfigure(
            0,
            weight=1
        )

        formulario = ttk.LabelFrame(
            contenedor,
            text="Datos del usuario",
            padding=15
        )

        formulario.grid(
            row=0,
            column=0,
            sticky="ns",
            padx=(0, 15)
        )

        ttk.Label(
            formulario,
            text="Identificación:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=5
        )

        self.identificacion_entry = ttk.Entry(
            formulario,
            width=30
        )

        self.identificacion_entry.grid(
            row=0,
            column=1,
            pady=5
        )

        ttk.Label(
            formulario,
            text="Nombre:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=5
        )

        self.nombre_usuario_entry = ttk.Entry(
            formulario,
            width=30
        )

        self.nombre_usuario_entry.grid(
            row=1,
            column=1,
            pady=5
        )

        ttk.Label(
            formulario,
            text="Usuario:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=5
        )

        self.usuario_entry = ttk.Entry(
            formulario,
            width=30
        )

        self.usuario_entry.grid(
            row=2,
            column=1,
            pady=5
        )

        ttk.Label(
            formulario,
            text="Contraseña:"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=5
        )

        self.password_usuario_entry = ttk.Entry(
            formulario,
            width=30,
            show="*"
        )

        self.password_usuario_entry.grid(
            row=3,
            column=1,
            pady=5
        )

        ttk.Label(
            formulario,
            text="Rol:"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=5
        )

        self.rol_combobox = ttk.Combobox(
            formulario,
            values=[
                "Administrador",
                "Empleado",
                "Cliente"
            ],
            state="readonly",
            width=27
        )

        self.rol_combobox.grid(
            row=4,
            column=1,
            pady=5
        )

        self.rol_combobox.set("Cliente")

        self.rol_combobox.bind(
            "<<ComboboxSelected>>",
            self.rol_seleccionado
        )

        botones = ttk.Frame(
            formulario
        )

        botones.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=20
        )

        ttk.Button(
            botones,
            text="Registrar",
            command=self.registrar_usuario
        ).pack(
            side="left",
            padx=3
        )

        ttk.Button(
            botones,
            text="Actualizar",
            command=self.actualizar_usuario
        ).pack(
            side="left",
            padx=3
        )

        ttk.Button(
            botones,
            text="Eliminar",
            command=self.eliminar_usuario
        ).pack(
            side="left",
            padx=3
        )

        ttk.Button(
            botones,
            text="Limpiar",
            command=self.limpiar_usuario
        ).pack(
            side="left",
            padx=3
        )

        self.identificacion_entry.bind(
            "<Return>",
            self.registrar_usuario_evento
        )

        self.nombre_usuario_entry.bind(
            "<Return>",
            self.registrar_usuario_evento
        )

        self.usuario_entry.bind(
            "<Return>",
            self.registrar_usuario_evento
        )

        self.password_usuario_entry.bind(
            "<Return>",
            self.registrar_usuario_evento
        )

        self.rol_combobox.bind(
            "<Return>",
            self.registrar_usuario_evento,
            add="+"
        )

        self.contenido.bind(
            "<Escape>",
            self.limpiar_usuario_evento
        )

        tabla_frame = ttk.LabelFrame(
            contenedor,
            text="Usuarios registrados",
            padding=10
        )

        tabla_frame.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        tabla_frame.rowconfigure(
            0,
            weight=1
        )

        tabla_frame.columnconfigure(
            0,
            weight=1
        )

        self.usuarios_tree = ttk.Treeview(
            tabla_frame,
            columns=(
                "identificacion",
                "nombre",
                "usuario",
                "rol"
            ),
            show="headings",
            selectmode="browse"
        )

        self.usuarios_tree.heading(
            "identificacion",
            text="Identificador"
        )

        self.usuarios_tree.heading(
            "nombre",
            text="Nombre"
        )

        self.usuarios_tree.heading(
            "usuario",
            text="Usuario"
        )

        self.usuarios_tree.heading(
            "rol",
            text="Rol"
        )

        self.usuarios_tree.column(
            "identificacion",
            width=110
        )

        self.usuarios_tree.column(
            "nombre",
            width=180
        )

        self.usuarios_tree.column(
            "usuario",
            width=130
        )

        self.usuarios_tree.column(
            "rol",
            width=130
        )

        self.usuarios_tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.usuarios_tree.yview
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.usuarios_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.usuarios_tree.bind(
            "<<TreeviewSelect>>",
            self.usuario_seleccionado
        )

        self.cargar_usuarios_tree()

    def rol_seleccionado(self, event=None):

        rol = self.rol_combobox.get()

        if rol:
            print(
                f"Rol seleccionado: {rol}"
            )

    def cargar_usuarios_tree(self):

        for item in self.usuarios_tree.get_children():
            self.usuarios_tree.delete(item)

        for usuario in self.servicio.obtener_usuarios():

            self.usuarios_tree.insert(
                "",
                "end",
                iid=usuario.identificacion,
                values=(
                    usuario.identificacion,
                    usuario.nombre,
                    usuario.usuario,
                    usuario.rol
                )
            )

    def usuario_seleccionado(self, event=None):

        seleccion = self.usuarios_tree.selection()

        if not seleccion:
            return

        identificacion = seleccion[0]

        usuario = self.servicio.obtener_usuario(
            identificacion
        )

        if not usuario:
            return

        self.identificacion_entry.delete(
            0,
            tk.END
        )

        self.identificacion_entry.insert(
            0,
            usuario.identificacion
        )

        self.nombre_usuario_entry.delete(
            0,
            tk.END
        )

        self.nombre_usuario_entry.insert(
            0,
            usuario.nombre
        )

        self.usuario_entry.delete(
            0,
            tk.END
        )

        self.usuario_entry.insert(
            0,
            usuario.usuario
        )

        self.password_usuario_entry.delete(
            0,
            tk.END
        )

        self.password_usuario_entry.insert(
            0,
            usuario.password
        )

        self.rol_combobox.set(
            usuario.rol
        )

    def registrar_usuario(self):

        try:

            usuario = self.servicio.registrar_usuario(
                self.identificacion_entry.get(),
                self.nombre_usuario_entry.get(),
                self.usuario_entry.get(),
                self.password_usuario_entry.get(),
                self.rol_combobox.get()
            )

            messagebox.showinfo(
                "Usuario registrado",
                f"El usuario {usuario.nombre} fue registrado correctamente"
            )

            self.limpiar_usuario()
            self.cargar_usuarios_tree()

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    def registrar_usuario_evento(self, event=None):
        self.registrar_usuario()

    def actualizar_usuario(self):
        identificacion = (
            self.identificacion_entry.get().strip()
        )

        if not identificacion:
            messagebox.showwarning(
                "Advertencia",
                "Seleccione un usuario para actualizar"
            )
            return

        try:

            usuario = self.servicio.actualizar_usuario(
                identificacion,
                self.nombre_usuario_entry.get(),
                self.usuario_entry.get(),
                self.password_usuario_entry.get(),
                self.rol_combobox.get()
            )

            messagebox.showinfo(
                "Usuario actualizado",
                f"El usuario {usuario.nombre} fue actualizado"
            )

            self.limpiar_usuario()
            self.cargar_usuarios_tree()

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    def eliminar_usuario(self):

        identificacion = (
            self.identificacion_entry.get().strip()
        )

        if not identificacion:
            messagebox.showwarning(
                "Advertencia",
                "Seleccione un usuario para eliminar"
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Está seguro de eliminar este usuario?"
        )

        if not confirmar:
            return

        try:

            self.servicio.eliminar_usuario(
                identificacion
            )

            messagebox.showinfo(
                "Usuario eliminado",
                "El usuario fue eliminado correctamente"
            )

            self.limpiar_usuario()
            self.cargar_usuarios_tree()

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    def limpiar_usuario(self):

        self.identificacion_entry.delete(
            0,
            tk.END
        )

        self.nombre_usuario_entry.delete(
            0,
            tk.END
        )

        self.usuario_entry.delete(
            0,
            tk.END
        )

        self.password_usuario_entry.delete(
            0,
            tk.END
        )

        self.rol_combobox.set(
            "Cliente"
        )

        seleccion = self.usuarios_tree.selection()

        if seleccion:
            self.usuarios_tree.selection_remove(
                seleccion
            )

        self.identificacion_entry.focus()

    def limpiar_usuario_evento(self, event=None):

        # Reutiliza el método existente.
        self.limpiar_usuario()

    def cerrar_sesion(self):
        self.on_logout()
