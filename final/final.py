import sqlite3

conexion = sqlite3.connect("/Users/martinreyes/Documents/Facultad/3ro/Computacion II/Computacion-II/final/trivia.db")

for row in conexion.execute("SELECT * FROM preguntas"):

    print("\n{}) {}".format(row[0] ,row[1]))

    contador = 1

    respuestas = []

    for row in conexion.execute("SELECT * FROM respuestas WHERE pregunta_id = {}".format(row[0])):

        print("     {}) {}".format(contador, row[1]))

        respuestas.append(row)

        contador = contador + 1

    respuesta = input("\nOpcion 1 o 2: ")

    while respuesta != "1" and respuesta != "2":

        respuesta = input("\nInvalido. Opcion 1 o 2: ")

    if respuesta == "1":

        respuesta = respuestas[0]

    else:

        respuesta = respuestas[1]

    
    if respuesta[3] == 1:

        print("\nCORRECTO!. {} es la respuesta correcta!".format(respuesta[1]))

    else:

        respuestas.remove(respuesta)

        print("\nINCORRECTO!. {} es la respuesta correcta!".format(respuestas[0][1]))










