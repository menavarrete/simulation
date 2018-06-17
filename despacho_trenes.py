from random import uniform
from camiones import nuevo_tramo2


# Esta funcion simula cuando se despacha un tren desde saladillo
def bodega_descontar(env, camino, quantity):
    camino.origen.cambia_cobre(- quantity)
    camino.traslado += quantity
    yield env.timeout(0)


# Esta funcion simula el despacho desde saladillo hasta andina
def despacho_trenes(env, camino, quantity_out, quantity_in):
    camino.origen.cambia_cobre(- quantity_out)
    camino.traslado += quantity_out
    yield env.timeout(24)
    camino.destino.cambia_cobre(quantity_in)


def tramo_trenes(env, camino, est):
    while True:
        aleatorio = uniform(0, 1)
        if aleatorio <= 0.05:
            env.process(nuevo_tramo2(env, camino, 740, est))
            yield env.timeout(12)
            quantity = min(int(camino.origen.bodega), 740)
            est.ocupacion_trenes_calculo(quantity)
            env.process(despacho_trenes(env, camino, quantity, quantity))
            yield env.timeout(12)
        elif aleatorio <= 0.25:
            env.process(nuevo_tramo2(env, camino, 1480, est))
            yield env.timeout(6)
            quantity1 = min(int(camino.origen.bodega), 740)
            est.ocupacion_trenes_calculo(quantity1)
            env.process(bodega_descontar(env, camino, quantity1))
            yield env.timeout(8)
            quantity2 = min(int(camino.origen.bodega), 740)
            est.ocupacion_trenes_calculo(quantity2)
            env.process(despacho_trenes(env, camino, quantity2, quantity1 + quantity2))
            yield env.timeout(10)
        elif aleatorio <= 0.7:
            env.process(nuevo_tramo2(env, camino, 2220, est))
            yield env.timeout(6)
            quantity1 = min(int(camino.origen.bodega), 740)
            est.ocupacion_trenes_calculo(quantity1)
            env.process(bodega_descontar(env, camino, quantity1))
            yield env.timeout(4)
            quantity2 = min(int(camino.origen.bodega), 740)
            est.ocupacion_trenes_calculo(quantity2)
            env.process(despacho_trenes(env, camino, quantity2, quantity1 + quantity2))
            yield env.timeout(4)
            quantity3 = min(int(camino.origen.bodega), 740)
            est.ocupacion_trenes_calculo(quantity3)
            env.process(despacho_trenes(env, camino, quantity3, quantity3))
            yield env.timeout(10)
        else:
            env.process(nuevo_tramo2(env, camino, 2960, est))
            yield env.timeout(6)
            quantity1 = min(int(camino.origen.bodega), 740)
            est.ocupacion_trenes_calculo(quantity1)
            env.process(bodega_descontar(env, camino, quantity1))
            yield env.timeout(4)
            quantity2 = min(int(camino.origen.bodega), 740)
            est.ocupacion_trenes_calculo(quantity2)
            env.process(despacho_trenes(env, camino, quantity2, quantity1 + quantity2))
            yield env.timeout(4)
            quantity3 = min(int(camino.origen.bodega), 740)
            est.ocupacion_trenes_calculo(quantity3)
            env.process(bodega_descontar(env, camino, quantity3))
            yield env.timeout(4)
            quantity4 = min(int(camino.origen.bodega), 740)
            est.ocupacion_trenes_calculo(quantity4)
            env.process(despacho_trenes(env, camino, quantity4, quantity3 + quantity4))
            yield env.timeout(6)