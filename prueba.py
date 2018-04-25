from objects import Bodega, Source, Sink, Camion, Camino, Puerto
from puerto import barcos_angloamerica, programacion_mensual
from despacho_trenes import tramo_trenes
from produccion import produccion_saladillo
from variables import *
import simpy
import random


saladillo_bodega = Bodega(saladillo_bodega1_name, saladillo_bodega1_capacity)

file = open('Resumen1.txt', 'w')

env = simpy.Environment()

env.process(produccion_saladillo(env, saladillo_bodega, file))

env.run(until=21392)

print(saladillo_bodega.bodega)
