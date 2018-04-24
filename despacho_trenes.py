import simpy


def despacho_trenes(env, camino, quantity_out, quantity_in, file):
    camino.origen.cambia_cobre(- quantity_out)
    yield env.timeout(24)
    camino.destino.cambia_cobre(quantity_in)


def un_tren(env, camino, quantity_out, file):
    yield env.timeout(12)
    env.process(despacho_trenes(env, camino, quantity_out, quantity_out, file))
    yield env.timeout(12)