import sqlite3, random

#Transforma un registro random de la tabla pregunta en un diccionario. Por ejemplo: pregunta = {id: 0, pregunta: “¿Quien ganó el último mundial?”}

conexion = sqlite3.connect("/Users/martinreyes/Documents/Facultad/3ro/Computacion II/Computacion-II/final/trivia.db")

def pregunta_random():

    numero = random.randint(0, 9)

    for x in conexion.execute("SELECT * FROM preguntas WHERE id = {}".format(numero)):
        pregunta = x

    pregunta = {"id":pregunta[0], "pregunta": pregunta[1]}

    pregunta_id = (pregunta["id"])


    respuestas = []
    for x in conexion.execute("SELECT * FROM respuestas WHERE pregunta_id = {}".format(pregunta_id)):
        respuestas.append(x)

    respuesta1 = {"id":respuestas[0][0], "respuesta": respuestas[0][1], "pregunta_id":respuestas[0][2], "correcta": respuestas[0][3] }

    respuesta2 = {"id":respuestas[1][0], "respuesta": respuestas[1][1], "pregunta_id":respuestas[1][2], "correcta": respuestas[1][3] }



    return pregunta, respuesta1, respuesta2

pregunta, respuesta1, respuesta2 = pregunta_random()

print(pregunta)
print(respuesta1)
print(respuesta2)



    

