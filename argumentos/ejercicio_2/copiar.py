#! /usr/bin/python

import argparse
import os.path


def main(args):
  variables = vars(args)
  first_file = variables["i"]
  second_file = variables["o"]
  if os.path.exists(first_file):
    with open(first_file, 'r')  as read_file,\
         open(second_file, 'w+') as write_file:
        write_file.write(read_file.read().strip())
  else:
    print(f'Archivo {first_file} no existe.')
    


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-i")
  parser.add_argument("-o")
  args = parser.parse_args()
  main(args)