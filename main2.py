from objects import Bodega, Source, Sink, Camion, Camino, Puerto
from puerto import barcos_angloamerica, programacion_mensual
from variables import *
import simpy
import random


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

def despacho_camiones_tramo2(env, camino, camiones, file):
    while True:
        if camino.origen.bodega >= 7500 and len(camiones) > 0:
            camion = camiones.pop()
            env.process(tramo_ida_camion(env, camino, camion, camiones, file))
        yield env.timeout(tramo2_between_time)

#esta funcion simula cuando se despacha un tren desde saladillo
def bodega_descontar(env, camino, quantity, file):
    camino.origen.cambia_cobre(- quantity)
    yield env.timeout(0)


#esta funcion simula el despacho desde saladillo hasta andina, considerando que no hay variabilidad en los tramos de tren
def despacho_trenes(env, camino, quantity_out, quantity_in, file):
    camino.origen.cambia_cobre(- quantity_out)
    yield env.timeout(24)
    camino.destino.cambia_cobre(quantity_in)


def tramo_trenes(env, camino, file):
    while True:
        aleatorio = random.uniform(0,1)
        #caso de 1 tren
        if aleatorio <= 0.05:
            yield env.timeout(12)
            quantity = min(max(0, camino.origen.bodega), 740)
            env.process(despacho_trenes(env, camino, quantity, quantity, file))
            yield env.timeout(12)
        #caso de 2 trenes
        elif aleatorio <= 0.25:
            yield env.timeout(6)
            quantity1 = min(max(0, camino.origen.bodega), 740)
            env.process(bodega_descontar(env, camino, quantity1, file))
            yield env.timeout(8)
            quantity2 = min(max(0, camino.origen.bodega), 740)
            env.process(despacho_trenes(env, camino, quantity2, quantity1 + quantity2, file))
            yield env.timeout(10)
        #caso de 3 trenes
        elif aleatorio <= 0.7:
            yield env.timeout(6)
            quantity1 = min(max(0, camino.origen.bodega), 740)
            env.process(bodega_descontar(env, camino, quantity1, file))
            yield env.timeout(4)
            quantity2 = min(max(0, camino.origen.bodega), 740)
            env.process(despacho_trenes(env, camino, quantity1, quantity1 + quantity2, file))
            yield env.timeout(4)
            quantity3 = min(max(0, camino.origen.bodega), 740)
            env.process(despacho_trenes(env, camino, quantity3, quantity3, file))
            yield env.timeout(10)
        #caso de 4 trenes
        else:
            yield env.timeout(6)
            quantity1 = min(max(0, camino.origen.bodega), 740)
            env.process(bodega_descontar(env, camino, quantity1, file))
            yield env.timeout(4)
            quantity2 = min(max(0, camino.origen.bodega), 740)
            env.process(despacho_trenes(env, camino, quantity2, quantity1 + quantity2, file))
            yield env.timeout(4)
            quantity3 = min(max(0, camino.origen.bodega), 740)
            env.process(bodega_descontar(env, camino, quantity3, file))
            yield env.timeout(4)
            quantity4 = min(max(0, camino.origen.bodega), 740)
            env.process(despacho_trenes(env, camino, quantity4, quantity3 + quantity4, file))
            yield env.timeout(6)


if __name__ == '__main__':

    anos = 8
    T = 8760 * anos

    # Entidades
    andina_bodega = Bodega(andina_name, andina_capacity)
    teniente_source = Source(teniente_name)
    ventanas = Sink(ventanas_name)
    saladillo_bodega = Bodega(saladillo_bodega1_name, saladillo_bodega1_capacity)
    #saladillo_bodega.bodega = 7168000
    potrerillos = Sink(potrerillos_name)
    puerto = Puerto()

    # Tramos
    tramo5 = Camino(tramo5_name, tramo5_travel_time, teniente_source, andina_bodega, tramo5_proyeccion)
    tramo4 = Camino(tramo4_name, tramo4_travel_time, andina_bodega, ventanas, tramo4_proyeccion)
    tramo1 = Camino(tramo1_name, tramo1_travel_time, saladillo_bodega, ventanas, tramo1_proyecion)
    tramo2 = Camino(tramo2_name, tramo2_travel_time, saladillo_bodega, andina_bodega, tramo2_proyeccion)
    tramo3 = Camino(tramo3_name, tramo3_travel_time, saladillo_bodega, potrerillos, tramo3_proyeccion)

    # Camiones
    t4_camiones = [Camion(tramo4, 0, truck_capacity) for i in range(tramo4_camiones)]
    t1_camiones = [Camion(tramo1, 0, truck_capacity) for i in range(tramo1_camiones)]
    t2_camiones = [Camion(tramo2, 0, truck_capacity) for i in range(tramo2_camiones)]
    t3_camiones = [Camion(tramo2, 0, truck_capacity) for i in range(tramo3_camiones)]

    # Archivo
    file = open('Resumen1.txt', 'w')

    # Simulacion
    env = simpy.Environment()
    env.process(tramo_despacho_5(env, tramo5, tramo5_between_time, file))
    env.process(tramo_despacho(env, tramo4, t4_camiones, tramo4_between_time, file))
    env.process(tramo_despacho(env, tramo1, t1_camiones, tramo1_between_time, file))
    env.process(tramo_despacho(env, tramo3, t3_camiones, tramo3_between_time, file))
    env.process(tramo_trenes(env, tramo2, file))
    env.process(saladillo_bodega.produccion(env, saladillo_entradas))
    env.process(despacho_camiones_tramo2(env, tramo2, t2_camiones, file))

    # Puerto
    env.process(barcos_angloamerica(env, puerto, andina_bodega, file))
    env.process(programacion_mensual(env, puerto, andina_bodega, file))

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
    print("-" * 20)
    print("T3 termina con carga proyeccion: ", tramo3.proyeccion)
    print("T3 termina con camiones que NO salieron: ", tramo3.numero_camiones_no_salieron)
