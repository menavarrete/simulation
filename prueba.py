from objects import Bodega, Source, Sink, Camion, Camino, Puerto
from puerto import barcos_angloamerica, programacion_mensual
from despacho_trenes import tramo_trenes
from variables import *
import simpy
import random


andina_bodega = Bodega(andina_name, andina_capacity)
saladillo_bodega = Bodega(saladillo_bodega1_name, saladillo_bodega1_capacity)
saladillo_bodega.bodega = 100000

tramo2 = Camino(tramo2_name, tramo2_travel_time, saladillo_bodega, andina_bodega, tramo2_proyeccion)

file = open('Resumen1.txt', 'w')

env = simpy.Environment()

env.process(tramo_trenes(env, tramo2, file))

env.run(until=120)

print(andina_bodega.bodega)
