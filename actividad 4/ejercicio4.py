import tkinter as tk
from tkinter import ttk, messagebox


class EquipoLlenoError(Exception):
    pass


class DatoInvalidoError(ValueError):
    pass


class Programador:
    def __init__(self, nombre, apellidos):
        self.nombre = nombre
        self.apellidos = apellidos

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class EquipoMaratonProgramacion:
    MINIMO = 2
    MAXIMO = 3

    def __init__(self, nombre, universidad, lenguaje, tamano):
        if not self.MINIMO <= tamano <= self.MAXIMO:
            raise DatoInvalidoError(f"El tamaño debe estar entre {self.MINIMO} y {self.MAXIMO}")
        self.nombre = nombre
        self.universidad = universidad
        self.lenguaje = lenguaje
        self.tamano = tamano
        self.programadores = []

    def esta_completo(self):
        return len(self.programadores) >= self.tamano

    def anadir_programador(self, programador):
        if self.esta_completo():
            raise EquipoLlenoError("El equipo está lleno, no se pueden añadir más programadores")
        self.programadores.append(programador)

    @staticmethod
    def validar_texto(valor, campo):
        if not valor.strip():
            raise DatoInvalidoError(f"El campo {campo} no puede estar vacío")
        for caracter in valor:
            if caracter.isdigit():
                raise DatoInvalidoError(f"El campo {campo} solo admite texto (no números)")
        if len(valor) >= 20:
            raise DatoInvalidoError(f"El campo {campo} debe tener menos de 20 caracteres")

    def validar_programador(self, nombre, apellidos):
        self.validar_texto(nombre, "nombre")
        self.validar_texto(apellidos, "apellidos")
        return Programador(nombre.strip(), apellidos.strip())


class VentanaEquipo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ejercicio 4 - Equipo de maratón de programación")
        self.equipo = None

        eq = ttk.LabelFrame(self, text="1. Datos del equipo", padding=10)
        eq.grid(row=0, column=0, padx=10, pady=6, sticky="ew")
        self.e_nombre, self.e_univ, self.e_leng = (ttk.Entry(eq, width=26) for _ in range(3))
        for i, (txt, ent) in enumerate((("Nombre:", self.e_nombre), ("Universidad:", self.e_univ), ("Lenguaje:", self.e_leng))):
            ttk.Label(eq, text=txt).grid(row=i, column=0, sticky="e")
            ent.grid(row=i, column=1, pady=2)
        ttk.Label(eq, text="Tamaño (2-3):").grid(row=3, column=0, sticky="e")
        self.s_tam = ttk.Spinbox(eq, from_=2, to=3, width=5)
        self.s_tam.set(2)
        self.s_tam.grid(row=3, column=1, sticky="w")
        ttk.Button(eq, text="Crear equipo", command=self.crear_equipo).grid(row=4, column=0, columnspan=2, pady=5)

        pr = ttk.LabelFrame(self, text="2. Añadir programador", padding=10)
        pr.grid(row=1, column=0, padx=10, pady=6, sticky="ew")
        self.p_nombre, self.p_apellidos = ttk.Entry(pr, width=26), ttk.Entry(pr, width=26)
        ttk.Label(pr, text="Nombre:").grid(row=0, column=0, sticky="e")
        self.p_nombre.grid(row=0, column=1, pady=2)
        ttk.Label(pr, text="Apellidos:").grid(row=1, column=0, sticky="e")
        self.p_apellidos.grid(row=1, column=1, pady=2)
        ttk.Button(pr, text="Añadir", command=self.anadir).grid(row=2, column=0, columnspan=2, pady=5)

        self.lista = tk.Listbox(self, height=4)
        self.lista.grid(row=2, column=0, padx=10, sticky="ew")
        self.estado = ttk.Label(self, text="Cree un equipo para comenzar.")
        self.estado.grid(row=3, column=0, pady=6)

    def crear_equipo(self):
        try:
            nombre, univ, leng = self.e_nombre.get().strip(), self.e_univ.get().strip(), self.e_leng.get().strip()
            if not (nombre and univ and leng):
                raise DatoInvalidoError("Complete todos los datos del equipo")
            self.equipo = EquipoMaratonProgramacion(nombre, univ, leng, int(self.s_tam.get()))
            self.lista.delete(0, "end")
            self.actualizar_estado()
        except ValueError as e:  # incluye DatoInvalidoError
            messagebox.showerror("Dato inválido", str(e))

    def anadir(self):
        if self.equipo is None:
            messagebox.showwarning("Falta el equipo", "Primero cree el equipo.")
            return
        try:
            prog = self.equipo.validar_programador(self.p_nombre.get(), self.p_apellidos.get())
            self.equipo.anadir_programador(prog)
            self.lista.insert("end", str(prog))
            self.p_nombre.delete(0, "end")
            self.p_apellidos.delete(0, "end")
            self.actualizar_estado()
        except DatoInvalidoError as e:
            messagebox.showerror("Dato inválido", str(e))
        except EquipoLlenoError as e:
            messagebox.showwarning("Equipo lleno", str(e))

    def actualizar_estado(self):
        e = self.equipo
        completo = "COMPLETO" if e.esta_completo() else "incompleto"
        self.estado.config(text=f"{e.nombre} ({e.universidad}, {e.lenguaje}): {len(e.programadores)}/{e.tamano} - {completo}")


if __name__ == "__main__":
    VentanaEquipo().mainloop()