import random
from flask import Flask, render_template, request, jsonify, url_for
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

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
        return self.tiempo + self.costo + self.personal * 100

def crear_individuo(actividades):
    return Individuo(actividades)

def crear_poblacion(tamano, actividades):
    return [crear_individuo(random.sample(actividades, len(actividades))) for _ in range(tamano)]

def seleccionar_padres(poblacion):
    poblacion.sort(key=lambda x: x.aptitud)
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
    evolucion_mejor_aptitud = []
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

        mejor_individuo = min(poblacion, key=lambda x: x.aptitud)
        peor_individuo = max(poblacion, key=lambda x: x.aptitud)
        tiempo_promedio = sum(individuo.tiempo for individuo in poblacion) / len(poblacion)
        costo_promedio = sum(individuo.costo for individuo in poblacion) / len(poblacion)

        evolucion_mejor_aptitud.append(mejor_individuo.aptitud)
        evolucion_tiempos.append((mejor_individuo.tiempo, tiempo_promedio, peor_individuo.tiempo))
        evolucion_costos.append((mejor_individuo.costo, costo_promedio, peor_individuo.costo))

        print(f"Generación {generacion}: Mejor Aptitud = {mejor_individuo.aptitud}")

    return peor_individuo, mejor_individuo, evolucion_mejor_aptitud, evolucion_tiempos, evolucion_costos

def calcular_datos(actividades, personal, peor=False):
    tiempo_total = sum([actividad['tiempo'] for actividad in actividades])
    costo_total = sum([actividad['costo'] for actividad in actividades]) * personal
    productos_necesarios = set([actividad['equipo'] for actividad in actividades])

    if peor and len(actividades) > 5:
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cantidad_actividades = int(request.form['cantidadActividades'])
        actividades_seleccionadas = request.form.getlist('actividad')

        actividades = [ACTIVIDADES_LIMPIEZA[int(index)] for index in actividades_seleccionadas]

        peor_individuo, mejor_individuo, evolucion_mejor_aptitud, evolucion_tiempos, evolucion_costos = algoritmo_genetico(
            tamano_poblacion=20, 
            actividades=actividades, 
            generaciones=100, 
            tasa_mutacion=0.01
        )

        peor = calcular_datos(peor_individuo.actividades, 1, peor=True)
        intermedio = calcular_datos(mejor_individuo.actividades, random.randint(2, 3))
        mejor = calcular_datos(mejor_individuo.actividades, random.randint(3, 5))

        generaciones = list(range(100))

        plt.figure(figsize=(14, 7))

        plt.subplot(1, 2, 1)
        tiempos_mejor = [t[0] for t in evolucion_tiempos]
        tiempos_promedio = [t[1] for t in evolucion_tiempos]
        tiempos_peor = [t[2] for t in evolucion_tiempos]
        plt.plot(generaciones, tiempos_mejor, label='Mejor Tiempo')
        plt.plot(generaciones, tiempos_promedio, label='Tiempo Promedio')
        plt.plot(generaciones, tiempos_peor, label='Peor Tiempo')
        plt.xlabel('Generaciones')
        plt.ylabel('Tiempo Total')
        plt.ylim(0, max(tiempos_peor) + 10)  # Asegurando que los valores sean positivos
        plt.legend()

        plt.subplot(1, 2, 2)
        costos_mejor = [c[0] for c in evolucion_costos]
        costos_promedio = [c[1] for c in evolucion_costos]
        costos_peor = [c[2] for c in evolucion_costos]
        plt.plot(generaciones, costos_mejor, label='Mejor Costo')
        plt.plot(generaciones, costos_promedio, label='Costo Promedio')
        plt.plot(generaciones, costos_peor, label='Peor Costo')
        plt.xlabel('Generaciones')
        plt.ylabel('Costo Total')
        plt.ylim(0, max(costos_peor) + 10)  # Asegurando que los valores sean positivos
        plt.legend()

        plt.tight_layout()
        plt.savefig('static/grafica_evolucion.png')
        plt.close()

        return jsonify({
            'solucion_un_empleado': peor,
            'solucion_intermedia': intermedio,
            'solucion_mejor': mejor,
            'grafica_tiempos_path': url_for('static', filename='grafica_evolucion.png'),
            'grafica_costos_path': url_for('static', filename='grafica_evolucion.png')
        })

    return render_template('index.html', actividades=ACTIVIDADES_LIMPIEZA)

if __name__ == '__main__':
    app.run(debug=True)
