import math
import tkinter as tk
from tkinter import ttk, messagebox


class CalculosNumericos:
    @staticmethod
    def logaritmo_neperiano(valor):
        if valor <= 0:
            raise ArithmeticError("El valor debe ser positivo para calcular el logaritmo")
        return math.log(valor)

    @staticmethod
    def raiz_cuadrada(valor):
        if valor <= 0:
            raise ArithmeticError("El valor debe ser positivo para calcular la raíz cuadrada")
        return math.sqrt(valor)


class VentanaCalculos(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ejercicio 3 - Cálculos numéricos")
        marco = ttk.Frame(self, padding=12)
        marco.grid()
        ttk.Label(marco, text="Valor:").grid(row=0, column=0)
        self.entrada = ttk.Entry(marco, width=18)
        self.entrada.grid(row=0, column=1, columnspan=2, pady=3)
        ttk.Button(marco, text="Logaritmo neperiano",
                   command=lambda: self.calcular(CalculosNumericos.logaritmo_neperiano, "ln")).grid(row=1, column=0, columnspan=2, pady=4)
        ttk.Button(marco, text="Raíz cuadrada",
                   command=lambda: self.calcular(CalculosNumericos.raiz_cuadrada, "√")).grid(row=1, column=2, pady=4)
        self.resultado = ttk.Label(marco, text="Resultado: -")
        self.resultado.grid(row=2, column=0, columnspan=3)

    def calcular(self, operacion, simbolo):
        try:
            valor = float(self.entrada.get().replace(",", "."))
            r = operacion(valor)
            self.resultado.config(text=f"{simbolo}({valor}) = {r:.6f}")
        except ValueError:  # equivalente a InputMismatchException
            messagebox.showerror("Entrada inválida", "Ingrese un valor numérico.")
        except ArithmeticError as e:
            messagebox.showerror("Error aritmético", str(e))


if __name__ == "__main__":
    VentanaCalculos().mainloop()