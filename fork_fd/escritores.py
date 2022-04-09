import sys
import os
import time
import argparse

processes = []

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']


def childs_function(n_childs, number_of_repetitions, file_directory, verbose):
		fileObject = open(file_directory, "w+")
		for r in range(int(number_of_repetitions)):
			for n in range(int(n_childs)):
				pid = os.fork()
				if pid == 0:
						if verbose:
							print(f'Proceso {os.getpid()} escribiendo letra {alphabet[n]}')
						fileObject.write(alphabet[n])
						fileObject.close()
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
		elif len(elements) == 6:
				childs_to_create = elements[1]
				number_of_repetitions = elements[3]
				file_directory = elements[5]
				childs_function(childs_to_create, number_of_repetitions, file_directory)
				while processes:
					pid, exit_code = os.wait()
					if pid != 0:
							processes.remove(pid)
				fileObject = open(file_directory, "r")
				fileContent = fileObject.read()
				print(fileContent)
				fileObject.flush()
		elif len(elements) == 7 and elements[6] == "-v":
				childs_to_create = elements[1]
				number_of_repetitions = elements[3]
				file_directory = elements[5]
				childs_function(childs_to_create, number_of_repetitions, file_directory, True)
				while processes:
					pid, exit_code = os.wait()
					if pid != 0:
							processes.remove(pid)
				fileObject = open(file_directory, "r")
				fileContent = fileObject.read()
				print(fileContent)
				fileObject.flush()		
		else:
				print("Error en la cantidad de argumentos o argumentos invalidos.")
				print("Argumentos validos: \n\t-h (ayuda) \n\t-n 1 (cant. hijos) \n\t-v (verbose)")
				os._exit(0)


if __name__ == "__main__":
    main()