

def produccion_saladillo(env, bodega, bodega2, t4, est, file):
    #produccion = [2572.6, 2931.5, 2586.3, 2386.3, 2290.4, 2071.2, 2400.0, 2400.0]
    produccion = [2074, 2348, 2498.6, 1630.1, 1534.3, 1315.1, 1643.83, 1643.83]
    index = -1
    while True:
        est.nuevo_dia(bodega.bodega, bodega2.bodega)
        if (env.now % 8760) == 0:
            print("ANO {}".format(index + 2))
            file.write("----------- Cambio de ano ----------- {}\n".format(env.now))
            index += 1
        carga = produccion[index]
        bodega.cambia_cobre(int(carga))
        est.calculo_error(bodega.bodega)

        # Tramos
        t4.proyeccion_diario = 200

        yield env.timeout(24)
