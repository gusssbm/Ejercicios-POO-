from enum import Enum


class TipoCuenta(Enum):
    AHORROS = 1
    CORRIENTE = 2


class CuentaBancaria:
    def __init__(self, nombres, apellidos, numero_cuenta, tipo_cuenta):
        self.nombres = nombres
        self.apellidos = apellidos
        self.numero_cuenta = numero_cuenta
        self.tipo_cuenta = tipo_cuenta  
        self.saldo = 0                  

    def imprimir(self):
        print("Titular:", self.nombres, self.apellidos)
        print("Número de cuenta:", self.numero_cuenta)
        print("Tipo de cuenta:", self.tipo_cuenta.name)
        print("Saldo:", self.saldo)

    def consultar_saldo(self):
        return self.saldo

    def consignar(self, valor):
        self.saldo += valor

    def retirar(self, valor):
        if valor > self.saldo:
            print("Fondos insuficientes: no se puede retirar", valor,
                  "(saldo actual:", self.saldo, ")")
        else:
            self.saldo -= valor


def main():
    cuenta = CuentaBancaria("Juan Camilo", "Pérez Gómez", 1234567890,
                            TipoCuenta.AHORROS)
    cuenta.imprimir()
    print()

    cuenta.consignar(500000)
    print("Saldo tras consignar 500000:", cuenta.consultar_saldo())

    cuenta.retirar(200000)
    print("Saldo tras retirar 200000:", cuenta.consultar_saldo())

    cuenta.retirar(1000000)  
    print("Saldo final:", cuenta.consultar_saldo())


if __name__ == "__main__":
    main()