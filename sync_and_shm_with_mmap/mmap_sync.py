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
  # os.kill(first, signal.SIGUSR1)
  signal.pause()


def child1(nro, frame):
  pass


def child_exit1(nro, frame):
  print('hijo 1 me voy')
  os.kill(os.getppid(),signal.SIGUSR2)
  # signal.pause()
  parent_kill2()
  exit()


def parent_exit(nro, frame):
  print('notificando...')
  # signal.pause()


def child_exit2(nro, frame):
  print('hijo 2 me voy')
  os.kill(os.getppid(),signal.SIGUSR2)
  # signal.pause()
  parent_kill()
  exit()


def parent_kill1():
  os.kill(first,signal.SIGUSR2)
  # signal.pause()


def parent_kill2():
  os.kill(second,signal.SIGUSR2)
  # signal.pause()


def parent_kill():
  print('Padre terminando')
  os.kill(os.getppid(), signal.SIGTERM)


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
    if line.__eq__("bye"):
      os.kill(os.getppid(),signal.SIGUSR2)
      parent_kill1()
      signal.pause()
      break
    else:
      lineb = bytes(line, 'utf-8')
      area.seek(0)
      area.write(lineb)
      os.kill(os.getppid(),signal.SIGUSR1)
      signal.pause()


def main(args):
  variables = vars(args)
  global file_directory
  file_directory = variables['f']
  signal.signal(signal.SIGUSR1, show_message)
  signal.signal(signal.SIGUSR2, parent_exit)
  pid = os.fork()
  first = os.getpid()

  if pid == 0:
    signal.signal(signal.SIGUSR1, child1)
    signal.signal(signal.SIGUSR2, child_exit1)
    fn_child1()
  else:
    pid2 = os.fork()
    if pid2 == 0:
      signal.signal(signal.SIGUSR1, child2)
      signal.signal(signal.SIGUSR2, child_exit2)
      second = os.getpid()
      signal.pause()
    # os.kill(first,signal.SIGUSR1)
    signal.pause()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", help='path donde se guarda el archivo')
  args = parser.parse_args()
  main(args)

