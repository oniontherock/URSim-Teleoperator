import numpy as np

dtype = [('val1', 'f8'), ('val2', 'f8'), ('val3', 'f8'), ('val4', 'i4')]

# 1. Start with a standard, fast Python list instead of a NumPy array
data_list = [(0.0, 0.0, 0.0, 0)]

def data_point_add(x, y, z, ts):
    # 2. Appending to a Python list is blindingly fast (O(1) complexity)
    data_list.append((x, y, z, ts))

def data_save():
    # 3. Convert the full list to a structured NumPy array all at once right before saving
    final_array = np.array(data_list, dtype=dtype)
    np.savetxt("data.txt", final_array, fmt='%.2f', delimiter=', ', header='Col1, Col2, Col3', comments='')
