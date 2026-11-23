import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText


class LeerArchivo:
    def __init__(self, ruta="prueba.txt"):
        self.ruta = ruta

    def leer(self):
        """Lee el archivo línea por línea desde un flujo de bytes y devuelve el texto."""
        flujo = None
        lineas = []
        try:
            flujo = open(self.ruta, "rb")  # flujo de bytes
            linea = flujo.readline()
            while linea:
                lineas.append(linea.decode("utf-8").rstrip("\r\n"))
                linea = flujo.readline()
            return "\n".join(lineas)
        finally:
            if flujo is not None:
                flujo.close()  # se cierra siempre, haya o no error


class VentanaLeerArchivo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ejercicio 5 - Leer archivo")
        marco = ttk.Frame(self, padding=12)
        marco.grid()
        ttk.Label(marco, text="Archivo:").grid(row=0, column=0)
        self.ruta = ttk.Entry(marco, width=40)
        self.ruta.insert(0, "prueba.txt")
        self.ruta.grid(row=0, column=1, padx=4)
        ttk.Button(marco, text="Examinar...", command=self.examinar).grid(row=0, column=2)
        ttk.Button(marco, text="Leer archivo", command=self.leer).grid(row=1, column=0, columnspan=3, pady=6)
        self.texto = ScrolledText(marco, width=60, height=14, state="disabled")
        self.texto.grid(row=2, column=0, columnspan=3)

    def examinar(self):
        ruta = filedialog.askopenfilename(filetypes=[("Texto", "*.txt"), ("Todos", "*.*")])
        if ruta:
            self.ruta.delete(0, "end")
            self.ruta.insert(0, ruta)

    def leer(self):
        try:
            contenido = LeerArchivo(self.ruta.get().strip()).leer()
        except FileNotFoundError:
            messagebox.showerror("Archivo no encontrado", "No existe el archivo indicado.")
            return
        except UnicodeDecodeError:
            messagebox.showerror("Codificación", "El archivo no está en UTF-8.")
            return
        except OSError as e:  # equivalente a IOException
            messagebox.showerror("Error de E/S", str(e))
            return
        self.texto.config(state="normal")
        self.texto.delete("1.0", "end")
        self.texto.insert("end", contenido)
        self.texto.config(state="disabled")


if __name__ == "__main__":
    VentanaLeerArchivo().mainloop()