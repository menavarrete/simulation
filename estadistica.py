
class Estadistica:

    def __init__(self):
        self.bodega_saladillo = []
        self.bodega_andina = []

    def nuevo_dia(self, saladillo, andina):
        self.bodega_saladillo.append(saladillo)
        self.bodega_andina.append(andina)

    def termine_simulacion(self):
        resultados = ""