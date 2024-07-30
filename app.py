import random
from flask import Flask, render_template, request, jsonify, url_for
import matplotlib.pyplot as plt
import matplotlib
import csv
import os

matplotlib.use('Agg')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

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

def formar_parejas(poblacion):
    parejas = []
    n = len(poblacion)
    for individuo in poblacion:
        m = random.randint(1, n)
        indices = random.sample(range(n), m)
        indices = [i for i in indices if i != poblacion.index(individuo)]
        for indice in indices:
            parejas.append((individuo, poblacion[indice]))
    return parejas

def cruce(padre1, padre2):
    punto_cruce = len(padre1.actividades) // 2 
    hijo1_actividades = padre1.actividades[:punto_cruce] + padre2.actividades[punto_cruce:]
    hijo2_actividades = padre2.actividades[:punto_cruce] + padre1.actividades[:punto_cruce:]
    return crear_individuo(hijo1_actividades), crear_individuo(hijo2_actividades)

def mutar(individuo, tasa_mutacion_gen, tasa_mutacion_individuo, actividades):
    if random.random() < tasa_mutacion_individuo:
        for i in range(len(individuo.actividades)):
            if random.random() < tasa_mutacion_gen:
                nuevo_actividad = random.choice(actividades)
                individuo.actividades[i] = nuevo_actividad
        individuo.personal, individuo.tiempo, individuo.costo = individuo.calcular_datos()
        individuo.aptitud = individuo.evaluar_aptitud()

def podar_poblacion(poblacion, poblacion_maxima):
    poblacion_unica = {individuo.aptitud: individuo for individuo in poblacion}.values()
    mejor_individuo = min(poblacion_unica, key=lambda x: x.aptitud)
    poblacion_restante = [ind for ind in poblacion_unica if ind != mejor_individuo] 
    num_eliminar = len(poblacion_restante) - (poblacion_maxima - 1) 
    if num_eliminar > 0:
        eliminar = random.sample(poblacion_restante, num_eliminar)
        poblacion_restante = [ind for ind in poblacion_restante if ind not in eliminar]
    poblacion_restante.append(mejor_individuo)
    return poblacion_restante

def algoritmo_genetico(tamano_poblacion, actividades, generaciones, tasa_mutacion_gen, tasa_mutacion_individuo):
    poblacion = crear_poblacion(tamano_poblacion, actividades)
    evolucion_mejor_aptitud = []
    evolucion_tiempos = []
    evolucion_costos = []
    evolucion_peor = []
    evolucion_promedio = []
    evolucion_mejor = []

    for generacion in range(generaciones):
        parejas = formar_parejas(poblacion)
        descendencia = []

        for pareja in parejas:
            hijo1, hijo2 = cruce(pareja[0], pareja[1])
            mutar(hijo1, tasa_mutacion_gen, tasa_mutacion_individuo, actividades)
            mutar(hijo2, tasa_mutacion_gen, tasa_mutacion_individuo, actividades)
            descendencia.append(hijo1)
            descendencia.append(hijo2)

        poblacion.extend(descendencia)
        poblacion = podar_poblacion(poblacion, tamano_poblacion)

        mejor_individuo = min(poblacion, key=lambda x: x.aptitud)
        peor_individuo = max(poblacion, key=lambda x: x.aptitud)
        tiempo_promedio = sum(individuo.tiempo for individuo in poblacion) / len(poblacion)
        costo_promedio = sum(individuo.costo for individuo in poblacion) / len(poblacion)
        personal_promedio = sum(individuo.personal for individuo in poblacion) / len(poblacion)

        evolucion_mejor_aptitud.append(mejor_individuo.aptitud)
        evolucion_tiempos.append((mejor_individuo.tiempo, tiempo_promedio, peor_individuo.tiempo))
        evolucion_costos.append((mejor_individuo.costo, costo_promedio, peor_individuo.costo))

        evolucion_peor.append({
            'tiempo': peor_individuo.tiempo,
            'costo': peor_individuo.costo,
            'personal': peor_individuo.personal
        })

        evolucion_promedio.append({
            'tiempo': tiempo_promedio,
            'costo': costo_promedio,
            'personal': personal_promedio
        })

        evolucion_mejor.append({
            'tiempo': mejor_individuo.tiempo,
            'costo': mejor_individuo.costo,
            'personal': mejor_individuo.personal
        })

        print(f"Generación {generacion + 1}:")
        print(f"  Peor - Tiempo: {peor_individuo.tiempo}, Costo: {peor_individuo.costo}, Personal: {peor_individuo.personal}")
        print(f"  Promedio - Tiempo: {tiempo_promedio}, Costo: {costo_promedio}, Personal: {personal_promedio}")
        print(f"  Mejor - Tiempo: {mejor_individuo.tiempo}, Costo: {mejor_individuo.costo}, Personal: {mejor_individuo.personal}")

    return peor_individuo, mejor_individuo, evolucion_mejor_aptitud, evolucion_tiempos, evolucion_costos, evolucion_peor, evolucion_promedio, evolucion_mejor

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

def cargar_empleados(filepath):
    empleados = []
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            empleados.append(row)
    return empleados

def asignar_actividades_a_empleados(empleados, actividades):
    actividades_asignadas = []
    for actividad in actividades:
        num_personal = max(1, actividad['tiempo'] // 60)
        empleados_para_actividad = random.sample(empleados, min(num_personal, len(empleados)))
        actividades_asignadas.append({
            'actividad': actividad['actividad'],
            'equipo': actividad['equipo'],
            'empleados': empleados_para_actividad
        })
    return actividades_asignadas

@app.route('/', methods=['GET', 'POST'])
def index():
    actividades_asignadas = None
    empleados = []
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                empleados = cargar_empleados(filepath)
                actividades_asignadas = asignar_actividades_a_empleados(empleados, ACTIVIDADES_LIMPIEZA)
            
        if 'cantidadActividades' in request.form:
            cantidad_actividades = int(request.form['cantidadActividades'])
        else:
            cantidad_actividades = 0

        actividades_seleccionadas = request.form.getlist('actividad')
        actividades_usuario = [ACTIVIDADES_LIMPIEZA[int(index)] for index in actividades_seleccionadas]

        peor_individuo, mejor_individuo, evolucion_mejor_aptitud, evolucion_tiempos, evolucion_costos, evolucion_peor, evolucion_promedio, evolucion_mejor = algoritmo_genetico(
            tamano_poblacion=26,
            actividades=actividades_usuario,
            generaciones=100,
            tasa_mutacion_gen=0.9,
            tasa_mutacion_individuo=0.9
        )

        peor = calcular_datos(actividades_usuario, 1, peor=True)
        intermedio = calcular_datos(actividades_usuario, random.randint(2, 3))
        mejor = calcular_datos(actividades_usuario, random.randint(3, 5))

        generaciones = list(range(100))

        max_tiempo = max(max(data['tiempo'] for data in evolucion_peor),
                         max(data['tiempo'] for data in evolucion_promedio),
                         max(data['tiempo'] for data in evolucion_mejor))

        max_costo = max(max(data['costo'] for data in evolucion_peor),
                        max(data['costo'] for data in evolucion_promedio),
                        max(data['costo'] for data in evolucion_mejor))

        y_max = max(max_tiempo, max_costo) + 100

        tiempos_peor = [data['tiempo'] for data in evolucion_peor]
        costos_peor = [data['costo'] for data in evolucion_peor]
        personal_peor = [data['personal'] for data in evolucion_peor]

        plt.figure(figsize=(10, 6))
        plt.plot(generaciones, tiempos_peor, label='Peor Tiempo', color='blue')
        plt.plot(generaciones, costos_peor, label='Peor Costo', color='#556B2F')
        plt.plot(generaciones, personal_peor, label='Peor Personal', color='red')
        plt.xlabel('Generaciones')
        plt.ylabel('Valores del Peor Individuo')
        plt.title('Evolución del Peor Individuo')
        plt.ylim(0, y_max)
        plt.yticks(range(0, y_max + 100, 25))
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('static/grafica_peor_individuo.png')
        plt.close()

        tiempos_promedio = [data['tiempo'] for data in evolucion_promedio]
        costos_promedio = [data['costo'] for data in evolucion_promedio]
        personal_promedio = [data['personal'] for data in evolucion_promedio]

        plt.figure(figsize=(10, 6))
        plt.plot(generaciones, tiempos_promedio, label='Promedio Tiempo', color='blue')
        plt.plot(generaciones, costos_promedio, label='Promedio Costo', color='#556B2F')
        plt.plot(generaciones, personal_promedio, label='Promedio Personal', color='gray')
        plt.xlabel('Generaciones')
        plt.ylabel('Valores Promedio')
        plt.title('Evolución del Promedio')
        plt.ylim(0, y_max)
        plt.yticks(range(0, y_max + 100, 25))
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('static/grafica_promedio.png')
        plt.close()

        tiempos_mejor = [data['tiempo'] for data in evolucion_mejor]
        costos_mejor = [data['costo'] for data in evolucion_mejor]
        personal_mejor = [data['personal'] for data in evolucion_mejor]

        plt.figure(figsize=(10, 6))
        plt.plot(generaciones, tiempos_mejor, label='Mejor Tiempo', color='blue')
        plt.plot(generaciones, costos_mejor, label='Mejor Costo', color='#556B2F')
        plt.plot(generaciones, personal_mejor, label='Mejor Personal', color='green')
        plt.xlabel('Generaciones')
        plt.ylabel('Valores del Mejor Individuo')
        plt.title('Evolución del Mejor Individuo')
        plt.ylim(0, y_max)
        plt.yticks(range(0, y_max + 100, 25))
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('static/grafica_mejor_individuo.png')
        plt.close()

        return jsonify({
            'solucion_un_empleado': peor,
            'solucion_intermedia': intermedio,
            'solucion_mejor': mejor,
            'grafica_peor_individuo_path': url_for('static', filename='grafica_peor_individuo.png'),
            'grafica_promedio_path': url_for('static', filename='grafica_promedio.png'),
            'grafica_mejor_individuo_path': url_for('static', filename='grafica_mejor_individuo.png'),
            'actividades_asignadas': actividades_asignadas or []
        })

    return render_template('index.html', actividades=ACTIVIDADES_LIMPIEZA, actividades_asignadas=actividades_asignadas or [], empleados=empleados)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
