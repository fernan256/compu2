import argparse
import subprocess as sp
import os
from os import fork


def main():

    parser = argparse.ArgumentParser(description="a")

    parser.add_argument("-f", "--path", type=str, required=True, help="archivo")

    args = parser.parse_args()

    with open(args.path, "r") as file1:
        total_lines = sum(1 for line in file1)

    file1 = open(args.path, "r")
    lineas = file1.readlines()
    fpid = os.getpid()
    r, w = os.pipe()
    r2, w2 = os.pipe()
    for count in range(total_lines):
        # r, w = os.pipe()
        # r2, w2 = os.pipe()

        os.fork()

        if os.getpid == fpid:
            os.close(r)
            w = os.fdopen(w,'w')
            w.write(lineas[count])
            # w.close()
        if os.getpid != fpid:
            os.close(w)
            os.close(r2)
            r = os.fdopen(r)
            str1 = r.read()

        if os.getpid() != fpid:
            os.close(r2)
            w2 = os.fdopen(w2, 'w')
            w2.write(f"{str1[::1]}")
            w2.close()

            os._exit(0)

        # if os.getpid() == fpid:

        #     os.close(w2)
        #     r2 = os.fdopen(r2)
        #     str2 = r2.read()
        #     print(str2)
    os.close(w2)
    r2 = os.fdopen(r2)
    str2 = r2.read()
    print(str2)
    os.close(w)
    for i in range(total_lines):
        os.wait()

if __name__ == "__main__":
	  main()