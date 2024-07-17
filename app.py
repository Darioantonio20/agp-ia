import random
from flask import Flask, render_template, request, jsonify

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
    def __init__(self, actividades, personal, tiempo, costo):
        self.actividades = actividades
        self.personal = personal
        self.tiempo = tiempo
        self.costo = costo
        self.aptitud = self.evaluarAptitud()

    def evaluarAptitud(self):
        return -(self.tiempo + self.costo + self.personal)

def crearIndividuo(actividades):
    personal = max(1, sum([actividad['tiempo'] for actividad in actividades]) // 60)
    tiempo = sum([actividad['tiempo'] for actividad in actividades])
    costo = sum([actividad['costo'] for actividad in actividades])
    return Individuo(actividades, personal, tiempo, costo)

def crearPoblacion(tamano, actividades):
    return [crearIndividuo(actividades) for _ in range(tamano)]

def seleccionarPadres(poblacion):
    poblacion.sort(key=lambda x: x.aptitud, reverse=True)
    return poblacion[:2]

def cruce(padre1, padre2):
    puntoCruce = random.randint(1, len(padre1.actividades) - 1)
    hijo1Actividades = padre1.actividades[:puntoCruce] + padre2.actividades[puntoCruce:]
    hijo2Actividades = padre2.actividades[:puntoCruce] + padre1.actividades[puntoCruce:]
    return crearIndividuo(hijo1Actividades), crearIndividuo(hijo2Actividades)

def mutar(individuo, tasaMutacion, actividades):
    if random.random() < tasaMutacion:
        individuo.actividades = random.sample(actividades, len(individuo.actividades))
        individuo.personal = max(1, sum([actividad['tiempo'] for actividad in individuo.actividades]) // 60)
        individuo.tiempo = sum([actividad['tiempo'] for actividad in individuo.actividades])
        individuo.costo = sum([actividad['costo'] for actividad in individuo.actividades])
        individuo.aptitud = individuo.evaluarAptitud()

def algoritmoGenetico(tamanoPoblacion, actividades, generaciones, tasaMutacion):
    poblacion = crearPoblacion(tamanoPoblacion, actividades)
    evolucionMejorAptitud = []

    for generacion in range(generaciones):
        padres = seleccionarPadres(poblacion)
        descendencia = []
        while len(descendencia) < tamanoPoblacion:
            hijo1, hijo2 = cruce(padres[0], padres[1])
            mutar(hijo1, tasaMutacion, actividades)
            mutar(hijo2, tasaMutacion, actividades)
            descendencia.append(hijo1)
            descendencia.append(hijo2)
        poblacion = descendencia
        mejorIndividuo = max(poblacion, key=lambda x: x.aptitud)
        peorIndividuo = min(poblacion, key=lambda x: x.aptitud)
        evolucionMejorAptitud.append(mejorIndividuo.aptitud)
        print(f"Generación {generacion}: Mejor Aptitud = {mejorIndividuo.aptitud}")

    mejoresIndividuos = sorted(poblacion, key=lambda x: x.aptitud, reverse=True)[:3]
    individuoAleatorio = random.choice(poblacion)

    return peorIndividuo, individuoAleatorio, mejorIndividuo, evolucionMejorAptitud, mejoresIndividuos

def calcularDatos(actividades, personal):
    tiempoTotal = sum([actividad['tiempo'] for actividad in actividades])
    costoTotal = sum([actividad['costo'] for actividad in actividades]) * personal
    productosNecesarios = set([actividad['equipo'] for actividad in actividades])

    satisfactorio = 'Sí' if tiempoTotal // personal <= tiempoTotal else 'No'

    return {
        'actividades': [actividad['actividad'] for actividad in actividades],
        'productos': list(productosNecesarios),
        'tiempo_total': tiempoTotal // personal,
        'costo_total': costoTotal,
        'personal_requerido': personal,
        'satisfactorio': satisfactorio
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cantidadActividades = int(request.form['cantidadActividades'])
        actividadesSeleccionadas = request.form.getlist('actividad')

        actividades = [ACTIVIDADES_LIMPIEZA[int(index)] for index in actividadesSeleccionadas]

        peorIndividuo, individuoAleatorio, mejorIndividuo, evolucion, mejoresIndividuos = algoritmoGenetico(
            tamanoPoblacion=10, 
            actividades=actividades, 
            generaciones=50, 
            tasaMutacion=0.1
        )

        peor = calcularDatos(actividades, 1)
        intermedio = calcularDatos(actividades, random.randint(2, 3))
        mejor = calcularDatos(actividades, random.randint(3, 5))

        peor['satisfactorio'] = 'Sí' if peor['tiempo_total'] <= peor['tiempo_total'] else 'No'
        intermedio['satisfactorio'] = 'Sí' if intermedio['tiempo_total'] <= intermedio['tiempo_total'] else 'No'
        mejor['satisfactorio'] = 'Sí' if mejor['tiempo_total'] <= mejor['tiempo_total'] else 'No'

        return jsonify({
            'solucion_un_empleado': peor,
            'solucion_intermedia': intermedio,
            'mejor_solucion': mejor
        })

    return render_template('index.html', actividades=ACTIVIDADES_LIMPIEZA)

if __name__ == '__main__':
    app.run(debug=True)
