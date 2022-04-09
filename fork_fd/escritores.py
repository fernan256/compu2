import sys
import os
import time
import argparse

processes = []

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']


def childs_function(n_childs, number_of_repetitions, file_directory, verbose):
		fileObject = open(file_directory, "w+")
		for r in range(int(number_of_repetitions)):
			time.sleep(1)
			for n in range(int(n_childs)):
				time.sleep(1)
				pid = os.fork()
				if pid == 0:
						if verbose:
							print(f'Proceso {os.getpid()} escribiendo letra {alphabet[n]}')
						fileObject.write(alphabet[n])
						fileObject.close()
						os._exit(0)
				else:
						processes.append(pid)


def main(args):
		variables = vars(args)
		childs_to_create = variables['n']
		number_of_repetitions = variables['r']
		file_directory = variables['f']
		if variables['v']:
			childs_function(childs_to_create, number_of_repetitions, file_directory, variables['v'])
		else:
			childs_function(childs_to_create, number_of_repetitions, file_directory, False)
		while processes:
			pid, exit_code = os.wait()
			if pid != 0:
					processes.remove(pid)
		fileObject = open(file_directory, "r")
		fileContent = fileObject.read()
		print(fileContent)
		fileObject.flush()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-n", help='entero indica cantidad de hijos')
	parser.add_argument("-r", help='cantidad de veces que se repite una letra')
	parser.add_argument("-f", help='path donde se guarda el archivp')
	parser.add_argument("-v", help='indica modo verboso', action='store_true')
	args = parser.parse_args()
	main(args)