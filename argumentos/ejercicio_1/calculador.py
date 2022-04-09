import argparse


def main(args):
  variables = vars(args)
  result = 0
  if variables['o'] == "+":
    result = int(variables["n"])+int(variables["m"])
    print(f'{variables["n"]} {variables["o"]} {variables["m"]} = {result}')
  elif variables['o'] == "-":
    result = int(variables["n"]) - int(variables["m"])
    print(f'{variables["n"]} {variables["o"]} {variables["m"]} = {result}')
  elif variables['o'] == "*":
    result = int(variables["n"]) * int(variables["m"])
    print(f'{variables["n"]} {variables["o"]} {variables["m"]} = {result}')
  else:
    result = int(variables["n"]) / int(variables["m"])
    print(f'{variables["n"]} {variables["o"]} {variables["m"]} = {result}')


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-o")
  parser.add_argument("-n")
  parser.add_argument("-m")
  args = parser.parse_args()
  main(args)
