import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

def init():
    global allDiagrams
    global lookupCount
    global lookupSuccess
    global lookupFailure
    allDiagrams = {}
    lookupCount = 0
    lookupSuccess = 0
    lookupFailure = 0