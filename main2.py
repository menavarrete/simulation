from objects import Bodega, Source, Sink, Camion, Camino
from variables import *
import simpy

author = 'menavarrete-rtacuna'


def tramo_vuelta_camion(env, camino, camion, camiones, file):
    yield env.timeout(camino.tiempo_viaje)
    camiones.append(camion)
    file.write("llegada de un camion vacio desde {} a {} a las {}\n".format(camino.destino.name, camino.origen.name, env.now))


def tramo_ida_camion(env, camino, camion, camiones, file):
    camino.origen.sale_camion(camion)
    yield env.timeout(camino.tiempo_viaje)
    file.write("llega camion desde {} a {} con {} kilos a las {}\n".format(camino.origen.name, camino.destino.name, camion.carga, env.now))
    camino.destino.llega_camion(camion)
    if camino.name != "Tramo 5 (El Teniente - Division Andina)":
        env.process(tramo_vuelta_camion(env, camino, camion, camiones, file))


def carga(env, camino, camion):
    camion.carga_camion(truck_capacity)
    camino.cambio_proyeccion(-truck_capacity, env.now)
    yield env.timeout(0)


def tramo_despacho_5(env, camino, between_time, file):
    while True:
        if camino.proyection(env.now) >= truck_capacity:
            camion = Camion(camino, 0, truck_capacity)
            env.process(carga(env, camino, camion))
            env.process(tramo_ida_camion(env, camino, camion, [], file))
            file.write("Despacho de un camion desde {} a {} a las {}\n".format(camino.origen.name, camino.destino.name, env.now))
            yield env.timeout(between_time)
        else:
            file.write("No hay suficiente materia prima en {} para ruta {}\n".format(camino.origen.name, camino.name))
            camino.no_salieron()
            yield env.timeout(between_time)


def tramo_despacho(env, camino, camiones, between_time, file):
    while True:
        if len(camiones) > 0 and camino.origen.bodega >= truck_capacity and camino.proyection(env.now) >= truck_capacity:
            camion = camiones.pop()
            env.process(carga(env, camino, camion))
            env.process(tramo_ida_camion(env, camino, camion, camiones, file))
            file.write("Despacho de un camion desde {} a {} a las {}\n".format(camino.origen.name, camino.destino.name, env.now))
            yield env.timeout(between_time)
        else:
            if len(camiones) < 1:
                file.write("No hay camiones disponibles en {} para ruta {}\n".format(camino.origen.name, camino.name))

            elif camino.origen.bodega < truck_capacity:
                file.write("No hay suficiente materia prima en bodega en {} para ruta {}\n".format(camino.origen.name, camino.name))

            else:
                file.write("Se supera la proyeccion para ruta {}\n".format(camino.name))
            camino.no_salieron()
            yield env.timeout(between_time)



if __name__ == '__main__':

    anos = 8
    T = 8760 * anos

    # Entidades
    andina_bodega = Bodega(andina_name, andina_capacity)
    teniente_source = Source(teniente_name)
    ventanas = Sink(ventanas_name)
    saladillo_bodega = Bodega(saladillo_bodega1_name, saladillo_bodega1_capacity)
    #saladillo_bodega.bodega = 7168000

    # Tramos
    tramo5 = Camino(tramo5_name, tramo5_travel_time, teniente_source, andina_bodega, tramo5_proyeccion)
    tramo4 = Camino(tramo4_name, tramo4_travel_time, andina_bodega, ventanas, tramo4_proyeccion)
    tramo1 = Camino(tramo1_name, tramo1_travel_time, saladillo_bodega, ventanas, tramo1_proyecion)

    # Camiones
    t4_camiones = [Camion(tramo4, 0, truck_capacity) for i in range(tramo4_camiones)]
    t1_camiones = [Camion(tramo1, 0, truck_capacity) for i in range(tramo1_camiones)]

    # Archivo
    file = open('Resumen1.txt', 'w')

    # Simulacion
    env = simpy.Environment()
    env.process(tramo_despacho_5(env, tramo5, tramo5_between_time, file))
    env.process(tramo_despacho(env, tramo4, t4_camiones, tramo4_between_time, file))
    env.process(tramo_despacho(env, tramo1, t1_camiones, tramo1_between_time, file))
    env.process(saladillo_bodega.produccion(env, saladillo_entradas))
    env.run(until=T)

    # Resumen
    print("-" * 20)
    print("Andina bodega termina con carga: ", andina_bodega.bodega)
    print("Andina bodega termina con camiones llegados: ", andina_bodega.camiones_llegaron)
    print("-"*20)
    print("Teniente termina con camiones que salieron: ", teniente_source.camiones_salieron)
    print("Teniente termina con camiones que NO salieron: ", tramo5.numero_camiones_no_salieron)
    print("-"*20)
    print("Ventana termina con carga: ", ventanas.cantidad_cobre)
    print("Ventana termina con camiones que llegaron: ", ventanas.cantidad_camiones)
    print("-" * 20)
    print("Saladillo termina con carga: ", saladillo_bodega.bodega)
    print("-"*20)
    print("-" * 20)
    print("T5 termina con carga proyeccion: ", tramo5.proyeccion)
    print("T5 termina con camiones que NO salieron: ", tramo5.numero_camiones_no_salieron)
    print("-" * 20)
    print("T4 termina con carga proyeccion: ", tramo4.proyeccion)
    print("T4 termina con camiones que NO salieron: ", tramo4.numero_camiones_no_salieron)
    print("-" * 20)
    print("T1 termina con carga proyeccion: ", tramo1.proyeccion)
    print("T1 termina con camiones que NO salieron: ", tramo1.numero_camiones_no_salieron)

