import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class DatoInvalidoError(ValueError):
    """Se lanza cuando un dato del empleado no cumple las validaciones."""


def moneda(valor):
    """Formatea un valor como pesos: $1.234.567"""
    return "$" + f"{valor:,.0f}".replace(",", ".")


def a_numero(texto, campo):
    try:
        return float(texto.strip().replace(",", "."))
    except ValueError:
        raise DatoInvalidoError(f"El campo «{campo}» debe ser un número")


class Empleado:
    CARGOS = ("Directivo", "Estratégico", "Operativo")
    GENEROS = ("Masculino", "Femenino")

    def __init__(self, nombre, apellidos, cargo, genero, salario_dia,
                 dias_trabajados, otros_ingresos, pagos_salud, aporte_pensiones):
        self.nombre = self._validar_texto(nombre, "nombre")
        self.apellidos = self._validar_texto(apellidos, "apellidos")
        if cargo not in self.CARGOS:
            raise DatoInvalidoError("Seleccione un cargo")
        if genero not in self.GENEROS:
            raise DatoInvalidoError("Seleccione un género")
        if not 1 <= dias_trabajados <= 31:
            raise DatoInvalidoError("Los días trabajados deben estar entre 1 y 31")
        for valor, campo in ((salario_dia, "salario por día"), (otros_ingresos, "otros ingresos"),
                             (pagos_salud, "pagos por salud"), (aporte_pensiones, "aporte pensiones")):
            if valor < 0:
                raise DatoInvalidoError(f"El campo «{campo}» no puede ser negativo")
        self.cargo = cargo
        self.genero = genero
        self.salario_dia = salario_dia
        self.dias_trabajados = dias_trabajados
        self.otros_ingresos = otros_ingresos
        self.pagos_salud = pagos_salud
        self.aporte_pensiones = aporte_pensiones

    @staticmethod
    def _validar_texto(valor, campo):
        valor = valor.strip()
        if not valor:
            raise DatoInvalidoError(f"El campo «{campo}» es obligatorio")
        if any(c.isdigit() for c in valor):
            raise DatoInvalidoError(f"El campo «{campo}» no puede contener números")
        return valor

    def salario_mensual(self):
        return (self.dias_trabajados * self.salario_dia) + self.otros_ingresos \
            - self.pagos_salud - self.aporte_pensiones


class Nomina:
    def __init__(self):
        self.empleados = []

    def agregar_empleado(self, empleado):
        self.empleados.append(empleado)

    def total_nomina(self):
        return sum(e.salario_mensual() for e in self.empleados)

    def guardar_archivo(self, carpeta):
        ruta = os.path.join(carpeta, "Nómina.txt")
        with open(ruta, "w", encoding="utf-8") as archivo:
            for i, e in enumerate(self.empleados, start=1):
                archivo.write(f"Empleado {i}\n")
                archivo.write(f"  Nombre: {e.nombre} {e.apellidos}\n")
                archivo.write(f"  Cargo: {e.cargo} | Género: {e.genero}\n")
                archivo.write(f"  Salario por día: {moneda(e.salario_dia)} | Días trabajados: {e.dias_trabajados}\n")
                archivo.write(f"  Otros ingresos: {moneda(e.otros_ingresos)}\n")
                archivo.write(f"  Pagos por salud: {moneda(e.pagos_salud)} | Aporte pensiones: {moneda(e.aporte_pensiones)}\n")
                archivo.write(f"  Sueldo mensual: {moneda(e.salario_mensual())}\n\n")
            archivo.write(f"TOTAL NÓMINA: {moneda(self.total_nomina())}\n")
        return ruta


class VentanaAgregar(tk.Toplevel):
    def __init__(self, master, nomina, al_agregar):
        super().__init__(master)
        self.title("Agregar empleado")
        self.nomina = nomina
        self.al_agregar = al_agregar
        marco = ttk.Frame(self, padding=12)
        marco.grid()

        self.entradas = {}
        campos = ("Nombre", "Apellidos")
        for i, c in enumerate(campos):
            ttk.Label(marco, text=c + ":").grid(row=i, column=0, sticky="e", pady=2)
            self.entradas[c] = ttk.Entry(marco, width=28)
            self.entradas[c].grid(row=i, column=1, sticky="w")

        ttk.Label(marco, text="Cargo:").grid(row=2, column=0, sticky="ne", pady=2)  # JList
        self.lista_cargo = tk.Listbox(marco, height=3, exportselection=False, width=20)
        for cargo in Empleado.CARGOS:
            self.lista_cargo.insert("end", cargo)
        self.lista_cargo.grid(row=2, column=1, sticky="w")

        ttk.Label(marco, text="Género:").grid(row=3, column=0, sticky="e", pady=2)  # JCheckBox
        marco_genero = ttk.Frame(marco)
        marco_genero.grid(row=3, column=1, sticky="w")
        self.var_masc, self.var_fem = tk.BooleanVar(), tk.BooleanVar()
        ttk.Checkbutton(marco_genero, text="Masculino", variable=self.var_masc,
                        command=lambda: self.var_fem.set(False)).pack(side="left")
        ttk.Checkbutton(marco_genero, text="Femenino", variable=self.var_fem,
                        command=lambda: self.var_masc.set(False)).pack(side="left", padx=8)

        for i, c in enumerate(("Salario por día", "Otros ingresos", "Pagos por salud", "Aporte pensiones"), start=4):
            ttk.Label(marco, text=c + ":").grid(row=i, column=0, sticky="e", pady=2)
            self.entradas[c] = ttk.Entry(marco, width=28)
            self.entradas[c].grid(row=i, column=1, sticky="w")

        ttk.Label(marco, text="Días trabajados:").grid(row=8, column=0, sticky="e", pady=2)  # JSpinner
        self.spin_dias = ttk.Spinbox(marco, from_=1, to=31, width=6)
        self.spin_dias.set(30)
        self.spin_dias.grid(row=8, column=1, sticky="w")

        ttk.Button(marco, text="Guardar empleado", command=self.guardar).grid(row=9, column=0, columnspan=2, pady=10)

    def guardar(self):
        try:
            seleccion = self.lista_cargo.curselection()
            cargo = self.lista_cargo.get(seleccion[0]) if seleccion else ""
            genero = "Masculino" if self.var_masc.get() else "Femenino" if self.var_fem.get() else ""
            try:
                dias = int(self.spin_dias.get())
            except ValueError:
                raise DatoInvalidoError("Los días trabajados deben ser un número entero")
            e = self.entradas
            empleado = Empleado(
                e["Nombre"].get(), e["Apellidos"].get(), cargo, genero,
                a_numero(e["Salario por día"].get(), "salario por día"), dias,
                a_numero(e["Otros ingresos"].get(), "otros ingresos"),
                a_numero(e["Pagos por salud"].get(), "pagos por salud"),
                a_numero(e["Aporte pensiones"].get(), "aporte pensiones"))
        except DatoInvalidoError as error:
            messagebox.showerror("Dato inválido", str(error), parent=self)
            return
        self.nomina.agregar_empleado(empleado)
        self.al_agregar()
        messagebox.showinfo("Empleado agregado", f"Se agregó a {empleado.nombre} {empleado.apellidos}.", parent=self)
        self.destroy()


class VentanaNomina(tk.Toplevel):
    def __init__(self, master, nomina):
        super().__init__(master)
        self.title("Nómina de la empresa")
        tabla = ttk.Treeview(self, columns=("nombre", "apellidos", "sueldo"), show="headings", height=8)
        for col, texto in (("nombre", "Nombre"), ("apellidos", "Apellidos"), ("sueldo", "Sueldo mensual")):
            tabla.heading(col, text=texto)
            tabla.column(col, width=160, anchor="w" if col != "sueldo" else "e")
        for e in nomina.empleados:
            tabla.insert("", "end", values=(e.nombre, e.apellidos, moneda(e.salario_mensual())))
        tabla.grid(padx=12, pady=12)
        ttk.Label(self, text=f"Total de la nómina: {moneda(nomina.total_nomina())}",
                  font=("TkDefaultFont", 11, "bold")).grid(pady=(0, 12))


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nómina de empleados")
        self.geometry("360x140")
        self.nomina = Nomina()
        barra = tk.Menu(self)
        barra.add_command(label="Agregar empleado", command=self.agregar)
        barra.add_command(label="Calcular nómina", command=self.calcular)
        barra.add_command(label="Guardar archivo", command=self.guardar)
        self.config(menu=barra)
        self.estado = ttk.Label(self, text="Empleados registrados: 0")
        self.estado.pack(expand=True)

    def actualizar_estado(self):
        self.estado.config(text=f"Empleados registrados: {len(self.nomina.empleados)}")

    def agregar(self):
        VentanaAgregar(self, self.nomina, self.actualizar_estado)

    def hay_empleados(self):
        if not self.nomina.empleados:
            messagebox.showwarning("Sin empleados", "Primero agregue al menos un empleado.")
            return False
        return True

    def calcular(self):
        if self.hay_empleados():
            VentanaNomina(self, self.nomina)

    def guardar(self):
        if not self.hay_empleados():
            return
        carpeta = filedialog.askdirectory(title="Seleccione la carpeta donde guardar Nómina.txt")
        if not carpeta:
            return
        try:
            ruta = self.nomina.guardar_archivo(carpeta)
            messagebox.showinfo("Archivo guardado", f"Se guardó en:\n{ruta}")
        except OSError as e:
            messagebox.showerror("Error al guardar", str(e))


if __name__ == "__main__":
    VentanaPrincipal().mainloop()