import tkinter as tk
from tkinter import ttk


class PruebaExcepciones:
    """Lógica: ejecuta una división y devuelve las líneas que 'se imprimen'."""

    def ejecutar(self, numerador, denominador):
        salida = []
        try:
            salida.append("Entrando al bloque try...")
            resultado = numerador / denominador
            salida.append(f"Resultado de la división: {resultado}")
        except ArithmeticError as e:  # ZeroDivisionError hereda de ArithmeticError
            salida.append(f"Se capturó una excepción aritmética: {e}")
        finally:
            salida.append("Bloque finally: se ejecuta siempre.")
        return salida


class VentanaPruebaExcepciones(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ejercicio 1 - Prueba de excepciones")
        self.prueba = PruebaExcepciones()
        marco = ttk.Frame(self, padding=12)
        marco.grid()

        ttk.Label(marco, text="Numerador:").grid(row=0, column=0, sticky="e")
        self.ent_num = ttk.Entry(marco, width=15)
        self.ent_num.grid(row=0, column=1, pady=3)
        ttk.Label(marco, text="Denominador:").grid(row=1, column=0, sticky="e")
        self.ent_den = ttk.Entry(marco, width=15)
        self.ent_den.grid(row=1, column=1, pady=3)

        ttk.Button(marco, text="Ejecutar", command=self.ejecutar).grid(row=2, column=0, columnspan=2, pady=6)
        self.salida = tk.Text(marco, width=55, height=8, state="disabled")
        self.salida.grid(row=3, column=0, columnspan=2)

    def ejecutar(self):
        try:
            num = float(self.ent_num.get().replace(",", "."))
            den = float(self.ent_den.get().replace(",", "."))
            lineas = self.prueba.ejecutar(num, den)
        except ValueError:
            lineas = ["Error: ingrese solo valores numéricos."]
        self.salida.config(state="normal")
        self.salida.delete("1.0", "end")
        self.salida.insert("end", "\n".join(lineas))
        self.salida.config(state="disabled")


if __name__ == "__main__":
    VentanaPruebaExcepciones().mainloop()