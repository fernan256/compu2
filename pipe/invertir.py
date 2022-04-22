import os
import argparse


def childs_function(file_directory):
	with open(file_directory, "r") as file1:
		total_lines = sum(1 for line in file1)
	fileObject = open(file_directory, "r")
	lines = fileObject.readlines()

	r,w = os.pipe()
	r_child,w_child = os.pipe()
	
	for n in range(total_lines):
		pid = os.fork()
		if pid == 0:
			os.close(w)
			os.close(r_child)
			r = os.fdopen(r, 'r')
			lineR = r.read()
			w_child = os.fdopen(w_child,'w')
			lineReverted = lineR[::-1]
			w_child.write(f"{lineReverted}")
			w_child.flush()
			w_child.close()
			os._exit(0)

	os.close(r)
	os.close(w_child)
	w = os.fdopen(w, 'w')

	for l in lines:
		w.write(l)

	w.close()

	r_child = os.fdopen(r_child)
	while True:
		line = r_child.read()
		if len(line) == 0:
			break
		print(line)


def main(args):
    variables = vars(args)

    childs_function(variables['f'])


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", help='archivo a leer')
	args = parser.parse_args()
	main(args)