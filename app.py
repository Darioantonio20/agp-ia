import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

SALARIO_POR_HORA = 17.71
COSTO_MAXIMO = 5000

class Individuo:
    def __init__(self, tareas, productos, personal, tiempo, costo):
        self.tareas = tareas
        self.productos = productos
        self.personal = personal
        self.tiempo = tiempo
        self.costo = costo
        self.aptitud = self.evaluarAptitud()

    def evaluarAptitud(self):
        aptitudTareas = sum(self.tareas) * -1
        aptitudProductos = sum(self.productos) * -1
        aptitudPersonal = sum(self.personal) * -1
        aptitudTiempo = sum(self.tiempo) * -1
        aptitudCosto = sum(self.costo) * -1
        return aptitudTareas + aptitudProductos + aptitudPersonal + aptitudTiempo + aptitudCosto

def crearIndividuo(cantidadTareas, cantidadProductos, cantidadPersonal, cantidadTiempo, cantidadCosto):
    tareas = [random.randint(0, 1) for _ in range(cantidadTareas)]
    productos = [random.randint(0, 1) for _ in range(cantidadProductos)]
    personal = [random.randint(1, 4) for _ in range(cantidadPersonal)]
    tiempo = [random.randint(60, 100) for _ in range(cantidadTiempo)]
    costo = [min(p * t * SALARIO_POR_HORA, COSTO_MAXIMO) for p, t in zip(personal, tiempo)]
    return Individuo(tareas, productos, personal, tiempo, costo)

def crearPoblacion(tamano, cantidadTareas, cantidadProductos, cantidadPersonal, cantidadTiempo, cantidadCosto):
    return [crearIndividuo(cantidadTareas, cantidadProductos, cantidadPersonal, cantidadTiempo, cantidadCosto) for _ in range(tamano)]

def seleccionarPadres(poblacion):
    poblacion.sort(key=lambda x: x.aptitud, reverse=True)
    return poblacion[:2]

def cruce(padre1, padre2):
    puntoCruce = random.randint(1, len(padre1.tareas) - 1)
    hijo1Tareas = padre1.tareas[:puntoCruce] + padre2.tareas[puntoCruce:]
    hijo2Tareas = padre2.tareas[:puntoCruce] + padre1.tareas[puntoCruce:]
    hijo1Productos = padre1.productos[:puntoCruce] + padre2.productos[puntoCruce:]
    hijo2Productos = padre2.productos[:puntoCruce] + padre1.productos[puntoCruce:]
    hijo1Personal = padre1.personal[:puntoCruce] + padre2.personal[puntoCruce:]
    hijo2Personal = padre2.personal[:puntoCruce] + padre1.personal[puntoCruce:]
    hijo1Tiempo = padre1.tiempo[:puntoCruce] + padre2.tiempo[puntoCruce:]
    hijo2Tiempo = padre2.tiempo[:puntoCruce] + padre1.tiempo[puntoCruce:]
    hijo1Costo = [min(p * t * SALARIO_POR_HORA, COSTO_MAXIMO) for p, t in zip(hijo1Personal, hijo1Tiempo)]
    hijo2Costo = [min(p * t * SALARIO_POR_HORA, COSTO_MAXIMO) for p, t in zip(hijo2Personal, hijo2Tiempo)]
    return Individuo(hijo1Tareas, hijo1Productos, hijo1Personal, hijo1Tiempo, hijo1Costo), \
           Individuo(hijo2Tareas, hijo2Productos, hijo2Personal, hijo2Tiempo, hijo2Costo)

def mutar(individuo, tasaMutacion):
    for i in range(len(individuo.tareas)):
        if random.random() < tasaMutacion:
            individuo.tareas[i] = 1 - individuo.tareas[i]
    for i in range(len(individuo.productos)):
        if random.random() < tasaMutacion:
            individuo.productos[i] = 1 - individuo.productos[i]
    for i in range(len(individuo.personal)):
        if random.random() < tasaMutacion:
            individuo.personal[i] = random.randint(1, 4)
    for i in range(len(individuo.tiempo)):
        if random.random() < tasaMutacion:
            individuo.tiempo[i] = random.randint(60, 100)
    individuo.costo = [min(p * t * SALARIO_POR_HORA, COSTO_MAXIMO) for p, t in zip(individuo.personal, individuo.tiempo)]
    individuo.aptitud = individuo.evaluarAptitud()

def algoritmoGenetico(tamanoPoblacion, cantidadTareas, cantidadProductos, cantidadPersonal, cantidadTiempo, cantidadCosto, generaciones, tasaMutacion):
    poblacion = crearPoblacion(tamanoPoblacion, cantidadTareas, cantidadProductos, cantidadPersonal, cantidadTiempo, cantidadCosto)
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
        cantidadTareas = int(request.form['cantidadTareas'])
        cantidadProductos = int(request.form['cantidadProductos'])
        cantidadPersonal = int(request.form['cantidadPersonal'])
        cantidadTiempo = int(request.form['cantidadTiempo'])
        cantidadCosto = int(request.form['cantidadCosto'])
        
        mejorSolucion, evolucion, mejoresIndividuos = algoritmoGenetico(
            tamanoPoblacion=10, 
            cantidadTareas=cantidadTareas, 
            cantidadProductos=cantidadProductos, 
            cantidadPersonal=cantidadPersonal, 
            cantidadTiempo=cantidadTiempo, 
            cantidadCosto=cantidadCosto, 
            generaciones=50, 
            tasaMutacion=0.1
        )
        
        return jsonify({
            'mejorSolucion': {
                'tareas': mejorSolucion.tareas,
                'productos': mejorSolucion.productos,
                'personal': mejorSolucion.personal,
                'tiempo': mejorSolucion.tiempo,
                'costo': mejorSolucion.costo
            },
            'evolucion': evolucion,
            'mejoresIndividuos': [
                {
                    'tareas': individuo.tareas,
                    'productos': individuo.productos,
                    'personal': individuo.personal,
                    'tiempo': individuo.tiempo,
                    'costo': individuo.costo
                }
                for individuo in mejoresIndividuos
            ]
        })
    
    return render_template('index.html')

@app.route('/escenarios', methods=['GET'])
def escenarios():
    # Ejemplo de escenarios basados en diferente personal
    escenarios = []
    for personal in range(1, 5):
        tiempo = random.randint(60, 100) // personal  # el tiempo disminuye con más personal
        costo = min(personal * tiempo * SALARIO_POR_HORA, COSTO_MAXIMO)
        escenarios.append({
            'personal': personal,
            'tiempo': tiempo,
            'costo': costo
        })
    
    return jsonify(escenarios)

if __name__ == '__main__':
    app.run(debug=True)
