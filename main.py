import tkinter as tk
from tkinter import ttk
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

class RestauranteApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Restaurante App"
        )

        self.root.geometry(
            "1100x700"
        )

        self.root.minsize(
            900,
            600
        )

        self.servicio = RestauranteServicio()

        self.mostrar_login()

    def limpiar_ventana(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_login(self):

        self.limpiar_ventana()

        login = LoginView(
            self.root,
            self.servicio,
            self.iniciar_sesion
        )

        login.pack(
            fill="both",
            expand=True
        )

    def iniciar_sesion(self, usuario):

        self.limpiar_ventana()

        main_view = MainView(
            self.root,
            self.servicio,
            usuario,
            self.mostrar_login
        )

        main_view.pack(
            fill="both",
            expand=True
        )

def main():

    root = tk.Tk()

    app = RestauranteApp(root)

    root.mainloop()

if __name__ == "__main__":
    main()
