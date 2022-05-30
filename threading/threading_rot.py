import threading, queue
import sys


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
    getUserEnter = sys.stdin.readline()
    q2.put(getUserEnter)
    while q:
        show_message(q)
        q.task_done()
        if q.empty:
            break


def reader(q,q2):
    escrito = q2.get()
    encrypted = rot13(escrito)
    q.put(encrypted)



def main():
    q = queue.Queue()
    q2 = queue.Queue()

    writerThread = threading.Thread(target=writer, args=(q,q2 ))
    readerThread = threading.Thread(target=reader, args=(q,q2 ))
 
    writerThread.start()
    readerThread.start()
    q.join()
    q2.join()

if __name__ == "__main__":
    main()    
