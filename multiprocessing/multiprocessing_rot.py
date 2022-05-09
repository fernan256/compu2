from multiprocessing import Process, Queue, Pipe
import os, sys


def rot13(value):
    Rot13=''
    abc = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in value:
        if i in abc:
            Rot13 += abc[abc.index(i) + 13]
        else:
            Rot13 += i
    return Rot13


def show_message(q):
    msg = q.get()
    print("\nEscritor mostrando mensaje encriptado: %s" % msg)
    return


def writer(q,w):
    sys.stdin = open(0)
    while True:
        print("Ingrese una linea: ")
        escrito = sys.stdin.readline()
        w.send(escrito)
        show_message(q)
        break
    


def reader(q,r):
    valor = r.recv()
    encrypted = rot13(valor)
    q.put(encrypted)



def main():
    r, w = Pipe()
    q = Queue()

    processes = []

    p1 = Process(target=writer, args=(q, w,))
    p2 = Process(target=reader, args=(q, r,))

    processes.extend([p1, p2])

    for p in processes:
        p.start()

    for p in processes:
        p.join()
    
    r.close()
    w.close()
    print("Padre terminando...")


if __name__ == "__main__":
    main()    
