print("in  sec one")

import os, sys

def runpy(pyfile):
    os.system(sys.executable + " " + pyfile)
runpy("t.py")

print("in  sec two")

