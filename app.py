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

def crearIndividuo(cantidadActividades):
    actividades = random.sample(ACTIVIDADES_LIMPIEZA, cantidadActividades)
    personal = max(1, sum([actividad['tiempo'] for actividad in actividades]) // 60)
    tiempo = sum([actividad['tiempo'] for actividad in actividades])
    costo = sum([actividad['costo'] for actividad in actividades])
    return Individuo(actividades, personal, tiempo, costo)

def crearPoblacion(tamano, cantidadActividades):
    return [crearIndividuo(cantidadActividades) for _ in range(tamano)]

def seleccionarPadres(poblacion):
    poblacion.sort(key=lambda x: x.aptitud, reverse=True)
    return poblacion[:2]

def cruce(padre1, padre2):
    puntoCruce = random.randint(1, len(padre1.actividades) - 1)
    hijo1Actividades = padre1.actividades[:puntoCruce] + padre2.actividades[puntoCruce:]
    hijo2Actividades = padre2.actividades[:puntoCruce] + padre1.actividades[puntoCruce:]
    return crearIndividuo(len(hijo1Actividades)), crearIndividuo(len(hijo2Actividades))

def mutar(individuo, tasaMutacion):
    if random.random() < tasaMutacion:
        individuo.actividades = random.sample(ACTIVIDADES_LIMPIEZA, len(individuo.actividades))
        individuo.personal = max(1, sum([actividad['tiempo'] for actividad in individuo.actividades]) // 60)
        individuo.tiempo = sum([actividad['tiempo'] for actividad in individuo.actividades])
        individuo.costo = sum([actividad['costo'] for actividad in individuo.actividades])
        individuo.aptitud = individuo.evaluarAptitud()

def algoritmoGenetico(tamanoPoblacion, cantidadActividades, generaciones, tasaMutacion):
    poblacion = crearPoblacion(tamanoPoblacion, cantidadActividades)
    evolucionMejorAptitud = []

    for generacion in range(generaciones):
        padres = seleccionarPadres(poblacion)
        descendencia = []
        while len(descendencia) < tamanoPoblacion:
            hijo1, hijo2 = cruce(padres[0], padres[1])
            mutar(hijo1, tasaMutacion)
            mutar(hijo2, tasaMutacion)
            descendencia.append(hijo1)
            descendencia.append(hijo2)
        poblacion = descendencia
        mejorIndividuo = max(poblacion, key=lambda x: x.aptitud)
        evolucionMejorAptitud.append(mejorIndividuo.aptitud)
        print(f"Generación {generacion}: Mejor Aptitud = {mejorIndividuo.aptitud}")

    mejoresIndividuos = sorted(poblacion, key=lambda x: x.aptitud, reverse=True)[:3]

    return mejorIndividuo, evolucionMejorAptitud, mejoresIndividuos

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cantidadActividades = int(request.form['cantidadActividades'])
        actividadesSeleccionadas = request.form.getlist('actividad')

        actividades = [ACTIVIDADES_LIMPIEZA[int(index)] for index in actividadesSeleccionadas]

        mejorSolucion, evolucion, mejoresIndividuos = algoritmoGenetico(
            tamanoPoblacion=10, 
            cantidadActividades=cantidadActividades, 
            generaciones=50, 
            tasaMutacion=0.1
        )

        actividadesSeleccionadas = [actividad['actividad'] for actividad in mejorSolucion.actividades]
        productosNecesarios = set([actividad['equipo'] for actividad in mejorSolucion.actividades])
        tiempoTotal = mejorSolucion.tiempo
        costoTotal = mejorSolucion.costo
        personalRequerido = mejorSolucion.personal

        return jsonify({
            'actividades': actividadesSeleccionadas,
            'productos': list(productosNecesarios),
            'tiempo_total': tiempoTotal,
            'costo_total': costoTotal,
            'personal_requerido': personalRequerido,
            'evolucion': evolucion
        })

    return render_template('index.html', actividades=ACTIVIDADES_LIMPIEZA)

if __name__ == '__main__':
    app.run(debug=True)
