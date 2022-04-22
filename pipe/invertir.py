import os
import argparse
import time, sys

processes = []

def childs_function(file_directory):
	fileObject = open(file_directory, "r")
	with open(file_directory, "r") as file1:
		total_lines = sum(1 for line in file1)

	r,w = os.pipe()
	r_child,w_child = os.pipe()

	for lineR in fileObject:
		pid = os.fork()
		# if pid:
		# 	os.close(w_child)
		# 	os.close(r)
		# 	r_child = os.fdopen(r_child)
		# 	print("padre leyendo...")
		# 	while True:
		# 		line = r_child.readline()
		# 		if line:
		# 			print("Padre leyendo: %s" % line)
		# 		else:
		# 			os.wait()
		# 			print("Terminando padre...")
		# 			sys.exit(0)
		# else:
		# 	os.close(w)
		# 	os.close(r_child)
		# 	w_child = os.fdopen(w_child,'w')
		# 	print("Hijo escribiendo...")
		# 	lineLenght = len(lineR)
		# 	lineReverted = lineR[lineLenght::-1]
		# 	w_child.write(f"{os.getpid()} + {lineReverted}")
		# 	w_child.flush()
		# 	print("Encontrado EOF en el stdin...")
		# 	# w_child.close()
		# 	# time.sleep(3)
		# 	print("Hijo terminando...")
		if pid == 0:
			os.close(r_child)
			os.close(w)
			w_child = os.fdopen(w_child,'w')
			lineLenght = len(lineR)
			lineReverted = lineR[lineLenght::-1]
			print(f"{os.getpid()} + {lineReverted}")
			os._exit(0)
		else:
			os.close(w_child)
			os.close(r)
			r_child = os.fdopen(r_child)
			line = r_child.readline()
			if line:
				print("Padre leyendo: %s" % line)
			else:
				processes.append(pid)
				# sys.exit(0)


def main(args):
    variables = vars(args)

    childs_function(variables['f'])
    
    while processes:
      pid, exit_code = os.wait()
      if pid != 0:
          processes.remove(pid)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", help='archivo a leer')
	args = parser.parse_args()
	main(args)