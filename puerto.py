from random import uniform, choice, expovariate
from objects import Barco
from variables import programacion, programacion2, ea


def angloamerica():
    capacidad = choice([10900, 21000, 32700])
    return Barco(capacidad, 2)


def carga_barco(env, puerto, bodega, embarque):
    while True:
        if len(puerto.barcos) > 0 or embarque.barco:
            if not embarque.barco:
                embarque.barco = puerto.barcos.pop(0)
            salida = 0
            if embarque.barco.tipo == 1:
                carga = min(embarque.capacidad-embarque.carga_diaria, embarque.barco.capacidad - embarque.barco.carga,
                            bodega.bodega, puerto.necesidad_embarco - puerto.carga_actual)
                if bodega.bodega == 0:
                    salida = 1
                    puerto.barco_parcialmente += 1
                puerto.cargando_barco(carga, embarque)
                bodega.cambia_cobre(-carga)
            else:
                carga = min(embarque.capacidad-embarque.carga_diaria, embarque.barco.capacidad - embarque.barco.carga)
                puerto.carga_diaria += carga

            tiempo = embarque.calculo_tiempo(carga)
            if embarque.barco.carga == embarque.barco.capacidad or puerto.carga_actual >= puerto.necesidad_embarco or salida == 1:
                puerto.salida_barco(embarque)

            if carga == bodega.bodega or tiempo == 0:
                nuevo_tiempo = max(1, embarque.tiempo)
                yield env.timeout(nuevo_tiempo)
            else:
                yield env.timeout(tiempo)
        else:
            yield env.timeout(24)


def llega_barco(env, puerto, bodega, barco):
    yield env.timeout(0)
    puerto.llegada_barco(barco)
    if bodega.bodega == 0 and type == 1:
        puerto.salida_barco()
        puerto.barco_perdido += 1


def programacion_barcos(env, dia, puerto, bodega, capacidad):
    retraso = uniform(0, 3)
    wait_time = 24 * (dia + retraso)
    yield env.timeout(wait_time)

    # LLegada barco angloamerica
    barco = Barco(capacidad, 1)
    env.process(llega_barco(env, puerto, bodega, barco))


def barcos_angloamerica(env, puerto, bodega):
    while True:
        espera = int(expovariate(0.00416))
        yield env.timeout(espera)
        barco = angloamerica()
        env.process(llega_barco(env, puerto, bodega, barco))


def calculo_bodega(index):
    # Mes enero
    if index == 0:
        return uniform(0.6, 0.7)
    # Mes diciembre
    elif index == 11:
        return uniform(1.3, 1.4)
    # Resto de los meses
    return uniform(0.9, 1.1)


def calculando_capacidades(anual, index, puerto):
    capacidades_barcos = []
    auxiliar = max(0, puerto.necesidad_embarco - puerto.carga_actual)
    bodega = int((ea[anual] * 1000 * calculo_bodega(index))/12)

    puerto.necesidad_embarco = bodega
    puerto.carga_actual = 0

    # Calulando los tipos de barcos -> Metodo cascada (mas grande al mas chico)
    for i in [32700, 21000, 10900]:
        cantidad = int(bodega//i)
        if i == 10900:
            cantidad += 1
        capacidades_barcos += [i]*cantidad
        bodega = bodega - i*cantidad

    if abs(bodega) < 5000:
        puerto.programcion = 1
    else:
        puerto.programcion = 0

    puerto.necesidad_embarco += auxiliar

    return capacidades_barcos


def programacion_mensual(env, puerto, bodega):

    meses = [744, 672, 744, 720, 744, 720, 744, 744, 720, 744, 720, 744]
    index = 0
    anual = 0

    while True:
        capacidades_barcos = calculando_capacidades(anual, index, puerto)
        if len(capacidades_barcos) > 0:
            capacidad = min(len(capacidades_barcos), 5)
            posicion = 0
            if puerto.programcion == 0:
                for n in programacion[capacidad]:
                    env.process(programacion_barcos(env, n, puerto, bodega, capacidades_barcos[posicion]))
                    posicion += 1
            else:
                for n in programacion2[capacidad]:
                    env.process(programacion_barcos(env, n, puerto, bodega, capacidades_barcos[posicion]))
                    posicion += 1
        yield env.timeout(meses[index])
        index += 1
        if index == 12:
            index = 0
            anual += 1
