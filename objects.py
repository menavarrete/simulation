
author = 'rtacuna'


class Camion:

    def __init__(self, ruta, carga):
        self.carga = carga
        self.ruta = ruta
        self.tiempo_llegada = 0


class Camino:

    def __init__(self, name, distancia, tiempo_viaje, origen, destino):
        self.name = name
        self.lista_camiones = []
        self.tiempo_mas_cercano = -1
        self.distancia = distancia
        self.tiempo_viaje = tiempo_viaje
        self.origen = origen
        self.destino = destino

        # Estadisticas

        self.numero_camiones_pasados = 0

    def llega_camion(self, camion):
        self.lista_camiones.append(camion)

    def sale_camion(self):
        camion = self.lista_camiones.pop(0)
        return camion

    def actualizar_tiempo(self):
        pass


class Sink:

    def __init__(self, name):
        self.name = name
        self.lista_camiones = []

        # Estadisticas

        self.cantidad_cobre = 0
        self.cantidad_camiones = 0

    def llega_camion(self, camion):
        self.lista_camiones.append(camion)
        self.cantidad_cobre = camion.carga
        self.cantidad_camiones += 1


class Bodega:

    def __init__(self, name, capacidad):
        self.name = name
        self.bodega = 0
        self.tiempo_salida = -1
        self.capacidad = capacidad

        # Estadisticas

        self.camiones_salieron = 0
        self.camiones_llegaron = 0

    def llega_camion(self, camion):
        self.cambia_cobre(camion.carga)
        camion.carga = 0
        self.camiones_llegaron += 1

    def sale_camion(self, camion):
        self.cambia_cobre(-camion.carga)
        self.camiones_salieron += 1

    def cambia_cobre(self, cantidad):
        self.bodega += cantidad

    def actualiza_tiempo(self):
        pass


class Source:

    def __init__(self, name):
        self.name = name
        self.tiempo_salida = -1

        # Estadistica

        self.camiones_salieron = 0

    def sale_camion(self):
        self.camiones_salieron +=1

    def actualiza_tiempo(self):
        pass


class Barco:

    def __init__(self, tipo):
        self.tipo_barco = tipo
        self.carga = 0

    def llenar_barco(self, carga):
        self.carga = carga


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


class CaminoTren:

    def __init__(self):
        pass


