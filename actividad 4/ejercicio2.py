import tkinter as tk
from tkinter import ttk, messagebox


class ArgumentoIlegalError(ValueError):
    """Equivalente en Python de IllegalArgumentException."""


class Vendedor:
    def __init__(self, nombre, apellidos, edad):
        self.verificar_edad(edad)  # si no cumple, el objeto no se instancia
        self.nombre = nombre
        self.apellidos = apellidos
        self.edad = edad

    @staticmethod
    def verificar_edad(edad):
        # Se revisa primero el rango; si no, el mensaje de "negativa o mayor a 120" sería inalcanzable.
        if edad < 0 or edad > 120:
            raise ArgumentoIlegalError("La edad no puede ser negativa ni mayor a 120")
        if edad <= 18:
            raise ArgumentoIlegalError("El vendedor debe ser mayor de 18 años")

    def imprimir(self):
        return f"Nombre: {self.nombre}\nApellidos: {self.apellidos}\nEdad: {self.edad}"


class VentanaVendedor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ejercicio 2 - Vendedor")
        marco = ttk.Frame(self, padding=12)
        marco.grid()
        self.campos = {}
        for i, etiqueta in enumerate(("Nombre", "Apellidos", "Edad")):
            ttk.Label(marco, text=etiqueta + ":").grid(row=i, column=0, sticky="e")
            e = ttk.Entry(marco, width=28)
            e.grid(row=i, column=1, pady=3)
            self.campos[etiqueta] = e
        ttk.Button(marco, text="Crear vendedor", command=self.crear).grid(row=3, column=0, columnspan=2, pady=6)
        self.resultado = ttk.Label(marco, text="", justify="left")
        self.resultado.grid(row=4, column=0, columnspan=2)

    def crear(self):
        try:
            nombre = self.campos["Nombre"].get().strip()
            apellidos = self.campos["Apellidos"].get().strip()
            if not nombre or not apellidos:
                raise ArgumentoIlegalError("Nombre y apellidos son obligatorios")
            edad = int(self.campos["Edad"].get())
            vendedor = Vendedor(nombre, apellidos, edad)
            self.resultado.config(text="Vendedor creado:\n" + vendedor.imprimir())
        except ArgumentoIlegalError as e:
            self.resultado.config(text="")
            messagebox.showerror("Dato inválido", str(e))
        except ValueError:
            self.resultado.config(text="")
            messagebox.showerror("Dato inválido", "La edad debe ser un número entero")


if __name__ == "__main__":
    VentanaVendedor().mainloop()