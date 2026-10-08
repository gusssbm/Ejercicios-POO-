class Persona:
    def __init__(self, nombre, apellido, numero_documento, a_nacimiento):
        self.nombre = nombre
        self.apellido = apellido
        self.numero_documento = numero_documento
        self.a_nacimiento = a_nacimiento

    def imprimir(self):
        print("Nombre:", self.nombre)
        print("Apellido:", self.apellido)
        print("Número de documento:", self.numero_documento)
        print("Año de nacimiento:", self.a_nacimiento)


def main():
    persona1 = Persona("Laura", "Ramírez", 1020304050, 1995)
    persona2 = Persona("Carlos", "Gómez", 1098765432, 1988)

    persona1.imprimir()
    print()
    persona2.imprimir()


if __name__ == "__main__":
    main()