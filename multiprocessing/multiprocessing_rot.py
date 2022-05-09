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
        


def escritor(q,pipe_w):
    print("Escritor escribiendo %d" % os.getpid())
    sys.stdin = open(0)
    while True:
        try:
            print("Ingrese una linea: ")
            escrito = sys.stdin.readline()
            if escrito == "exit":
                break
            pipe_w.send(escrito)
            while q:
                # try:
                msg = q.get()
                print("Escritor leyendo encriptado: %s" % msg)
                break
        except IOError:
            pass
    


def lector(q,pipe_r):
    valor = pipe_r.recv()
    print(f"valor: {valor}")
    if valor:
        encrypted = rot13(valor)
        q.put(encrypted)
        pipe_r.send("Ya lei...")



def main():
    r,w = Pipe()
    q = Queue()

    p1 = Process(target=escritor, args=(q,w))
    p2 = Process(target=lector, args=(q,r))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    r.close()
    w.close()
    print("Padre terminando...")


if __name__ == "__main__":
    main()    
