import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

def init():
    global allDiagrams
    global lookupCount
    allDiagrams = {}
    lookupCount = 0