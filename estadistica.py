
class Estadistica:

    def __init__(self):
        self.bodega_saladillo = []
        self.bodega_andina = []
        self.camiones_t2 = 0
        self.error_bodega = 0

    def nuevo_dia(self, saladillo, andina):
        self.bodega_saladillo.append(saladillo)
        self.bodega_andina.append(andina)

    def tramo2(self):
        self.camiones_t2 += 1

    def calculo_error(self, bodega):
        if bodega > 7500:
            self.error_bodega += 1

    def termine_simulacion(self):
        resultados = ""