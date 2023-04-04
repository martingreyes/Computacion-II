def escribir(mensaje,lock):
    lock.acquire()
    try:
        with open("log.txt", 'a') as archivo:
            archivo.write("\n{}".format(mensaje))
            archivo.close()
    finally:
        lock.release()