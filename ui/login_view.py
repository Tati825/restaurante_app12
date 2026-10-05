import tkinter as tk
from tkinter import ttk, messagebox

class LoginView(ttk.Frame):

    def __init__(self, parent, servicio, on_login):
        super().__init__(parent)

        self.parent = parent
        self.servicio = servicio
        self.on_login = on_login

        self.config(padding=30)

        self.crear_interfaz()

    def crear_interfaz(self):

        contenedor = ttk.Frame(self)
        contenedor.pack(
            expand=True
        )

        titulo = ttk.Label(
            contenedor,
            text="RESTAURANTE APP",
            font=("Arial", 22, "bold")
        )
        titulo.pack(pady=(20, 5))

        subtitulo = ttk.Label(
            contenedor,
            text="Inicio de sesión"
        )
        subtitulo.pack(pady=(0, 20))

        ttk.Label(
            contenedor,
            text="Usuario:"
        ).pack(anchor="w")

        self.usuario_entry = ttk.Entry(
            contenedor,
            width=30
        )
        self.usuario_entry.pack(
            pady=(5, 15)
        )

        ttk.Label(
            contenedor,
            text="Contraseña:"
        ).pack(anchor="w")

        self.password_entry = ttk.Entry(
            contenedor,
            width=30,
            show="*"
        )
        self.password_entry.pack(
            pady=(5, 20)
        )

        boton = ttk.Button(
            contenedor,
            text="Iniciar sesión",
            command=self.iniciar_sesion
        )
        boton.pack()

        self.password_entry.bind(
            "<Return>",
            lambda event: self.iniciar_sesion()
        )

        self.usuario_entry.focus()

    def iniciar_sesion(self):

        usuario = self.usuario_entry.get()
        password = self.password_entry.get()

        usuario_encontrado = self.servicio.autenticar_usuario(
            usuario,
            password
        )

        if usuario_encontrado:
            self.on_login(usuario_encontrado)
        else:
            messagebox.showerror(
                "Error",
                "Usuario o contraseña incorrectos"
            )
