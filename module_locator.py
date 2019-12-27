import sys
import os

#Code by Daniel Stutzbach and modified slightly for Python 3
#see https://stackoverflow.com/questions/2632199/how-do-i-get-the-path-of-the-current-executed-file-in-python

def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")

def module_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return (os.path.dirname(sys.executable.encode(encoding))).decode('ascii')
    return (os.path.dirname(__file__.encode(encoding))).decode('ascii')