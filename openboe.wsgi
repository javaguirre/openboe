import os, sys

path = '/home/javaguirre/python/Proyectos/openboe'
if path not in sys.path:
    sys.path.append(path)
print sys.path
from openboe.application import app as application
