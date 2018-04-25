

def produccion_saladillo(env, bodega, file):
    produccion = [2572.6, 2931.5, 2586.3, 2386.3, 2290.4, 2071.2, 2400.0, 2400.0]
    index = -1
    while True:
        if (env.now % 8760) == 0:
            print("AÑO {}".format(index + 2))
            file.write("----------- Cambio de ano ----------- {}\n".format(env.now))
            index += 1
        carga = produccion[index]
        bodega.cambia_cobre(int(carga))
        yield env.timeout(24)
