from variables import truck_capacity

author = 'rtacuna'


def espera_camiones(env, tramo, carga):
    yield env.timeout(tramo.tiempo_viaje)
    tramo.destino.cambia_cobre(carga)


def despacho_camiones(env, tramo):
    while True:
        capacidad_camiones = tramo.camiones * truck_capacity
        capacidad_bodega = tramo.origen.bodega

        carga = min(capacidad_bodega, capacidad_camiones)
        tramo.origen.cambia_cobre(-carga)

        espera_camiones(env, tramo, carga)

        yield env.timeout(24)


def tramo2(env, tramo, est):
    capacidad_camiones = tramo.camiones * truck_capacity
    capacidad_bodega = tramo.origen.bodega

    carga = min(capacidad_bodega, capacidad_camiones)

    est.usando_camiones(int(carga/truck_capacity))

    tramo.origen.cambia_cobre(-carga)

    espera_camiones(env, tramo, carga)

    yield env.timeout(0)