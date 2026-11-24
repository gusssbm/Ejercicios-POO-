import tkinter as tk
from datetime import date, datetime
from tkinter import ttk, messagebox


class DatoInvalidoError(ValueError):
    pass


class HabitacionOcupadaError(Exception):
    pass


class HabitacionNoOcupadaError(Exception):
    pass


def moneda(valor):
    return "$" + f"{valor:,.0f}".replace(",", ".")


class Huesped:
    def __init__(self, nombre, apellidos, documento):
        self.nombre = nombre
        self.apellidos = apellidos
        self.documento = documento

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class Habitacion:
    def __init__(self, numero, precio):
        self.numero = numero
        self.precio = precio
        self.huesped = None
        self.fecha_ingreso = None

    def esta_ocupada(self):
        return self.huesped is not None


class Hotel:
    PRECIO_BAJO = 120000   # habitaciones 1 a 5
    PRECIO_ALTO = 160000   # habitaciones 6 a 10

    def __init__(self):
        self.habitaciones = [Habitacion(n, self.PRECIO_BAJO if n <= 5 else self.PRECIO_ALTO)
                             for n in range(1, 11)]

    def obtener_habitacion(self, numero):
        if not isinstance(numero, int) or not 1 <= numero <= len(self.habitaciones):
            raise DatoInvalidoError("El número de habitación debe estar entre 1 y 10")
        return self.habitaciones[numero - 1]

    def verificar_disponible(self, numero):
        hab = self.obtener_habitacion(numero)
        if hab.esta_ocupada():
            raise HabitacionOcupadaError(f"La habitación {numero} está ocupada")
        return hab

    def verificar_ocupada(self, numero):
        hab = self.obtener_habitacion(numero)
        if not hab.esta_ocupada():
            raise HabitacionNoOcupadaError(f"La habitación {numero} no está ocupada")
        return hab

    def registrar_ingreso(self, numero, huesped, fecha_ingreso):
        hab = self.verificar_disponible(numero)
        hab.huesped = huesped
        hab.fecha_ingreso = fecha_ingreso

    def calcular_estancia(self, numero, fecha_salida):
        hab = self.verificar_ocupada(numero)
        if fecha_salida <= hab.fecha_ingreso:
            raise DatoInvalidoError("La fecha de salida debe ser mayor a la fecha de ingreso")
        dias = (fecha_salida - hab.fecha_ingreso).days
        return dias, dias * hab.precio

    def registrar_salida(self, numero):
        hab = self.verificar_ocupada(numero)
        hab.huesped = None
        hab.fecha_ingreso = None

    @staticmethod
    def parsear_fecha(texto):
        try:
            return datetime.strptime(texto.strip(), "%Y-%m-%d").date()
        except ValueError:
            raise DatoInvalidoError("La fecha debe tener el formato AAAA-MM-DD (por ejemplo 2026-11-23)")

    @staticmethod
    def validar_huesped(nombre, apellidos, documento):
        for valor, campo in ((nombre, "nombre"), (apellidos, "apellidos"), (documento, "documento de identidad")):
            if not valor.strip():
                raise DatoInvalidoError(f"El campo «{campo}» es obligatorio")
        for valor, campo in ((nombre, "nombre"), (apellidos, "apellidos")):
            if any(c.isdigit() for c in valor):
                raise DatoInvalidoError(f"El campo «{campo}» no puede contener números")
        if not documento.strip().isdigit():
            raise DatoInvalidoError("El documento de identidad debe contener solo números")
        return Huesped(nombre.strip(), apellidos.strip(), documento.strip())


class VentanaRegistro(tk.Toplevel):
    """Registro del huésped en la habitación seleccionada."""

    def __init__(self, master, hotel, numero, al_registrar):
        super().__init__(master)
        self.title(f"Registro de huésped - habitación {numero}")
        self.hotel, self.numero, self.al_registrar = hotel, numero, al_registrar
        marco = ttk.Frame(self, padding=12)
        marco.grid()
        self.entradas = {}
        for i, (campo, defecto) in enumerate((("Fecha de ingreso", date.today().isoformat()),
                                              ("Nombre", ""), ("Apellidos", ""), ("Documento", ""))):
            ttk.Label(marco, text=campo + ":").grid(row=i, column=0, sticky="e", pady=3)
            e = ttk.Entry(marco, width=26)
            e.insert(0, defecto)
            e.grid(row=i, column=1)
            self.entradas[campo] = e
        ttk.Label(marco, text="Formato de fecha: AAAA-MM-DD").grid(row=4, column=1, sticky="w")
        ttk.Button(marco, text="Registrar", command=self.registrar).grid(row=5, column=0, columnspan=2, pady=8)

    def registrar(self):
        e = self.entradas
        try:
            fecha = Hotel.parsear_fecha(e["Fecha de ingreso"].get())
            huesped = Hotel.validar_huesped(e["Nombre"].get(), e["Apellidos"].get(), e["Documento"].get())
            self.hotel.registrar_ingreso(self.numero, huesped, fecha)
        except (DatoInvalidoError, HabitacionOcupadaError) as error:
            messagebox.showerror("No se pudo registrar", str(error), parent=self)
            return
        messagebox.showinfo("Registro exitoso", f"{huesped} fue registrado en la habitación {self.numero}.", parent=self)
        self.al_registrar()
        self.destroy()


class VentanaConsulta(tk.Toplevel):
    """Lista de habitaciones y su estado."""

    def __init__(self, master, hotel):
        super().__init__(master)
        self.title("Consultar habitaciones")
        self.hotel = hotel
        self.tabla = ttk.Treeview(self, columns=("numero", "precio", "estado"), show="headings",
                                  height=10, selectmode="browse")
        for col, texto, ancho in (("numero", "Habitación", 90), ("precio", "Precio por día", 130),
                                  ("estado", "Estado", 120)):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho, anchor="center")
        self.tabla.grid(padx=12, pady=12)
        ttk.Button(self, text="Ocupar habitación seleccionada", command=self.ocupar).grid(pady=(0, 12))
        self.refrescar()

    def refrescar(self):
        self.tabla.delete(*self.tabla.get_children())
        for h in self.hotel.habitaciones:
            estado = "No disponible" if h.esta_ocupada() else "Disponible"
            self.tabla.insert("", "end", iid=str(h.numero), values=(h.numero, moneda(h.precio), estado))

    def ocupar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Seleccione una habitación de la lista.", parent=self)
            return
        numero = int(seleccion[0])
        try:
            self.hotel.verificar_disponible(numero)
        except HabitacionOcupadaError as error:
            messagebox.showerror("Habitación ocupada", str(error), parent=self)
            return
        VentanaRegistro(self, self.hotel, numero, self.refrescar)


class VentanaSalida(tk.Toplevel):
    """Fecha de salida, cálculo del total y registro de la salida."""

    def __init__(self, master, hotel, numero):
        super().__init__(master)
        self.title(f"Salida - habitación {numero}")
        self.hotel, self.numero, self.fecha_salida = hotel, numero, None
        hab = hotel.obtener_habitacion(numero)
        marco = ttk.Frame(self, padding=12)
        marco.grid()
        ttk.Label(marco, text=f"Habitación {numero} - {hab.huesped}").grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(marco, text=f"Fecha de ingreso: {hab.fecha_ingreso.isoformat()}").grid(row=1, column=0, columnspan=2, sticky="w")
        ttk.Label(marco, text="Fecha de salida:").grid(row=2, column=0, sticky="e", pady=6)
        self.ent_fecha = ttk.Entry(marco, width=16)
        self.ent_fecha.insert(0, date.today().isoformat())
        self.ent_fecha.grid(row=2, column=1, sticky="w")
        self.ent_fecha.bind("<KeyRelease>", lambda _e: self.reiniciar())
        ttk.Button(marco, text="Validar fecha", command=self.validar_fecha).grid(row=3, column=0, columnspan=2)
        self.btn_calcular = ttk.Button(marco, text="Calcular total", command=self.calcular, state="disabled")
        self.btn_calcular.grid(row=4, column=0, columnspan=2, pady=4)
        self.lbl_resultado = ttk.Label(marco, text="")
        self.lbl_resultado.grid(row=5, column=0, columnspan=2)
        self.btn_salida = ttk.Button(marco, text="Registrar salida", command=self.registrar_salida, state="disabled")
        self.btn_salida.grid(row=6, column=0, columnspan=2, pady=4)

    def reiniciar(self):
        self.btn_calcular.config(state="disabled")
        self.btn_salida.config(state="disabled")
        self.lbl_resultado.config(text="")

    def validar_fecha(self):
        try:
            fecha = Hotel.parsear_fecha(self.ent_fecha.get())
            self.hotel.calcular_estancia(self.numero, fecha)  # solo para validar
        except DatoInvalidoError as error:
            self.reiniciar()
            messagebox.showerror("Fecha inválida", str(error), parent=self)
            return
        self.fecha_salida = fecha
        self.btn_calcular.config(state="normal")

    def calcular(self):
        dias, total = self.hotel.calcular_estancia(self.numero, self.fecha_salida)
        self.lbl_resultado.config(text=f"Días de alojamiento: {dias}\nTotal a pagar: {moneda(total)}")
        self.btn_salida.config(state="normal")

    def registrar_salida(self):
        self.hotel.registrar_salida(self.numero)
        messagebox.showinfo("Salida registrada", f"La habitación {self.numero} quedó disponible.", parent=self)
        self.destroy()


class VentanaSolicitud(tk.Toplevel):
    """Pide el número de habitación a entregar."""

    def __init__(self, master, hotel):
        super().__init__(master)
        self.title("Salida de huéspedes")
        self.hotel = hotel
        marco = ttk.Frame(self, padding=12)
        marco.grid()
        ttk.Label(marco, text="Número de habitación:").grid(row=0, column=0, padx=4)
        self.entrada = ttk.Entry(marco, width=8)
        self.entrada.grid(row=0, column=1)
        ttk.Button(marco, text="Continuar", command=self.continuar).grid(row=1, column=0, columnspan=2, pady=8)

    def continuar(self):
        try:
            try:
                numero = int(self.entrada.get())
            except ValueError:
                raise DatoInvalidoError("Ingrese un número de habitación válido (1 a 10)")
            self.hotel.verificar_ocupada(numero)
        except (DatoInvalidoError, HabitacionNoOcupadaError) as error:
            messagebox.showerror("No se puede continuar", str(error), parent=self)
            return
        self.destroy()
        VentanaSalida(self.master, self.hotel, numero)


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hotel")
        self.geometry("340x120")
        self.hotel = Hotel()
        barra = tk.Menu(self)
        barra.add_command(label="Consultar habitaciones", command=lambda: VentanaConsulta(self, self.hotel))
        barra.add_command(label="Salida de huéspedes", command=lambda: VentanaSolicitud(self, self.hotel))
        self.config(menu=barra)
        ttk.Label(self, text="Use el menú para gestionar las habitaciones.").pack(expand=True)


if __name__ == "__main__":
    VentanaPrincipal().mainloop()