from ast import arg
from binascii import b2a_hqx
import threading, queue
import os, sys
import threading


# check = threading.Condition()


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


def writer(q,q2):
    sys.stdin = open(0)
    print("Ingrese una linea: ")
    # check.acquire()
    getUserEnter = sys.stdin.readline()
    print(getUserEnter)

    # escrito = getUserEnter
    # check.wait()
    # if escrito:
    #     print(f'estoy {escrito}')
    #     check.notify()
    #     check.release()
    q2.put(getUserEnter)
    while q:
        show_message(q)
        q.task_done()
        if q.empty:
            break


def reader(q,q2):
    # if escrito:
    # check.acquire()
    escrito = q2.get()
    print(f'aa {escrito}')
    encrypted = rot13(escrito)
    q.put(encrypted)
    # check.notify()
    # check.release()



def main():
    escrito = ""
    q = queue.Queue()
    q2 = queue.Queue()

    a = threading.Thread(target=writer, args=(q,q2 ))
    b = threading.Thread(target=reader, args=(q,q2 ))
 
    # Now start both threads
    a.start()
    b.start()
    # a.join()
    # b.join()
    q.join()
    q2.join()

if __name__ == "__main__":
    main()    
