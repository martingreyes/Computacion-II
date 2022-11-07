from celery_config import app
import math

@app.task
def raiz(filas):
    resultado = []
    for fila in filas:
        for x in fila:
            if x.isdigit():
                resultado.append(round(math.sqrt(int(x)),2)) 
        resultado.append("\n")
    return resultado
    
@app.task
def pot(filas):
    resultado = []
    for fila in filas:
        for x in fila:
            if x.isdigit():
                resultado.append(int(x) ** int(x)) 
        resultado.append("\n")
    return resultado
    
@app.task
def log(filas):
    resultado = []
    for fila in filas:
        for x in fila:     
            if x.isdigit():
                resultado.append(round((math.log(int(x))), 2)) 
        resultado.append("\n")
    return resultado

@app.task
def nada(fila):
    resultado = []
    for x in fila:
        if x.isdigit():
            resultado.append(x) 
    resultado.append("\n")
    return resultado
    