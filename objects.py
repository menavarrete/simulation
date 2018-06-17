
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

        # Tipo programacion
        self.programcion = 0

        # Angloamerica
        self.angloamerica = 0

        # Barcos que se van porque no hay cobre
        self.barco_parcialmente = 0

        # Porcentaje utilizacion barcos
        self.barcos_salen = []

        # Barco que se va en cero
        self.barco_perdido = 0

        # Lista puntos de carga
        self.puntos_carga = []

    def llegada_barco(self, barco):
        self.barcos.append(barco)
        if barco.tipo == 2:
            self.angloamerica += 1

    def salida_barco(self, embarque):
        barco = embarque.barco
        if barco.tipo == 2:
            self.angloamerica -= 1
        else:
            self.barcos_salen.append(barco.carga/barco.capacidad)
        embarque.barco = None

    def cargando_barco(self, carga, embarque):
        embarque.carga_diaria += carga
        self.carga_actual += carga

    def nuevo_dia(self):
        for n in self.puntos_carga:
            n.nuevo_dia()


class Embarque:

    def __init__(self, capacidad):
        self.barco = None
        self.capacidad = capacidad
        self.carga_diaria = 0
        self.tiempo = 24

    def cargando(self, carga):
        self.carga_diaria += carga
        if self.carga_diaria > self.capacidad:
            raise AttributeError

    def nuevo_dia(self):
        self.tiempo = 24
        self.carga_diaria = 0

    def llega_barco(self, barco):
        self.barco = barco

    def sale_barco(self):
        self.barco = None

    def calculo_tiempo(self, carga):
        tiempo = int((carga / 7000) * 24)
        self.tiempo -= tiempo
        self.barco.llenar_barco(carga)
        return tiempo
