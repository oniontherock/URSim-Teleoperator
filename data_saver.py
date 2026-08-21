# this file is responsible for tracking data live while the program is running. It writes down data but on it's own it does nothing to preserve data outside of the current program
# if this file was the only one, no data would be preserved outside of the current instance of the program.
import numpy as np
from numpy.typing import NDArray
import string

def data_save_singular(file_name, formatted_data, data_format, data_header):
    np.savetxt(
        file_name,
        formatted_data, 
        fmt=data_format, 
        delimiter=', ', 
        header=data_header, 
        comments=''
    )