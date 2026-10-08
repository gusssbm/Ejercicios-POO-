from enum import Enum


class TipoCombustible(Enum):
    GASOLINA = 1
    BIOETANOL = 2
    DIESEL = 3
    BIODIESEL = 4
    GAS_NATURAL = 5


class TipoAutomovil(Enum):
    CIUDAD = 1
    SUBCOMPACTO = 2
    COMPACTO = 3
    FAMILIAR = 4
    EJECUTIVO = 5
    SUV = 6


class Color(Enum):
    BLANCO = 1
    NEGRO = 2
    ROJO = 3
    NARANJA = 4
    AMARILLO = 5
    VERDE = 6
    AZUL = 7
    VIOLETA = 8


class Automovil:
    def __init__(self, marca, modelo, motor, tipo_combustible, tipo_automovil,
                 numero_puertas, cantidad_asientos, velocidad_maxima, color):
        self._marca = marca
        self._modelo = modelo                      
        self._motor = motor                        
        self._tipo_combustible = tipo_combustible  
        self._tipo_automovil = tipo_automovil      
        self._numero_puertas = numero_puertas
        self._cantidad_asientos = cantidad_asientos
        self._velocidad_maxima = velocidad_maxima  
        self._color = color                        
        self._velocidad_actual = 0                 

    # ---------- get ----------
    def get_marca(self):
        return self._marca

    def get_modelo(self):
        return self._modelo

    def get_motor(self):
        return self._motor

    def get_tipo_combustible(self):
        return self._tipo_combustible

    def get_tipo_automovil(self):
        return self._tipo_automovil

    def get_numero_puertas(self):
        return self._numero_puertas

    def get_cantidad_asientos(self):
        return self._cantidad_asientos

    def get_velocidad_maxima(self):
        return self._velocidad_maxima

    def get_color(self):
        return self._color

    def get_velocidad_actual(self):
        return self._velocidad_actual

    # ---------- set ----------
    def set_marca(self, marca):
        self._marca = marca

    def set_modelo(self, modelo):
        self._modelo = modelo

    def set_motor(self, motor):
        self._motor = motor

    def set_tipo_combustible(self, tipo_combustible):
        self._tipo_combustible = tipo_combustible

    def set_tipo_automovil(self, tipo_automovil):
        self._tipo_automovil = tipo_automovil

    def set_numero_puertas(self, numero_puertas):
        self._numero_puertas = numero_puertas

    def set_cantidad_asientos(self, cantidad_asientos):
        self._cantidad_asientos = cantidad_asientos

    def set_velocidad_maxima(self, velocidad_maxima):
        self._velocidad_maxima = velocidad_maxima

    def set_color(self, color):
        self._color = color

    def set_velocidad_actual(self, velocidad_actual):
        self._velocidad_actual = velocidad_actual

    # ---------- comportamiento ----------
    def acelerar(self, incremento):
        if self._velocidad_actual + incremento > self._velocidad_maxima:
            print("No se puede acelerar: se superaría la velocidad máxima de",
                  self._velocidad_maxima, "km/h")
        else:
            self._velocidad_actual += incremento

    def desacelerar(self, decremento):
        if self._velocidad_actual - decremento < 0:
            print("No se puede desacelerar: la velocidad quedaría negativa")
        else:
            self._velocidad_actual -= decremento

    def frenar(self):
        self._velocidad_actual = 0

    def calcular_tiempo_llegada(self, distancia):
        if self._velocidad_actual == 0:
            print("El automóvil está detenido: no se puede calcular el tiempo")
            return None
        return distancia / self._velocidad_actual

    def imprimir(self):
        print("Marca:", self._marca)
        print("Modelo:", self._modelo)
        print("Motor:", self._motor, "L")
        print("Tipo de combustible:", self._tipo_combustible.name)
        print("Tipo de automóvil:", self._tipo_automovil.name)
        print("Número de puertas:", self._numero_puertas)
        print("Cantidad de asientos:", self._cantidad_asientos)
        print("Velocidad máxima:", self._velocidad_maxima, "km/h")
        print("Color:", self._color.name)
        print("Velocidad actual:", self._velocidad_actual, "km/h")


def main():
    auto = Automovil("Mazda", 2022, 2.0, TipoCombustible.GASOLINA,
                     TipoAutomovil.COMPACTO, 4, 5, 200, Color.ROJO)
    auto.imprimir()
    print()

    auto.set_velocidad_actual(100)
    print("Velocidad actual:", auto.get_velocidad_actual(), "km/h")

    auto.acelerar(20)
    print("Velocidad actual:", auto.get_velocidad_actual(), "km/h")

    auto.desacelerar(50)
    print("Velocidad actual:", auto.get_velocidad_actual(), "km/h")

    auto.frenar()
    print("Velocidad actual:", auto.get_velocidad_actual(), "km/h")

    print()
    auto.acelerar(300)       
    auto.desacelerar(10)     
    auto.set_velocidad_actual(80)
    print("Tiempo estimado para 240 km:",
          auto.calcular_tiempo_llegada(240), "horas")


if __name__ == "__main__":
    main()