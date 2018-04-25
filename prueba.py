from objects import Bodega, Source, Sink, Camion, Camino, Puerto
from puerto import barcos_angloamerica, programacion_mensual
from variables import *
import simpy
import random


puerto = Puerto()
andina_bodega = Bodega(andina_name, andina_capacity)
andina_bodega.bodega = 100000

file = open('Resumen1.txt', 'w')

env = simpy.Environment()

# Puerto
env.process(barcos_angloamerica(env, puerto, andina_bodega, file))
env.process(programacion_mensual(env, puerto, andina_bodega, file))

env.run(until=1000)

print(andina_bodega.bodega)
