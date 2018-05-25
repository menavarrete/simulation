from variables import tramo2_camiones, tramo5_proyeccion, tramo5_camiones


def produccion_saladillo(env, bodega, bodega2, puerto, tramo2, est):
    while True:
        # Estadisticas bodega al inicio del dia
        # est.nuevo_dia(bodega.bodega, bodega2.bodega)
        est.nuevo_dia_dos(bodega2.bodega, bodega.bodega)

        # Barcos en el puerto diario
        est.barcos_puerto.append(len(puerto.barcos))

        # Estadisticas calculo de error en bodega
        est.calculo_error(bodega.bodega)

        yield env.timeout(24)


def produccion_saladillo_horaria(env, bodega, tramo, bodega2, tramo5, est):
    produccion = [2074, 2348, 2498.6, 1630.1, 1534.3, 1315.1, 1643.83, 1643.83]
    index = -1
    while True:
        if (env.now % 8760) == 0:
            index += 1
            bodega.anual = produccion[index]
            tramo.camiones = tramo2_camiones[index]
            tramo5.maximo_diario = tramo5_proyeccion[index]
            tramo5.camiones = tramo5_camiones[index]

        # Agrega a la bodega
        carga = int(produccion[index] / 24)

        bodega.cambia_cobre(carga)

        # est.nueva_hora(bodega.bodega, bodega2.bodega)

        yield env.timeout(1)