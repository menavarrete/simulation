
author = 'rtacuna'


class Camion:

    def __init__(self, ruta, carga, capacidad):
        self.carga = carga
        self.ruta = ruta
        self.tiempo_llegada = 0
        self.capacidad = capacidad

    def carga_camion(self, carga):
        if carga > self.capacidad:
            raise TypeError
        self.carga = carga


class Camino:

    def __init__(self, name, tiempo_viaje, origen, destino, proyeccion):
        self.name = name
        self.tiempo_viaje = tiempo_viaje
        self.origen = origen
        self.destino = destino
        self.proyeccion = proyeccion

        # Estadisticas

        self.numero_camiones_no_salieron = 0

    def no_salieron(self):
        self.numero_camiones_no_salieron += 1

    def cambio_proyeccion(self, proyeccion, time):
        index = int(time // 8760)
        self.proyeccion[index] += proyeccion

    def proyection(self, time):
        index = int(time // 8760)
        return self.proyeccion[index]


class Sink:

    def __init__(self, name):
        self.name = name

        # Estadisticas

        self.cantidad_cobre = 0
        self.cantidad_camiones = 0

    def llega_camion(self, camion):
        self.cantidad_cobre += camion.carga
        self.cantidad_camiones += 1


class Bodega:

    def __init__(self, name, capacidad):
        self.name = name
        self.bodega = 0
        self.capacidad = capacidad

        # Estadisticas

        self.camiones_salieron = 0
        self.camiones_llegaron = 0

    def llega_camion(self, camion):
        self.cambia_cobre(camion.carga)
        self.camiones_llegaron += 1

    def sale_camion(self, camion):
        self.cambia_cobre(-camion.carga)
        self.camiones_salieron += 1

    def cambia_cobre(self, cantidad):
        self.bodega += cantidad

    def produccion(self, env, cantidades):
        while True:
            index = int(env.now // 8760)
            q = cantidades[index]
            self.cambia_cobre(float(q/17520))
            yield env.timeout(0.5)


class Source:

    def __init__(self, name):
        self.name = name
        self.bodega = 999999
        # Estadistica

        self.camiones_salieron = 0
        self.cobre_llegado = 0


    def sale_camion(self, camion):
        self.camiones_salieron += 1
        self.cobre_llegado += camion.carga


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


class CaminoTren:

    def __init__(self):
        pass


