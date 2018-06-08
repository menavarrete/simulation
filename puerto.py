from random import uniform, shuffle, expovariate
from objects import Barco
from variables import programacion


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
        if len(puerto.barcos) > 0:
            if puerto.barcos[0].tipo == 1:
                carga = min(7000-puerto.carga_diaria, puerto.barcos[0].capacidad - puerto.barcos[0].carga, bodega.bodega,
                            puerto.necesidad_embarco - puerto.carga_actual)
                puerto.cargando_barco(carga)
                bodega.cambia_cobre(-carga)
            else:
                carga = min(7000-puerto.carga_diaria, puerto.barcos[0].capacidad - puerto.barcos[0].carga)
                puerto.carga_diaria += carga

            tiempo = puerto.calculo_tiempo(carga)
            if puerto.barcos[0].carga == puerto.barcos[0].capacidad or puerto.carga_actual >= puerto.necesidad_embarco:
                print("SALIENDO BARCO ", puerto.barcos[0].carga)
                puerto.salida_barco()

            if carga == bodega.bodega or tiempo == 0:
                nuevo_tiempo = max(1, puerto.tiempo)
                yield env.timeout(nuevo_tiempo)
            else:
                yield env.timeout(tiempo)
        else:
            yield env.timeout(24)


def llega_barco(env, puerto, bodega, type, capacidad):
    yield env.timeout(0)
    if type == 1:
        barco = barco_codelco(capacidad)
    else:
        barco = tipo_barco()
    print("LLEGA-BARCO")
    puerto.llegada_barco(barco)
    if bodega.bodega == 0 and type == 1:
        # print("CACACACACA")
        puerto.salida_barco()


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


def calculo_bodega(index):
    if index == 0:
        return uniform(0.6, 0.7)
    elif index == 11:
        return uniform(1.3, 1.4)
    else:
        return uniform(0.9, 1.1)


def calculando_capacidades(anual, index, puerto):

    ea = [905, 982, 1039, 696, 602, 407, 527, 527]

    caps = []
    auxiliar = max(0, puerto.necesidad_embarco - puerto.carga_actual)
    uniforme = calculo_bodega(index)
    bodega = int((ea[anual] * 1000 * uniforme)/12)
    puerto.total_necesidad_embarque += bodega
    puerto.necesidad_embarco = bodega
    puerto.carga_actual = 0

    #print("bodega", bodega)

    primeros = int(bodega//32700)
    for n in range(primeros):
        caps.append(32700)

    bodega = bodega - 32700*(primeros)
    segundos = int(bodega//21000)

    for n in range(segundos):
        caps.append(21000)

    bodega = bodega - 21000*(segundos)
    terceros = int(bodega//10900) + 1

    for n in range(terceros):
        caps.append(10900)

    puerto.necesidad_embarco += auxiliar

    print(caps)

    return caps


def programacion_mensual(env, puerto, bodega):

    meses = [744, 672, 744, 720, 744, 720, 744, 744, 720, 744, 720, 744]
    index = 0
    anual = 0

    while True:
        caps = calculando_capacidades(anual, index, puerto)
        if len(caps) > 0:
            capacidad = min(len(caps), 5)
            print(capacidad)
            posicion = 0
            for n in programacion[capacidad]:
                print(n)
                env.process(programacion_barcos(env, n, puerto, bodega, caps[posicion]))
                posicion += 1
        yield env.timeout(meses[index])
        index += 1
        if index == 12:
            index = 0
            anual += 1
