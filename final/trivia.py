import sqlite3

conexion = sqlite3.connect("/Users/martinreyes/Documents/Facultad/3ro/Computacion II/Computacion-II/final/trivia.db")

preguntas = [(0, "¿Capital de Brasil?"),
            (1, "¿Nacionalidad de Roger Federer?"),
            (2, "¿Cantidad de Champions League que ha ganado el Real Madrid?"),
            (3, "¿Moneda del Reino Unido?"),
            (4, "¿Quién canta Viva la Vida?"),
            (5, "¿Cuántos Mundiales jugó Messi hasta el momento?"),
            (6, "¿Cantidad de provincias que tiene Argentina?"),
            (7, "¿Dónde se juega Roland Garros?"),
            (8, "¿Cuál es el río más largo del mundo?"),
            (9, "¿Cuál es el océano más grande del mundo?"),
            (10, "¿Quién es Jeff Bezos?"),
            (11, "¿Cuál es el atleta con más medallas olímpicas?"),
            (12,"¿En qué año comenzó la II Guerra Mundial?"),
            (13, "¿Cuánto vale el número pi?"),
            (14, "¿Quién es el CEO de Tesla?")
            ]

respuestas = [(0, "Río de Janeiro", 0, 0),
            (1, "Brasilia", 0, 1),
            (2, "Frances", 1, 0),
            (3, "Suizo", 1, 1),
            (4, "14", 2, 1),
            (5, "11", 2, 0),
            (6, "Libra", 3, 1),
            (7, "Euro", 3, 0),
            (8, "Oasis", 4, 0),
            (9, "Coldplay", 4, 1),
            (10, "4", 5, 0),
            (11, "5", 5, 1),
            (12, "25", 6, 0),
            (13, "23", 6, 1),
            (14, "Italia", 7, 0),
            (15, "Francia", 7, 1),
            (16, "Río Nilo", 8, 0),
            (17, "Río Amazonas", 8, 1),
            (18, "Oceano Pacífico", 9, 1),
            (19, "Oceano Índico", 9, 0),
            (20, "El fundador de Google", 10, 0),
            (21, "El fundador de Amazon", 10, 1),
            (22, "Usuain Bolt", 11, 0),
            (23, "Michael Phelps",11,1),
            (24, "En 1939",12,1),
            (25, "En 1942",12,0),
            (26, "9,8", 13,0),
            (27, "3,1416", 13,1),
            (28, "Elon Musk", 14, 1),
            (29, "Tim Cook", 14, 0)
        ]
        
conexion.execute("CREATE TABLE preguntas (id int AUTO_INCREMENT, pregunta varchar(255), PRIMARY KEY (id))")

conexion.execute("CREATE TABLE respuestas (id int AUTO_INCREMENT, respuesta varchar(255), pregunta_id int, correcta BIT, PRIMARY KEY (id), FOREIGN KEY (pregunta_id) REFERENCES preguntas(id))")

conexion.execute("CREATE TABLE jugadores (id int AUTO_INCREMENT, ip varchar(255), puerto varchar(255), alias varchar(255), password varchar(255), puntaje int, PRIMARY KEY (id))")

conexion.commit()

conexion.executemany("INSERT INTO preguntas VALUES (?,?)", preguntas)

conexion.executemany("INSERT INTO respuestas VALUES (?,?,?,?)", respuestas)

conexion.execute("INSERT INTO jugadores VALUES (?,?,?,?,?,?)", (0,"test","test","test",1,0))

conexion.commit()
                    
conexion.close()

# {'id': 6, 'respuesta': 'Sudafrica', 'pregunta_id': 3, 'correcta': 1}