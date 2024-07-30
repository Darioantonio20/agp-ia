import csv
import random

nombres = ["Juan", "María", "Pedro", "Ana", "Luis", "Carmen", "Jorge", "Laura", "Ricardo", "Sofía"]
apellidos = ["García", "Martínez", "Rodríguez", "López", "Pérez", "González", "Hernández", "Sánchez", "Ramírez", "Cruz"]

clasificaciones = ["mejor empleado", "empleado promedio", "peor empleado"]

num_empleados = 30

with open('empleados.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Nombre", "Apellido", "Clasificación"])

    for _ in range(num_empleados):
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        clasificacion = random.choice(clasificaciones)
        writer.writerow([nombre, apellido, clasificacion])

print("Dataset de empleados generado con éxito.")
