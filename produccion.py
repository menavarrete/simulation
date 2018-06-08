from variables import tramo2_camiones, tramo5_proyeccion, tramo5_camiones, produccion


def produccion_saladillo(env, bodega, bodega2, puerto, tramo2, est):
    while True:
        # Estadisticas bodega al inicio del dia
        # est.nuevo_dia(bodega.bodega, bodega2.bodega)
        est.nuevo_dia_dos(bodega2.bodega, bodega.bodega)

        # Barcos en el puerto diario
        est.barcos_puerto.append(len(puerto.barcos))
        print(int(env.now/24),end="-")
        for n in puerto.barcos:
            print(n.capacidad, end="")
        print()

        # Estadisticas calculo de error en bodega
        est.calculo_error(bodega.bodega)

        # Puerto carga diaria
        puerto.carga_diaria = 0
        puerto.tiempo = 24

        yield env.timeout(24)


def produccion_saladillo_horaria(env, bodega, tramo, bodega2, tramo5, est):
    index = 0
    while True:
        if (env.now % 8760) == 0 and env.now != 0:
            index += 1
            bodega.anual = produccion[index]
            tramo.camiones = tramo2_camiones[index]
            tramo5.cambio_anual(tramo5_camiones[index], tramo5_proyeccion[index])

        # Agrega a la bodega
        carga = int(produccion[index] / 24)
        bodega.cambia_cobre(carga)

        # est.nueva_hora(bodega.bodega, bodega2.bodega)

        yield env.timeout(1)