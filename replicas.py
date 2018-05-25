import os
from variables import *

author = "rtacuna"


class Replicas:

    def __init__(self, name):
        self.bodega_andina = []
        self.bodega_andina_fin = []
        self.bodega_saladillo = []
        self.bodega_saladillo_fin = []
        self.puerto = []
        self.puerto_fin = []
        self.camiones = []
        self.camiones_fin = []
        self.name = name

    def fin_replica(self, andina, saladillo, puerto, camiones):
        self.bodega_andina.append(andina)
        self.bodega_saladillo.append(saladillo)
        self.puerto.append(puerto)
        self.camiones.append(camiones)

    def promedio_andina(self):
        largo = len(self.bodega_andina[0])
        for n in range(largo):
            suma = 0
            for a in self.bodega_andina:
                suma += a[n]
            self.bodega_andina_fin.append(int(suma/len(self.bodega_andina)))

    def promedio_saladillo(self):
        largo = len(self.bodega_saladillo[0])
        for n in range(largo):
            suma = 0
            for a in self.bodega_saladillo:
                suma += a[n]
            self.bodega_saladillo_fin.append(int(suma/len(self.bodega_saladillo)))

    def promedio_barcos(self):
        largo = len(self.puerto[0])
        for n in range(largo):
            suma = 0
            for a in self.puerto:
                suma += a[n]
            self.puerto_fin.append(suma/len(self.puerto))

    def promedio_camiones(self):
        largo = len(self.camiones[0])
        for n in range(largo):
            suma = 0
            for a in self.camiones:
                suma += a[n]
            self.camiones_fin.append(suma/len(self.camiones))

    def visualizacion(self):
        if not os.path.exists("resultados/"+self.name):
            os.makedirs("resultados/"+self.name)

        file2 = open('resultados/'+self.name+'/bodega_andina.csv', 'w')
        for i in self.bodega_andina_fin:
            file2.write(str(i) + '\n')

        file4 = open('resultados/'+self.name+'/bodega_saladillo.csv', 'w')
        for i in self.bodega_saladillo_fin:
            file4.write(str(i) + '\n')

        file5 = open('resultados/'+self.name+'/barcos_puerto.csv', 'w')
        for i in self.puerto_fin:
            file5.write(str(i) + '\n')

        file6 = open('resultados/'+self.name+'/camiones.csv', 'w')
        for i in self.camiones_fin:
            file6.write(str(i) + '\n')

        file3 = open('resultados/'+self.name+'/variables.txt', 'w')
        file3.write("ANOS: "+str(anos) + '\n')
        file3.write("REPLICAS: "+str(replicas) + '\n')

    def end(self):
        self.promedio_andina()
        self.promedio_saladillo()
        self.promedio_barcos()
        self.promedio_camiones()
        self.visualizacion()