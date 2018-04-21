
author = 'menavarrete'

from objects import *
from variables import *
import simpy


def teniente_vuelta_camion(env, camion, camiones):
    yield env.timeout(tramo5_travel_time)
    camiones.append(camion)
    print "llegada de un camion vacio desde andina a teniente a las ", env.now

def teniente_ida_camion(env, camion, camiones, destino):
    yield env.timeout(tramo5_travel_time)
    print "llega camion desde andina con ", camion.carga, "kilos a las ", env.now
    destino.llega_camion(camion)
    env.process(teniente_vuelta_camion(env, camion, camiones))

def teniente_despacho(env, camiones, destino):
    while True:
        if len(camiones):
            camion = camiones.pop()
            camion.carga = truck_capacity
            env.process(teniente_ida_camion(env, camion, camiones, destino))
            print "despacho de un camion desde teniente a andina a las ", env.now
            yield env.timeout(6)
        else:
            yield env.timeout(2)




andina_bodega = Bodega(andina_name, andina_capacity)

teniente_source = Source(teniente_name)
teniente_camiones = [Camion(tramo5_name, 0) for i in range(teniente_n_camiones)]

teniente_andina_road = Camino(tramo5_name, tramo5_distance, tramo5_travel_time, teniente_source, andina_bodega)


env = simpy.Environment()
env.process(teniente_despacho(env, teniente_camiones, andina_bodega))
env.run(until=12410)




