
author = 'menavarrete'

from objects import *
from variables import *
import simpy


def tramo_vuelta_camion(env, camino, camion, camiones):
    yield env.timeout(camino.tiempo_viaje)
    camiones.append(camion)
    print "llegada de un camion vacio desde",camino.destino.name, "a", camino.origen.name, "a las ", env.now


def tramo_ida_camion(env, camino, camion, camiones):
    camino.origen.sale_camion(camion)
    yield env.timeout(camino.tiempo_viaje)
    print "llega camion desde", camino.origen.name, "a", camino.destino.name, "con", camion.carga, "kilos a las ", env.now
    camino.destino.llega_camion(camion)
    env.process(tramo_vuelta_camion(env, camino, camion, camiones))


def tramo_despacho(env, camino, camiones, between_time, wait_time):
    while True:
        if len(camiones) > 0 and camino.origen.bodega >= truck_capacity:
            camion = camiones.pop()
            camion.carga = camion.capacidad
            env.process(tramo_ida_camion(env, camino, camion, camiones))
            print "Despacho de un camion desde", camino.origen.name, "a", camino.destino.name, "a las ", env.now
            yield env.timeout(between_time)
        else:
            yield env.timeout(wait_time)


def produccion(env, bodega, cantidad, time):
    while True:
        bodega.bodega += cantidad
        yield env.timeout(time)




#entidades
andina_bodega = Bodega(andina_name, andina_capacity)
teniente_source = Source(teniente_name)
ventanas = Sink(ventanas_name)
saladillo_bodega1 = Bodega(saladillo_bodega1_name, saladillo_bodega1_capacity)
saladillo_bodega2 = Bodega(saladillo_bodega2_name, saladillo_bodega2_capacity)


#camiones
teniente_camiones = [Camion(tramo5_name, 0, truck_capacity) for i in range(teniente_n_camiones)]
andina_camiones = [Camion(tramo4_name, 0, truck_capacity) for j in range(andina_n_camiones)]


#tramos
tramo5 = Camino(tramo5_name, tramo5_distance, tramo5_travel_time, teniente_source, andina_bodega)
tramo4 = Camino(tramo4_name, tramo4_distance, tramo4_travel_time, andina_bodega, ventanas)



env = simpy.Environment()
env.process(tramo_despacho(env, tramo5, teniente_camiones, teniente_between_time, teniente_wait_time))
env.process(tramo_despacho(env, tramo4, andina_camiones, andina_between_time, andina_wait_time))
env.run(until=12410*5)




