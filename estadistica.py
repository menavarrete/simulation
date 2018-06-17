
class Estadistica:

    def __init__(self):
        self.bodega_saladillo = []
        self.bodega_saladillo_hora = []
        self.bodega_andina = []
        self.bodega_andina_hora = []
        self.camiones_t2 = []
        self.error_bodega = 0
        self.barcos_puerto = []
        self.ocupacion_trenes = []

    def promedios(self):
        suma1 = 0
        suma2 = 0
        for n in self.bodega_saladillo_hora:
            suma1 += n
        for n in self.bodega_andina_hora:
            suma2 += n
        self.bodega_saladillo.append(suma1/len(self.bodega_saladillo_hora))
        self.bodega_andina.append(suma2/len(self.bodega_andina_hora))

    def ocupacion_trenes_calculo(self, carga):
        self.ocupacion_trenes.append(carga/740)

    def nuevo_dia(self, saladillo, andina):

        self.bodega_saladillo_hora.append(saladillo)
        self.bodega_andina_hora.append(andina)

        self.promedios()

        self.bodega_saladillo_hora = []
        self.bodega_andina_hora = []

    def nueva_hora(self, saladillo, andina):

        self.bodega_saladillo_hora.append(saladillo)
        self.bodega_andina_hora.append(andina)

    def nuevo_dia_dos(self, andina, saladillo):
        self.bodega_andina.append(andina)
        self.bodega_saladillo.append(saladillo)

    def tramo2(self):
        self.camiones_t2 += 1

    def calculo_error(self, bodega):
        if bodega > 7500:
            self.error_bodega += 1

    def usando_camiones(self, camiones):
        self.camiones_t2.append(camiones)

    def bodega_csv(self):
        file = open('bodega_saladillo.csv', 'a')
        for i in self.bodega_saladillo:
            file.write(","+str(i) + '\n')
        file.write("-" + '\n')
        file2 = open('bodega_andina.csv', 'a')
        for i in self.bodega_andina:
            file2.write(","+str(i) + '\n')
        file2.write("-" + '\n')
        file3 = open('puerto.csv', 'a')
        for i in self.barcos_puerto:
            file3.write(";"+str(i) + '\n')
        file3.write("-" + '\n')
        file4 = open('tramo2.csv', 'a')
        for i in self.camiones_t2:
            file4.write(";"+str(i) + '\n')
        file4.write("-"+'\n')


