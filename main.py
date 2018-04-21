
author = 'menavarrete'

from objects import *
from variables import *
import simpy

# 1 anho tiene 12410 horas. (24*365)



andina_bodega = Bodega(andina_name, andina_capacity)
andina_sink = Sink(andinasink_name)

teniente_source = Source(teniente_name)
teniente_camiones = [Camion(tramo5_name, 0) for i in teniente_n_camiones]

teniente_andina_road = Camino(tramo5_name, tramo5_distance, tramo5_travel_time, teniente_source, andina_bodega)










'''
def clock(env, name, tick):
    while True:
        print name, env.now
        yield env.timeout(tick)


env = simpy.Environment()
env.process(clock(env, 'fast', 0.5))
env.process(clock(env, 'slow', 5))
env.run(until=10)
'''

