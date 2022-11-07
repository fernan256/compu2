from celery_config import app
from math import log
import argparse


@app.task
def raiz(num):
    return int(num) * 2

@app.task
def pot(num):
    return pow(num,num)

@app.task
def logFn(num):
    return log(num)

def main(args):
    funcs = {'raiz': raiz, 'pot': pot, 'log': logFn}
    file_directory = args.path
    fn_to_run = funcs[args.func]    
    print(f"Funcion a ejecutar: {fn_to_run}")
    result = []
    with open(file_directory, 'r') as f:
        matrix = [[int(num) for num in line.split(',')] for line in f if line.strip() != "" ]
        print(f'\nMatriz original {matrix}')
        for row in matrix:
            for elem in row:
                res = fn_to_run.delay(elem)
                result.append(res.get())

    print(f'\nMatriz resultado {result}\n')


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", '--path', required=True,
                        help='path donde se guarda el archivo')
	parser.add_argument('-c', '--func', dest='func',
                        choices=['raiz', 'pot', 'log'], 
                        required=True,
                        help='indica tipo de funcion')
	args = parser.parse_args()
	main(args)