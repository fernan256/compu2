import os  
import signal, mmap
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
  # exit()


def paren_exit(nro, frame):
  # print('notificando...')
  print(first)
  print(second)
  os.kill(first,signal.SIGUSR2)
  # exit()


def child_exit2(nro, frame):
  print('hijo 2 me voy')
  # os.kill(os.getppid(),signal.SIGUSR2)
  # exit()


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
      try:
        line = input("Ingreso de caracteres: ")
        print(line)
        if line.__eq__("bye"):
          print("by")
          os.kill(os.getppid(),signal.SIGUSR2)
          signal.pause()
          break
        else:
          lineb = bytes(line, 'utf-8')
          area.seek(0)
          area.write(lineb)
          os.kill(os.getppid(),signal.SIGUSR1)
          signal.pause()
      except Exception as e:
        print('error -->',str(e))


def main(args):
  child=[]

  variables = vars(args)
  global file_directory
  file_directory = variables['f']
  for i in range(2):
    pid = os.fork()
    if pid == 0:
        child=[]
        print('child start,pid',os.getpid())
        break
    else:
        child.append(pid)
  if(child):
    print("child:: ", child)
    first = child[0]
    second = child[1]
    if first:
      signal.signal(signal.SIGUSR1, child1)
      signal.signal(signal.SIGUSR2, child_exit1)
      fn_child1()
    if second:
      signal.signal(signal.SIGUSR1, child2)
      signal.signal(signal.SIGUSR2, child_exit2)
      signal.pause()
  else:
    signal.signal(signal.SIGUSR1, show_message)
    signal.signal(signal.SIGUSR2, paren_exit)
    signal.pause()

  #     def onsig1(a,b):
  #         print('onsig1->',a)

  #     signal.signal(signal.SIGCHLD,onsig1)
  #     signal.signal(signal.SIGUSR1,onsig1)

  #     try:
  #         print(os.getpid(),' start wait...',str(child))
  #         while True:
  #             pid, stat = os.wait()
  #             print('--->',pid,stat)
  #     except Exception as e:
  #         print('error -->',str(e))
  # else:
  #     def onsig2(a,b):
  #         print('onsig2->',a)
  #     signal.signal(signal.SIGUSR2,onsig2)
  #     while True:
  #         sleep(10)
  #         print(os.getpid(),'say ...')

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", help='path donde se guarda el archivo')
  args = parser.parse_args()
  main(args)
