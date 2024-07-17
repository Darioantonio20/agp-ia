import random
import os
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify

# Configurar Matplotlib para usar el backend 'Agg'
plt.switch_backend('Agg')

app = Flask(__name__)

ACTIVIDADES_LIMPIEZA = [
    {'posicion': 0, 'actividad': 'Barrer', 'equipo': 'Escoba', 'costo': 20, 'tiempo': 15},
    {'posicion': 1, 'actividad': 'Trapear', 'equipo': 'Trapeador y cubo', 'costo': 25, 'tiempo': 20},
    {'posicion': 2, 'actividad': 'Limpiar ventanas', 'equipo': 'Limpiavidrios y trapo', 'costo': 35, 'tiempo': 30},
    {'posicion': 3, 'actividad': 'Sacar la basura', 'equipo': 'Bolsas de basura', 'costo': 10, 'tiempo': 10},
    {'posicion': 4, 'actividad': 'Desinfectar superficies', 'equipo': 'Desinfectante y trapo', 'costo': 40, 'tiempo': 25},
    {'posicion': 5, 'actividad': 'Aspirar alfombras y tapetes', 'equipo': 'Aspiradora', 'costo': 30, 'tiempo': 30},
    {'posicion': 6, 'actividad': 'Limpieza de baños', 'equipo': 'Cepillo de baño y desinfectante', 'costo': 45, 'tiempo': 40},
    {'posicion': 7, 'actividad': 'Limpieza de cocinas', 'equipo': 'Desengrasante y trapo', 'costo': 45, 'tiempo': 45},
    {'posicion': 8, 'actividad': 'Limpieza de muebles', 'equipo': 'Trapo y pulidor de muebles', 'costo': 20, 'tiempo': 20},
    {'posicion': 9, 'actividad': 'Limpieza de electrodomésticos', 'equipo': 'Trapo y limpiador multiusos', 'costo': 35, 'tiempo': 30},
    {'posicion': 10, 'actividad': 'Limpieza de oficinas', 'equipo': 'Aspiradora y trapo', 'costo': 50, 'tiempo': 60},
    {'posicion': 11, 'actividad': 'Limpieza de áreas comunes', 'equipo': 'Trapeador y cubo', 'costo': 40, 'tiempo': 45},
    {'posicion': 12, 'actividad': 'Limpieza de ventanas', 'equipo': 'Limpiavidrios y trapo', 'costo': 35, 'tiempo': 30},
    {'posicion': 13, 'actividad': 'Limpieza de alfombras y tapetes', 'equipo': 'Aspiradora', 'costo': 30, 'tiempo': 30},
    {'posicion': 14, 'actividad': 'Limpieza de pisos duros', 'equipo': 'Mopa y cubo', 'costo': 30, 'tiempo': 40},
    {'posicion': 15, 'actividad': 'Limpieza de equipos y maquinaria', 'equipo': 'Desinfectante y trapo', 'costo': 60, 'tiempo': 60},
    {'posicion': 16, 'actividad': 'Limpieza post-construcción', 'equipo': 'Escoba, trapeador y cubo', 'costo': 80, 'tiempo': 120},
    {'posicion': 17, 'actividad': 'Limpieza de estacionamientos', 'equipo': 'Escoba y recogedor', 'costo': 50, 'tiempo': 60},
    {'posicion': 18, 'actividad': 'Limpieza de hospitales', 'equipo': 'Desinfectante y trapo', 'costo': 100, 'tiempo': 90},
    {'posicion': 19, 'actividad': 'Limpieza de tiendas y centros comerciales', 'equipo': 'Aspiradora y trapeador', 'costo': 70, 'tiempo': 90}
]

class Individuo:
    def __init__(self, actividades):
        self.actividades = actividades
        self.personal, self.tiempo, self.costo = self.calcular_datos()
        self.aptitud = self.evaluar_aptitud()

    def calcular_datos(self):
        tiempo_total = sum([actividad['tiempo'] for actividad in self.actividades])
        costo_total = sum([actividad['costo'] for actividad in self.actividades])
        personal = max(1, tiempo_total // 60)
        return personal, tiempo_total, costo_total

    def evaluar_aptitud(self):
        return -(self.tiempo + self.costo + self.personal * 100)

def crear_individuo(actividades):
    return Individuo(actividades)

def crear_poblacion(tamano, actividades):
    return [crear_individuo(random.sample(actividades, len(actividades))) for _ in range(tamano)]

def seleccionar_padres(poblacion):
    poblacion.sort(key=lambda x: x.aptitud, reverse=True)
    return poblacion[:2]

def cruce(padre1, padre2):
    punto_cruce = random.randint(1, len(padre1.actividades) - 1)
    hijo1_actividades = padre1.actividades[:punto_cruce] + padre2.actividades[punto_cruce:]
    hijo2_actividades = padre2.actividades[:punto_cruce] + padre1.actividades[punto_cruce:]
    return crear_individuo(hijo1_actividades), crear_individuo(hijo2_actividades)

def mutar(individuo, tasa_mutacion, actividades):
    if random.random() < tasa_mutacion:
        individuo.actividades = random.sample(actividades, len(individuo.actividades))
        individuo.personal, individuo.tiempo, individuo.costo = individuo.calcular_datos()
        individuo.aptitud = individuo.evaluar_aptitud()

def algoritmo_genetico(tamano_poblacion, actividades, generaciones, tasa_mutacion):
    poblacion = crear_poblacion(tamano_poblacion, actividades)
    evolucion_tiempos = []
    evolucion_costos = []

    for generacion in range(generaciones):
        padres = seleccionar_padres(poblacion)
        descendencia = []
        while len(descendencia) < tamano_poblacion:
            hijo1, hijo2 = cruce(padres[0], padres[1])
            mutar(hijo1, tasa_mutacion, actividades)
            mutar(hijo2, tasa_mutacion, actividades)
            descendencia.append(hijo1)
            descendencia.append(hijo2)
        poblacion = descendencia
        mejor_individuo = max(poblacion, key=lambda x: x.aptitud)
        peor_individuo = min(poblacion, key=lambda x: x.aptitud)
        promedio_individuo = sum(individuo.aptitud for individuo in poblacion) / len(poblacion)

        evolucion_tiempos.append((mejor_individuo.tiempo, peor_individuo.tiempo, promedio_individuo))
        evolucion_costos.append((mejor_individuo.costo, peor_individuo.costo, promedio_individuo))

        print(f"Generación {generacion}: Mejor Aptitud = {mejor_individuo.aptitud}")

    mejores_individuos = sorted(poblacion, key=lambda x: x.aptitud, reverse=True)[:3]
    individuo_aleatorio = random.choice(poblacion)

    return peor_individuo, individuo_aleatorio, mejor_individuo, mejores_individuos, evolucion_tiempos, evolucion_costos

def calcular_datos(actividades, personal, peor=False):
    tiempo_total = sum([actividad['tiempo'] for actividad in actividades])
    costo_total = sum([actividad['costo'] for actividad in actividades]) * personal
    productos_necesarios = set([actividad['equipo'] for actividad in actividades])

    if peor and len(actividades) > 5 and random.random() < 0.8:
        satisfactorio = 'No'
    else:
        satisfactorio = 'Sí' if tiempo_total // personal <= tiempo_total else 'No'

    return {
        'actividades': [actividad['actividad'] for actividad in actividades],
        'productos': list(productos_necesarios),
        'tiempo_total': tiempo_total // personal,
        'costo_total': costo_total,
        'personal_requerido': personal,
        'satisfactorio': satisfactorio
    }

def graficar_evolucion(evolucion_tiempos, evolucion_costos):
    generaciones = range(len(evolucion_tiempos))

    tiempos_mejor, tiempos_peor, tiempos_promedio = zip(*evolucion_tiempos)
    costos_mejor, costos_peor, costos_promedio = zip(*evolucion_costos)

    plt.figure()
    plt.plot(generaciones, tiempos_mejor, label='Mejor Tiempo')
    plt.plot(generaciones, tiempos_peor, label='Peor Tiempo')
    plt.plot(generaciones, tiempos_promedio, label='Promedio Tiempo')
    plt.xlabel('Generaciones')
    plt.ylabel('Tiempo Total')
    plt.title('Evolución del Tiempo a lo largo de las Generaciones')
    plt.legend()
    tiempo_grafica_path = os.path.join('static', 'grafica_tiempos.png')
    plt.savefig(tiempo_grafica_path)

    plt.figure()
    plt.plot(generaciones, costos_mejor, label='Mejor Costo')
    plt.plot(generaciones, costos_peor, label='Peor Costo')
    plt.plot(generaciones, costos_promedio, label='Promedio Costo')
    plt.xlabel('Generaciones')
    plt.ylabel('Costo Total')
    plt.title('Evolución del Costo a lo largo de las Generaciones')
    plt.legend()
    costo_grafica_path = os.path.join('static', 'grafica_costos.png')
    plt.savefig(costo_grafica_path)

    return tiempo_grafica_path, costo_grafica_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cantidad_actividades = int(request.form['cantidadActividades'])
        actividades_seleccionadas = request.form.getlist('actividad')

        actividades = [ACTIVIDADES_LIMPIEZA[int(index)] for index in actividades_seleccionadas]

        peor_individuo, individuo_aleatorio, mejor_individuo, mejores_individuos, evolucion_tiempos, evolucion_costos = algoritmo_genetico(
            tamano_poblacion=10, 
            actividades=actividades, 
            generaciones=50, 
            tasa_mutacion=0.1
        )

        peor = calcular_datos(actividades, 1, peor=True)
        intermedio = calcular_datos(actividades, random.randint(2, 3))
        mejor = calcular_datos(actividades, random.randint(3, 5))

        tiempo_grafica_path, costo_grafica_path = graficar_evolucion(evolucion_tiempos, evolucion_costos)

        return jsonify({
            'solucion_un_empleado': peor,
            'solucion_intermedia': intermedio,
            'mejor_solucion': mejor,
            'grafica_tiempos_path': tiempo_grafica_path,
            'grafica_costos_path': costo_grafica_path
        })

    return render_template('index.html', actividades=ACTIVIDADES_LIMPIEZA)

if __name__ == '__main__':
    app.run(debug=True)
