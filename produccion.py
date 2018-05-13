from camiones import tramo2
from variables import tramo2_camiones


def produccion_saladillo(env, bodega, bodega2, puerto, tramo2 ,est):
    while True:
        # Estadisticas bodega al inicio del dia
        est.nuevo_dia(bodega.bodega, bodega2.bodega)

        # Barcos en el puerto diario
        est.barcos_puerto.append(len(puerto.barcos))

        # Estadisticas calculo de error en bodega
        est.calculo_error(bodega.bodega)

        tramo2.dia = 0

        yield env.timeout(24)


def produccion_saladillo_horaria(env, bodega, tramo, bodega2 ,est):
    produccion = [2074, 2348, 2498.6, 1630.1, 1534.3, 1315.1, 1643.83, 1643.83]
    index = -1
    while True:
        if (env.now % 8760) == 0:
            index += 1
            tramo.camiones = tramo2_camiones[index]

        # Agrega a la bodega
        carga = produccion[index] / 24

        bodega.cambia_cobre(int(carga))

        if bodega.bodega > 7500 and tramo.dia == 0:
            env.process(tramo2(env, tramo, est))
            tramo.dia = 1

        est.nueva_hora(bodega.bodega, bodega2.bodega)

        yield env.timeout(1)