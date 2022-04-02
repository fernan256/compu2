import sys
from os import fork, getpid
import time

# print (sys.argv)
# print (sys.argv[1:])
print(len(sys.argv))

elements = sys.argv[1:]

if len(elements) == 4:
    print (elements)
    print (sys.argv[1:])

for i in range(len(elements)):
    # if i == 0:
    #     print("Function name: %s" % sys.argv[0])
    # else:
    if elements[i] == '-n':
        print ("%d. argument: %s" % (i,elements[i]))
    elif elements[i] == '-v':
        print ("%d. verbose: %s" % (i,elements[i]))
    elif elements[i] == '-h':
        print ("%d. help: %s" % (i,elements[i]))
    else:
        print ("%d. number: %s" % (i,elements[i]))
        # fork()
      