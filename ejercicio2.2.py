from enum import Enum


class TipoPlaneta(Enum):
    GASEOSO = 1
    TERRESTRE = 2
    ENANO = 3


class Planeta:
    UA_EN_KM = 149597870
    LIMITE_CINTURON_UA = 3.4
    def __init__(self, nombre=None, cantidad_satelites=0, masa=0.0, volumen=0.0,
                 diametro=0, distancia_sol=0, tipo=None, observable=False):
        self.nombre = nombre
        self.cantidad_satelites = cantidad_satelites
        self.masa = masa
        self.volumen = volumen
        self.diametro = diametro
        self.distancia_sol = distancia_sol
        self.tipo = tipo
        self.observable = observable

    def imprimir(self):
        tipo = self.tipo.name if self.tipo is not None else None
        print("Nombre:", self.nombre)
        print("Cantidad de satélites:", self.cantidad_satelites)
        print("Masa:", self.masa, "kg")
        print("Volumen:", self.volumen, "km³")
        print("Diámetro:", self.diametro, "km")
        print("Distancia media al Sol:", self.distancia_sol, "millones de km")
        print("Tipo de planeta:", tipo)
        print("Observable a simple vista:", self.observable)

    def calcular_densidad(self):
        if self.volumen == 0:
            return 0.0
        return self.masa / self.volumen

    def es_exterior(self):
        limite = self.LIMITE_CINTURON_UA * self.UA_EN_KM / 1000000
        return self.distancia_sol > limite


def main():
    tierra = Planeta("Tierra", 1, 5.972e24, 1.08321e12, 12742, 150,
                     TipoPlaneta.TERRESTRE, True)
    jupiter = Planeta("Júpiter", 95, 1.898e27, 1.4313e15, 139820, 779,
                      TipoPlaneta.GASEOSO, True)

    for planeta in (tierra, jupiter):
        planeta.imprimir()
        print("Densidad:", planeta.calcular_densidad(), "kg/km³")
        print("¿Es planeta exterior?", planeta.es_exterior())
        print()


if __name__ == "__main__":
    main()