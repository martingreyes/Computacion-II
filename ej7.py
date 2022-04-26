import os, mmap, argparse, sys, signal

parser = argparse.ArgumentParser()
# parser.add_argument("-f", type=str, help= "ruta de archivo txt", required=True)
args = parser.parse_args()

# el h2 debe crear el archivo:
# archivo = open(args.f + "/archivo", "w+")

memoria = mmap.mmap(-1, 100 )

def main():

    for x in range(2):

        pid = os.fork()

        if pid == False:

            if x == 0:      # esto hace h1
                pass 
            
            else:           # esto hace h2
                pass
                
            os._exit(0)
    
    for i in range(2):
        os.wait()   
        

if __name__=="__main__":
    main()