import numpy as np

def read(filename):
   a = np.loadtxt(filename, dtype=int, skiprows=1)
   return a
