import os
import numpy as np
import sys
import h5py
filename = 'practice/TRAAAAW128F429D538.h5'
f = h5py.File(filename, 'r')

# List all groups
print("Keys: %s" % f.keys())
a_group_key = list(f.keys())[0]

# Get the data
data = list(f[a_group_key])
np.savetxt(sys.stdout, h5py.File(filename))
