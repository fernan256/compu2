import sys
import os
import time

processes = []

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
			pid = os.fork()
			if pid == 0:
					resultado = suma_pares()
					print("%d - %d: %d" % (os.getpid(), os.getppid(),resultado))
					os._exit(0)
			else:
					processes.append(pid)


def childs_function_v(n_childs):
		for n in range(int(n_childs)):
				pid = os.fork()
				if pid == 0:
						print("Starting process %d" % (os.getpid()))
						resultado = suma_pares()
						print("%d - %d: %d" % (os.getpid(), os.getppid(),resultado))
						print("Ending process %d" % (os.getpid()))
						os._exit(0)
				else:
						processes.append(pid)


def main():
		elements = sys.argv[1:]
		if len(elements) == 1 and elements[0] == "-h":
				print("Forma de uso: ")
				print("\tpython sumapares.py -n 1 -v")
				print("Argumentos:")
				print("\t-n entero indica cantidad de hijos ")
				print("\t-v indica modo verboso")
				print("\t-h ayuda")
				os._exit(0)
		elif len(elements) == 2:
				childs_to_create = elements[1]
				childs_function(childs_to_create)
				while processes:
					pid, exit_code = os.wait()
					if pid != 0:
							processes.remove(pid)
		elif len(elements) == 3 and elements[2] == "-v":
				childs_to_create = elements[1]
				childs_function_v(childs_to_create)
				while processes:
					pid, exit_code = os.wait()
					if pid != 0:
							processes.remove(pid)		
		else:
				print("Error en la cantidad de argumentos o argumentos invalidos.")
				print("Argumentos validos: \n\t-h (ayuda) \n\t-n 1 (cant. hijos) \n\t-v (verbose)")
				os._exit(0)


if __name__ == "__main__":
    main()