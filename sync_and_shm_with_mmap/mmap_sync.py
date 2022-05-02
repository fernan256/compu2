import mmap, os, signal
import argparse

first = 0
second = 0
file_directory = ""
lineb = bytes()
area = mmap.mmap(-1,1024)


def show_message(nro, frame):
  area.seek(0)
  leido = area.read(1024)
  print(f'Lectura del Padre: {leido.decode()}')
  fn_child2(file_directory)
  os.kill(second, signal.SIGUSR1)
  signal.pause()


def child2(nro, frame):
  # os.kill(hijo1, signal.SIGUSR1)
  signal.pause()


def child1(nro, frame):
  # padre_lee()
  pass


def fn_child2(file_directory):
  print(f'Hijo 2 notificado ...')
  area.seek(0)
  leido = area.read(1024)
  file2 = open(file_directory, "w+") 
  file2.write(leido.decode().upper())
  file2.flush()
  file2.close()
  os.kill(first, signal.SIGUSR1)


def fn_child1():
  while True: 
    line = input("Ingreso de caracteres: ")
    if "bye" == line:
      break
    lineb = bytes(line, 'utf-8')
    area.seek(0)
    area.write(lineb)
    os.kill(os.getppid(),signal.SIGUSR1)
    signal.pause()


def main(args):
  variables = vars(args)
  global file_directory
  file_directory = variables['f']
  pid = os.fork()
  first = os.getpid()

  if pid == 0:
    signal.signal(signal.SIGUSR1, child1)
    fn_child1()
  else:
    signal.signal(signal.SIGUSR1, show_message)
    pid2 = os.fork()
    if pid2 == 0:
      signal.signal(signal.SIGUSR1, child2)
      second = os.getpid()
      signal.pause()
    signal.pause()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", help='path donde se guarda el archivo')
  args = parser.parse_args()
  main(args)

