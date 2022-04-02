import sys
import os
import time

def suma_pares():
		i = 0
		suma = 0
		while i <= os.getpid():
				if i % 2 == 0:
						suma = suma + i
				i+=1
		return suma


def childs_function(n_childs):
		for n in range(int(n_childs)):
				if os.fork() == 0:
						print("Hijo procesando... "+str(n))
						print("hijo: mi pid es: %d, soy hijo de %d" % (os.getpid(), os.getppid()))
						resultado = suma_pares()
						print("%d - %d: %d" % (os.getpid(), os.getppid(),resultado))
						exit(0)


def main():
		elements = sys.argv[1:]
		if len(elements) == 1:
				print ("Forma de uso: ")
				print ("python sumapares.py -n 1")
				print ("Modo verboso -> python sumapares.py [argumentos]")
				print ("-n entero indica cantidad de hijos ")
				print ("-v indica modo verboso")
				print ("-h ayuda")
				exit(0)
		elif len(elements) == 2 or len(elements) == 3:
				childs_to_create = elements[1]
				print("padre esperando... soy %d" % os.getpid())
				childs_function(childs_to_create)
				pid,estado = os.wait()
				print("%d - %d" % (os.getpid(), os.getppid()))
				
		else:
				print("Error en la cantidad de argumentos")
				exit(0)


if __name__ == "__main__":
    main()