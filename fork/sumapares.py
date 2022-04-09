import os
import argparse

processes = []

def suma_pares():
		i = 0
		suma = 0
		while i <= os.getpid():
				if i % 2 == 0:
						suma = suma + i
				i+=1
		return suma


def childs_function(n_childs, verbose):
		for n in range(int(n_childs)):
			pid = os.fork()
			if pid == 0:
					if verbose:
						print("Starting process %d" % (os.getpid()))
						resultado = suma_pares()
						print("%d - %d: %d" % (os.getpid(), os.getppid(),resultado))
						print("Ending process %d" % (os.getpid()))
					else:
						resultado = suma_pares()
						print("%d - %d: %d" % (os.getpid(), os.getppid(),resultado))
					os._exit(0)
			else:
					processes.append(pid)


def main(args):
	variables = vars(args)
	childs_to_create = variables['n']
	if variables['v']:
		childs_function(childs_to_create, variables['v'])
	else:
		childs_function(childs_to_create, False)
	while processes:
		pid, exit_code = os.wait()
		if pid != 0:
				processes.remove(pid)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-n", help='entero indica cantidad de hijos')
	parser.add_argument("-v", help='indica modo verboso', action='store_true')
	args = parser.parse_args()
	main(args)