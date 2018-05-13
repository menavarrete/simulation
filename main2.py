from objects import Bodega, Source, Sink, Camino, Puerto
from puerto import barcos_angloamerica, programacion_mensual
from despacho_trenes import tramo_trenes
from produccion import produccion_saladillo, produccion_saladillo_horaria
from camiones import despacho_camiones
from estadistica import Estadistica
from variables import *
import simpy


author = 'menavarrete-rtacuna'


if __name__ == '__main__':

    anos = 1
    T = 8760 * anos

    # Entidades
    andina_bodega = Bodega(andina_name, andina_capacity)
    teniente_source = Source(teniente_name)
    ventanas = Sink(ventanas_name)
    saladillo_bodega = Bodega(saladillo_bodega1_name, saladillo_bodega1_capacity)
    puerto = Puerto()

    andina_bodega.bodega = 10000

    # Tramos
    tramo5 = Camino(tramo5_name, tramo5_travel_time, teniente_source, andina_bodega, tramo5_camiones[0])
    tramo4 = Camino(tramo4_name, tramo4_travel_time, andina_bodega, ventanas, tramo4_camiones[0])
    tramo2 = Camino(tramo2_name, tramo2_travel_time, saladillo_bodega, andina_bodega, tramo2_camiones[0])

    # Estadisticas
    estadistica = Estadistica()

    # Simulacion
    env = simpy.Environment()

    # Estadisticas
    env.process(produccion_saladillo(env, saladillo_bodega, andina_bodega, puerto, tramo2, estadistica))

    # Produccion
    env.process(produccion_saladillo_horaria(env, saladillo_bodega, tramo2, andina_bodega, estadistica))

    # Tramo 5
    env.process(despacho_camiones(env, tramo5))

    # Tramo 4
    env.process(despacho_camiones(env, tramo4))

    # Tramo 2
    env.process(tramo_trenes(env, tramo2))

    # Puerto
    env.process(barcos_angloamerica(env, puerto, andina_bodega))
    env.process(programacion_mensual(env, puerto, andina_bodega))

    env.run(until=T)

    suma = 0
    largo = 0
    for n in estadistica.bodega_andina:
        largo += 1
        suma += n
    print(suma/largo)

    suma = 0
    largo = 0
    for n in estadistica.bodega_saladillo:
        largo += 1
        suma += n
    print(suma/largo)

    estadistica.bodega_csv()
