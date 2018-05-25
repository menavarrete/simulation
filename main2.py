from objects import Bodega, Source, Sink, Camino, Puerto
from puerto import barcos_angloamerica, programacion_mensual, carga_barco
from despacho_trenes import tramo_trenes
from produccion import produccion_saladillo, produccion_saladillo_horaria
from camiones import despacho_camiones
from estadistica import Estadistica
from replicas import Replicas
from variables import *
import simpy


author = 'menavarrete-rtacuna'


def simulacion():

    rep = Replicas(name)

    for replica in range(replicas):

        print(replica)

        # Simulacion
        env = simpy.Environment()

        # Periodo
        T = 8760 * anos

        # Entidades
        andina_bodega = Bodega(andina_name, andina_capacity)
        teniente_source = Source(teniente_name)
        ventanas = Sink(ventanas_name)
        saladillo_bodega = Bodega(saladillo_bodega1_name, saladillo_bodega1_capacity)
        puerto = Puerto()

        andina_bodega.bodega = 10000

        # Tramos
        tramo5 = Camino(tramo5_name, tramo5_travel_time, teniente_source, andina_bodega, tramo5_camiones[0], tramo5_proyeccion[0])
        tramo4 = Camino(tramo4_name, tramo4_travel_time, andina_bodega, ventanas, tramo4_camiones[0], tramo4_proyeccion[0])
        tramo2 = Camino(tramo2_name, tramo2_travel_time, saladillo_bodega, andina_bodega, tramo2_camiones[0], 0)

        # Estadisticas
        estadistica = Estadistica()
        env.process(produccion_saladillo(env, saladillo_bodega, andina_bodega, puerto, tramo2, estadistica))

        # Produccion
        env.process(produccion_saladillo_horaria(env, saladillo_bodega, tramo2, andina_bodega, tramo5, estadistica))

        # Puerto
        env.process(barcos_angloamerica(env, puerto, andina_bodega))
        env.process(programacion_mensual(env, puerto, andina_bodega))
        env.process(carga_barco(env, puerto, andina_bodega))

        # Tramo 5
        env.process(despacho_camiones(env, tramo5))

        # Tramo 4
        env.process(despacho_camiones(env, tramo4))

        # Tramo 2
        env.process(tramo_trenes(env, tramo2, estadistica))

        env.run(until=T)

        rep.fin_replica(estadistica.bodega_andina, estadistica.bodega_saladillo, estadistica.barcos_puerto, estadistica.camiones_t2)

    rep.end()

    largo = 0
    suma = 0
    for n in rep.bodega_andina_fin:
        print(int(n))
        suma += n
        largo += 1
    print(suma/largo)


if __name__ == '__main__':
    simulacion()
