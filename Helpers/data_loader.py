import numpy as np

def load_data(name, skip_count, unpack=True):

    data = np.loadtxt(
        "Data/" + name + ".txt",
        delimiter=',',
        skiprows=skip_count,
        unpack=unpack,
    )

    return data
