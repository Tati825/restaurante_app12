import json
from pathlib import Path

class ArchivoServicio:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.datos_dir = self.base_dir / "datos"

        self.productos_file = self.datos_dir / "productos.json"
        self.usuarios_file = self.datos_dir / "usuarios.json"
        self.ventas_file = self.datos_dir / "ventas.json"

        self.datos_dir.mkdir(exist_ok=True)

    def cargar(self, archivo):
        if not archivo.exists():
            return []

        try:
            with open(archivo, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def guardar(self, archivo, datos):
        with open(archivo, "w", encoding="utf-8") as file:
            json.dump(datos, file, ensure_ascii=False, indent=4)

    def cargar_productos(self):
        return self.cargar(self.productos_file)

    def guardar_productos(self, productos):
        self.guardar(self.productos_file, productos)

    def cargar_usuarios(self):
        return self.cargar(self.usuarios_file)

    def guardar_usuarios(self, usuarios):
        self.guardar(self.usuarios_file, usuarios)

    def cargar_ventas(self):
        return self.cargar(self.ventas_file)

    def guardar_ventas(self, ventas):
        self.guardar(self.ventas_file, ventas)
