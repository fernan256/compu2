import os  
import signal  
from time import sleep  

child=[]

for i in range(2):
    pid = os.fork()
    if pid == 0:
        child=[]
        print('child start,pid',os.getpid())
        break
    else:
        child.append(pid)

if(child):
    def onsig1(a,b):
        print('onsig1->',a)

    signal.signal(signal.SIGCHLD,onsig1)
    signal.signal(signal.SIGUSR1,onsig1)

    try:
        print(os.getpid(),' start wait...',str(child))
        while True:
            pid, stat = os.wait()
            print('--->',pid,stat)
    except Exception as e:
        print('error -->',str(e))
else:
    def onsig2(a,b):
        print('onsig2->',a)
    signal.signal(signal.SIGUSR2,onsig2)
    while True:
        sleep(10)
        print(os.getpid(),'say ...')