# this file is responsible for tracking data live while the program is running. It writes down data but on it's own it does nothing to preserve data outside of the current program
# if this file was the only one, no data would be preserved outside of the current instance of the program.
import numpy as np
from numpy.typing import NDArray

dtype = [('x', 'f8'), ('y', 'f8'), ('z', 'f8'), ('ts_grab', 'i8'), ('ts_infer', 'i8')]

data_list: dict[int, tuple[float, float, float, int, int]] = {}


data_dict = {} # example of setting an element: data_dict[name][element_name] = element_value
data_array = {}
data_type_dict = {}
data_format_dict = {}


# appends a new element to data_type_dict under the given name, with the value being a unique data type, this is used for formatting and saving later
def data_structure_add(name, data_type, data_format):
    data_type_dict[name] = data_type
    data_format_dict[name] = data_format
    data_array[name] = []
    data_dict[name] = {}
def data_element_add(name, element_name, element_value):
    data_dict[name][element_name] = element_value
def data_element_add_group(name, element_name, element_value):
    for name_cur, value_cur in zip(element_name, element_value):
        data_dict[name][name_cur] = value_cur
# please note that when you call this function, the data you've been logging MUST be complete (I.E. fully populated to match the data_type you assigned). If it's not, an error will be thrown.
def data_log(name):
    data_array[name].append(data_dict[name].copy())

def data_format(name):

    data_format = data_format_dict[name]
    data_type = data_type_dict[name]
    data = data_array[name]

    data_header = ""
    for data_type_key, data_type_element in data_type:
        if (data_header == ""):
            data_header = data_type_key
        else:
            data_header = data_header + ", " + data_type_key

    formatted_data = []
    for data_dict_cur in data:

        tuple = ()

        for data_element_cur in data_dict_cur:
            tuple += (data_dict_cur[data_element_cur],)
        formatted_data.append(tuple)


    formatted_data: NDArray[np.void] = np.array(formatted_data, dtype=data_type)

    return {"data":formatted_data, "format":data_format, "header":data_header}

### example usage of the data tracker system below (please note this incorporates functions from both data_tracker.py AND data_saver.py):
# data_structure_add("pos", [('x', 'f8'), ('y', 'f8'), ('z', 'f8')], ['%.16f', '%.16f', '%.16f'])
#
# data_element_add("pos", 'x', 1)
# data_element_add("pos", 'y', 2)
# data_element_add("pos", 'z', 3)
# data_log("pos")
#
# data_element_add_group("pos", ['x', 'y', 'z'], [4, 5, 6])
# data_log("pos")
#
# data_element_add_group("pos", ['x', 'y', 'z'], [7, 8, 9])
# data_element_add("pos", 'x', -999)
# data_log("pos")
#
# data = data_format("pos")
#
# import data_saver # we import data_saver here to show that past this point we use a function from it, and that prior to this point we use nothing from data_saver
#
# data_saver.data_save_singular("pos.txt", data["data"], data["format"], data["header"])
#
# this will be written to a file named "pos.txt":
#
# x, y, z
# 1.0000000000000000, 2.0000000000000000, 3.0000000000000000
# 4.0000000000000000, 5.0000000000000000, 6.0000000000000000
# -999.0000000000000000, 8.0000000000000000, 9.0000000000000000
###