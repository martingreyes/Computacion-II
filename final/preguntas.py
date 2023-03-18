import sqlite3

conexion = sqlite3.connect("/Users/martinreyes/Documents/Facultad/3ro/Computacion II/Computacion-II/final/prueba.db")

preguntas = [(0, "¿Cuándo tuvo lugar la primera Copa Mundial de Fútbol?"),
            (1, "¿Quién es el máximo goleador de la historia de la Copa Mundial de Fútbol?"),
            (2, "¿Cuántos mundiales de fútbol ha ganado Argentina?"),
            (3, "¿Recuerdas dónde se jugó la Copa del Mundial del año 2010?"),
            (4, "¿A quiénes le ganó Argentina en 1978 y 1986?"),
            (5, "¿Cuántos Mundiales jugó Messi hasta el momento?"),
            (6, "¿Cuándo fue la última vez que Brasil fue campeón?"),
            (7, "¿Cuál de estas selecciones fue más veces subcampeona?"),
            (8, "¿Cuál es el jugador con más partidos jugados en Mundiales?"),
            (9, "¿Cuantos Mundiales se han disputado hasta el momento?"),
            ]

respuestas = [(0, "En 1920", 0, 0),
            (1, "En 1930", 0, 1),
            (2, "Ronaldo Nazario", 1, 0),
            (3, "Miroslav Klose", 1, 1),
            (4, "3", 2, 1),
            (5, "2", 2, 0),
            (6, "Sudafrica", 3, 1),
            (7, "Alemania", 3, 0),
            (8, "Alemania e Inglaterra", 4, 0),
            (9, "Paises Bajos y Alemania", 4, 1),
            (10, "3", 5, 0),
            (11, "4", 5, 1),
            (12, "1994", 6, 0),
            (13, "2002", 6, 1),
            (14, "Italia", 7, 0),
            (15, "Paises Bajos", 7, 1),
            (16, "Lothar Matthäus", 8, 1),
            (17, "Paolo Maldini", 8, 0),
            (18, "21", 9, 0),
            (19, "22", 9, 1),
        ]
        
conexion.execute("CREATE TABLE preguntas (id int AUTO_INCREMENT, pregunta varchar(255), PRIMARY KEY (id))")

conexion.execute("CREATE TABLE respuestas (id int AUTO_INCREMENT, respuesta varchar(255), pregunta_id int, correcta BIT, PRIMARY KEY (id), FOREIGN KEY (pregunta_id) REFERENCES preguntas(id))")

conexion.commit()

conexion.executemany("INSERT INTO preguntas VALUES (?,?)", preguntas)

conexion.executemany("INSERT INTO respuestas VALUES (?,?,?,?)", respuestas)

conexion.commit()
                    
conexion.close()

# {'id': 6, 'respuesta': 'Sudafrica', 'pregunta_id': 3, 'correcta': 1}