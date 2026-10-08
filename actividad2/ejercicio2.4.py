import math


class Circulo:
    def __init__(self, radio):
        self.radio = radio  

    def calcular_area(self):
        return math.pi * self.radio ** 2

    def calcular_perimetro(self):
        return 2 * math.pi * self.radio


class Rectangulo:
    def __init__(self, base, altura):
        self.base = base      
        self.altura = altura  

    def calcular_area(self):
        return self.base * self.altura

    def calcular_perimetro(self):
        return 2 * (self.base + self.altura)


class Cuadrado:
    def __init__(self, lado):
        self.lado = lado  

    def calcular_area(self):
        return self.lado ** 2

    def calcular_perimetro(self):
        return 4 * self.lado


class TrianguloRectangulo:
    def __init__(self, base, altura):
        self.base = base      
        self.altura = altura  

    def calcular_area(self):
        return self.base * self.altura / 2

    def calcular_hipotenusa(self):
        return math.sqrt(self.base ** 2 + self.altura ** 2)

    def calcular_perimetro(self):
        return self.base + self.altura + self.calcular_hipotenusa()

    def tipo_triangulo(self):
        hipotenusa = self.calcular_hipotenusa()
        if self.base == self.altura == hipotenusa:
            return "Equilátero"  
        elif (self.base == self.altura or self.base == hipotenusa
              or self.altura == hipotenusa):
            return "Isósceles"
        else:
            return "Escaleno"


def main():
    circulo = Circulo(5)
    rectangulo = Rectangulo(6, 4)
    cuadrado = Cuadrado(5)
    triangulo = TrianguloRectangulo(3, 4)

    print("Círculo (radio 5 cm)")
    print("  Área:", round(circulo.calcular_area(), 2), "cm²")
    print("  Perímetro:", round(circulo.calcular_perimetro(), 2), "cm")

    print("Rectángulo (6 x 4 cm)")
    print("  Área:", rectangulo.calcular_area(), "cm²")
    print("  Perímetro:", rectangulo.calcular_perimetro(), "cm")

    print("Cuadrado (lado 5 cm)")
    print("  Área:", cuadrado.calcular_area(), "cm²")
    print("  Perímetro:", cuadrado.calcular_perimetro(), "cm")

    print("Triángulo rectángulo (base 3 cm, altura 4 cm)")
    print("  Área:", triangulo.calcular_area(), "cm²")
    print("  Perímetro:", triangulo.calcular_perimetro(), "cm")
    print("  Hipotenusa:", triangulo.calcular_hipotenusa(), "cm")
    print("  Tipo:", triangulo.tipo_triangulo())

    isosceles = TrianguloRectangulo(3, 3)
    print("Triángulo rectángulo (base 3 cm, altura 3 cm)")
    print("  Tipo:", isosceles.tipo_triangulo())


if __name__ == "__main__":
    main()