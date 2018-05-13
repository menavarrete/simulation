from random import uniform, shuffle, expovariate
from objects import Barco


def tipo_barco():
    items = [1, 2, 3]
    tipo = shuffle(items)
    if tipo == 1:
        capacidad = 10900
    elif tipo == 2:
        capacidad = 21800
    else:
        capacidad = 32000
    barco = Barco(capacidad, 2)
    return barco


def barco_codelco(capacidad):
    barco = Barco(capacidad, 1)
    return barco


def carga_barco(env, puerto, bodega):
    while True:
        carga = min(7000, puerto.barcos[0].capacidad - puerto.barcos[0].carga, bodega.bodega)
        if bodega.bodega > carga and puerto.barcos[0].tipo == 1:
            bodega.cambia_cobre(-carga)
        yield env.timeout(int((carga/7000)*24))

        puerto.barcos[0].llenar_barco(carga)
        if puerto.barcos[0].carga == puerto.barcos[0].capacidad:
            puerto.salida_barco()
            if len(puerto.barcos) == 0:
                break


def llega_barco(env, puerto, bodega, type, capacidad):
    yield env.timeout(0)
    if type == 1:
        barco = barco_codelco(capacidad)
    else:
        barco = tipo_barco()
    puerto.llegada_barco(barco)
    if bodega.bodega < 0:
        puerto.salida_barco()
    else:
        if len(puerto.barcos) == 1:
            env.process(carga_barco(env, puerto, bodega))


def programacion_barcos(env, dia, puerto, bodega, capacidad):
    retraso = uniform(0, 3)
    wait_time = 24 * (dia + retraso)
    yield env.timeout(wait_time)
    env.process(llega_barco(env, puerto, bodega, 1, capacidad))


def barcos_angloamerica(env, puerto, bodega):
    while True:
        espera = int(expovariate(0.00416))
        yield env.timeout(espera)
        env.process(llega_barco(env, puerto, bodega, 2, 0))


def calculando_capacidades(bodega):
    caps = []
    primeros = int(bodega//32700)
    for n in range(primeros):
        caps.append(32700)

    bodega = bodega - 32700*primeros
    segundos = bodega//21000

    for n in range(segundos):
        caps.append(21000)

    bodega = bodega - 21000*segundos
    terceros = bodega//10900

    for n in range(terceros):
        caps.append(10900)

    return caps


def programacion_mensual(env, puerto, bodega):
    programacion = {1: [10], 2: [1, 15], 3: [1, 10, 20], 4: [1, 7, 14, 21], 5: [1, 5, 10, 15, 20]}
    while True:
        caps = calculando_capacidades(bodega.bodega)
        if len(caps) > 0:
            capacidad = min(len(caps), 5)
            posicion = 0
            for n in programacion[capacidad]:
                env.process(programacion_barcos(env, n, puerto, bodega, caps[posicion]))
                posicion += 1
        yield env.timeout(720)
