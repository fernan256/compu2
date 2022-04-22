import argparse
import subprocess as sp
import os
from os import fork

def invertline(line, r, w, r1, w1, i):
    r[i], w[i] = os.pipe()
    r1[i], w1[i] = os.pipe()

    pid = fork()
    if pid == 0:
        os.close(w[i])
        os.close(r1[i])
        r[i] = os.fdopen(r[i])
        linea1 = r[i].read()
        print(f"aaa: {line[::1]}")
        w1[i] = os.fdopen(w1[i], 'w')
        w1[i].write(f"{linea1[::1]}")
        w1[i].flush()
        w1[i].close
        os._exit(0)
    else:
        os.close(r[i])
        os.close(w1[i])
        w[i] = os.fdopen(w[i],'w')
        w[i].write(f"{line}")
        w[i].flush()
        w[i].close

def main():

    parser = argparse.ArgumentParser(description="a")

    parser.add_argument("-f", "--path", type=str, required=True, help="archivo")

    args = parser.parse_args()

    with open(args.path, "r") as file1:
        total_lines = sum(1 for line in file1)
    r = [[] for x in range(total_lines)]
    w = [[] for y in range(total_lines)]
    r1 = [[] for z in range(total_lines)]
    w1 = [[] for w in range(total_lines)]
    print(f"{args.path}")
    file1 = open(args.path, "r")
    count = 0
    for line in file1:
        invertline(line, r, w, r1, w1, count)
        count = count + 1
    for i in range(total_lines):
        r1[i] = os.fdopen(r1[i])
        linea = r1[i].read()
        print(f"{linea}")
        os.wait()
    file1.close()

if __name__ == "__main__":
	  main()