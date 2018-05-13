from random import uniform


# Esta funcion simula cuando se despacha un tren desde saladillo
def bodega_descontar(env, camino, quantity):
    camino.origen.cambia_cobre(- quantity)
    yield env.timeout(0)


# Esta funcion simula el despacho desde saladillo hasta andina
def despacho_trenes(env, camino, quantity_out, quantity_in):
    camino.origen.cambia_cobre(- quantity_out)
    yield env.timeout(24)
    camino.destino.cambia_cobre(quantity_in)


def tramo_trenes(env, camino):
    while True:
        aleatorio = uniform(0, 1)
        if aleatorio <= 0.05:
            yield env.timeout(12)
            quantity = int(min(max(0, camino.origen.bodega), 740))
            env.process(despacho_trenes(env, camino, quantity, quantity))
            yield env.timeout(12)
        elif aleatorio <= 0.25:
            yield env.timeout(6)
            quantity1 = int(min(max(0, camino.origen.bodega), 740))
            env.process(bodega_descontar(env, camino, quantity1))
            yield env.timeout(8)
            quantity2 = int(min(max(0, camino.origen.bodega), 740))
            env.process(despacho_trenes(env, camino, quantity2, quantity1 + quantity2))
            yield env.timeout(10)
        elif aleatorio <= 0.7:
            yield env.timeout(6)
            quantity1 = int(min(max(0, camino.origen.bodega), 740))
            env.process(bodega_descontar(env, camino, quantity1))
            yield env.timeout(4)
            quantity2 = int(min(max(0, camino.origen.bodega), 740))
            env.process(despacho_trenes(env, camino, quantity1, quantity1 + quantity2))
            yield env.timeout(4)
            quantity3 = int(min(max(0, camino.origen.bodega), 740))
            env.process(despacho_trenes(env, camino, quantity3, quantity3))
            yield env.timeout(10)
        else:
            yield env.timeout(6)
            quantity1 = int(min(max(0, camino.origen.bodega), 740))
            env.process(bodega_descontar(env, camino, quantity1))
            yield env.timeout(4)
            quantity2 = int(min(max(0, camino.origen.bodega), 740))
            env.process(despacho_trenes(env, camino, quantity2, quantity1 + quantity2))
            yield env.timeout(4)
            quantity3 = int(min(max(0, camino.origen.bodega), 740))
            env.process(bodega_descontar(env, camino, quantity3))
            yield env.timeout(4)
            quantity4 = int(min(max(0, camino.origen.bodega), 740))
            env.process(despacho_trenes(env, camino, quantity4, quantity3 + quantity4))
            yield env.timeout(6)