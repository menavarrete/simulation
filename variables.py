
author = 'menavarrete-rtacuna'

# Caracteristicas simulacion
name = "Version_definitiva"
caracteristicas = "Version final de la simulacion"

# Tiempo simulacion
anos = 8

# Replicas
replicas = 100

# Fundicion ventanas
ventanas_name = "Fundicion Ventanas"

# Camiones
truck_capacity = 28

# El Teniente
teniente_name = "Division El Teniente"


# Bodega division andina
andina_capacity = 10000
andina_name = "Bodega Division Andina"


# bodega saladillo
saladillo_bodega1_name = "Bodega principal Saladillo"
saladillo_bodega1_capacity = 7500

saladillo_bodega2_name = "Bodega secundaria Saladillo"
saladillo_bodega2_capacity = 7500
saladillo_production_quantity = 25
saladillo_production_time = 12
saladillo_between_time = 12
saladillo_n_camiones = 8


# fundicion potrerillos
potrerillos_name = "Fundicion Potrerillos (Division El Salvador)"
potrerillos_n_camiones = 5


# Tramo 5
tramo5_travel_time = 3
tramo5_name = "Tramo 5 (El Teniente - Division Andina)"
tramo5_camiones = [21, 21, 21, 21, 21, 0, 0, 0]
tramo5_proyeccion = [606, 554, 548, 478, 315, 0, 0, 0]


# Tramo 4
tramo4_travel_time = 1
tramo4_name = "tramo 4 (Division Andina - Fundicion Ventanas)"
tramo4_camiones = [8, 8, 8, 8, 8, 8, 8, 8]
tramo4_proyeccion = [200, 200, 200, 200, 200, 200, 200, 200]


# tTamo 2
tramo2_travel_time = 3
tramo2_name = "tramo 2 (Saladillo - Division Andina)"
tramo2_camiones = [37, 34, 38, 4, 4, 4, 4, 4]


# Produccion
produccion = [2074, 2348, 2498.6, 1630.1, 1534.3, 1315.1, 1643.83, 1643.83]

# Programacion de barcos
programacion = {1: [12], 2: [1, 13], 3: [1, 14, 20], 4: [1, 10, 20, 25], 5: [1, 7, 14, 21, 25]}
programacion2 = {1: [12], 2: [10, 22], 3: [1, 16, 25], 4: [1, 10, 22, 25], 5: [1, 8, 16, 24, 25]}

# Necesidad de embarque anual
ea = [905, 982, 1039, 696, 602, 407, 527, 527]
