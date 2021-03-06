
import tables
import pandas as pd
import numpy as np
from root_numpy import array2root
from rootpy.root2hdf5 import root2hdf5

# create ROOT testfile with root_numpy
x = np.linspace(0, 1000, num=1000, dtype=[('w', 'float64')])
print(x[15][0])
array2root(x, 'test.root', 'test_tree', mode='recreate')
print("Wrote test.root")

# convert to hdf5 with rootpy
root2hdf5('test.root','test.h5',entries=500,show_progress=True)

# read hdf5 with PyTables 
h5file = tables.open_file('test.h5', mode='r')
table = h5file.root.test_tree
x2 = np.array( [entry['w'] for entry in table.iterrows() ] )
print(x2[15])
h5file.close()

# alternatively, read hdf5 directly as pandas dataframe
df = pd.read_hdf('test.h5')
print(df.iloc[15]['w'])

