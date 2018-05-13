
author = 'rtacuna'


class Camino:

    def __init__(self, name, tiempo_viaje, origen, destino, camiones):
        self.name = name
        self.tiempo_viaje = tiempo_viaje
        self.origen = origen
        self.destino = destino
        self.camiones = camiones
        self.dia = 0


class Sink:

    def __init__(self, name):
        self.name = name
        self.bodega = 0

    def cambia_cobre(self, cantidad):
        self.bodega += cantidad


class Bodega:

    def __init__(self, name, capacidad):
        self.name = name
        self.bodega = 0
        self.capacidad = capacidad
        self.file = open('saladilo.txt', 'w')

    def cambia_cobre(self, cantidad):
        if self.name == "Bodega principal Saladillo":
            self.file.write("CAMBIA COBRE {}, {}\n".format(cantidad, self.bodega))
        self.bodega += cantidad


class Source:

    def __init__(self, name):
        self.name = name
        self.bodega = 99999
        # Estadistica

    def cambia_cobre(self, cantidad):
        self.bodega += cantidad

class Barco:

    def __init__(self, capacidad, tipo):
        self.capacidad = capacidad
        self.carga = 0
        self.tipo = tipo

    def llenar_barco(self, carga):
        self.carga += carga


class Puerto:

    def __init__(self):
        self.barcos = []

        # Estadisticas

        self.cantidad_barcos = 0

    def llegada_barco(self, barco):
        self.cantidad_barcos += 1
        self.barcos.append(barco)

    def salida_barco(self):
        self.cantidad_barcos -= 1
        self.barcos.pop(0)


class Tren:

    def __init__(self, carga, ruta):
        self.carga = carga
        self.ruta = ruta
        self.tiempo_llegada = 0
