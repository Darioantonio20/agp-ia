import numpy as np
import matplotlib.pyplot as plt
import random

# Definir las actividades sin la columna 'posicion'
actividades = [
    {'actividad': 'Barrer', 'equipo': 'Escoba', 'costo': 20, 'tiempo': 15},
    {'actividad': 'Trapear', 'equipo': 'Trapeador y cubo', 'costo': 25, 'tiempo': 20},
    {'actividad': 'Limpiar ventanas', 'equipo': 'Limpiavidrios y trapo', 'costo': 35, 'tiempo': 30},
    {'actividad': 'Sacar la basura', 'equipo': 'Bolsas de basura', 'costo': 10, 'tiempo': 10},
    {'actividad': 'Desinfectar superficies', 'equipo': 'Desinfectante y trapo', 'costo': 40, 'tiempo': 25},
    {'actividad': 'Aspirar alfombras y tapetes', 'equipo': 'Aspiradora', 'costo': 30, 'tiempo': 30},
    {'actividad': 'Limpieza de baños', 'equipo': 'Cepillo de baño y desinfectante', 'costo': 45, 'tiempo': 40},
    {'actividad': 'Limpieza de cocinas', 'equipo': 'Desengrasante y trapo', 'costo': 45, 'tiempo': 45},
    {'actividad': 'Limpieza de muebles', 'equipo': 'Trapo y pulidor de muebles', 'costo': 20, 'tiempo': 20},
    {'actividad': 'Limpieza de electrodomésticos', 'equipo': 'Trapo y limpiador multiusos', 'costo': 35, 'tiempo': 30},
    {'actividad': 'Limpieza de oficinas', 'equipo': 'Aspiradora y trapo', 'costo': 50, 'tiempo': 60},
    {'actividad': 'Limpieza de áreas comunes', 'equipo': 'Trapeador y cubo', 'costo': 40, 'tiempo': 45},
    {'actividad': 'Limpieza de ventanas', 'equipo': 'Limpiavidrios y trapo', 'costo': 35, 'tiempo': 30},
    {'actividad': 'Limpieza de alfombras y tapetes', 'equipo': 'Aspiradora', 'costo': 30, 'tiempo': 30},
    {'actividad': 'Limpieza de pisos duros', 'equipo': 'Mopa y cubo', 'costo': 30, 'tiempo': 40},
    {'actividad': 'Limpieza de equipos y maquinaria', 'equipo': 'Desinfectante y trapo', 'costo': 60, 'tiempo': 60},
    {'actividad': 'Limpieza post-construcción', 'equipo': 'Escoba, trapeador y cubo', 'costo': 80, 'tiempo': 120},
    {'actividad': 'Limpieza de estacionamientos', 'equipo': 'Escoba y recogedor', 'costo': 50, 'tiempo': 60},
    {'actividad': 'Limpieza de hospitales', 'equipo': 'Desinfectante y trapo', 'costo': 100, 'tiempo': 90},
    {'actividad': 'Limpieza de tiendas y centros comerciales', 'equipo': 'Aspiradora y trapeador', 'costo': 70, 'tiempo': 90}
]

# Parámetros del algoritmo
num_generaciones = 50
tamaño_población = 20
prob_mutacion = 0.1
num_actividades = len(actividades)

# Generar una población inicial aleatoria
def generar_individuo():
    """Genera un individuo como una lista de asignaciones de empleados."""
    return [random.randint(0, 4) for _ in range(num_actividades)]  # Máximo de 5 empleados

def generar_población():
    """Genera una población de individuos."""
    return [generar_individuo() for _ in range(tamaño_población)]

# Función de aptitud
def calcular_aptitud(individuo):
    """Calcula la aptitud de un individuo considerando costo, tiempo y empleados."""
    costo_total = 0
    tiempo_total = 0
    empleados_usados = set()
    
    for i, empleado in enumerate(individuo):
        actividad = actividades[i]
        costo_total += actividad['costo']
        tiempo_total += actividad['tiempo']
        empleados_usados.add(empleado)
    
    max_empleados = len(empleados_usados)
    penalizacion = 0
    if tiempo_total > 240:  # Supongamos un límite de 4 horas (240 minutos)
        penalizacion = tiempo_total - 240  # Penalización por exceso de tiempo
    
    # Aptitud considerando costo, tiempo y número de empleados (menor es mejor)
    aptitud = 1 / (costo_total + tiempo_total + max_empleados * 10 + penalizacion)
    return aptitud

# Selección
def seleccionar_padres(población, aptitudes):
    """Selecciona dos padres de la población usando ruleta."""
    seleccionados = random.choices(población, weights=aptitudes, k=2)
    return seleccionados

# Cruce
def cruzar(padre1, padre2):
    """Cruza dos padres para generar dos hijos."""
    punto_cruce = random.randint(1, num_actividades - 1)
    hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
    hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
    return hijo1, hijo2

# Mutación
def mutar(individuo):
    """Mutación simple que cambia aleatoriamente la asignación de un empleado."""
    if random.random() < prob_mutacion:
        punto = random.randint(0, num_actividades - 1)
        individuo[punto] = random.randint(0, 4)  # Cambiar a un empleado diferente

# Algoritmo Genético con Poda
población = generar_población()
mejores_aptitudes = []

for _ in range(num_generaciones):
    aptitudes = [calcular_aptitud(individuo) for individuo in población]
    mejores_aptitudes.append(max(aptitudes))
    
    nueva_población = []
    
    while len(nueva_población) < tamaño_población:
        padre1, padre2 = seleccionar_padres(población, aptitudes)
        hijo1, hijo2 = cruzar(padre1, padre2)
        mutar(hijo1)
        mutar(hijo2)
        nueva_población.append(hijo1)
        nueva_población.append(hijo2)
    
    # Poda: mantener los mejores individuos
    población = sorted(nueva_población, key=calcular_aptitud, reverse=True)[:tamaño_población]

# Resultados y gráfica
mejor_individuo = max(población, key=calcular_aptitud)
mejor_aptitud = calcular_aptitud(mejor_individuo)

# Graficar la evolución de la mejor aptitud a lo largo de las generaciones
plt.plot(mejores_aptitudes)
plt.title('Evolución de la aptitud')
plt.xlabel('Generaciones')
plt.ylabel('Mejor aptitud')
plt.grid(True)
plt.show()

# Graficar aptitud de cada individuo en la población final con media de aptitud
aptitudes_finales = [calcular_aptitud(individuo) for individuo in población]
mejor_aptitud_final = max(aptitudes_finales)
peor_aptitud_final = min(aptitudes_finales)

colores = ['green' if apt == mejor_aptitud_final else 'red' if apt == peor_aptitud_final else 'blue' for apt in aptitudes_finales]

plt.figure(figsize=(10, 6))
plt.scatter(range(len(población)), aptitudes_finales, c=colores)
plt.axhline(y=np.mean(aptitudes_finales), color='orange', linestyle='--', label='Aptitud promedio')
plt.title('Aptitud de los individuos en la población final')
plt.xlabel('Individuo')
plt.ylabel('Aptitud')
plt.legend()
plt.grid(True)
plt.show()

print("Mejor individuo:", mejor_individuo)
print("Mejor aptitud:", mejor_aptitud)
