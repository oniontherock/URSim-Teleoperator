import numpy as np

def load_data(name, skip_count, unpack=True):

    data = np.loadtxt(
        "Data/" + name + ".txt",
        delimiter=',',
        skiprows=skip_count,
        unpack=unpack,
    )

    return data

# dict loading functions
def data_convert_to_dict(data, timestamp_index=-1):

    data_as_dict = {}

    for i in range(len(data)):
        data_as_dict[round(data[i][timestamp_index])] = [data[i][0]]

    return data_as_dict

def data_load_as_dict(file_name, timestamp_index=-1):
    pos_data = load_data(file_name, 1, False)

    data_as_dict = data_convert_to_dict(pos_data, timestamp_index)

    return data_as_dict

