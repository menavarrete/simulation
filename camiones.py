from variables import truck_capacity

author = 'rtacuna'


def espera_camiones(env, tramo, carga):
    tramo.traslado += carga
    yield env.timeout(tramo.tiempo_viaje)
    tramo.destino.cambia_cobre(carga)


def despacho_camiones(env, tramo):
    while True:
        capacidad_camiones = tramo.camiones * truck_capacity
        capacidad_bodega = tramo.origen.bodega
        capacidad_diaria = tramo.maximo_diario

        carga = min(capacidad_bodega, capacidad_camiones, capacidad_diaria)

        tramo.origen.cambia_cobre(-carga)

        env.process(espera_camiones(env, tramo, carga))

        yield env.timeout(24)


def tramo2(env, tramo, est):
    capacidad_camiones = tramo.camiones * truck_capacity
    capacidad_bodega = tramo.origen.bodega

    carga = min(capacidad_bodega, capacidad_camiones)

    est.usando_camiones(int(carga/truck_capacity))

    tramo.origen.cambia_cobre(-carga)

    espera_camiones(env, tramo, carga)

    yield env.timeout(0)


def nuevo_tramo2(env, tramo, carga, est):
    yield env.timeout(0)
    imaginario = tramo.origen.bodega - carga + tramo.origen.anual
    if imaginario > 7500:
        diferencia = imaginario - 7500
        camiones = int(diferencia/truck_capacity) + 1
        camiones = min(camiones, tramo.camiones)
        est.usando_camiones(camiones)
        carga = camiones*truck_capacity
        tramo.origen.cambia_cobre(-carga)
        env.process(espera_camiones(env, tramo, carga))
    else:
        est.usando_camiones(0)