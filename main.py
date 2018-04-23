from objects import Bodega, Source, Sink, Camion, Camino
from variables import *
import simpy

author = 'menavarrete-rtacuna'


def tramo_vuelta_camion(env, camino, camion, camiones):
    yield env.timeout(camino.tiempo_viaje)
    camiones.append(camion)
    print("llegada de un camion vacio desde",camino.destino.name, "a", camino.origen.name, "a las ", env.now)


def tramo_ida_camion(env, camino, camion, camiones):
    camino.origen.sale_camion(camion)
    yield env.timeout(camino.tiempo_viaje)
    print("llega camion desde", camino.origen.name, "a", camino.destino.name, "con", camion.carga, "kilos a las ", env.now)
    camino.destino.llega_camion(camion)
    env.process(tramo_vuelta_camion(env, camino, camion, camiones))


def tramo_despacho(env, camino, camiones, between_time, wait_time):
    while True:
        if len(camiones) > 0 and camino.origen.bodega >= truck_capacity:
            camion = camiones.pop()
            camion.carga = camion.capacidad
            env.process(tramo_ida_camion(env, camino, camion, camiones))
            print("Despacho de un camion desde", camino.origen.name, "a", camino.destino.name, "a las ", env.now)
            yield env.timeout(between_time)
        else:
            if len(camiones) < 1:
                print("No hay camiones disponibles en", camino.origen.name, "para ruta", camino.name)
            elif camino.origen.bodega < truck_capacity:
                print("No hay suficiente materia prima en", camino.origen.name, "para ruta", camino.name)
            else:
                print("No hay camiones disponibles y no hay suficiente materia prima en", camino.origen.name, "para ruta", camino.name)
            yield env.timeout(wait_time)


def produccion(env, bodega, cantidad, time):
    while True:
        bodega.cambia_cobre(cantidad)
        print("Entrada de produccion de cobre en", bodega.name)
        yield env.timeout(time)


#entidades
andina_bodega = Bodega(andina_name, andina_capacity)
teniente_source = Source(teniente_name)
ventanas = Sink(ventanas_name)
saladillo_bodega1 = Bodega(saladillo_bodega1_name, saladillo_bodega1_capacity)
saladillo_bodega2 = Bodega(saladillo_bodega2_name, saladillo_bodega2_capacity)
potrerillos = Sink(potrerillos_name)


#camiones
teniente_camiones = [Camion(tramo5_name, 0, truck_capacity) for i in range(teniente_n_camiones)]
andina_camiones = [Camion(tramo4_name, 0, truck_capacity) for j in range(andina_n_camiones)]
potrerillos_camiones = [Camion(tramo3_name, 0, truck_capacity) for k in range(potrerillos_n_camiones)]



#tramos
tramo5 = Camino(tramo5_name, tramo5_distance, tramo5_travel_time, teniente_source, andina_bodega)
tramo4 = Camino(tramo4_name, tramo4_distance, tramo4_travel_time, andina_bodega, ventanas)
tramo3 = Camino(tramo3_name, tramo3_distance, tramo3_travel_time, saladillo_bodega1, potrerillos)
tramo2 = Camino(tramo2_name, tramo2_distance, tramo2_travel_time, saladillo_bodega1, andina_bodega)
tramo1 = Camino(tramo1_name, tramo1_distance, tramo1_travel_time, saladillo_bodega1, ventanas)



########################################################################################################################

env = simpy.Environment()
env.process(produccion(env, saladillo_bodega1, saladillo_production_quantity, saladillo_production_time))
env.process(tramo_despacho(env, tramo5, teniente_camiones, teniente_between_time, teniente_wait_time))
env.process(tramo_despacho(env, tramo4, andina_camiones, andina_between_time, andina_wait_time))
env.process(tramo_despacho(env, tramo3, potrerillos_camiones, saladillo_between_time, saladillo_production_time))
env.process(tramo_despacho(env, tramo2, andina_camiones, saladillo_between_time, saladillo_production_time))
env.process(tramo_despacho(env, tramo1, andina_camiones, saladillo_between_time, saladillo_production_time))
env.run(until=8760*1)




