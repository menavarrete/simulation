
author = 'rtacuna'


class Camino:

    def __init__(self, name, tiempo_viaje, origen, destino, camiones, diario):
        self.name = name
        self.tiempo_viaje = tiempo_viaje
        self.origen = origen
        self.destino = destino
        self.camiones = camiones
        self.dia = 0
        self.traslado = 0
        self.maximo_diario = diario
        self.traslado_anual = []

    def cambio_anual(self, camiones, maximo_diario):
        self.traslado_anual.append(self.traslado)
        self.traslado = 0
        self.camiones = camiones
        self.maximo_diario = maximo_diario


class Sink:

    def __init__(self, name):
        self.name = name
        self.bodega = 0

    def cambia_cobre(self, cantidad):
        self.bodega += cantidad
        if self.bodega < 0:
            raise AttributeError


class Bodega:

    def __init__(self, name, capacidad):
        self.name = name
        self.bodega = 0
        self.capacidad = capacidad
        self.anual = 0

    def cambia_cobre(self, cantidad):
        self.bodega += cantidad
        if self.name == "Bodega principal Saladillo":
            pass
        if self.bodega < 0:
            raise AttributeError

    def cambia_anual(self, anual):
        self.anual = anual


class Source:

    def __init__(self, name):
        self.name = name
        self.bodega = 99999
        # Estadistica

    def cambia_cobre(self, cantidad):
        pass


class Barco:

    def __init__(self, capacidad, tipo):
        self.capacidad = capacidad
        self.carga = 0
        self.tipo = tipo

    def llenar_barco(self, carga):
        self.carga += carga
        if self.carga > self.capacidad:
            raise AttributeError


class Puerto:

    def __init__(self):
        self.barcos = []
        self.necesidad_embarco = 0
        self.carga_actual = 0
        self.sacado = 0
        self.total_necesidad_embarque = 0

        # Carga diaria
        self.carga_diaria = 0
        self.tiempo = 24

    def llegada_barco(self, barco):
        self.barcos.append(barco)

    def salida_barco(self):
        self.barcos.pop(0)

    def cargando_barco(self, carga):
        self.sacado += carga
        self.carga_diaria += carga
        self.carga_actual += carga

    def calculo_tiempo(self, carga):
        tiempo = int((carga / 7000) * 24)
        self.tiempo -= tiempo
        self.barcos[0].llenar_barco(carga)
        return tiempo


class Tren:

    def __init__(self, carga, ruta):
        self.carga = carga
        self.ruta = ruta
        self.tiempo_llegada = 0
